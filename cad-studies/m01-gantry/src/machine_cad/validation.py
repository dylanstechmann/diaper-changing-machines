"""Geometric evidence only: valid solids and sampled motion clearances."""

import cadquery as cq

from .model import Component
from .parameters import Parameters


def bounds(shape: cq.Shape) -> dict:
    b = shape.BoundingBox()
    return {"size_mm": [round(b.xlen, 6), round(b.ylen, 6), round(b.zlen, 6)],
            "min_mm": [round(b.xmin, 6), round(b.ymin, 6), round(b.zmin, 6)],
            "max_mm": [round(b.xmax, 6), round(b.ymax, 6), round(b.zmax, 6)]}


def measurements(parts: list[Component]) -> list[dict]:
    return [{"name": part.name, "category": part.category, "moving": part.moving,
             "description": part.description, "local_bounds": bounds(part.shape),
             "world_bounds_at_center": bounds(part.world()),
             "placement_mm": list(part.placement),
             "volume_mm3": round(part.shape.Volume(), 6),
             "valid": not part.shape.isNull() and part.shape.isValid(),
             "solid_count": len(part.shape.Solids())} for part in parts]


def swept_bounds(metrics: list[dict], travel_mm: float) -> dict:
    """Axis-aligned bounds across the entire nominal linear carriage span."""
    moving = [part["world_bounds_at_center"] for part in metrics if part["moving"]]
    minimum = [min(part["min_mm"][axis] for part in moving) for axis in range(3)]
    maximum = [max(part["max_mm"][axis] for part in moving) for axis in range(3)]
    minimum[0] -= travel_mm / 2
    maximum[0] += travel_mm / 2
    return {
        "min_mm": [round(value, 6) for value in minimum],
        "max_mm": [round(value, 6) for value in maximum],
        "size_mm": [round(high - low, 6) for low, high in zip(minimum, maximum)],
    }


def validate(parts: list[Component], p: Parameters) -> dict:
    metrics = measurements(parts)
    failures = []
    for metric in metrics:
        if not metric["valid"] or metric["solid_count"] != 1 or metric["volume_mm3"] <= 0:
            failures.append({"check": "solid_validity", "part": metric["name"], "measurement": metric})

    # A sparse sample must never allow the carriage to jump over an end support
    # or leave a rail. This conservative X envelope is independent of sampling.
    support_travel = (p.width_mm - p.frame_mm - p.support_width_mm
                      - p.carriage_width_mm - 2 * p.minimum_clearance_mm)
    rail_engagement_travel = p.width_mm - p.frame_mm - p.bearing_length_mm
    travel_limit = min(support_travel, rail_engagement_travel)
    if p.travel_mm > travel_limit + 1e-6:
        failures.append({"check": "travel_envelope", "travel_mm": p.travel_mm,
                         "maximum_mm": round(travel_limit, 6),
                         "message": "Travel exceeds the conservative end-support / full rail-engagement envelope."})
    envelope = {
        "axis": "x",
        "swept_bounds": swept_bounds(metrics, p.travel_mm),
        "requested_travel_mm": p.travel_mm,
        "travel_limits_mm": {
            "end_supports": round(support_travel, 6),
            "full_rail_engagement": round(rail_engagement_travel, 6),
        },
        "travel_reserve_per_end_mm": round((travel_limit - p.travel_mm) / 2, 6),
    }

    moving = [part for part in parts if part.moving]
    obstacles = [part for part in parts if not part.moving and not part.name.startswith("rail_")]
    obstacle_shape = cq.Compound.makeCompound([part.world() for part in obstacles])
    rails = [part for part in parts if part.name.startswith("rail_")]
    samples = []
    for i in range(p.motion_samples):
        position = -p.travel_mm / 2 + p.travel_mm * i / (p.motion_samples - 1)
        movable = cq.Compound.makeCompound([part.world(position) for part in moving])
        overlap = movable.intersect(obstacle_shape).Volume()
        clearance = movable.distance(obstacle_shape)
        sample = {"position_mm": round(position, 6), "obstacle_overlap_mm3": round(overlap, 6),
                  "obstacle_clearance_mm": round(clearance, 6), "rail_clearances": []}
        if overlap > 1e-5 or clearance + 1e-6 < p.minimum_clearance_mm:
            for part in moving:
                for obstacle in obstacles:
                    amount = part.world(position).intersect(obstacle.world()).Volume()
                    gap = part.world(position).distance(obstacle.world())
                    if amount > 1e-5 or gap + 1e-6 < p.minimum_clearance_mm:
                        failures.append({"check": "motion_clearance", "position_mm": position,
                                         "parts": [part.name, obstacle.name],
                                         "overlap_mm3": round(amount, 6), "clearance_mm": round(gap, 6),
                                         "required_mm": p.minimum_clearance_mm})
        for part in moving:
            for rail in rails:
                # A bored sliding block intentionally surrounds its own rail.
                # Other pairs retain the generic gap requirement.
                same_bearing = part.name == rail.name.replace("rail_", "bearing_")
                required = p.radial_clearance_mm if same_bearing else p.minimum_clearance_mm
                amount = part.world(position).intersect(rail.world()).Volume()
                gap = part.world(position).distance(rail.world())
                sample["rail_clearances"].append({"parts": [part.name, rail.name],
                                                  "clearance_mm": round(gap, 6), "required_mm": required})
                if amount > 1e-5 or gap + 1e-6 < required:
                    failures.append({"check": "rail_clearance", "position_mm": position,
                                     "parts": [part.name, rail.name], "overlap_mm3": round(amount, 6),
                                     "clearance_mm": round(gap, 6), "required_mm": required})
        samples.append(sample)
    return {"status": "pass" if not failures else "fail", "failures": failures,
            "parts": metrics, "motion_samples": samples,
            "motion_envelope": envelope,
            "suggested_max_travel_mm": round(max(0, travel_limit), 6),
            "scope": "Solid validity, a conservative travel envelope, and clearances at the reported sample positions. Not strength, dynamics or safety validation.",
            "assumptions": ["Nominal stock profiles and rails; no vendor compatibility claim.",
                            "Support-to-frame and plate-to-block mating contacts are intentional.",
                            "Fasteners, clamping, actuation and a changing surface are not modeled.",
                            "Intermediate motion is sampled, not continuously certified."]}

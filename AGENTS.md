# Agent instructions — diaper-changing-machines

Open this repo only when the user named it. Ten Blender concept models. They are not built machines and not medical devices.

## Do not

- Claim a design was fabricated, safety-tested, or appropriate for unsupervised use with an infant.
- Add electronics, pressure, or “AI vision works” without a measurement that is actually in the repo.
- Convert this into a regenerative-medicine project.

## Improve, in this order

1. If you touch a `.blend` or render, say which machine id and what changed visually.
2. Keep the README table in sync with filenames `M01`–`M10` and `showroom.blend`.
3. Do not delete source blends to “clean up.”

## Done when

The file you changed still opens as a concept, and the README does not say it is a product.

## Agent tooling (portable across harnesses)

<!-- agent-toolbox:installed -->

This repo vendors its agent tooling (no secrets inside) so Claude Code,
Cline, Codex, OpenCode, Kilo Code, Kimi Code and Grok share one setup:

- `.mcp.json` — project MCP servers:
  `scholar` (PubMed, OpenAlex, Semantic Scholar, CORE, ORCID, Crossref),
  `web` (Exa, Brave, Jina, Firecrawl), `github` (read-only, token via
  `gh auth token`), `context7` (library docs), `playwright` (browser).  Also `blender` (Blender MCP; needs the addon running).
- `opencode.json` — the same servers for OpenCode;
  `AGENT_TOOLS.md` has merge snippets for Codex / Cline / Kilo Code and
  CLI fallbacks for Kimi / Grok.
- `.claude/skills/` — project skills: literature-search, web-research, secrets-guard.
- Keys: `~/.config/ai-keys.env` via the `agentkeys` loader — never in git,
  MCP config or chat. Run `secrets-guard` (`--staged`) before committing.

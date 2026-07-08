# Installation

Two independent deliverables. Install whichever you need — they share no runtime.

## Requirements

- Python **3.9+** (standard library only for the Skill; the MCP adds the `mcp` package).
- Node.js is only needed to *regenerate* the catalog from the upstream toolkit.

---

## 1. The Agent Skill

### Claude Code / Cowork / Agent SDK

Place the skill folder where your client discovers skills, e.g.:

```bash
mkdir -p ~/.claude/skills
cp -R skill/claudii-exploratores ~/.claude/skills/
```

Or install the packaged archive `dist/claudii-exploratores.skill` through your
client's "add skill" UI. Rebuild the archive any time with
`scripts/build_release.sh`.

The model will trigger the skill on OSINT-style requests (see `SKILL.md`'s
`description`). You can also run the CLI standalone:

```bash
cd skill/claudii-exploratores
python scripts/exploratores.py urls "example.com"
python scripts/exploratores.py --help
```

---

## 2. The MCP server

```bash
cd mcp
python -m venv .venv && source .venv/bin/activate    # optional but recommended
pip install -e .                                     # or: uv pip install -e .
```

Verify it runs:

```bash
python -m exploratores_osint_mcp.server   # starts a stdio MCP server; Ctrl-C to stop
```

### Register with Claude Desktop

Edit `claude_desktop_config.json` (macOS:
`~/Library/Application Support/Claude/claude_desktop_config.json`) and merge the
contents of `mcp/config.example.json`. Restart Claude Desktop. The seven tools
appear under the `claudii-exploratores` server.

If you used a virtualenv, set `"command"` to that venv's `python` (absolute path),
or install globally so the `claudii-exploratores-mcp` console script is on PATH.

---

## Smoke test

```bash
# Skill
python skill/claudii-exploratores/scripts/exploratores.py classify "8.8.8.8"

# MCP (lists tools without a client)
cd mcp && python -c "import asyncio,exploratores_osint_mcp.server as s; \
print([t.name for t in asyncio.run(s.mcp.list_tools())])"
```

# Installation

Two independent deliverables. Install whichever you need — they share no runtime.

## Requirements

- **Agent Skill:** Python **3.9+**, standard library only.
- **MCP server:** Python **3.10+** and the `mcp` package (1.x or 2.x, installed
  automatically).
- Regenerating the catalog from Exploratores needs only Python and a checkout of
  [Exploratores](https://github.com/SOsintOps/Exploratores) (branch `v3`).

---

## 1. The Agent Skill

### Claude Code / Cowork / Agent SDK

Place the skill folder where your client discovers skills, e.g.:

```bash
mkdir -p ~/.claude/skills
cp -R skill/claudii-exploratores ~/.claude/skills/
```

Or install the packaged archive `claudii-exploratores.skill` (attached to every
[GitHub Release](https://github.com/SOsintOps/claudii-exploratores/releases)) through
your client's "add skill" UI. Rebuild the archive any time with
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
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -e .                                     # or: uv pip install -e .
```

Verify it runs:

```bash
python -m exploratores_osint_mcp.server   # starts a stdio MCP server; Ctrl-C to stop
```

### Register with Claude Desktop

Edit `claude_desktop_config.json` and merge the contents of
`mcp/config.example.json`:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Restart Claude Desktop. The seven tools appear under the `claudii-exploratores`
server. If you used a virtualenv, set `"command"` to that venv's `python` (absolute
path), or use the `claudii-exploratores-mcp` console script if it is on PATH.

### Register with Claude Code

```bash
claude mcp add claudii-exploratores -- python -m exploratores_osint_mcp.server
```

---

## Smoke test

```bash
# Skill
python skill/claudii-exploratores/scripts/exploratores.py classify "8.8.8.8"

# MCP (lists tools without a client)
python -c "import asyncio, exploratores_osint_mcp.server as s; \
print([t.name for t in asyncio.run(s.mcp.list_tools())])"

# Full test suite (from the repository root)
pip install pytest && pytest -q tests
```

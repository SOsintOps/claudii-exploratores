# Publishing & Distribution

This repo is self-contained and ready to synchronise to a Git host and share.

## 1. Initialise the Git repository

```bash
cd Claudii-Exploratores
git init
git add .
git commit -m "Claudii Exploratores 1.0.0 — OSINT Skill + MCP"
git branch -M main
git remote add origin git@github.com:<you>/claudii-exploratores.git
git push -u origin main
```

`dist/` and `__pycache__/` are git-ignored. `catalog.json` **is** committed (it is
the runtime data, generated but required at run time).

## 2. Release the Skill

- Run `scripts/build_release.sh` to produce `dist/claudii-exploratores.skill`.
- Attach that `.skill` file to a GitHub Release, or share it directly. Users can
  import it from their Claude client, or unzip it into `~/.claude/skills/`.

## 3. Publish the MCP server

### Option A — from source (simplest)
Users clone the repo and `pip install -e mcp/`. Done.

### Option B — to PyPI
```bash
cd mcp
python -m build            # produces dist/*.whl and *.tar.gz
python -m twine upload dist/*
```
Then anyone can `pip install claudii-exploratores-mcp` and configure the
`claudii-exploratores-mcp` command in their client.

### Option C — list it in MCP directories
Once public, submit the server to community MCP registries/directories so it is
discoverable. Point them at the repo and `mcp/README.md`.

## 4. Keeping the catalog current

The upstream Exploratores toolkit evolves. To refresh:

```bash
scripts/build_release.sh /path/to/new/Exploratores-x.y.z
git add shared/catalog.json skill mcp
git commit -m "Refresh catalog from Exploratores x.y.z"
```

## 5. Licence obligations (AGPL-3.0)

Because the upstream toolkit is AGPL-3.0, this derivative is too. If you distribute
it — or run a modified version as a network service — you must make the
corresponding source available under the same licence. Keep `LICENSE` and `NOTICE`
intact and preserve attribution to the original author (Ramingo / SOsintOps).

## 6. Responsible-use note for your README/release

State clearly that the suite is for authorised, lawful OSINT only, that it builds
search links rather than fetching data, and that outputs are investigative leads to
be independently verified. This protects users and reflects the tradecraft the
skill teaches.

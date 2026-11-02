# Releasing and keeping in sync

## 1. Keeping the catalog in sync with Exploratores

The catalog comes from the Exploratores export `assets/data/search-library.json`
(with `catalogue-meta.json`, whose SHA-256 is checked). A weekly workflow
(`.github/workflows/sync-exploratores.yml`) compares it with `shared/catalog.json`
and opens an issue when Exploratores has changed. To update:

```bash
scripts/build_release.sh /path/to/Exploratores     # checkout of branch v3
pytest -q tests
```

`build_release.sh` re-syncs the catalog, rebuilds the desk classification
(`docs/query_classification.csv` and its page), the access map
(`shared/access.json`) and the catalog overview, copies the engine into `skill/`
and `mcp/`, and packages `dist/claudii-exploratores.skill`. Then add an entry to
`docs/versionhistory.md` and open a pull request.

Never edit the copies in `skill/` or `mcp/`, nor the generated files, by hand: CI
fails when they differ from what the scripts produce.

## 2. Access requirements

`shared/access.json` merges two sources: the live verification in
`docs/access-requirements-guide.md` (browser checks, then a VPN in the candidate
country for the links that did not work) and the desk classification. To recheck:

```bash
python scripts/check_links.py --out passA.json                                   # current exit
python scripts/check_links.py --retry-from passA.json --country US --out passB-US.json   # after switching the VPN
```

Raw results stay in the private work repository; only the cleaned guide is public.

## 3. Release

1. Bump the version in `mcp/pyproject.toml`, `mcp/exploratores_osint_mcp/server.py`
   (`__version__`), `server.json`, the README badge and `CITATION.cff`.
2. Add the release to `docs/versionhistory.md`.
3. Merge to `main` with CI green, then tag and publish:

```bash
git tag v1.1.0-alpha && git push origin v1.1.0-alpha
gh release create v1.1.0-alpha --prerelease --notes-file <notes> dist/claudii-exploratores.skill
```

### MCP server on PyPI and in the MCP registry (optional)

```bash
cd mcp && python -m build && python -m twine upload dist/*
mcp-publisher login github && mcp-publisher publish     # uses ../server.json
```

`mcp/README.md` carries the `mcp-name: io.github.SOsintOps/claudii-exploratores`
line the registry uses to check that the PyPI package belongs to this server.

## 4. Licence obligations (AGPL-3.0)

Because Exploratores is AGPL-3.0, this derivative is too. If you distribute it, or
run a modified version as a network service, you must make the corresponding
source available under the same licence. Keep `LICENSE` and `NOTICE` intact and
preserve attribution to the original author (Ramingo / SOsintOps).

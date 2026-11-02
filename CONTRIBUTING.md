# Contributing

Thank you for helping. Claudii Exploratores is a derivative of
[Exploratores](https://github.com/SOsintOps/Exploratores): the catalog is synced
from it, so some changes belong there first.

## Where a change goes

| Change | Where |
| --- | --- |
| New OSINT source, changed or dead link | **Exploratores** first (issue or pull request there). It reaches this repository on the next weekly sync. You can still open an issue here with the template. |
| Engine (classifier, placeholders, encoding), MCP server, skill, docs, tests | Here. |
| Method pages (OPSEC, source evaluation, report writing) | [Intelligence Field Notes](https://github.com/SOsintOps/intelligence-field-notes). |

## Workflow

1. Open an issue describing the bug or the proposal.
2. Fork, create a branch, make the change.
3. Engine changes go in `shared/` only. Never edit the copies in `skill/` and `mcp/`
   or the generated files (`docs/query_classification.csv`, its page,
   `shared/access.json`, `references/catalog_overview.md`): run
   `scripts/build_release.sh` instead. CI fails if they differ.
4. Add or update tests in `tests/` and run them:
   ```bash
   pip install -e mcp/ pytest
   pytest -q tests
   ```
5. Add a line to `docs/versionhistory.md` under the next version.
6. Open a pull request using the template.

## Style

- British English in documentation, short sentences, terms spelled out at first use.
- Python 3.9-compatible code in `shared/` and the skill (standard library only);
  the MCP server may use Python 3.10+.
- Commits: imperative subject line, body explaining why.

## Conduct and responsible use

By contributing you agree to the [Code of Conduct](CODE_OF_CONDUCT.md). Do not
submit sources whose main purpose is stalking or harassing private individuals.

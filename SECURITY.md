# Security Policy

## Supported versions

Only the latest release (currently the 1.1.x alpha line) receives fixes.

## Reporting a vulnerability

Please **do not open a public issue** for security problems. Report them privately
through GitHub: **Security → Report a vulnerability** on this repository
(a private security advisory). Include the version, steps to reproduce and the
impact you see.

You can expect an acknowledgement within a week. Fixes are released as a new
version and credited in `docs/versionhistory.md` unless you ask otherwise.

## Scope

In scope: the engine (`shared/`), the skill scripts, the MCP server, the build and
sync scripts, and the workflows. Examples: a crafted indicator that makes the engine
produce a URL to an unexpected host, a redaction that leaks the value it should hide,
a path traversal or command execution in any script.

Out of scope: the behaviour of the third-party OSINT services the catalog links to,
and broken or dead links (open a normal issue with the "Broken link" template).

## Design notes

- The MCP server and the skill make **no network requests**: they build URLs from a
  bundled catalog. Only `scripts/check_links.py` (a maintainer tool) and the sync
  workflow fetch anything.
- `redact_pii` runs locally; the redaction map never leaves the machine unless the
  user sends it.

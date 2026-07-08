# Claudii Exploratores — v1.0.0-alpha

**First public alpha.** OSINT reconnaissance ported for Claude, packaged as an
Agent Skill and an MCP server.

> ⚠️ **ALPHA — do not use in production before testing.** Functionally tested but
> not hardened. Verify every output independently and validate against trusted
> sources before relying on it. See the README Disclaimer.

## Highlights

- **898 curated OSINT tools** across **24 categories**, ported from the Exploratores
  OSINT Toolkit 3.4.1 into a language-neutral `catalog.json`.
- **Agent Skill** (`skill/claudii-exploratores/`) — teaches Claude OSINT tradecraft
  (analytic standards, 5W1H, OPSEC) and ships a CLI that turns an indicator into a
  curated set of search links.
- **MCP server** (Python / FastMCP) — 7 tools: `classify_indicator`,
  `build_osint_urls`, `search_catalog`, `list_categories`, `verify_iban`,
  `redact_pii`, `restore_pii`.
- **Indicator classifier**, **input validators**, **offline IBAN verifier**
  (ISO 13616 mod-97, 71 countries) and a **reversible PII redactor**.

## Install

- **Skill:** unzip `claudii-exploratores.skill` into `~/.claude/skills/`, or install
  it from your Claude client.
- **MCP:** `cd mcp && pip install -e .` then add the server to your client config
  (see `mcp/README.md`).

## Verified in this release

Internal QA (see repository report): catalog integrity (identical across the three
copies, 898 entries), URL encoding on accented/space inputs, IBAN mod-97 valid/invalid
cases, PII redaction round-trip, MCP tool registration, and skill↔MCP output parity.

## Known limitations

- A few URL templates are inherited verbatim from upstream and may be imperfect
  (dork operators with literal spaces; one degenerate short-URL template).
- Phone-number field derivation is best-effort (no full `libphonenumber` parity).
- IBAN bank-name resolution is not ported (structural validation only).

## Credits & licence

Derived from the **Exploratores OSINT Toolkit** by *Ramingo* (SOsintOps),
AGPL-3.0. See `LICENSE` and `NOTICE`.

---

### Assets to attach to this GitHub Release
- `claudii-exploratores.skill` (from `dist/`)
- Optionally the MCP wheel/sdist (`python -m build` in `mcp/`)

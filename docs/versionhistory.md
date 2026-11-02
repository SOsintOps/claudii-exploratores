# Version History

Changelog of all releases of Claudii Exploratores, the Exploratores OSINT catalogue as an agent skill and an MCP server for Claude.

---

## 1.1.0-alpha — 2026

- **Changed:** Catalog synced with Exploratores 3.10.5: 909 tools across 26 categories (was 874 across 24). New categories **Legal** (15 Italian and European Union sources: Normattiva, SentenzeWeb, Corte costituzionale, Giustizia amministrativa, Gazzetta Ufficiale, Garante privacy, CONSOB, Portale Vendite Pubbliche, Brocardi, EUR-Lex, CURIA, VIES, TMview) and **Telegram** (14 tools, replacing the six `communities-tg-*` entries). Also added: SanctionsKit for officers and companies, the eleven Italian registries and lookups of Exploratores 3.8.0 (Portale Antenati, FNOMCeO doctors' register, Pagine Bianche reverse lookup, Registro Imprese, Verifica Partita IVA, INI-PEC, IndicePA, dati.gov.it, cadastral geoportal, .it WHOIS; the Gazzetta Ufficiale is now under Legal).
- **Changed:** The catalog is now built by `scripts/sync_catalog.py` from the JSON export that Exploratores publishes (`assets/data/search-library.json`), with its SHA-256 checked against `catalogue-meta.json`; no JavaScript is evaluated and Node.js is no longer needed. Labels come from the toolkit pages, then from the Janua map, so the 30 VK tools now have readable names. `scripts/extract_catalog.js` is removed.
- **Added:** Weekly sync check (`.github/workflows/sync-exploratores.yml`): every Monday the catalog is compared with Exploratores and an issue lists the tools added, removed or changed upstream.
- **Added:** Access warnings. `shared/access.json` records, for each host, whether it needs a VPN exit in a given country, Tor, or an account (live verdicts from the access guide first, desk classification otherwise). `build_osint_urls` and the CLI attach an `access_note` to each link and a `warnings` summary: geo-locked links are flagged before anyone opens them, and `exclude_geo_locked` (`--no-geo-locked`) drops them.
- **Added:** Indicator types `NORMATTIVA_URN`, `CURIA_CASE`, `EU_VAT`, `HASHTAG`, and routing for MD5 hashes, AdSense and Analytics IDs, numeric user IDs and (forced) addresses. New placeholders filled: `{q}`, `{urn}`, `{case}`, `{vat_country}`, `{vat_number}`, `{national_raw}`, `{full_dash}`, `{md5_hash}`, `{adsenseid}`, `{analyticsid}`, `{hashtag}`, `{tag}`, `{userid}`, `{phone}`. `{urn}` keeps `:` and `;` (encodeURI), as Normattiva requires and as Exploratores does.
- **Fixed:** MCP server failed to start on a fresh install: `pip` now pulls `mcp` 2.x, where `FastMCP` was renamed `MCPServer`. The server supports both 1.x and 2.x; Python 3.10 or later is required for the MCP server (the skill still runs on 3.9).
- **Added:** MCP tool annotations (`readOnlyHint`, `idempotentHint`, `openWorldHint: false`) and titles on all seven tools; server instructions tell the client to show access warnings before any link is opened.
- **Fixed:** The desk classification page left out categories missing from a fixed list (Legal and Telegram); its date is now the catalog date, not the day of the run.
- **Added:** Test suite (`tests/`, pytest) and continuous integration on Python 3.9 to 3.13 with `mcp` 1.x and 2.x, including a check that generated files are up to date.
- **Changed:** Access recheck on 2026-11-01. Every host was checked automatically from an Italian VPN exit; the ones that failed were opened in a browser through a VPN exit in their candidate country (United States, Sweden) and compared with a home IP in Italy. Now confirmed geo-locked to the United States: numpi, Yellow Pages people search, Advanced Background Checks, Carvana, FamilyTreeNow, FastPeopleSearch (22 sources in all). B2BHint, Telemetr and CallerSmart open from Italy and lose the US-only flag. The Swedish people-search sites Eniro, Merinfo and Ratsit open from a Swedish exit; MrKoll stays behind a Cloudflare check. The sources still behind a human verification step (seven US people-search and tools sites, MrKoll) and checko.ru follow the Exploratores review, which keeps them active.
- **Added:** `scripts/check_links.py`, an automated per-host access check: pass A from the current exit for every host, pass B only for the hosts that failed, after switching the VPN to the candidate country.
- **Added:** [FAQ](faq.md), with a section on using MCP and LLMs for OSINT; this version history; community files (contributing guide, security policy, code of conduct, issue and pull request templates); logo.
- **Removed:** `docs/github-repo-setup.txt` (setup notes, applied) and `docs/RELEASE_NOTES_v1.0.0-alpha.md` (moved here).

---

## 1.0.0-alpha, catalog update — 2026-11-01

- **Removed:** 28 tools on closed services, following the Exploratores 3.10.2–3.10.4 dead-link review: RiskIQ (7), ThreatCrowd (2), psbdmp (2), Nuwber (2), SpyTox (2), BTC Validation, OXT.me, Columbus, DomainApp, Memento Time Travel, web-archive-scan.com, web-scout.io, SpyOnWeb, SiteMapper, PhishCheck.me, USA-Official, Checkistan, PoliticalMoneyLine. Catalog: 898 → 874 tools.
- **Changed:** `communities-reddit-archive` from unddit to Arctic Shift; the three UDRP tools from UDRPSearch to the WIPO decision database; the FOIA tools from `search.foia.gov` to `search.usa.gov`; `ip-security-ikwyd` over HTTPS.
- **Added:** `ip-security-alienvault` (AlienVault OTX for IP addresses) and the three CAC UDRP tools (Czech Arbitration Court).
- **Changed:** Desk classification regenerated; access guide revised by hand with recomputed counts.

---

## 1.0.0-alpha — 2026-07-10

- **Added:** First public alpha. 898 curated OSINT tools across 24 categories, ported from the Exploratores OSINT Toolkit 3.4.1 into a language-neutral `catalog.json`.
- **Added:** Agent Skill (`skill/claudii-exploratores/`): OSINT tradecraft (analytic standards, 5W1H, OPSEC) and a CLI that turns an indicator into a curated set of search links.
- **Added:** MCP server (Python): seven tools, `classify_indicator`, `build_osint_urls`, `search_catalog`, `list_categories`, `verify_iban`, `redact_pii`, `restore_pii`.
- **Added:** Indicator classifier, input validators, offline IBAN verifier (ISO 13616 mod-97, 71 countries) and a reversible PII redactor.
- **Added:** Desk classification of every query by login and VPN requirement (`docs/query_classification.csv`, `docs/query-auth-vpn-classification.md`) and a live-verified access guide (`docs/access-requirements-guide.md`: home IP in Italy, then a United States VPN exit for the hosts that did not work).
- **Known limitations:** a few URL templates inherited from upstream may be imperfect; phone-number derivation is best-effort (no full `libphonenumber`); IBAN bank-name resolution is not ported.

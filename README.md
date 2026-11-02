<div align="center">

<img src="assets/logo/claudii-exploratores-logo.svg" alt="Claudii Exploratores logo: a Roman helmet whose crest is a network of nodes" width="180">

# Claudii Exploratores

### OSINT Suite for Claude — Agent Skill + MCP Server

*"The scouts of Claudius"* — a nod to the Roman reconnaissance units (*exploratores*)
and to Claude. OSINT reconnaissance, ported for AI agents.

[![status](https://img.shields.io/badge/status-alpha-orange)](#-project-status)
[![version](https://img.shields.io/badge/version-1.1.0--alpha-blue)](docs/versionhistory.md)
[![CI](https://github.com/SOsintOps/claudii-exploratores/actions/workflows/ci.yml/badge.svg)](https://github.com/SOsintOps/claudii-exploratores/actions/workflows/ci.yml)
[![license](https://img.shields.io/badge/license-AGPL--3.0-green)](LICENSE)
[![python](https://img.shields.io/badge/python-3.9%2B%20skill%20%C2%B7%203.10%2B%20MCP-blue)](#-requirements)
[![MCP](https://img.shields.io/badge/protocol-MCP-8A2BE2)](https://modelcontextprotocol.io)
[![tools](https://img.shields.io/badge/OSINT%20tools-909-informational)](#-features)

</div>

---

> [!WARNING]
> **This is ALPHA software. Do not use it in production before testing.**
>
> Claudii Exploratores is an early (alpha), community-maintained port of the Exploratores
> toolkit. It is covered by an automated test suite, but it has **not** been hardened or
> validated for production or operational use. Search URLs, validators and the tool
> catalog may contain errors inherited from upstream or introduced by the port.
> **Verify every output independently, test thoroughly in a safe environment, and
> validate results against trusted sources before relying on them.** Use at your own
> risk — see [Disclaimer](#-disclaimer).

---

## Table of Contents

- [About](#-about)
- [Features](#-features)
- [How it works](#-how-it-works)
- [Repository layout](#-repository-layout)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [Available MCP tools](#-available-mcp-tools)
- [Access warnings: VPN, Tor, accounts](#-access-warnings-vpn-tor-accounts)
- [Keeping in sync with Exploratores](#-keeping-in-sync-with-exploratores)
- [Project status](#-project-status)
- [Roadmap](#-roadmap)
- [FAQ and version history](#-faq-and-version-history)
- [Contributing](#-contributing)
- [Security & responsible use](#-security--responsible-use)
- [Disclaimer](#-disclaimer)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

## 🔎 About

**Claudii Exploratores** turns the [**Exploratores OSINT Toolkit**](https://github.com/SOsintOps/Exploratores)
— a static web application of curated OSINT search links — into two AI-native
distributions:

1. **An Agent Skill** (`skill/`) — a drop-in skill for Claude in Claude Code, Cowork
   or the Agent SDK. It teaches the model professional OSINT tradecraft (analytic
   standards, the 5W1H method, OPSEC) and gives it a CLI that turns any indicator
   into a curated set of search links.
2. **An MCP server** (`mcp/`) — a [Model Context Protocol](https://modelcontextprotocol.io)
   server (Python) exposing the same engine as callable tools for Claude Desktop,
   Claude Code or any MCP-compatible client.

Both share one language-neutral core: a **catalog of 909 OSINT tools** across **26
categories** (synced with Exploratores 3.10.5), an indicator classifier, per-source
access requirements (VPN country, Tor, account), an offline IBAN verifier and a
reversible PII redactor — all ported from the original toolkit.

> [!IMPORTANT]
> These tools **build** OSINT search URLs; they never open pages by themselves.
> Opening and reading stays with the operator (or an explicitly-invoked browser
> agent), so OPSEC — VPN, sterile browser profile — remains under human control.

## ✨ Features

- **909 curated OSINT tools** across 26 categories (people, usernames, email,
  domains, IP, phones, companies, crypto, IBAN, maps, media, social platforms,
  Telegram, Italian and EU legal sources…).
- **Indicator classifier** — auto-detects whether a value is a domain, email, IP,
  username, person name, phone, coordinates, IBAN, crypto address, VIN, hashtag,
  Normattiva URN, EU case number, EU VAT number, and more.
- **Curated URL builder** — fills and URL-encodes only the tools that fit the
  indicator, so you get a relevant, scoped set instead of 900 raw links.
- **Access warnings** — every link to a source that is geo-locked (needs a VPN exit
  in a given country), Tor-only or behind a login is flagged before you open it.
- **Cross-platform pivoting** — one username fans out to the right search across
  every social/community platform that supports it.
- **Offline IBAN verifier** — ISO 13616 mod-97 check against a 71-country table.
- **Reversible PII redactor** — strip emails, IPs, phones, IBANs, cards, URLs and
  crypto addresses before sending case text to an external model; restore afterwards.
- **Offline by design** — no network requests, no API keys; the MCP tools are
  annotated read-only and closed-world.
- **No mandatory dependencies for the skill** — standard-library Python 3.9+.
- **Single source of truth** — one shared engine + catalog, synced into both
  deliverables by a build script, checked weekly against Exploratores, tested in CI.

## 🧭 How it works

```
indicator ──▶ classify ──▶ build fields ──▶ select matching tools ──▶ URL-encode ──▶ link set + access warnings
 "Mario Rossi"   PERSON_NAME   {firstname,lastname,…}   names + records          %20…        grouped Markdown / JSON
```

The engine is a faithful Python port of the toolkit's original JavaScript logic
(`indicator-classifier.js`, `validators.js`, `main.js`), so generated URLs match
what the web toolkit produces.

## 📦 Repository layout

```text
claudii-exploratores/
├── skill/claudii-exploratores/   # the Agent Skill (SKILL.md + scripts + references)
│   ├── SKILL.md
│   ├── scripts/                  # exploratores.py CLI + engine + catalog.json + access.json
│   └── references/               # methodology.md, catalog_overview.md
├── mcp/                          # the MCP server (Python)
│   ├── exploratores_osint_mcp/   # package: server.py + engine + catalog.json + access.json
│   ├── pyproject.toml
│   ├── config.example.json
│   └── README.md
├── shared/                       # single source of truth for the engine + data
│   ├── osint_core.py             # classifier, field builder, URL renderer, access warnings
│   ├── iban_tools.py, redactor.py, _iban_countries.py
│   ├── catalog.json              # 909 tools (generated from Exploratores)
│   └── access.json               # per-host VPN / Tor / account requirements (generated)
├── scripts/                      # build, sync & verification tooling
│   ├── sync_catalog.py           # (re)generate catalog.json from the Exploratores export
│   ├── build_release.sh          # rebuild generated files, sync engine, package .skill
│   ├── classify_queries.py       # desk classification (auth/VPN) -> CSV
│   ├── generate_docs.py          # render the desk classification page
│   ├── build_access_map.py       # live + desk verdicts -> shared/access.json
│   ├── generate_catalog_overview.py  # render the skill's catalog overview
│   ├── check_links.py            # automated access check (pass A, then pass B per country)
│   ├── build_verification_worklist.py, record_verification.py,
│   └── generate_live_report.py, generate_access_guide.py   # live-verification pipeline
├── tests/                        # pytest suite (run in CI)
├── docs/                         # FAQ, version history, INSTALL, DISTRIBUTION, access guides
├── assets/                       # logo, social preview
├── .github/                      # CI, weekly sync check, issue and PR templates
├── dist/                         # build outputs (.skill archive) — git-ignored
├── LICENSE                       # AGPL-3.0 (inherited from Exploratores)
└── NOTICE
```

`shared/` is authoritative. `scripts/build_release.sh` copies the engine and data
into both `skill/` and `mcp/` so each is independently installable; CI fails if a
copy or a generated file is out of date.

## ⚙️ Requirements

- **Python 3.9+** for the skill (standard library only).
- **Python 3.10+** for the MCP server, with the `mcp` package (1.x or 2.x).
- A modern browser (and, recommended, a VPN + sterile profile) to *open* the
  generated links. Which sources need a **login**, a **VPN** (and which country),
  or **Tor** is flagged in every result — see
  [Access warnings](#-access-warnings-vpn-tor-accounts).

## 🚀 Installation

### Agent Skill (Claude Code / Cowork)

```bash
mkdir -p ~/.claude/skills
cp -R skill/claudii-exploratores ~/.claude/skills/
# or install claudii-exploratores.skill from the latest GitHub Release
```

Then simply ask, e.g. *"Run OSINT on the domain example.com"*.

### MCP Server (Claude Desktop, Claude Code)

```bash
cd mcp
pip install -e .            # or: uv pip install -e .
```

Add the server to your MCP client config (see [`mcp/README.md`](mcp/README.md)):

```json
{
  "mcpServers": {
    "claudii-exploratores": {
      "command": "python",
      "args": ["-m", "exploratores_osint_mcp.server"]
    }
  }
}
```

Claude Code: `claude mcp add claudii-exploratores -- python -m exploratores_osint_mcp.server`.
Details, Windows paths and a smoke test in [`docs/INSTALL.md`](docs/INSTALL.md).

## 💻 Usage

```bash
cd skill/claudii-exploratores

# Detect what an indicator is
python scripts/exploratores.py classify "john.doe@example.com"

# Build a curated OSINT link set (grouped Markdown, with ⚠️ access warnings)
python scripts/exploratores.py urls "example.com" --format markdown

# Force a type, add structured fields, or narrow to specific platforms
python scripts/exploratores.py urls "Mario Rossi" --type PERSON_NAME \
  --field firstname=Mario --field lastname=Rossi
python scripts/exploratores.py urls "johndoe" --categories x,instagram,vk

# Italian and EU legal sources, Telegram
python scripts/exploratores.py urls "urn:nir:stato:legge:1990-08-07;241"
python scripts/exploratores.py urls "IT00905811006" --type EU_VAT
python scripts/exploratores.py urls "durov" --type TELEGRAM_USERNAME

# Drop links that need a VPN exit in a specific country, and Tor links
python scripts/exploratores.py urls "John Smith" --no-geo-locked --no-onion

# Utilities
python scripts/exploratores.py iban "GB82 WEST 1234 5698 7654 32"
python scripts/exploratores.py redact "Contact john@x.com from 8.8.8.8"
python scripts/exploratores.py search "wayback"
```

## 🛠 Available MCP tools

All seven are read-only, idempotent and make no network request.

| Tool | Purpose |
| --- | --- |
| `classify_indicator(value)` | Detect the indicator type(s) with confidence scores. |
| `build_osint_urls(value, indicator_type?, categories?, fields?, include_onion?, limit?, exclude_geo_locked?)` | Curated OSINT search-URL set, with an `access_note` per link and `warnings`. |
| `search_catalog(query, limit?)` | Free-text search across the catalog. |
| `list_categories()` | Categories and tool counts. |
| `verify_iban(value)` | Offline IBAN validation (ISO 13616 mod-97). |
| `redact_pii(text, only?, custom_patterns?)` | Redact PII, returning a reversible map. |
| `restore_pii(text, redaction_map)` | Reverse a redaction. |

## 🌍 Access warnings: VPN, Tor, accounts

Some sources only work under conditions you should know *before* opening them.
Each result can carry an `access` record and an `access_note`, and the response
starts with `warnings`:

- **GEO-LOCKED** — the source only answers IP addresses in one country (mostly US
  people-search and phone lookups). Set the VPN to an exit in that country first,
  or drop these links with `exclude_geo_locked` / `--no-geo-locked`.
- **VPN recommended** — estimated at the desk, not verified: try without first.
- **Tor only** — `.onion` services, Tor Browser only.
- **Account required / recommended**, **bot protection seen**.

The data lives in `shared/access.json`, built from the live checks in
[`docs/access-requirements-guide.md`](docs/access-requirements-guide.md) (browser
probes from Italy, then a VPN exit in the candidate country for the hosts that did
not work) and the desk classification in
[`docs/query-auth-vpn-classification.md`](docs/query-auth-vpn-classification.md).
A VPN changes the exit IP, not the identity: keep a sterile browser profile.

## 🔄 Keeping in sync with Exploratores

The catalog is generated from the JSON export that Exploratores publishes; a weekly
workflow opens an issue when Exploratores changes. To update:

```bash
scripts/build_release.sh /path/to/Exploratores   # checkout of branch v3
pytest -q tests
```

This re-syncs `catalog.json` (labels from the toolkit's pages), rebuilds the
classification, the access map and the catalog overview, copies the engine into
both deliverables, and repackages the `.skill` archive. See
[`docs/DISTRIBUTION.md`](docs/DISTRIBUTION.md).

## 🧪 Project status

**Alpha (v1.1.0-alpha).** The suite is functional and covered by an automated test
suite run in CI (catalog integrity, every placeholder reachable, URL encoding,
access warnings, IBAN and redaction round-trips, MCP tool registration on `mcp` 1.x
and 2.x). It has **not** been hardened for production. Known limitations:

- A small number of URL templates are inherited verbatim from upstream and may be
  imperfect (e.g. dork operators with literal spaces; the Bitly template, which
  uses the short link itself).
- Some sources need inputs the indicator cannot provide (a US state for licence
  plates, a full address, a date range): pass them in `fields` / `--field`.
- Phone-number field derivation is best-effort and does not replicate the full
  `libphonenumber` logic of the original web toolkit.
- Offline **bank-name** resolution for IBANs is not ported (only structural
  validation); that dataset lives in the original web toolkit.

Please **test in a controlled environment** and report issues before any
operational use.

## 🗺 Roadmap

- [x] Automated test suite (pytest) covering classifier, renderer, IBAN, redactor.
- [x] CI (GitHub Actions) on every push and pull request.
- [x] Weekly sync check against Exploratores.
- [x] Access warnings for geo-locked, Tor-only and login-only sources.
- [x] Access recheck (2026-11-01): automated pass on every host, browser pass through US and Swedish VPN exits on the hosts that failed, compared with a home IP in Italy.
- [x] Sources behind interactive checks and the Russian sources: reviewed by hand in Exploratores, which keeps them active (alive behind bot protection; checko.ru hostile to western IP addresses).
- [ ] PyPI release of the MCP server and listing in the MCP registry (`server.json` ready).
- [ ] Fuller phone-number parsing parity with the upstream toolkit.
- [ ] Optional bank-name resolution for IBANs.

## 📚 FAQ and version history

- [**FAQ**](docs/faq.md) — the name, OSINT practice, and a section on using MCP and
  LLMs for OSINT (offline design, what a model may and may not do, prompt injection,
  redact-then-restore, local models, browser agents, other OSINT MCP servers).
- [**Version history**](docs/versionhistory.md).

## 🤝 Contributing

Contributions and bug reports are welcome: see [`CONTRIBUTING.md`](CONTRIBUTING.md)
and the [Code of Conduct](CODE_OF_CONDUCT.md). New sources and dead links are handled
in [Exploratores](https://github.com/SOsintOps/Exploratores) first and reach this
repository on the next sync. Keep engine changes in `shared/`, run
`scripts/build_release.sh` and `pytest`, and preserve attribution.

## 🛡 Security & responsible use

- **For authorised, lawful investigation only** — research, security, journalism,
  due diligence. Do not use it for stalking, harassment or doxxing.
- **The tools build links; they do not fetch data.** Opening pages exposes your IP
  and fingerprint to target-controlled infrastructure — use a VPN and a sterile
  browser profile, and prefer cached/archived views for first contact.
- **Treat all outputs as leads to verify**, never as conclusions. Corroborate across
  independent sources and record provenance.
- Some catalog entries are **Tor hidden services** (`.onion`) and require Tor
  Browser; exclude them with `--no-onion` / `include_onion=false`.

To report a security concern, follow [`SECURITY.md`](SECURITY.md) (private security
advisory, not a public issue).

## ⚠️ Disclaimer

This software is provided **"as is", without warranty of any kind**, express or
implied. It is **alpha** software and **not intended for production use**. The authors and
contributors accept **no liability** for any damage, loss, legal consequence or
misuse arising from its use. You are solely responsible for ensuring your use
complies with all applicable laws, regulations and third-party terms of service, and
for independently verifying every result before acting on it.

## 📄 License

Licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)** — the same
licence as the original work. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).

## 🙏 Acknowledgements

Derived from the **Exploratores OSINT Toolkit** by *Ramingo* ([SOsintOps](https://github.com/SOsintOps/Exploratores)).
This project ports its search catalog, classifier, validators, IBAN table and
redactor concept to a Python engine packaged as a Claude skill and an MCP server.
All credit for the original toolkit and its curation belongs to the upstream author.

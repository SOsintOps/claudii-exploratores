<div align="center">

# Claudii Exploratores

### OSINT Suite for Claude — Agent Skill + MCP Server

*"The scouts of Claudius"* — a nod to the Roman reconnaissance units (*exploratores*)
and to Claude. OSINT reconnaissance, ported for AI agents.

[![status](https://img.shields.io/badge/status-alpha-orange)](#-project-status)
[![version](https://img.shields.io/badge/version-1.0.0--alpha-blue)](#)
[![license](https://img.shields.io/badge/license-AGPL--3.0-green)](LICENSE)
[![python](https://img.shields.io/badge/python-3.9%2B-blue)](#-requirements)
[![MCP](https://img.shields.io/badge/protocol-MCP-8A2BE2)](https://modelcontextprotocol.io)
[![tools](https://img.shields.io/badge/OSINT%20tools-898-informational)](#-features)

</div>

---

> [!WARNING]
> **This is ALPHA software. Do not use it in production before testing.**
>
> Claudii Exploratores is a very early (alpha), community-maintained port of the Exploratores
> toolkit. It has been functionally tested, but it has **not** been hardened or
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
  - [Agent Skill](#agent-skill-claude-code--cowork)
  - [MCP Server](#mcp-server-claude-desktop)
- [Usage](#-usage)
- [Available MCP tools](#-available-mcp-tools)
- [Rebuilding the catalog](#-rebuilding-the-catalog)
- [Project status](#-project-status)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [Security & responsible use](#-security--responsible-use)
- [Disclaimer](#-disclaimer)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

## 🔎 About

**Claudii Exploratores** turns the [**Exploratores OSINT Toolkit**](https://github.com/SOsintOps/Exploratores)
— a static web application of curated OSINT search links — into two AI-native
distributions:

1. **An Agent Skill** (`skill/`) — a drop-in skill for Claude (Opus/Sonnet) in
   Claude Code, Cowork or the Agent SDK. It teaches the model professional OSINT
   tradecraft (analytic standards, the 5W1H method, OPSEC) and gives it a CLI that
   turns any indicator into a curated set of search links.
2. **An MCP server** (`mcp/`) — a [Model Context Protocol](https://modelcontextprotocol.io)
   server (Python / FastMCP) exposing the same engine as callable tools for Claude
   Desktop or any MCP-compatible client.

Both share one language-neutral core: a **catalog of 898 OSINT tools** across **24
categories**, an indicator classifier, input validators, an offline IBAN verifier
and a reversible PII redactor — all ported from the original toolkit.

> [!IMPORTANT]
> These tools **build** OSINT search URLs; they never open pages by themselves.
> Opening and reading stays with the operator (or an explicitly-invoked browser
> agent), so OPSEC — VPN, sterile browser profile — remains under human control.

## ✨ Features

- **898 curated OSINT tools** across 24 categories (people, usernames, email,
  domains, IP, phones, companies, crypto, IBAN, maps, media, social platforms…).
- **Indicator classifier** — auto-detects whether a value is a domain, email, IP,
  username, person name, phone, coordinates, IBAN, crypto address, VIN, and more.
- **Curated URL builder** — fills and URL-encodes only the tools that fit the
  indicator, so you get a relevant, scoped set instead of 898 raw links.
- **Cross-platform pivoting** — one username fans out to the right search across
  every social/community platform that supports it.
- **Offline IBAN verifier** — ISO 13616 mod-97 check against a 71-country table.
- **Reversible PII redactor** — strip emails, IPs, phones, IBANs, cards, URLs and
  crypto addresses before sending case text to an external model; restore afterwards.
- **No mandatory dependencies for the skill** — standard-library Python 3.9+.
- **Single source of truth** — one shared engine + catalog, synced into both
  deliverables by a build script; regenerable from the upstream toolkit.

## 🧭 How it works

```
indicator ──▶ classify ──▶ build fields ──▶ select matching tools ──▶ URL-encode ──▶ curated link set
 "Mario Rossi"   PERSON_NAME   {firstname,lastname,…}   names + records          %20…        grouped Markdown / JSON
```

The engine is a faithful Python port of the toolkit's original JavaScript logic
(`indicator-classifier.js`, `validators.js`, `main.js`), so generated URLs match
what the web toolkit produces.

## 📦 Repository layout

```text
Claudii-Exploratores/
├── skill/claudii-exploratores/   # the Agent Skill (SKILL.md + scripts + references)
│   ├── SKILL.md
│   ├── scripts/                  # exploratores.py CLI + engine + catalog.json
│   └── references/               # methodology.md, catalog_overview.md
├── mcp/                          # the MCP server (Python, FastMCP)
│   ├── exploratores_osint_mcp/   # package: server.py + engine + catalog.json
│   ├── pyproject.toml
│   ├── config.example.json
│   └── README.md
├── shared/                       # single source of truth for the engine + catalog
│   ├── osint_core.py             # classifier, field builder, URL renderer
│   ├── iban_tools.py, redactor.py, _iban_countries.py
│   └── catalog.json              # 898 tools (generated)
├── scripts/                      # build & extraction tooling
│   ├── extract_catalog.js        # (re)generate catalog.json from the web toolkit
│   └── build_release.sh          # sync engine into skill+mcp, package .skill
├── docs/                         # INSTALL.md, DISTRIBUTION.md
├── dist/                         # build outputs (.skill archive) — git-ignored
├── LICENSE                       # AGPL-3.0 (inherited from Exploratores)
└── NOTICE
```

`shared/` is authoritative. `scripts/build_release.sh` copies the engine + catalog
into both `skill/` and `mcp/` so each is independently installable.

## ⚙️ Requirements

- **Python 3.9+** (standard library only for the skill; the MCP adds the `mcp` package).
- **Node.js** — only needed to *regenerate* the catalog from the upstream toolkit.
- A modern browser (and, recommended, a VPN + sterile profile) to *open* the
  generated links.

## 🚀 Installation

### Agent Skill (Claude Code / Cowork)

Copy the skill into your skills directory, or install the packaged archive from
your client's UI:

```bash
mkdir -p ~/.claude/skills
cp -R skill/claudii-exploratores ~/.claude/skills/
# or install dist/claudii-exploratores.skill from your Claude client
```

Then simply ask, e.g. *"Run OSINT on the domain example.com"*.

### MCP Server (Claude Desktop)

```bash
cd mcp
pip install -e .            # or: uv pip install -e .
```

Add the server to your MCP client config (see [`mcp/README.md`](mcp/README.md) and
[`docs/INSTALL.md`](docs/INSTALL.md)):

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

## 💻 Usage

Drive the skill's CLI directly:

```bash
cd skill/claudii-exploratores

# Detect what an indicator is
python scripts/exploratores.py classify "john.doe@example.com"

# Build a curated OSINT link set (grouped Markdown by default)
python scripts/exploratores.py urls "example.com" --format markdown

# Force a type, add structured fields, or narrow to specific platforms
python scripts/exploratores.py urls "Mario Rossi" --type PERSON_NAME \
  --field firstname=Mario --field lastname=Rossi
python scripts/exploratores.py urls "johndoe" --categories x,instagram,vk

# Utilities
python scripts/exploratores.py iban "GB82 WEST 1234 5698 7654 32"
python scripts/exploratores.py redact "Contact john@x.com from 8.8.8.8"
python scripts/exploratores.py search "wayback"
```

## 🛠 Available MCP tools

| Tool | Purpose |
| --- | --- |
| `classify_indicator(value)` | Detect the indicator type(s) with confidence scores. |
| `build_osint_urls(value, indicator_type?, categories?, fields?, include_onion?, limit?)` | Curated OSINT search-URL set for the indicator. |
| `search_catalog(query, limit?)` | Free-text search across the 898-tool catalog. |
| `list_categories()` | Categories and tool counts. |
| `verify_iban(value)` | Offline IBAN validation (ISO 13616 mod-97). |
| `redact_pii(text, only?, custom_patterns?)` | Redact PII, returning a reversible map. |
| `restore_pii(text, redaction_map)` | Reverse a redaction. |

## 🔄 Rebuilding the catalog

If the upstream toolkit is updated, regenerate everything from it:

```bash
scripts/build_release.sh /path/to/Exploratores-3.4.1
```

This re-extracts `catalog.json` (with human-readable labels harvested from the
toolkit's HTML pages), re-syncs the engine into both deliverables, and repackages
the `.skill` archive.

## 🧪 Project status

**Alpha (v1.0.0-alpha).** The suite is functional and has passed an internal QA pass
(catalog integrity, URL encoding, IBAN and redaction round-trips, MCP tool
registration). It has **not** been hardened for production. Known limitations:

- A small number of URL templates are inherited verbatim from upstream and may be
  imperfect (e.g. dork operators with literal spaces; one degenerate short-URL
  template).
- Phone-number field derivation is best-effort and does not replicate the full
  `libphonenumber` logic of the original web toolkit.
- Offline **bank-name** resolution for IBANs is not ported (only structural
  validation); that dataset lives in the original web toolkit.

Please **test in a controlled environment** and report issues before any
operational use.

## 🗺 Roadmap

- [ ] Automated test suite (pytest) covering classifier, renderer, IBAN, redactor.
- [ ] CI (GitHub Actions) for lint + tests on every push.
- [ ] Optional PyPI release of the MCP server.
- [ ] Fuller phone-number parsing parity with the upstream toolkit.
- [ ] Optional bank-name resolution for IBANs.

## 🤝 Contributing

Contributions and bug reports are welcome.

1. Open an issue describing the bug or proposal.
2. Fork the repo and create a feature branch.
3. Keep the engine changes in `shared/` (the single source of truth) and run
   `scripts/build_release.sh` to sync them into `skill/` and `mcp/`.
4. Open a pull request with a clear description and, where relevant, before/after
   examples.

Please follow the conventions in the upstream `AGENTS.md` and preserve attribution.

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

To report a security concern, please open a private security advisory on GitHub
rather than a public issue.

## ⚠️ Disclaimer

This software is provided **"as is", without warranty of any kind**, express or
implied. It is **beta** and **not intended for production use**. The authors and
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

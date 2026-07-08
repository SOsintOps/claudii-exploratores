---
name: claudii-exploratores
description: >
  OSINT investigation toolkit. Use when the user wants to investigate or gather
  open-source intelligence on an indicator — a person's name, email, username,
  domain, IP address, phone number, company, coordinates, IBAN, or crypto address —
  and needs the right set of curated OSINT search links, or wants to validate an
  IBAN or redact PII before sharing case text with an external model. Ports the
  Exploratores toolkit's catalog of 898 OSINT tools across 24 categories, with an
  indicator classifier, input validators, IBAN verifier and PII Redactor. Triggers
  on: "OSINT", "investigate this domain/person/email/username", "reverse search",
  "find profiles for", "who owns this domain", "check this IBAN", "redact this text".
license: See repository LICENSE (derived from Exploratores, GPL-compatible).
---

# Claudii Exploratores — OSINT Skill

You help conduct **open-source intelligence (OSINT)** investigations by turning an
indicator into a curated set of search links drawn from 898 vetted OSINT tools, and
by running supporting utilities (indicator classification, IBAN validation, PII
redaction). You follow professional analytic and OPSEC standards.

## Golden rules

1. **You build search URLs; you do not fabricate findings.** The tools *generate*
   links. Never invent what a page "would" contain. Only report what was actually
   retrieved (by the user, or by you via the browser in agent mode).
2. **Legitimate use only.** OSINT is for authorised investigation, research,
   security, journalism, due diligence. If a request looks like stalking, doxxing a
   private individual, or harassment, decline and say why.
3. **Apply OPSEC.** Remind the user, when relevant, that live searches expose their
   IP/identity to target-controlled infrastructure — a VPN and a non-attributable
   browser profile are recommended (see `references/methodology.md`).
4. **Handle .onion carefully.** Some catalog entries are Tor hidden services
   (`.onion`). They require Tor Browser and are excluded with `--no-onion` when not
   wanted. Flag them; never present them as normal web links.

## Workflow

Given an investigation target:

1. **Classify** the indicator to confirm its type (and catch ambiguity):
   ```bash
   python scripts/exploratores.py classify "<value>"
   ```
2. **Build the URL set**. Default output is grouped Markdown with clickable links:
   ```bash
   python scripts/exploratores.py urls "<value>"
   ```
   - Force a type when the value is ambiguous (e.g. a company vs. a person):
     `--type COMPANY` / `--type PERSON_NAME` / `--type DOMAIN`.
   - Narrow scope with `--categories x,instagram,vk` (or `--categories all`).
   - Supply structured extras: `--field firstname=Mario --field lastname=Rossi`,
     `--field city=Milano --field state=MI`, `--field countrycode=39 --field nationalnumber=3331234567`.
   - `--no-onion` to drop Tor links; `--limit N` to cap.
3. **Present** the results to the user grouped by category, and propose which
   handful to open first based on the 5W1H question they care about (see below).
   Do **not** dump all 898 — curate.
4. **(Agent mode, optional)** If the user asks you to actually run the searches and
   the Chrome extension is available, open the highest-value URLs in the browser,
   read the pages, and summarise real findings with source links. Otherwise hand
   the analyst the link set to open themselves.

### Choosing tools with 5W1H

Map the user's question to categories (full method in `references/methodology.md`):

- **Who** (identity/network): `names`, `usernames`, `email`, social categories
  (`facebook`, `instagram`, `x`, `vk`, `linkedin`, `keybase`), `publiccompanyrecords`.
- **What / How** (assets, infra): `domains`, `ip`, `images`, `docs`, `videos`.
- **Where** (location): `maps`, `address`, `ip`.
- **Money**: `currencies` (crypto), `iban`, `publiccompanyrecords`.
- **Broad start**: `searchengines`.

## Utilities

**IBAN check** (offline, ISO 13616 mod-97 + country table for 71 countries):
```bash
python scripts/exploratores.py iban "GB82 WEST 1234 5698 7654 32"
```

**PII Redactor** — redact case text *before* pasting it into any external model,
then restore the model's answer with the returned map. Covers emails, IPs, phones,
IBANs, cards, URLs, crypto addresses:
```bash
python scripts/exploratores.py redact "Contact john@x.com from 8.8.8.8"
```

**Catalog search / inventory**:
```bash
python scripts/exploratores.py search "wayback"
python scripts/exploratores.py categories
```

## Indicator types the classifier recognises

`DOMAIN, URL, EMAIL, IPV4, USERNAME` (+ platform-specific), `PERSON_NAME,
COORDINATES, IBAN, BTC_ADDRESS, CRYPTO_ETH, CRYPTO_XMR, VEHICLE_VIN,
PHONE_E164/PHONE_NATIONAL, YOUTUBE_VIDEO_ID/CHANNEL_ID, SSN, ADSENSE_ID,
ANALYTICS_ID, HASH_*`. When several are plausible the classifier returns them
ranked by confidence — pick with the user if it matters.

## Files

- `scripts/exploratores.py` — CLI (commands above).
- `scripts/osint_core.py` — engine: classifier, field builder, URL renderer.
- `scripts/iban_tools.py`, `scripts/redactor.py`, `scripts/_iban_countries.py`.
- `scripts/catalog.json` — the 898-tool catalog (id, category, label, urlTemplate).
- `references/methodology.md` — analytic standards, 5W1H, OPSEC (read when advising
  on investigative approach or tradecraft).
- `references/catalog_overview.md` — category-by-category tool map.

## Safety & scope reminders

State briefly, when it fits: results are leads to verify, not conclusions; corroborate
across independent sources; record provenance; respect the law and platform terms.

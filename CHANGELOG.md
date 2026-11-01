# Changelog

## 2026-11-01 — catalog aligned with the Exploratores dead-link review (3.10.2–3.10.4)

The catalog is still the Exploratores 3.4.1 port; only the dead-link review done upstream on 2026-10-31 and 2026-11-01 is applied. Every source below was re-checked by hand upstream (public DNS, registry data, residential IP, browser). Catalog: 898 → 874 tools.

**Removed** (28 tools on closed services):
- RiskIQ, 7 tools (`community.riskiq.com`, folded into the licensed Microsoft Defender portal): `domains-sec-riskiq`, `domains-adsense-riskiq`, `domains-analytics-riskiq`, `ip-security-riskiq`, `names-riskiq`, `phoneint-riskiq`, `usernames-riskiq`
- ThreatCrowd (`ci-www.threatcrowd.org`): `domains-sec-threatcrowd`, `ip-security-threatcrowd`
- psbdmp (`psbdmp.ws`): `email-psbdmp`, `usernames-psbdmp`
- Nuwber (`nuwber.com`, shut down in September 2026): `names-us-nuwber`, `phoneus-nuwber`
- SpyTox (`spytox.com`): `email-spytox`, `phoneus-spytox`
- `currencies-btc-validation` (bitcoin-e.org), `currencies-btc-oxtme` (OXT.me), `domains-dns-subdomains-columbus` (Columbus), `domains-dns-domainapp` (DomainApp), `domains-archive-mementoweb` (Memento Time Travel), `domains-archive-archivescan` (web-archive-scan.com, domain lapsed), `domains-profile-webscout` (web-scout.io, domain lapsed), `domains-profile-spyonweb` (SpyOnWeb), `domains-seo-sitemapper` (SiteMapper), `domains-sec-phishcheck` (PhishCheck.me, domain now points to someone else's server), `names-us-usaofficial` (USA-Official), `usernames-checkistan` (Checkistan), `publiccompanyrecords-officer-moneyline` (PoliticalMoneyLine)

**Changed:**
- `communities-reddit-archive`: unddit (gone) → Arctic Shift
- `domains-records-udrp`, `names-udrp`, `publiccompanyrecords-company-udrp`: UDRPSearch (switched off) → WIPO decision database
- `publiccompanyrecords-officer-foia`, `publiccompanyrecords-company-foia`: `search.foia.gov` (gone) → `search.usa.gov` with `affiliate=foia.gov`
- `ip-security-ikwyd`: now over HTTPS

**Added:**
- `ip-security-alienvault` (AlienVault OTX for IP addresses)
- `domains-records-udrp-cac`, `names-udrp-cac`, `publiccompanyrecords-company-udrp-cac` (CAC UDRP decision database, Czech Arbitration Court)

**Docs:** `docs/query_classification.csv` and `docs/query-auth-vpn-classification.md` regenerated with the project scripts; `docs/access-requirements-guide.md` revised by hand (its live-verification data is not in the repository): the removed sources are dropped and every count is recomputed. Tool counts updated in the README, the skill, the MCP server and the catalog overview.

**Not done here:** the full re-sync with the current Exploratores catalog. Upstream has 44 tools that are not in this port (Legal page, Italian sources, SanctionsKit, the new Telegram page) and they use 7 placeholders that `osint_core.py` does not build yet (`{urn}`, `{vat_country}`, `{vat_number}`, `{case}`, `{msgid}`, `{q}`, `{national_raw}`), so `build_release.sh` would produce broken URLs for them.

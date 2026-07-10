# -*- coding: utf-8 -*-
"""Render the human-readable classification page from query_classification.csv."""
import csv, datetime, os
from collections import defaultdict, Counter

HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
SRC=os.path.join(ROOT,"docs","query_classification.csv")
OUT=os.path.join(ROOT,"docs","query-auth-vpn-classification.md")
rows=list(csv.DictReader(open(SRC,encoding="utf-8")))

CAT_LABEL={
 'searchengines':'Search engines','domains':'Domains / infrastructure','names':'Names / people',
 'phoneus':'US phone','phoneint':'International phone','publiccompanyrecords':'Public company records',
 'email':'Email','usernames':'Usernames','communities':'Communities / forums','maps':'Maps / geospatial',
 'address':'Addresses','currencies':'Cryptocurrencies','videos':'Videos','keybase':'Keybase','ip':'IP / network',
 'docs':'Documents','images':'Images','linkedin':'LinkedIn','x':'X / Twitter','facebook':'Facebook',
 'instagram':'Instagram','vehicles':'Vehicles','vk':'VK','iban':'IBAN',
}
ORDER=['searchengines','usernames','names','email','domains','ip','publiccompanyrecords','address',
 'phoneus','phoneint','facebook','instagram','x','linkedin','vk','communities','maps','images','videos',
 'docs','currencies','vehicles','keybase','iban']

def esc(s): return (s or '').replace('|','\\|').replace('\n',' ')
def bv(v):
    if v.startswith('Tor'): return 'Tor'
    if v.startswith('No '): return 'no-VPN'
    if 'United States' in v: return 'VPN-US'
    return 'VPN-country'
def ba(a):
    if a.startswith('Platform login'): return 'social-login'
    if a.startswith('No (free'): return 'free-opt'
    if a=='No login': return 'no-login'
    return 'account/paywall'

tot=len(rows)
authc=Counter(ba(r['auth_access']) for r in rows); vpnc=Counter(bv(r['vpn_access']) for r in rows)
confc=Counter(r['confidence'] for r in rows)
ICON={'High':'● High','Medium':'◑ Medium','Low':'○ Low'}

hdr=f"""# OSINT query classification: authenticated Chrome profile & VPN

> **Project:** Claudii-Exploratores (standalone)
> **Scope:** Exploratores 3.4.1 catalog (`shared/catalog.json`) — **{tot} queries across 24 categories**
> **Last updated:** {datetime.date.today().isoformat()}
> **Status:** **desk** analysis (no live testing) — see disclaimer.

---

## 1. Purpose

For every query launchable from Exploratores, decide:

1. **Is an authenticated Chrome profile required** (dedicated account / sock-puppet), or does the query work without login?
2. **Is a VPN in a specific country (or Tor) required**, or does it work from any network exit?

The goal is an operational guide on *what to prepare beforehand* for each search category (profiles, service accounts, VPN/Tor exits) and *which OPSEC precautions* to apply.

## 2. Method and disclaimer (important)

- **Desk analysis.** Classification is derived from knowledge of each service (known login and geo-blocking behaviour), **not from live tests** run in this session. No result is presented as verified.
- **Per-row confidence.** Each entry carries a level: **{ICON['High']}** (stable, well-known behaviour), **{ICON['Medium']}** (depends on feature/region/anti-bot), **{ICON['Low']}** (variable or subject to paywalls/frequent change).
- **Field verification.** Login requirements and geo-blocks change over time. Medium/Low rows should be confirmed at time of use.
- **Two readings per axis.** We separate the **access requirement** (login/VPN *technically* needed to obtain the data) from the **OPSEC recommendation** (what is prudent anyway to avoid burning identity or IP). The former is in the tables below; both (4 columns) are in the companion CSV `query_classification.csv`.

## 3. Legend

**Access requirement — Authentication**

| Value | Meaning |
|---|---|
| `No login` | The query returns a result without authentication. |
| `No (free; account only for volume/extras)` | Works without login; a free account only unlocks volume/extras. |
| `Registration/account/paywall` | An account (free or paid) or API key is needed for the useful result. |
| `Platform login: X` | You must be logged into social platform **X** to view content → use a **dedicated sock-puppet**. |

**Access requirement — VPN / country**

| Value | Meaning |
|---|---|
| `No (global access)` | No VPN required for access. |
| `VPN <country> recommended` | The service may limit/block foreign IPs or give better results from that country. |
| `Tor required` | `.onion` resource: reachable only via Tor, not on the clearnet. |

**OPSEC recommendation** (per-row detail in the CSV; summary in §5)

- *Auth-OPSEC:* which identity to use (dedicated research profile / service account / sock-puppet).
- *VPN-OPSEC:* network attribution (recommended for everything; **mandatory** for direct visits to the target's profile; **Tor** for onions).

## 4. Executive summary

**Authentication** ({tot} queries)

| Requirement bucket | Queries | Share |
|---|---:|---:|
| No login | {authc['no-login']} | {authc['no-login']*100//tot}% |
| Social platform login (sock-puppet) | {authc['social-login']} | {authc['social-login']*100//tot}% |
| Registration/account/paywall | {authc['account/paywall']} | {authc['account/paywall']*100//tot}% |
| Free (optional account) | {authc['free-opt']} | {authc['free-opt']*100//tot}% |

**VPN / country** ({tot} queries)

| Requirement bucket | Queries | Share |
|---|---:|---:|
| No VPN required | {vpnc['no-VPN']} | {vpnc['no-VPN']*100//tot}% |
| VPN US recommended | {vpnc['VPN-US']} | {vpnc['VPN-US']*100//tot}% |
| VPN specific country recommended (SE/RU/NG/CA/IT/UK) | {vpnc['VPN-country']} | {vpnc['VPN-country']*100//tot}% |
| Tor required (.onion) | {vpnc['Tor']} | {vpnc['Tor']*100//tot}% |

**Confidence:** {ICON['High']} {confc['High']} · {ICON['Medium']} {confc['Medium']} · {ICON['Low']} {confc['Low']}

**At a glance.** The large majority of queries (~{authc['no-login']*100//tot}%) need no login and (~{vpnc['no-VPN']*100//tot}%) work from any network exit: search engines, whois/DNS, block explorers, archives and public aggregators. Requirements cluster in clear blocks: **login** for social platforms (Facebook, Instagram, X, VK, LinkedIn, part of Telegram/Discord); **account/paywall** for infrastructure and breach-data services (Shodan, Censys, DeHashed, DomainTools, VirusTotal…); **geography** for US people-search and some national registries (Sweden, Russia); **Tor** for dark-web search engines.

## 5. Operational decision guide

1. **Social queries with content** (facebook, instagram, x, vk, linkedin; part of communities/usernames) → **authenticated Chrome profile with a dedicated platform sock-puppet**, never a personal account. Network attribution **mandatory** (VPN/managed attribution): you directly visit a resource the target can control.
2. **Infrastructure/breach services** (Shodan, Censys, DeHashed, DomainTools, VirusTotal, Hunter, IntelX…) → **dedicated service account / non-personal API key**. No country VPN needed; generic VPN recommended.
3. **US people-search and US phone** → no login, but **US VPN exit recommended** (many sites limit/block EU IPs due to GDPR/CCPA, or serve data better from a US IP).
4. **National registries/directories** (Sweden, Russia; to a lesser extent Nigeria/Canada/Italy/UK) → consider a **VPN exit in that country** if access from a foreign IP is blocked or degraded.
5. **Dark-web search engines** (`.onion`) → **Tor** (Tor Browser / OSINT VM with Tor), not a clearnet VPN.
6. **Everything else** (search engines, whois/DNS, archives, block explorers, geospatial) → **no login and no country VPN**; still use a **dedicated research profile** and **managed network attribution** as baseline OPSEC hygiene. Note: with VPN/Tor, search engines (Google above all) may prompt captchas.

> **Direct visits to the target.** Some queries hit the target's own infrastructure (e.g. `domain/robots.txt`, favicon, live site screenshot). Even if they technically need no login/VPN, **managed network attribution is always mandatory** for these: the analyst's IP would land in the target's logs.

---

## 6. Per-category detail (all {tot} queries)

Columns: **Service** · **Host** · **Auth (access)** · **VPN/country (access)** · **Conf.**
Per-row OPSEC recommendations (identity and network) are in the companion CSV.
"""

by=defaultdict(list)
for r in rows: by[r['category']].append(r)
parts=[hdr]
for c in ORDER:
    rs=by.get(c,[])
    if not rs: continue
    a=Counter(ba(x['auth_access']) for x in rs); v=Counter(bv(x['vpn_access']) for x in rs)
    def frag(cnt):
        m=[]
        for k in ['no-login','social-login','account/paywall','free-opt','no-VPN','VPN-US','VPN-country','Tor']:
            if cnt.get(k): m.append(f"{cnt[k]} {k}")
        return ', '.join(m)
    parts.append(f"\n### {CAT_LABEL.get(c,c)}  —  {len(rs)} queries\n")
    parts.append(f"*Auth:* {frag(a)}  ·  *VPN:* {frag(v)}\n")
    parts.append("| Service | Host | Auth (access) | VPN/country (access) | Conf. |")
    parts.append("|---|---|---|---|:--:|")
    for x in sorted(rs,key=lambda r:(r['host'],r['label'])):
        ci={'High':'●','Medium':'◑','Low':'○'}[x['confidence']]
        parts.append(f"| {esc(x['label'])} | `{esc(x['host'])}` | {esc(x['auth_access'])} | {esc(x['vpn_access'])} | {ci} |")
    parts.append("")

foot=f"""
---

## 7. Notes, limits and maintenance

- **Data source:** `shared/catalog.json` (Exploratores 3.4.1). If the catalog is regenerated, re-run the classification script.
- **Reproducibility:** the table is produced by `scripts/classify_queries.py` (host/category rules) → `docs/query_classification.csv` → `scripts/generate_docs.py` → this `.md`. Rules are declarative and inspectable.
- **Out of scope:** it does not test real-time reachability, does not handle credentials, and does not weigh legal/mandate limits (using sock-puppets and accessing certain services must be authorised within the operational framework).
- **Medium/Low rows:** confirm login and geo-blocking at time of use; report deviations to update the rules.
- **Confidence legend:** ● High · ◑ Medium · ○ Low.

*Generated as a desk analysis; it is not a guarantee of accessibility for individual services.*
"""
parts.append(foot)
open(OUT,'w',encoding='utf-8').write('\n'.join(parts))
print("Wrote:",OUT,"| lines:",sum(1 for _ in open(OUT,encoding='utf-8')))

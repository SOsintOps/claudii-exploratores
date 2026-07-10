# OSINT query classification: authenticated Chrome profile & VPN

> **Project:** Claudii-Exploratores (standalone)
> **Scope:** Exploratores 3.4.1 catalog (`shared/catalog.json`) — **898 queries across 24 categories**
> **Last updated:** 2026-07-10
> **Status:** **desk** analysis (no live testing) — see disclaimer.

---

## 1. Purpose

For every query launchable from Exploratores, decide:

1. **Is an authenticated Chrome profile required** (dedicated account / sock-puppet), or does the query work without login?
2. **Is a VPN in a specific country (or Tor) required**, or does it work from any network exit?

The goal is an operational guide on *what to prepare beforehand* for each search category (profiles, service accounts, VPN/Tor exits) and *which OPSEC precautions* to apply.

## 2. Method and disclaimer (important)

- **Desk analysis.** Classification is derived from knowledge of each service (known login and geo-blocking behaviour), **not from live tests** run in this session. No result is presented as verified.
- **Per-row confidence.** Each entry carries a level: **● High** (stable, well-known behaviour), **◑ Medium** (depends on feature/region/anti-bot), **○ Low** (variable or subject to paywalls/frequent change).
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

**Authentication** (898 queries)

| Requirement bucket | Queries | Share |
|---|---:|---:|
| No login | 628 | 69% |
| Social platform login (sock-puppet) | 138 | 15% |
| Registration/account/paywall | 110 | 12% |
| Free (optional account) | 22 | 2% |

**VPN / country** (898 queries)

| Requirement bucket | Queries | Share |
|---|---:|---:|
| No VPN required | 768 | 85% |
| VPN US recommended | 94 | 10% |
| VPN specific country recommended (SE/RU/NG/CA/IT/UK) | 27 | 3% |
| Tor required (.onion) | 9 | 1% |

**Confidence:** ● High 642 · ◑ Medium 211 · ○ Low 45

**At a glance.** The large majority of queries (~69%) need no login and (~85%) work from any network exit: search engines, whois/DNS, block explorers, archives and public aggregators. Requirements cluster in clear blocks: **login** for social platforms (Facebook, Instagram, X, VK, LinkedIn, part of Telegram/Discord); **account/paywall** for infrastructure and breach-data services (Shodan, Censys, DeHashed, DomainTools, VirusTotal…); **geography** for US people-search and some national registries (Sweden, Russia); **Tor** for dark-web search engines.

## 5. Operational decision guide

1. **Social queries with content** (facebook, instagram, x, vk, linkedin; part of communities/usernames) → **authenticated Chrome profile with a dedicated platform sock-puppet**, never a personal account. Network attribution **mandatory** (VPN/managed attribution): you directly visit a resource the target can control.
2. **Infrastructure/breach services** (Shodan, Censys, DeHashed, DomainTools, VirusTotal, Hunter, IntelX…) → **dedicated service account / non-personal API key**. No country VPN needed; generic VPN recommended.
3. **US people-search and US phone** → no login, but **US VPN exit recommended** (many sites limit/block EU IPs due to GDPR/CCPA, or serve data better from a US IP).
4. **National registries/directories** (Sweden, Russia; to a lesser extent Nigeria/Canada/Italy/UK) → consider a **VPN exit in that country** if access from a foreign IP is blocked or degraded.
5. **Dark-web search engines** (`.onion`) → **Tor** (Tor Browser / OSINT VM with Tor), not a clearnet VPN.
6. **Everything else** (search engines, whois/DNS, archives, block explorers, geospatial) → **no login and no country VPN**; still use a **dedicated research profile** and **managed network attribution** as baseline OPSEC hygiene. Note: with VPN/Tor, search engines (Google above all) may prompt captchas.

> **Direct visits to the target.** Some queries hit the target's own infrastructure (e.g. `domain/robots.txt`, favicon, live site screenshot). Even if they technically need no login/VPN, **managed network attribution is always mandatory** for these: the analyst's IP would land in the target's logs.

---

## 6. Per-category detail (all 898 queries)

Columns: **Service** · **Host** · **Auth (access)** · **VPN/country (access)** · **Conf.**
Per-row OPSEC recommendations (identity and network) are in the companion CSV.


### Search engines  —  28 queries

*Auth:* 28 no-login  ·  *VPN:* 19 no-VPN, 9 Tor

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| OnionLand | `3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2jobad.onion` | No login | Tor required (.onion, not on clearnet) | ● |
| OnionCenter | `5qqrlc7hw3tsgokkqifb33p3mrlpnleka2bjg7n46vih2synghb6ycid.onion` | No login | Tor required (.onion, not on clearnet) | ● |
| Ahmia (Clear) | `ahmia.fi` | No login | No (global access) | ● |
| Baidu | `baidu.com` | No login | No (global access) | ● |
| Searx | `baresearch.org` | No login | No (global access) | ● |
| Bing | `bing.com` | No login | No (global access) | ● |
| Bing News | `bing.com` | No login | No (global access) | ● |
| DuckDuckGo | `duckduckgo.com` | No login | No (global access) | ● |
| FreshOnion | `freshonifyfe4rmuh6qwpsexfhdrww7wnt5qmkoertwxmcuvm4woo4ad.onion` | No login | Tor required (.onion, not on clearnet) | ● |
| Google | `google.com` | No login | No (global access) | ● |
| Google Date | `google.com` | No login | No (global access) | ● |
| Google FTP | `google.com` | No login | No (global access) | ● |
| Google Index | `google.com` | No login | No (global access) | ● |
| Google News | `google.com` | No login | No (global access) | ● |
| Ahmia (Onion) | `juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion` | No login | Tor required (.onion, not on clearnet) | ● |
| Submarine | `no6m4wzdexe3auiupv2zwif7rm6qwxcyhslkcnzisxgeiw6pvjsgafad.onion` | No login | Tor required (.onion, not on clearnet) | ● |
| Google Patents | `patents.google.com` | No login | No (global access) | ● |
| Qwant | `qwant.com` | No login | No (global access) | ● |
| Google Scholar | `scholar.google.com` | No login | No (global access) | ● |
| Brave | `search.brave.com` | No login | No (global access) | ● |
| Yahoo | `search.yahoo.com` | No login | No (global access) | ● |
| DeepSearch | `searchgf7gdtauh7bhnbyed4ivxqmuoat3nm6zfrg3ymkq6mtnpye3ad.onion` | No login | Tor required (.onion, not on clearnet) | ● |
| StartPage | `startpage.com` | No login | No (global access) | ● |
| Tor66 | `tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion` | No login | Tor required (.onion, not on clearnet) | ● |
| Hidden Reviews | `u5lyidiw4lpkonoctpqzxgyk6xop7w7w3oho4dzzsi272rwnjhyx7ayd.onion` | No login | Tor required (.onion, not on clearnet) | ● |
| Wayback | `web.archive.org` | No login | No (global access) | ● |
| Yandex | `yandex.com` | No login | No (global access) | ● |
| GDark | `zb2jtkhnbvhkya3d46twv3g7lkobi4s62tjffqmafjibixk6pmq75did.onion` | No login | Tor required (.onion, not on clearnet) | ● |


### Usernames  —  69 queries

*Auth:* 44 no-login, 17 social-login, 4 account/paywall, 4 free-opt  ·  *VPN:* 66 no-VPN, 1 VPN-US, 2 VPN-country

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| Venmo User | `account.venmo.com` | No login | No (global access) | ● |
| OCCRP Aleph Search | `aleph.occrp.org` | No (free; account only for volume/extras) | No (global access) | ○ |
| ASA Search | `asa.org.uk` | No login | No (global access) | ● |
| Bing | `bing.com` | No login | No (global access) | ● |
| CashApp User | `cash.app` | No login | No (global access) | ● |
| Checko (RU) Search | `checko.ru` | No login | VPN Russia recommended (possible block/limit for foreign IPs) | ◑ |
| RiskIQ Trackers Search | `community.riskiq.com` | No login | No (global access) | ● |
| Telegago (Telegram Search) | `cse.google.com` | No login | No (global access) | ● |
| Dehashed (Breaches) | `dehashed.com` | Paid account | No (global access) | ● |
| Dehashed Emails (Breaches) | `dehashed.com` | Paid account | No (global access) | ● |
| Gravatar | `en.gravatar.com` | No login | No (global access) | ● |
| Facebook Posts Search | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Facebook Profile | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Facebook Search (Direct) | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| GitHub User | `github.com` | No login | No (global access) | ● |
| Ghunt (Google Account) | `gmail-osint.activetk.jp` | No (free; account only for volume/extras) | No (global access) | ○ |
| Mail.Ru Social Search | `go.mail.ru` | Platform login: VK / Mail.ru (to view content) | No (global access) | ◑ |
| Email Search (from Username) | `google.com` | No login | No (global access) | ● |
| Facebook Search (Google) | `google.com` | No login | No (global access) | ● |
| Google (Exact Username) | `google.com` | No login | No (global access) | ● |
| Google Search (Strict) | `google.com` | No login | No (global access) | ● |
| Instagram Search (Google) | `google.com` | No login | No (global access) | ● |
| VK (Google Search) | `google.com` | No login | No (global access) | ● |
| X Search (Google) | `google.com` | No login | No (global access) | ● |
| Google Groups Search | `groups.google.com` | No login | No (global access) | ● |
| ID Crawl | `idcrawl.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Instagram Profile | `instagram.com` | Platform login: Instagram (to view content) | No (global access) | ● |
| Instagram User (Direct) | `instagram.com` | Platform login: Instagram (to view content) | No (global access) | ● |
| InstantUser | `instantusername.com` | No login | No (global access) | ● |
| Kik User | `kik.me` | Platform login: Kik (to view content) | No (global access) | ◑ |
| Krebs Security Search | `krebsonsecurity.com` | No login | No (global access) | ● |
| LinkedIn Keyword Search | `linkedin.com` | Platform login: LinkedIn (to view content) | No (global access) | ● |
| LinkTree | `linktr.ee` | No login | No (global access) | ● |
| Medium | `medium.com` | No login | No (global access) | ● |
| MeWe User | `mewe.com` | Platform login: MeWe (to view content) | No (global access) | ◑ |
| NaijaPlanet User | `naijaplanet.com` | No login | Global access; Nigeria national data (VPN Nigeria only if blocked) | ○ |
| NameChecker | `namechecker.org` | No login | No (global access) | ● |
| NameChck | `namechk.com` | No login | No (global access) | ● |
| NameVine | `namevine.com` | No login | No (global access) | ● |
| OFAC Sanctions Search | `ofac.treasury.gov` | No login | No (global access) | ● |
| AlienVault Indicator | `otx.alienvault.com` | No login | No (global access) | ● |
| Pastebin User | `pastebin.com` | No login | No (global access) | ● |
| PayPalMe User | `paypal.com` | No login | No (global access) | ● |
| Arkham Entity | `platform.arkhamintelligence.com` | Free registration | No (global access) | ◑ |
| ProfileDiscover | `profilediscover.com` | No login | No (global access) | ● |
| PSBDMP (Pastes) | `psbdmp.ws` | No (free; account only for volume/extras) | No (global access) | ○ |
| Reddit Profile | `reddit.com` | No login | No (global access) | ● |
| Remitano Profile | `remitano.com` | No login | No (global access) | ● |
| DomainTools WHOIS | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| SMAT VK Search | `smat-app.com` | No login | No (global access) | ● |
| Snapchat | `snapchat.com` | Platform login: Snapchat (to view content) | No (global access) | ◑ |
| SocialSearcher | `social-searcher.com` | No (free; account only for volume/extras) | No (global access) | ○ |
| Steam Community Search | `steamcommunity.com` | No login | No (global access) | ● |
| SteamID Lookup | `steamid.uk` | No login | No (global access) | ● |
| Stop Forum Spam Search | `stopforumspam.com` | No login | No (global access) | ● |
| Telegram User | `t.me` | Platform login: Telegram (to join channels) (to view content) | No (global access) | ◑ |
| TikTok Profile | `tiktok.com` | Platform login: TikTok (to view content) | No (global access) | ◑ |
| Tinder | `tinder.com` | Platform login: Tinder (to view content) | No (global access) | ● |
| X User Search (Direct) | `twitter.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Checkistan | `usernamechecker.checkistan.com` | No login | No (global access) | ● |
| UserSearch.org | `usersearch.org` | No login | No (global access) | ● |
| VK (Direct Search) | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| VK.me Profile | `vk.me` | Platform login: VK (to view content) | No (global access) | ● |
| WebArchive (RU Media) | `web.archive.org` | No login | No (global access) | ● |
| WhatsMyName App Page | `whatsmyname.app` | No login | No (global access) | ● |
| X Profile | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Tumblr | `x.tumblr.com` | No login | No (global access) | ● |
| Xbox Gamertag Search | `xboxgamertag.com` | No login | No (global access) | ● |
| Yandex | `yandex.com` | No login | No (global access) | ● |


### Names / people  —  61 queries

*Auth:* 53 no-login, 2 social-login, 4 account/paywall, 2 free-opt  ·  *VPN:* 23 no-VPN, 25 VPN-US, 13 VPN-country

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| 9ja Book | `9jabook.com` | No login | Global access; Nigeria national data (VPN Nigeria only if blocked) | ○ |
| Addresses.com | `addresses.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| AdvBackgroundChk | `advancedbackgroundchecks.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| OCCRP Aleph | `aleph.occrp.org` | No (free; account only for volume/extras) | No (global access) | ○ |
| ASA | `asa.org.uk` | No login | No (global access) | ● |
| Canada411 | `canada411.ca` | No login | Global access; Canada national data (VPN Canada only if blocked) | ○ |
| Checko | `checko.ru` | No login | VPN Russia recommended (possible block/limit for foreign IPs) | ◑ |
| Classmates | `classmates.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| RiskIQ - Address | `community.riskiq.com` | No login | No (global access) | ● |
| Crunchbase - Person | `crunchbase.com` | Free registration for details | No (global access) | ◑ |
| CyberBackground | `cyberbackgroundchecks.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Eniro | `eniro.se` | No login | VPN Sweden recommended (possible block/limit for foreign IPs) | ◑ |
| Facebook (Direct) | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| FamilyTreeNow | `familytreenow.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| FastPeople | `fastpeoplesearch.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Facebook (Google) | `google.com` | No login | No (global access) | ● |
| Google Maps | `google.com` | No login | No (global access) | ● |
| Google Search | `google.com` | No login | No (global access) | ● |
| Instagram (Google) | `google.com` | No login | No (global access) | ● |
| RocketReach | `google.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Twitter (Google) | `google.com` | No login | No (global access) | ● |
| Hitta.se | `hitta.se` | No login | VPN Sweden recommended (possible block/limit for foreign IPs) | ◑ |
| ID Crawl | `idcrawl.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| iD Crawl | `idcrawl.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Intelius | `intelius.com` | Paywall for reports | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Interpol - RedNotices | `interpol.int` | No login | No (global access) | ● |
| Merinfo | `merinfo.se` | No login | VPN Sweden recommended (possible block/limit for foreign IPs) | ◑ |
| Mr Koll | `mrkoll.se` | No login | VPN Sweden recommended (possible block/limit for foreign IPs) | ◑ |
| Nuwber | `nuwber.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| OFAC Sanctions - Rec. | `ofac.treasury.gov` | No login | No (global access) | ● |
| Open Corporates | `opencorporates.com` | No login | No (global access) | ● |
| Open Sanctions | `opensanctions.org` | No login | No (global access) | ● |
| Pagine Bianche | `paginebianche.it` | No login | Global access; Italy national data (VPN Italy only if blocked) | ○ |
| Pagine Gialle | `paginegialle.it` | No login | Global access; Italy national data (VPN Italy only if blocked) | ○ |
| PeopleByName | `peoplebyname.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| PeopleSearchNow | `peoplesearchnow.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Search Systems | `publicrecords.searchsystems.net` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Radaris | `radaris.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Ratsit | `ratsit.se` | No login | VPN Sweden recommended (possible block/limit for foreign IPs) | ◑ |
| DomainTools - WHOIS | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| RusFinder | `rusfinder.pro` | No login | VPN Russia recommended (possible block/limit for foreign IPs) | ◑ |
| OFAC Sanctions - Search | `sanctionssearch.ofac.treas.gov` | No login | No (global access) | ● |
| Censys Certificates | `search.censys.io` | Free registration | No (global access) | ◑ |
| SearchPeopleFree | `searchpeoplefree.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Social Searcher | `social-searcher.com` | No (free; account only for volume/extras) | No (global access) | ○ |
| Spokeo | `spokeo.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| ThatsThem | `thatsthem.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| ThatsThem | `thatsthem.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| TruePeople | `truepeoplesearch.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| TruthFinder | `truthfinder.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Twitter (Direct) | `twitter.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| UDRPsearch | `udrpsearch.com` | No login | No (global access) | ● |
| UKPhoneBook (Name) | `ukphonebook.com` | No login | Global access; United Kingdom national data (VPN United Kingdom only if blocked) | ○ |
| UKPhoneBook (Res.) | `ukphonebook.com` | No login | Global access; United Kingdom national data (VPN United Kingdom only if blocked) | ○ |
| USA-Official | `usa-official.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| WebMii | `webmii.com` | No login | No (global access) | ● |
| WhitePages | `whitepages.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| YachtlyCrew | `yachtlycrew.com` | No login | No (global access) | ● |
| Yasni | `yasni.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Zabasearch | `zabasearch.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Zauba Corp (Person) | `zaubacorp.com` | No login | No (global access) | ● |


### Email  —  25 queries

*Auth:* 13 no-login, 8 account/paywall, 4 free-opt  ·  *VPN:* 23 no-VPN, 2 VPN-US

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| AnalyzeID | `analyzeid.com` | No login | No (global access) | ● |
| Protonmail | `api.protonmail.ch` | No login | No (global access) | ● |
| Bing | `bing.com` | No login | No (global access) | ● |
| HudsonRock | `cavalier.hudsonrock.com` | No login | No (global access) | ● |
| Cybernews | `check.cybernews.com` | No (free; account only for volume/extras) | No (global access) | ○ |
| CleanTalk | `cleantalk.org` | No login | No (global access) | ● |
| OCCRP | `data.occrp.org` | No login | No (global access) | ● |
| Dehashed | `dehashed.com` | Paid account | No (global access) | ● |
| Emailrep | `emailrep.io` | No (free; account only for volume/extras) | No (global access) | ○ |
| Flickr | `flickr.com` | No login | No (global access) | ● |
| Ghunt (Google Account) | `gmail-osint.activetk.jp` | No (free; account only for volume/extras) | No (global access) | ○ |
| Google | `google.com` | No login | No (global access) | ● |
| Gravatar | `gravatar.com` | No login | No (global access) | ● |
| HunterVerify | `hunter.io` | Free registration for results | No (global access) | ◑ |
| IntelX | `intelx.io` | Registration / account | No (global access) | ◑ |
| LeakIX | `leakix.net` | Account for some results | No (global access) | ◑ |
| MySpace | `myspace.com` | No login | No (global access) | ● |
| Spycloud | `portal.spycloud.com` | Account (enterprise) | No (global access) | ● |
| PSBDMP | `psbdmp.ws` | No (free; account only for volume/extras) | No (global access) | ○ |
| ScamSearch | `scamsearch.io` | Registration | No (global access) | ◑ |
| SpyTox | `spytox.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| ThatsThem | `thatsthem.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Whoisology | `whoisology.com` | Account / paywall | No (global access) | ◑ |
| Whoxy | `whoxy.com` | Account / API for results | No (global access) | ◑ |
| Yandex | `yandex.com` | No login | No (global access) | ● |


### Domains / infrastructure  —  149 queries

*Auth:* 112 no-login, 32 account/paywall, 5 free-opt  ·  *VPN:* 149 no-VPN

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| Bit.ly Expand | `` | No login | No (global access) | ● |
| OCCRP Aleph | `aleph.occrp.org` | No (free; account only for volume/extras) | No (global access) | ○ |
| AnalyzeID | `analyzeid.com` | No login | No (global access) | ● |
| AnalyzeID | `analyzeid.com` | No login | No (global access) | ● |
| AnalyzeID | `analyzeid.com` | No login | No (global access) | ● |
| Archive-IT | `archive-it.org` | No login | No (global access) | ● |
| Archive.md | `archive.md` | No login | No (global access) | ● |
| archive.ph | `archive.ph` | No login | No (global access) | ● |
| Arquivo.pt | `arquivo.pt` | No login | No (global access) | ● |
| ASA Search | `asa.org.uk` | No login | No (global access) | ● |
| Baidu (Exact) | `baidu.com` | No login | No (global access) | ● |
| Bing (Exact) | `bing.com` | No login | No (global access) | ● |
| BuiltWith | `builtwith.com` | No (free; account only for volume/extras) | No (global access) | ○ |
| CarbonDating | `carbondate.cs.odu.edu` | No login | No (global access) | ● |
| HudsonRock | `cavalier.hudsonrock.com` | No login | No (global access) | ● |
| CentralOps Dossier | `centralops.net` | No login | No (global access) | ● |
| Spamhaus Check | `check.spamhaus.org` | No login | No (global access) | ● |
| ThreatCrowd | `ci-threatcrowd.org` | No login | No (global access) | ● |
| Columbus Subdomains | `columbus.elmasy.com` | No login | No (global access) | ● |
| RiskIQ | `community.riskiq.com` | No login | No (global access) | ● |
| RiskIQ | `community.riskiq.com` | No login | No (global access) | ● |
| RiskIQ Search | `community.riskiq.com` | No login | No (global access) | ● |
| CopyScape | `copyscape.com` | No login | No (global access) | ● |
| CRT.sh | `crt.sh` | No login | No (global access) | ● |
| Dehashed | `dehashed.com` | Paid account | No (global access) | ● |
| DMNs.app | `dmns.app` | No login | No (global access) | ● |
| DNPedia | `dnpedia.com` | No login | No (global access) | ● |
| DomainApp DNS | `dns.domainapp.com` | No login | No (global access) | ● |
| DNSDumpster | `dnsdumpster.com` | No login | No (global access) | ● |
| AdSense Lookup | `dnslytics.com` | No login | No (global access) | ● |
| DNSlytics | `dnslytics.com` | No login | No (global access) | ● |
| DNSlytics | `dnslytics.com` | No login | No (global access) | ● |
| DNSlytics | `dnslytics.com` | No login | No (global access) | ● |
| GA Lookup | `dnslytics.com` | No login | No (global access) | ● |
| DomainCodex | `domaincodex.com` | No login | No (global access) | ● |
| DomainIQ | `domainiq.com` | Account / paywall | No (global access) | ◑ |
| DomainIQ | `domainiq.com` | Account / paywall | No (global access) | ◑ |
| EasyCounter | `easycounter.com` | No login | No (global access) | ● |
| Elephind | `elephind.com` | No login | No (global access) | ● |
| Etherscan (ENS) | `etherscan.io` | No login | No (global access) | ● |
| IBM X-Force | `exchange.xforce.ibmcloud.com` | No login | No (global access) | ● |
| Expand Any URL | `expandurl.net` | No login | No (global access) | ● |
| Calculate Hash | `favicon-hash.kmsec.uk` | No login | No (global access) | ● |
| FCA Warnings | `fca.org.uk` | No login | No (global access) | ● |
| GoDaddy WHOIS | `godaddy.com` | No login | No (global access) | ● |
| Congress Archives | `google.com` | No login | No (global access) | ● |
| Google (Exact) | `google.com` | No login | No (global access) | ● |
| Google Cache | `google.com` | No login | No (global access) | ● |
| Google Site Search | `google.com` | No login | No (global access) | ● |
| Google Groups | `groups.google.com` | No login | No (global access) | ● |
| HackerTarget | `hackertarget.com` | No login | No (global access) | ● |
| HackerTarget | `hackertarget.com` | No login | No (global access) | ● |
| Host.io | `host.io` | No login | No (global access) | ● |
| Host.io Backlinks | `host.io` | No login | No (global access) | ● |
| Host.io Redirects | `host.io` | No login | No (global access) | ● |
| Hybrid Analysis | `hybrid-analysis.com` | Free registration | No (global access) | ◑ |
| HypeStat | `hypestat.com` | No login | No (global access) | ● |
| IntelligenceX | `intelx.io` | Registration / account | No (global access) | ◑ |
| Joe Sandbox | `joesandbox.com` | Registration | No (global access) | ◑ |
| LeakIX Domain | `leakix.net` | Account for some results | No (global access) | ◑ |
| LeakIX Search | `leakix.net` | Account for some results | No (global access) | ◑ |
| Backlinks (Linkody) | `linkody.com` | No login | No (global access) | ● |
| Maltiverse | `maltiverse.com` | No login | No (global access) | ● |
| Moz | `moz.com` | Free registration | No (global access) | ◑ |
| MyWOT | `mywot.com` | No login | No (global access) | ● |
| NerdyData | `nerdydata.com` | No login | No (global access) | ● |
| NetworksDB IPs | `networksdb.io` | No login | No (global access) | ● |
| OFAC Sanctions | `ofac.treasury.gov` | No login | No (global access) | ● |
| AlienVault OTX | `otx.alienvault.com` | No login | No (global access) | ● |
| PhishCheck.me | `phishcheck.me` | No login | No (global access) | ● |
| PublicWWW | `publiccom` | No login | No (global access) | ● |
| PublicWWW | `publiccom` | No login | No (global access) | ● |
| Pulsedive | `pulsedive.com` | No login | No (global access) | ● |
| Reddit Mentions | `reddit.com` | No login | No (global access) | ● |
| Reddit URL Search | `reddit.com` | No login | No (global access) | ● |
| DomainTools | `research.domaintools.com` | Account / paywall | No (global access) | ◑ |
| DomainTools History | `research.domaintools.com` | Account / paywall | No (global access) | ◑ |
| Resolve.rs DNS | `resolve.rs` | No login | No (global access) | ● |
| Robtex | `robtex.com` | No login | No (global access) | ● |
| Censys CSP Search | `search.censys.io` | Free registration | No (global access) | ◑ |
| Censys DNS | `search.censys.io` | Free registration | No (global access) | ◑ |
| Censys IP Search | `search.censys.io` | Free registration | No (global access) | ◑ |
| Search Censys | `search.censys.io` | Free registration | No (global access) | ◑ |
| Netcraft Subdomains | `searchdns.netcraft.com` | No login | No (global access) | ● |
| Security Headers | `securityheaders.com` | No login | No (global access) | ● |
| SecurityTrails | `securitytrails.com` | Free registration | No (global access) | ◑ |
| SecurityTrails Overview | `securitytrails.com` | Free registration | No (global access) | ◑ |
| SharedCount | `sharedcount.com` | No login | No (global access) | ● |
| Search Shodan | `shodan.io` | Free registration for full search | No (global access) | ◑ |
| Shodan Domain | `shodan.io` | Free registration for full search | No (global access) | ◑ |
| Shodan Hostname | `shodan.io` | Free registration for full search | No (global access) | ◑ |
| Shodan Query | `shodan.io` | Free registration for full search | No (global access) | ◑ |
| SimilarWeb | `similarweb.com` | Registration for details | No (global access) | ◑ |
| SiteMapper | `sitemapper.com` | No login | No (global access) | ● |
| Netcraft Report | `sitereport.netcraft.com` | No login | No (global access) | ● |
| Skymem | `skymem.info` | No login | No (global access) | ● |
| Spam.org | `spam.org` | No login | No (global access) | ● |
| SpyFu | `spyfu.com` | Account / paywall | No (global access) | ◑ |
| SpyOnWeb | `spyonweb.com` | No login | No (global access) | ● |
| SRA Search | `sra.org.uk` | No login | No (global access) | ● |
| Stop Forum Spam | `stopforumspam.com` | No login | No (global access) | ● |
| Blacklight | `themarkup.org` | No login | No (global access) | ● |
| ThreatIntel | `threatintelligenceplatform.com` | No login | No (global access) | ● |
| Mementoweb | `timetravel.mementoweb.org` | No login | No (global access) | ● |
| Tiny.cc Expand | `tiny.cc` | No login | No (global access) | ● |
| Triage (SMTP) | `tria.ge` | Registration | No (global access) | ◑ |
| Triage (URL) | `tria.ge` | Registration | No (global access) | ◑ |
| UDRPSearch | `udrpsearch.com` | No login | No (global access) | ● |
| URLScan | `urlscan.io` | No (free; account only for volume/extras) | No (global access) | ○ |
| URLScan Page Search | `urlscan.io` | No (free; account only for volume/extras) | No (global access) | ○ |
| urlscan.io General | `urlscan.io` | No (free; account only for volume/extras) | No (global access) | ○ |
| Abuse Contact | `viewdns.info` | No login | No (global access) | ● |
| Chinese Firewall Test | `viewdns.info` | No login | No (global access) | ● |
| DNS Records | `viewdns.info` | No login | No (global access) | ● |
| DNS Report | `viewdns.info` | No login | No (global access) | ● |
| DNSSEC Test | `viewdns.info` | No login | No (global access) | ● |
| HTTP Headers | `viewdns.info` | No login | No (global access) | ● |
| IP History | `viewdns.info` | No login | No (global access) | ● |
| Iran Firewall Test | `viewdns.info` | No login | No (global access) | ● |
| Is My Site Down | `viewdns.info` | No login | No (global access) | ● |
| Port Scan | `viewdns.info` | No login | No (global access) | ● |
| Reverse DNS | `viewdns.info` | No login | No (global access) | ● |
| Reverse IP Lookup | `viewdns.info` | No login | No (global access) | ● |
| Traceroute | `viewdns.info` | No login | No (global access) | ● |
| ViewDNS WHOIS | `viewdns.info` | No login | No (global access) | ● |
| Search VirusTotal | `virustotal.com` | Free registration for full features | No (global access) | ◑ |
| VirusTotal | `virustotal.com` | Free registration for full features | No (global access) | ◑ |
| Archive Scan (CDX) | `web-archive-scan.com` | No login | No (global access) | ● |
| Webscout | `web-scout.io` | No login | No (global access) | ● |
| Archive URL Wildcard | `web.archive.org` | No login | No (global access) | ● |
| Archive.org | `web.archive.org` | No login | No (global access) | ● |
| WayBack Keyword | `web.archive.org` | No login | No (global access) | ● |
| Informer | `website.informer.com` | No login | No (global access) | ● |
| InformerEmails | `website.informer.com` | No login | No (global access) | ● |
| Who.Is | `who.is` | No login | No (global access) | ● |
| Who.Is DNS | `who.is` | No login | No (global access) | ● |
| Who.Is History | `whois.com` | No login | No (global access) | ● |
| Whois Archive (who.is) | `whois.com` | No login | No (global access) | ● |
| Whois.com | `whois.com` | No login | No (global access) | ● |
| DomainTools WHOIS | `whois.domaintools.com` | Account for details | No (global access) | ◑ |
| Whois Archive (DT) | `whois.domaintools.com` | Account for details | No (global access) | ◑ |
| EURid WHOIS | `whois.eurid.eu` | No login | No (global access) | ● |
| Whoisology | `whoisology.com` | Account / paywall | No (global access) | ◑ |
| Whois Archive (Whoxy) | `whoxy.com` | Account / API for results | No (global access) | ◑ |
| Whoxy | `whoxy.com` | Account / API for results | No (global access) | ◑ |
| WIPO Search | `wipo.int` | No login | No (global access) | ● |
| WMTips | `wmtips.com` | No login | No (global access) | ● |
| Robots.txt | `x` | No login | No (global access) | ● |
| Yandex (Exact) | `yandex.com` | No login | No (global access) | ● |


### IP / network  —  58 queries

*Auth:* 46 no-login, 12 account/paywall  ·  *VPN:* 57 no-VPN, 1 VPN-US

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| ipapi.co (Bulk Geo) | `app.ipapi.co` | No login | No (global access) | ● |
| Baidu | `baidu.com` | No login | No (global access) | ● |
| Shodan History | `beta.shodan.io` | Free registration | No (global access) | ◑ |
| Shodan Host | `beta.shodan.io` | Free registration | No (global access) | ◑ |
| Shodan Raw | `beta.shodan.io` | Free registration | No (global access) | ◑ |
| Bing | `bing.com` | No login | No (global access) | ● |
| ThreatCrowd | `ci-threatcrowd.org` | No login | No (global access) | ● |
| RiskIQ IP | `community.riskiq.com` | No login | No (global access) | ● |
| Dehashed (IP) | `dehashed.com` | Paid account | No (global access) | ● |
| DNSChecker | `dnschecker.org` | No login | No (global access) | ● |
| Google | `google.com` | No login | No (global access) | ● |
| IKWYD Torrents | `iknowwhatyoudownload.com` | No login | No (global access) | ● |
| InfoByIp | `infobyip.com` | No login | No (global access) | ● |
| IPLookup.org | `ip-lookup.org` | No login | No (global access) | ● |
| IPAddress.com | `ipaddress.com` | No login | No (global access) | ● |
| IPLocation.net | `iplocation.net` | No login | No (global access) | ● |
| LeakIX Host | `leakix.net` | Account for some results | No (global access) | ◑ |
| Maltiverse | `maltiverse.com` | No login | No (global access) | ● |
| MaxMind Demo | `maxmind.com` | Account | No (global access) | ◑ |
| MXTool (ARIN) | `mxtoolbox.com` | No login | No (global access) | ● |
| MXTool Blacklist | `mxtoolbox.com` | No login | No (global access) | ● |
| MXTool Blocklist | `mxtoolbox.com` | No login | No (global access) | ● |
| ASN Search | `networksdb.io` | No login | No (global access) | ● |
| Domains on IP | `networksdb.io` | No login | No (global access) | ● |
| IP Details | `networksdb.io` | No login | No (global access) | ● |
| Network Search | `networksdb.io` | No login | No (global access) | ● |
| NetworksDB Range | `networksdb.io` | No login | No (global access) | ● |
| Resolve.rs Geo | `resolve.rs` | No login | No (global access) | ● |
| Robtex | `robtex.com` | No login | No (global access) | ● |
| Censys Host | `search.censys.io` | Free registration | No (global access) | ◑ |
| SecurityTrails | `securitytrails.com` | Free registration | No (global access) | ◑ |
| Shodan Search | `shodan.io` | Free registration for full search | No (global access) | ◑ |
| Stop Forum Spam | `stopforumspam.com` | No login | No (global access) | ● |
| That's Them IP | `thatsthem.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| ASN Lookup | `viewdns.info` | No login | No (global access) | ● |
| Abuse Contact | `viewdns.info` | No login | No (global access) | ● |
| Chinese Firewall Test | `viewdns.info` | No login | No (global access) | ● |
| DNS Records | `viewdns.info` | No login | No (global access) | ● |
| DNS Report | `viewdns.info` | No login | No (global access) | ● |
| DNSSEC Test | `viewdns.info` | No login | No (global access) | ● |
| Global Ping | `viewdns.info` | No login | No (global access) | ● |
| HTTP Headers | `viewdns.info` | No login | No (global access) | ● |
| IP History | `viewdns.info` | No login | No (global access) | ● |
| Iran Firewall Test | `viewdns.info` | No login | No (global access) | ● |
| Is My Site Down | `viewdns.info` | No login | No (global access) | ● |
| LocateIP | `viewdns.info` | No login | No (global access) | ● |
| PortScan | `viewdns.info` | No login | No (global access) | ● |
| ReverseDNS | `viewdns.info` | No login | No (global access) | ● |
| ReverseIP | `viewdns.info` | No login | No (global access) | ● |
| Spam DB Lookup | `viewdns.info` | No login | No (global access) | ● |
| TraceRoute | `viewdns.info` | No login | No (global access) | ● |
| Whois | `viewdns.info` | No login | No (global access) | ● |
| VirusTotal Relations | `virustotal.com` | Free registration for full features | No (global access) | ◑ |
| GreyNoise | `viz.greynoise.io` | Free registration | No (global access) | ◑ |
| DomainTools Whois | `whois.domaintools.com` | Account for details | No (global access) | ◑ |
| Wigle Postal | `wigle.net` | No login | No (global access) | ● |
| Wigle SSID | `wigle.net` | No login | No (global access) | ● |
| Yandex | `yandex.com` | No login | No (global access) | ● |


### Public company records  —  56 queries

*Auth:* 47 no-login, 7 account/paywall, 2 free-opt  ·  *VPN:* 50 no-VPN, 2 VPN-US, 4 VPN-country

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| AIHIT | `aihitdata.com` | Registration for details | No (global access) | ○ |
| AIHIT | `aihitdata.com` | Registration for details | No (global access) | ○ |
| AIHIT (Email) | `aihitdata.com` | Registration for details | No (global access) | ○ |
| AIHIT (Phone) | `aihitdata.com` | Registration for details | No (global access) | ○ |
| OCCRP Aleph | `aleph.occrp.org` | No (free; account only for volume/extras) | No (global access) | ○ |
| OCCRP Aleph | `aleph.occrp.org` | No (free; account only for volume/extras) | No (global access) | ○ |
| ASA | `asa.org.uk` | No login | No (global access) | ● |
| B2BHint | `b2bhint.com` | Registration for details | No (global access) | ◑ |
| Clarified By | `clarifiedby.diligenciagroup.com` | No login | No (global access) | ● |
| Recap (Courtlistener) | `courtlistener.com` | No login | No (global access) | ● |
| Recap (Courtlistener) | `courtlistener.com` | No login | No (global access) | ● |
| Crunchbase | `crunchbase.com` | Free registration for details | No (global access) | ◑ |
| European e-Justice | `e-justice.europa.eu` | No login | No (global access) | ● |
| FCA (UK) | `fca.org.uk` | No login | No (global access) | ● |
| FCA (UK) | `fca.org.uk` | No login | No (global access) | ● |
| Companies House (UK) | `find-and-update.company-information.service.gov.uk` | No login | No (global access) | ● |
| SSDI | `genealogybank.com` | No login | No (global access) | ● |
| P.IVA (Italy) | `google.com` | No login | No (global access) | ● |
| UniCourt | `google.com` | No login | No (global access) | ● |
| UniCourt | `google.com` | No login | No (global access) | ● |
| Infobel | `infobel.com` | No login | No (global access) | ● |
| Infobel | `infobel.com` | No login | No (global access) | ● |
| IOSCO Alerts | `iosco.org` | No login | No (global access) | ● |
| IOSCO Alerts | `iosco.org` | No login | No (global access) | ● |
| JudyRecords | `judyrecords.com` | No login | No (global access) | ● |
| JudyRecords | `judyrecords.com` | No login | No (global access) | ● |
| LittleSis | `littlesis.org` | No login | No (global access) | ● |
| LittleSis | `littlesis.org` | No login | No (global access) | ● |
| MuckrockFOIA | `muckrock.com` | No login | No (global access) | ● |
| MuckrockFOIA | `muckrock.com` | No login | No (global access) | ● |
| NG-Check (Nigeria) | `ng-check.com` | No login | Global access; Nigeria national data (VPN Nigeria only if blocked) | ○ |
| Nigeria24 | `nigeria24.me` | No login | Global access; Nigeria national data (VPN Nigeria only if blocked) | ○ |
| Nigeria24 | `nigeria24.me` | No login | Global access; Nigeria national data (VPN Nigeria only if blocked) | ○ |
| OFAC Recent Actions | `ofac.treasury.gov` | No login | No (global access) | ● |
| OFAC Recent Actions | `ofac.treasury.gov` | No login | No (global access) | ● |
| OpenCorporates (AL) | `opencorporates.al` | No login | No (global access) | ● |
| OpenCorporates | `opencorporates.com` | No login | No (global access) | ● |
| OpenCorporates | `opencorporates.com` | No login | No (global access) | ● |
| Open Payrolls | `openpayrolls.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| OpenSanctions | `opensanctions.org` | No login | No (global access) | ● |
| OpenSanctions | `opensanctions.org` | No login | No (global access) | ● |
| Open Secrets | `opensecrets.org` | No login | No (global access) | ● |
| MoneyLine | `politicalmoneyline.com` | No login | No (global access) | ● |
| CAC (Nigeria) | `search.cac.gov.ng` | No login | Global access; Nigeria national data (VPN Nigeria only if blocked) | ○ |
| Censys Certificates | `search.censys.io` | Free registration | No (global access) | ◑ |
| FOIA | `search.foia.gov` | No login | No (global access) | ● |
| FOIA | `search.foia.gov` | No login | No (global access) | ● |
| Pacer | `search.uscourts.gov` | No login | No (global access) | ● |
| Pacer | `search.uscourts.gov` | No login | No (global access) | ● |
| SRA (UK Solicitors) | `sra.org.uk` | No login | No (global access) | ● |
| Trellis | `trellis.law` | No login | No (global access) | ● |
| Trellis | `trellis.law` | No login | No (global access) | ● |
| UDRP Search | `udrpsearch.com` | No login | No (global access) | ● |
| Voter Records | `voterrecords.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| WIPO (Google) | `wipo.int` | No login | No (global access) | ● |
| Zauba Corp (India) | `zaubacorp.com` | No login | No (global access) | ● |


### Addresses  —  22 queries

*Auth:* 22 no-login  ·  *VPN:* 2 no-VPN, 17 VPN-US, 3 VPN-country

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| Addresses.com | `addresses.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| AdvBackgChk | `advancedbackgroundchecks.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| CyberBkgChk | `cyberbackgroundchecks.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| FastPeople | `fastpeoplesearch.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| FastPeople EU | `fastpeoplesearch.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Google | `google.com` | No login | No (global access) | ● |
| Google | `google.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Hudway | `hudway.co` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Search Companies | `paginebianche.it` | No login | Global access; Italy national data (VPN Italy only if blocked) | ○ |
| Search People | `paginebianche.it` | No login | Global access; Italy national data (VPN Italy only if blocked) | ○ |
| Search Pagine Gialle | `paginegialle.it` | No login | Global access; Italy national data (VPN Italy only if blocked) | ○ |
| PeopleFinders | `peoplefinders.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Rehold | `rehold.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| SearchPplFree | `searchpeoplefree.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| GISGraphy | `services.gisgraphy.com` | No login | No (global access) | ● |
| GISGraphy | `services.gisgraphy.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| SmartBkgChk | `smartbackgroundchecks.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Spokeo | `spokeo.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| TruePeople | `truepeoplesearch.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| USA People | `usa-people-search.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| WhitePages | `whitepages.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Zillow | `zillow.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |


### US phone  —  29 queries

*Auth:* 26 no-login, 1 social-login, 2 account/paywall  ·  *VPN:* 29 VPN-US

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| 411 | `411.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| 800 Notes | `800notes.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| AdvBackground | `advancedbackgroundchecks.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| AmericaPhone | `americaphonebook.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Bing Search | `bing.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| CallerSmart | `callersmart.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| CyberBackground | `cyberbackgroundchecks.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Dehashed | `dehashed.com` | Paid account | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| FastPeople | `fastpeoplesearch.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Google Search | `google.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| InfoTracer | `infotracer.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Facebook | `mbasic.facebook.com` | Platform login: Facebook (to view content) | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Numpi | `numpi.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Nuwber | `nuwber.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| OKCaller | `okcaller.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| YellowPages | `people.yellowpages.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| PeopleSearchNow | `peoplesearchnow.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| PhoneOwner | `phoneowner.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| SearchPeopleFree | `searchpeoplefree.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Spytox | `spytox.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Sync.me | `sync.me` | Login / app | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| ThatsThem | `thatsthem.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| TruePeople | `truepeoplesearch.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| USPhonebook | `usphonebook.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| WhatsApp | `whatsapp.checkleaked.cc` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| WhitePages | `whitepages.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| WhoseNo | `whoseno.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Yandex Search | `yandex.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| ZabaSearch | `zabasearch.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |


### International phone  —  44 queries

*Auth:* 14 no-login, 1 social-login, 29 account/paywall  ·  *VPN:* 39 no-VPN, 2 VPN-US, 3 VPN-country

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| 411.com | `411.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Bing Search | `bing.com` | No login | No (global access) | ● |
| RiskIQ WHOIS | `community.riskiq.com` | No login | No (global access) | ● |
| EmobileTracker (Manual) | `emobiletracker.com` | No login | No (global access) | ● |
| EPIEOS | `epieos.com` | Free registration for full results | No (global access) | ◑ |
| Facebook (Posts) | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| FreeCarrierLookup (Manual) | `freecarrierlookup.com` | No login | No (global access) | ● |
| Google Search | `google.com` | No login | No (global access) | ● |
| My SMS Box (Ru) | `mysmsbox.ru` | No login | VPN Russia recommended (possible block/limit for foreign IPs) | ◑ |
| Nigeria Phonebook | `nigeriaphonebook.com` | No login | Global access; Nigeria national data (VPN Nigeria only if blocked) | ○ |
| AQL Network (UK) | `portal.aql.com` | Account | No (global access) | ◑ |
| +CC.0Num | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| +CC.Num | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| 0Num Only | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| Num Only | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| Num@gmail.com | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| Num@hotmail.com | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| Num@mail.ru | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| Num@pm.me | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| Num@proton.me | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| Num@protonmail.ch | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| Num@protonmail.com | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| Num@yahoo.com | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| Num@yandex.com | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| Num@yandex.ru | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| eNum@gmail | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| eNum@hotmail.com | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| eNum@mail.ru | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| eNum@pm.me | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| eNum@proton.ch | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| eNum@proton.me | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| eNum@protonmail | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| eNum@yahoo.com | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| eNum@yandex.com | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| eNum@yandex.ru | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| phoneint-dt-base | `reversewhois.domaintools.com` | Account / paywall | No (global access) | ◑ |
| OFAC Sanctions | `sanctionssearch.ofac.treas.gov` | No login | No (global access) | ● |
| Sync.me | `sync.me` | Login / app | No (global access) | ◑ |
| Tellows | `tellows.it` | No login | Global access; Italy national data (VPN Italy only if blocked) | ○ |
| ThatsThem | `thatsthem.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Truecaller | `truecaller.com` | Login / app required | No (global access) | ◑ |
| Vedbex (Manual) | `vedbex.com` | No login | No (global access) | ● |
| WhatsApp leaks | `whatsapp.checkleaked.cc` | No login | No (global access) | ● |
| Yandex Search | `yandex.com` | No login | No (global access) | ● |


### Facebook  —  46 queries

*Auth:* 46 social-login  ·  *VPN:* 46 no-VPN

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| About | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Apps | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Apps & Games | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Basic Info | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Biography | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Books | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Check-ins | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Contact Info | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Education | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Employment | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Events | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Events | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Facts | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Family | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Following | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Friends | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Groups | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Life Events | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Likes | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Links | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Locations | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Marketplace | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Movies | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Music | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Notes | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Pages | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| People | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Photo Albums | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Photos | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Photos | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Places | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Posts | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Profile | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Recent Check-ins | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Reels | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Relationships | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Reviews | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Reviews Given | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Reviews Written | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Sports | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| TV Shows | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Timeline | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Videos | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Videos | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Visits (Map) | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Watch | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |


### Instagram  —  18 queries

*Auth:* 11 no-login, 7 social-login  ·  *VPN:* 18 no-VPN

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| Bing Search | `bing.com` | No login | No (global access) | ● |
| Dumpor Profile | `dumpor.com` | No login | No (global access) | ● |
| Dumpor Tag | `dumpor.com` | No login | No (global access) | ● |
| Associations (Google) | `google.com` | No login | No (global access) | ● |
| Google: Incoming Mentions | `google.com` | No login | No (global access) | ● |
| Google: Outgoing Mentions | `google.com` | No login | No (global access) | ● |
| Instagram Terms (Google) | `google.com` | No login | No (global access) | ● |
| User + Term (Google) | `google.com` | No login | No (global access) | ● |
| X/Twitter Posts | `google.com` | No login | No (global access) | ● |
| Channel | `instagram.com` | Platform login: Instagram (to view content) | No (global access) | ● |
| Followers | `instagram.com` | Platform login: Instagram (to view content) | No (global access) | ● |
| Following | `instagram.com` | Platform login: Instagram (to view content) | No (global access) | ● |
| Instagram Hashtag | `instagram.com` | Platform login: Instagram (to view content) | No (global access) | ● |
| Profile | `instagram.com` | Platform login: Instagram (to view content) | No (global access) | ● |
| Tagged | `instagram.com` | Platform login: Instagram (to view content) | No (global access) | ● |
| Threads Profile | `threads.net` | Platform login: Threads (Meta) (to view content) | No (global access) | ◑ |
| Toolzu Profile | `toolzu.com` | No login | No (global access) | ● |
| Yandex Search | `yandex.com` | No login | No (global access) | ● |


### X / Twitter  —  31 queries

*Auth:* 8 no-login, 23 social-login  ·  *VPN:* 31 no-VPN

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| Bing Archives | `bing.com` | No login | No (global access) | ● |
| Google Archives | `google.com` | No login | No (global access) | ● |
| Google Tweets | `google.com` | No login | No (global access) | ● |
| Memory.lol | `memory.lol` | No login | No (global access) | ● |
| Memory.lol ID | `memory.lol` | No login | No (global access) | ● |
| TwitterAudit | `twitteraudit.com` | No login | No (global access) | ● |
| Wayback | `web.archive.org` | No login | No (global access) | ● |
| Followers | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Followers | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Following | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Highlights | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Incoming | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Incoming Mentions | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Links | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| List | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Lists Created | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Lists Included | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Media | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Media | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Members | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| No Replies | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| No Replies | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Only Replies | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Only Replies | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Outgoing | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Outgoing Mentions | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Profile | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Profile Search | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Term | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Topics | `x.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Yandex Archives | `yandex.com` | No login | No (global access) | ● |


### LinkedIn  —  11 queries

*Auth:* 6 no-login, 5 social-login  ·  *VPN:* 11 no-VPN

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| Bing Images | `bing.com` | No login | No (global access) | ● |
| Bing People | `bing.com` | No login | No (global access) | ● |
| Google Images | `google.com` | No login | No (global access) | ● |
| Google People | `google.com` | No login | No (global access) | ● |
| Video Search | `google.com` | No login | No (global access) | ● |
| Companies | `linkedin.com` | Platform login: LinkedIn (to view content) | No (global access) | ● |
| Events | `linkedin.com` | Platform login: LinkedIn (to view content) | No (global access) | ● |
| Groups | `linkedin.com` | Platform login: LinkedIn (to view content) | No (global access) | ● |
| Profile | `linkedin.com` | Platform login: LinkedIn (to view content) | No (global access) | ● |
| Schools | `linkedin.com` | Platform login: LinkedIn (to view content) | No (global access) | ● |
| Yandex People | `yandex.com` | No login | No (global access) | ● |


### VK  —  30 queries

*Auth:* 4 no-login, 26 social-login  ·  *VPN:* 29 no-VPN, 1 VPN-country

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| vk-ext-checko | `checko.ru` | No login | VPN Russia recommended (possible block/limit for foreign IPs) | ◑ |
| vk-ext-mailru | `go.mail.ru` | Platform login: VK / Mail.ru (to view content) | No (global access) | ◑ |
| vk-ext-google | `google.com` | No login | No (global access) | ● |
| vk-ext-smat | `smat-app.com` | No login | No (global access) | ● |
| vk-profile-id | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-profile-username | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-search-all | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-search-audio | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-search-docs | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-search-groups | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-search-market | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-search-news | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-search-people | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-search-photos | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-search-tag | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-search-videos | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-user-allposts | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-user-apps | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-user-audio | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-user-followers | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-user-friends | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-user-gifts | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-user-groups | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-user-market | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-user-notes | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-user-photoalbums | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-user-photos | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-user-videos | `vk.com` | Platform login: VK (to view content) | No (global access) | ● |
| vk-profile-link | `vk.me` | Platform login: VK (to view content) | No (global access) | ● |
| vk-ext-webarchive | `web.archive.org` | No login | No (global access) | ● |


### Communities / forums  —  32 queries

*Auth:* 27 no-login, 5 social-login  ·  *VPN:* 32 no-VPN

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| Archive | `4plebs.org` | No login | No (global access) | ● |
| API Asc | `api.pullpush.io` | No login | No (global access) | ● |
| API Desc | `api.pullpush.io` | No login | No (global access) | ● |
| PullPush Asc | `api.pullpush.io` | No login | No (global access) | ● |
| PullPush Desc | `api.pullpush.io` | No login | No (global access) | ● |
| Boards | `boards.4chan.org` | No login | No (global access) | ● |
| Threads | `boards.4chan.org` | No login | No (global access) | ● |
| Archive | `camas.unddit.com` | No login | No (global access) | ● |
| Disboard | `disboard.org` | No login | No (global access) | ● |
| Invite | `discord.com` | Platform login: Discord (to view content) | No (global access) | ● |
| Bee | `discord.gg` | Platform login: Discord (to view content) | No (global access) | ● |
| Discord.me | `discord.me` | Platform login: Discord (to view content) | No (global access) | ◑ |
| Servers | `discordservers.com` | No login | No (global access) | ● |
| Google | `google.com` | No login | No (global access) | ● |
| Google | `google.com` | No login | No (global access) | ● |
| Google Site | `google.com` | No login | No (global access) | ● |
| Search | `hn.algolia.com` | No login | No (global access) | ● |
| Channel Search | `lyzem.com` | No login | No (global access) | ● |
| Favorites | `news.ycombinator.com` | No login | No (global access) | ● |
| Profile | `news.ycombinator.com` | No login | No (global access) | ● |
| Submissions | `news.ycombinator.com` | No login | No (global access) | ● |
| Threads | `news.ycombinator.com` | No login | No (global access) | ● |
| Comments | `reddit.com` | No login | No (global access) | ● |
| Keyword | `reddit.com` | No login | No (global access) | ● |
| Profile | `reddit.com` | No login | No (global access) | ● |
| Submissions | `reddit.com` | No login | No (global access) | ● |
| Title | `reddit.com` | No login | No (global access) | ● |
| Channel Preview | `t.me` | Platform login: Telegram (to join channels) (to view content) | No (global access) | ◑ |
| Profile/Channel | `t.me` | Platform login: Telegram (to join channels) (to view content) | No (global access) | ◑ |
| Telemetr.io | `telemetr.io` | No login | No (global access) | ● |
| Telesco.pe | `telesco.pe` | No login | No (global access) | ● |
| Group Search | `tgstat.com` | No login | No (global access) | ● |


### Maps / geospatial  —  32 queries

*Auth:* 32 no-login  ·  *VPN:* 28 no-VPN, 4 VPN-US

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| AcreValue | `acrevalue.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Apple Maps | `beta.maps.apple.com` | No login | No (global access) | ● |
| Bing Map | `bing.com` | No login | No (global access) | ● |
| Bing Sat | `bing.com` | No login | No (global access) | ● |
| Bing Sat (E) | `bing.com` | No login | No (global access) | ● |
| Bing Sat (N) | `bing.com` | No login | No (global access) | ● |
| Bing Sat (S) | `bing.com` | No login | No (global access) | ● |
| Bing Sat (W) | `bing.com` | No login | No (global access) | ● |
| Bing Street (E) | `bing.com` | No login | No (global access) | ● |
| Bing Street (N) | `bing.com` | No login | No (global access) | ● |
| Bing Street (S) | `bing.com` | No login | No (global access) | ● |
| Bing Street (W) | `bing.com` | No login | No (global access) | ● |
| Land Viewer | `eos.com` | No login | No (global access) | ● |
| Google Map | `google.com` | No login | No (global access) | ● |
| Google Sat | `google.com` | No login | No (global access) | ● |
| Google Street | `google.com` | No login | No (global access) | ● |
| Google Street (E) | `google.com` | No login | No (global access) | ● |
| Google Street (N) | `google.com` | No login | No (global access) | ● |
| Google Street (S) | `google.com` | No login | No (global access) | ● |
| Google Street (W) | `google.com` | No login | No (global access) | ● |
| KartaView | `kartaview.org` | No login | No (global access) | ● |
| World Imagery | `livingatlas.arcgis.com` | No login | No (global access) | ● |
| Mapillary | `mapillary.com` | No login | No (global access) | ● |
| Convert Address | `nominatim.openstreetmap.org` | No login | No (global access) | ● |
| Convert Address | `nominatim.openstreetmap.org` | No login | No (global access) | ● |
| Realtor | `realtor.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Apple Maps Alt | `satellites.pro` | No login | No (global access) | ● |
| Trulia | `trulia.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Here Sat | `wego.here.com` | No login | No (global access) | ● |
| Yandex Sat | `yandex.com` | No login | No (global access) | ● |
| Zillow | `zillow.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| Zoom Earth | `zoom.earth` | No login | No (global access) | ● |


### Images  —  16 queries

*Auth:* 12 no-login, 2 social-login, 1 account/paywall, 1 free-opt  ·  *VPN:* 16 no-VPN

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| Bing | `bing.com` | No login | No (global access) | ● |
| Bing Images | `bing.com` | No login | No (global access) | ● |
| Facebook Images | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| FaceCheck | `facecheck.id` | Registration / credits | No (global access) | ◑ |
| Flickr Images | `flickr.com` | No login | No (global access) | ● |
| Google Images | `google.com` | No login | No (global access) | ● |
| Google Images | `google.com` | No login | No (global access) | ● |
| Instagram Images | `google.com` | No login | No (global access) | ● |
| LinkedIn Images | `google.com` | No login | No (global access) | ● |
| Google Lens | `lens.google.com` | No login | No (global access) | ● |
| Repost Sleuth | `repostsleuth.com` | No login | No (global access) | ● |
| TinEye | `tineye.com` | No (free; account only for volume/extras) | No (global access) | ○ |
| Tumblr Images | `tumblr.com` | No login | No (global access) | ● |
| Twitter Images | `twitter.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Yandex | `yandex.com` | No login | No (global access) | ● |
| Yandex Images | `yandex.com` | No login | No (global access) | ● |


### Videos  —  39 queries

*Auth:* 33 no-login, 3 social-login, 3 free-opt  ·  *VPN:* 39 no-VPN

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| Archives (Video) | `archive.org` | No login | No (global access) | ● |
| Archives I (Movies) | `archive.org` | No login | No (global access) | ● |
| Archives II (OpenSource) | `archive.org` | No login | No (global access) | ● |
| TV Archives | `archive.org` | No login | No (global access) | ● |
| Bing | `bing.com` | No login | No (global access) | ● |
| Bing | `bing.com` | No login | No (global access) | ● |
| Bing Reverse | `bing.com` | No login | No (global access) | ● |
| Bing Videos | `bing.com` | No login | No (global access) | ● |
| Facebook Videos | `facebook.com` | Platform login: Facebook (to view content) | No (global access) | ● |
| Google | `google.com` | No login | No (global access) | ● |
| Google | `google.com` | No login | No (global access) | ● |
| Google Reverse | `google.com` | No login | No (global access) | ● |
| Google Videos | `google.com` | No login | No (global access) | ● |
| Metadata (Video) | `googleapis.com` | No login | No (global access) | ● |
| Search | `googleapis.com` | No login | No (global access) | ● |
| Thumbnail 2 | `i.ytimg.com` | No login | No (global access) | ● |
| Thumbnail 3 | `i.ytimg.com` | No login | No (global access) | ● |
| Thumbnail 4 | `i.ytimg.com` | No login | No (global access) | ● |
| Thumbnail HQ | `i.ytimg.com` | No login | No (global access) | ● |
| Baidu | `image.baidu.com` | No login | No (global access) | ● |
| Age Bypass | `nsfwyoutube.com` | No login | No (global access) | ● |
| Restrictions I | `polsy.org.uk` | No login | No (global access) | ● |
| Reddit Videos | `reddit.com` | No login | No (global access) | ● |
| Search | `tiktok.com` | Platform login: TikTok (to view content) | No (global access) | ◑ |
| TinEye | `tineye.com` | No (free; account only for volume/extras) | No (global access) | ○ |
| TinEye | `tineye.com` | No (free; account only for volume/extras) | No (global access) | ○ |
| TinEye Reverse | `tineye.com` | No (free; account only for volume/extras) | No (global access) | ○ |
| Twitter Videos | `twitter.com` | Platform login: X / Twitter (to view content) | No (global access) | ● |
| Restrictions II | `watannetwork.com` | No login | No (global access) | ● |
| Download | `y2mate.is` | No login | No (global access) | ● |
| Yandex | `yandex.com` | No login | No (global access) | ● |
| Yandex | `yandex.com` | No login | No (global access) | ● |
| Yandex Reverse | `yandex.com` | No login | No (global access) | ● |
| Yandex Videos | `yandex.ru` | No login | No (global access) | ● |
| Account | `youtube.com` | No login | No (global access) | ● |
| Full Screen | `youtube.com` | No login | No (global access) | ● |
| Profile | `youtube.com` | No login | No (global access) | ● |
| YouTube Videos | `youtube.com` | No login | No (global access) | ● |
| Metadata | `youtube.googleapis.com` | No login | No (global access) | ● |


### Documents  —  30 queries

*Auth:* 30 no-login  ·  *VPN:* 30 no-VPN

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| Archive.org | `archive.org` | No login | No (global access) | ● |
| GrayHatWarfare | `buckets.grayhatwarfare.com` | No login | No (global access) | ● |
| Core | `core.ac.uk` | No login | No (global access) | ● |
| Amazon AWS | `google.com` | No login | No (global access) | ● |
| Cloudfront | `google.com` | No login | No (global access) | ● |
| DOC/DOCX | `google.com` | No login | No (global access) | ● |
| Google API | `google.com` | No login | No (global access) | ● |
| Google Books | `google.com` | No login | No (global access) | ● |
| Google Docs | `google.com` | No login | No (global access) | ● |
| Google Drive | `google.com` | No login | No (global access) | ● |
| JPG/JPEG/PNG | `google.com` | No login | No (global access) | ● |
| MP3/WAV | `google.com` | No login | No (global access) | ● |
| MPG/MP4 | `google.com` | No login | No (global access) | ● |
| ODT/ODS/ODP | `google.com` | No login | No (global access) | ● |
| PDF | `google.com` | No login | No (global access) | ● |
| PPT/PPTX/KEY | `google.com` | No login | No (global access) | ● |
| TXT/RTF/XML | `google.com` | No login | No (global access) | ● |
| XLS/XLSX/CSV | `google.com` | No login | No (global access) | ● |
| ZIP/RAR/7Z | `google.com` | No login | No (global access) | ● |
| ISSUU | `issuu.com` | No login | No (global access) | ● |
| MS Docs | `learn.microsoft.com` | No login | No (global access) | ● |
| openAFRICA | `open.africa` | No login | No (global access) | ● |
| PDF Drive | `pdfdrive.com` | No login | No (global access) | ● |
| Powershow | `powershow.com` | No login | No (global access) | ● |
| Prezi | `prezi.com` | No login | No (global access) | ● |
| Refseek | `refseek.com` | No login | No (global access) | ● |
| Scribd | `scribd.com` | No login | No (global access) | ● |
| Wikileaks | `search.wikileaks.org` | No login | No (global access) | ● |
| Slide Bean | `slidebean.com` | No login | No (global access) | ● |
| SlideShare | `slideshare.net` | No login | No (global access) | ● |


### Cryptocurrencies  —  48 queries

*Auth:* 36 no-login, 11 account/paywall, 1 free-opt  ·  *VPN:* 48 no-VPN

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| Creation Date | `api.blockchair.com` | No login | No (global access) | ● |
| BTC Validation | `bitcoin-e.org` | No login | No (global access) | ● |
| BitcoinWhosWho | `bitcoinwhoswho.com` | No login | No (global access) | ● |
| Blockchain.com | `blockchain.com` | No login | No (global access) | ● |
| Satoshi Balance | `blockchain.info` | No login | No (global access) | ● |
| Satoshi Received | `blockchain.info` | No login | No (global access) | ● |
| Satoshi Sent | `blockchain.info` | No login | No (global access) | ● |
| BC BTC | `blockchair.com` | No login | No (global access) | ● |
| BC Bitcoin-Cash | `blockchair.com` | No login | No (global access) | ● |
| BC Bitcoin-SV | `blockchair.com` | No login | No (global access) | ● |
| BC Dash | `blockchair.com` | No login | No (global access) | ● |
| BC Dogecoin | `blockchair.com` | No login | No (global access) | ● |
| BC Ethereum | `blockchair.com` | No login | No (global access) | ● |
| BC Litecoin | `blockchair.com` | No login | No (global access) | ● |
| Blockscan | `blockscan.com` | No login | No (global access) | ● |
| Blockscan Token | `blockscan.com` | No login | No (global access) | ● |
| Breadcrumbs | `breadcrumbs.app` | Registration | No (global access) | ◑ |
| Chainabuse | `chainabuse.com` | No login | No (global access) | ● |
| Debank (Profile) | `debank.com` | Wallet login for features | No (global access) | ○ |
| Etherscan (ETH) | `etherscan.io` | No login | No (global access) | ● |
| Crystal Explorer | `explorer.crystalblockchain.com` | Account | No (global access) | ◑ |
| Crystal Visualizer | `explorer.crystalblockchain.com` | Account | No (global access) | ◑ |
| BTC &gt; EUR | `google.com` | No login | No (global access) | ● |
| BTC &gt; USD | `google.com` | No login | No (global access) | ● |
| EUR &gt; BTC | `google.com` | No login | No (global access) | ● |
| Google Search | `google.com` | No login | No (global access) | ● |
| Satoshi &gt; USD | `google.com` | No login | No (global access) | ● |
| USD &gt; BTC | `google.com` | No login | No (global access) | ● |
| USD &gt; Satoshi | `google.com` | No login | No (global access) | ● |
| Summary (mempool) | `mempool.space` | No login | No (global access) | ● |
| MetaSleuth (BSC) | `metasleuth.io` | Free registration | No (global access) | ◑ |
| MetaSleuth (BTC) | `metasleuth.io` | Free registration | No (global access) | ◑ |
| MetaSleuth (ETH) | `metasleuth.io` | Free registration | No (global access) | ◑ |
| MetaSleuth (Poly) | `metasleuth.io` | Free registration | No (global access) | ◑ |
| OKLink Explorer | `oklink.com` | No login | No (global access) | ● |
| OKLink Visualisation | `oklink.com` | No login | No (global access) | ● |
| OXT.me | `oxt.me` | No login | No (global access) | ● |
| Phalcon Explorer | `phalcon.blocksec.com` | No (free; account only for volume/extras) | No (global access) | ○ |
| Arkham (Explorer) | `platform.arkhamintelligence.com` | Free registration | No (global access) | ◑ |
| Arkham (Visualizer) | `platform.arkhamintelligence.com` | Free registration | No (global access) | ◑ |
| PolygonScan | `polygonscan.com` | No login | No (global access) | ● |
| SolanaFM | `solana.fm` | No login | No (global access) | ● |
| Address | `tronscan.org` | No login | No (global access) | ● |
| Contract | `tronscan.org` | No login | No (global access) | ● |
| Transaction | `tronscan.org` | No login | No (global access) | ● |
| WalletExplorer | `walletexplorer.com` | No login | No (global access) | ● |
| WalletExplorer | `walletexplorer.com` | No login | No (global access) | ● |
| Zapper (DeFi/NFT) | `zapper.fi` | Wallet login for features | No (global access) | ○ |


### Vehicles  —  13 queries

*Auth:* 13 no-login  ·  *VPN:* 1 no-VPN, 11 VPN-US, 1 VPN-country

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| Launch Carnet.ai | `carnet.ai` | No login | No (global access) | ● |
| Carvana | `carvana.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| CheckThatVIN | `checkthatvin.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| CanadaVIN | `csps.con.rcmp-grc.gc.ca` | No login | Global access; Canada national data (VPN Canada only if blocked) | ○ |
| CycleVIN | `cyclevin.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| FaxVIN | `faxvin.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| InfoTracer | `infotracer.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| RecordFinder | `recordsfinder.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| RecordFinder | `recordsfinder.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| SearchQuarry | `searchquarry.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| SearchQuarry | `searchquarry.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| VINCheck.info | `vincheck.info` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |
| VINDecoderz | `vindecoderz.com` | No login | VPN United States recommended (many sites limit/block EU IPs due to GDPR/CCPA) | ◑ |


### Keybase  —  6 queries

*Auth:* 6 no-login  ·  *VPN:* 6 no-VPN

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| Team Profile | `keybase.io` | No login | No (global access) | ● |
| User Devices | `keybase.io` | No login | No (global access) | ● |
| User Graph | `keybase.io` | No login | No (global access) | ● |
| User Profile | `keybase.io` | No login | No (global access) | ● |
| User Sigchain | `keybase.io` | No login | No (global access) | ● |
| User Stellar Info | `keybase.io` | No login | No (global access) | ● |


### IBAN  —  5 queries

*Auth:* 5 no-login  ·  *VPN:* 5 no-VPN

| Service | Host | Auth (access) | VPN/country (access) | Conf. |
|---|---|---|---|:--:|
| Baidu Search | `baidu.com` | No login | No (global access) | ● |
| Bing Search | `bing.com` | No login | No (global access) | ● |
| Google Search | `google.com` | No login | No (global access) | ● |
| IBAN Calculator | `ibancalculator.com` | No login | No (global access) | ● |
| Yandex Search | `yandex.com` | No login | No (global access) | ● |


---

## 7. Notes, limits and maintenance

- **Data source:** `shared/catalog.json` (Exploratores 3.4.1). If the catalog is regenerated, re-run the classification script.
- **Reproducibility:** the table is produced by `scripts/classify_queries.py` (host/category rules) → `docs/query_classification.csv` → `scripts/generate_docs.py` → this `.md`. Rules are declarative and inspectable.
- **Out of scope:** it does not test real-time reachability, does not handle credentials, and does not weigh legal/mandate limits (using sock-puppets and accessing certain services must be authorised within the operational framework).
- **Medium/Low rows:** confirm login and geo-blocking at time of use; report deviations to update the rules.
- **Confidence legend:** ● High · ◑ Medium · ○ Low.

*Generated as a desk analysis; it is not a guarantee of accessibility for individual services.*

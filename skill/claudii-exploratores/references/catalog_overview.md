# Catalog Overview

The catalog holds **909 OSINT tools** across **26 categories** (source: Exploratores OSINT Toolkit 3.10.5 (https://github.com/SOsintOps/Exploratores)). Each entry is a URL template filled from the classified indicator and URL-encoded, exactly as the original toolkit does.

Use `python scripts/exploratores.py categories` for live counts and `... search "<keyword>"` to find a specific tool. Access requirements per source (VPN country, Tor, account) are in `scripts/access.json` and appear as warnings in the `urls` output.

| Category | Tools | What it covers |
|---|---|---|
| `domains` | 139 | Domain intelligence: WHOIS/history, DNS, tech profiling, screenshots, archives, subdomains. |
| `usernames` | 66 | Pivot a username/handle across dozens of platforms and enumeration services. |
| `publiccompanyrecords` | 63 | Corporate registries and officer/company records across jurisdictions. |
| `names` | 61 | Search a person by full name across people-search, directories and social platforms. |
| `ip` | 57 | IP-address intelligence: geolocation, reputation, ports/services, WiFi (WiGLE), ranges. |
| `currencies` | 46 | Cryptocurrency address analysis and blockchain explorers (BTC/ETH/XMR). |
| `facebook` | 46 | Facebook-specific search by name, username or numeric ID. |
| `phoneint` | 44 | International phone number lookups (E.164 variants, reverse WHOIS, messaging apps). |
| `videos` | 39 | Video platform search and analysis (YouTube, Vimeo, TikTok, etc.). |
| `maps` | 33 | Geolocation and mapping tools by coordinates/address. |
| `x` | 31 | X/Twitter search by handle, ID, list, real name, date range. |
| `docs` | 30 | Document and file search (leaks, pastes, code, scribd-style repositories). |
| `vk` | 30 | VKontakte search by username, ID, tag. |
| `searchengines` | 28 | General clear-web and Tor search engines (Google dorks, Yandex, Bing, DuckDuckGo, Wayback, Ahmia, .onion engines). |
| `phoneus` | 27 | US phone number lookups (reverse phone, carrier, people search). |
| `communities` | 26 | Forums and community platforms (Reddit, Discord, Hacker News, 4chan, etc.). |
| `email` | 23 | Investigate an email address: breach/exposure lookups, reverse email, validators. |
| `address` | 22 | Physical-address lookups (US and international property/people directories). |
| `instagram` | 18 | Instagram-specific search by username, user ID, hashtag. |
| `images` | 16 | Reverse image search and image analysis. |
| `legal` | 15 | Italian and European Union legal sources: legislation (Normattiva URN), case law, regulators, registers, trade marks, VAT check (VIES). |
| `telegram` | 14 | Telegram channels, groups, users and messages: previews, in-channel search, message history, search engines and archives. |
| `vehicles` | 13 | Vehicle intelligence by VIN or licence plate. |
| `linkedin` | 11 | LinkedIn people/company/content search. |
| `keybase` | 6 | Keybase identity lookups. |
| `iban` | 5 | IBAN-related lookups and validation. |

## Example: sample tools per category (first 5)

### `domains` (139)
- **AnalyzeID** — `domains-adsense-analyzeid`
- **DNSlytics** — `domains-adsense-dnslytics`
- **HackerTarget** — `domains-adsense-hackertarget`
- **AnalyzeID** — `domains-analytics-analyzeid`
- **DNSlytics** — `domains-analytics-dnslytics`

### `usernames` (66)
- **AlienVault Indicator** — `usernames-alienvault`
- **Arkham Entity** — `usernames-arkham`
- **ASA Search** — `usernames-asa`
- **Bing** — `usernames-bing-search`
- **CashApp User** — `usernames-cashapp`

### `publiccompanyrecords` (63)
- **AIHIT** — `publiccompanyrecords-company-aihit`
- **ASA** — `publiccompanyrecords-company-asa`
- **B2BHint** — `publiccompanyrecords-company-b2bhint`
- **CAC (Nigeria)** — `publiccompanyrecords-company-cac`
- **Censys Certificates** — `publiccompanyrecords-company-censys`

### `names` (61)
- **9ja Book** — `names-9jabook`
- **ASA** — `names-asa`
- **Canada411** — `names-canada411`
- **Censys Certificates** — `names-censys-cert`
- **Checko** — `names-checkoru`

### `ip` (57)
- **DNSChecker** — `ip-info-dnschecker`
- **DomainTools Whois** — `ip-info-domaintools`
- **InfoByIp** — `ip-info-infobyip`
- **IPAddress.com** — `ip-info-ipaddresscom`
- **ipapi.co (Bulk Geo)** — `ip-info-ipapico`

### `currencies` (46)
- **Arkham (Explorer)** — `currencies-analysis-arkham-exp`
- **Arkham (Visualizer)** — `currencies-analysis-arkham-viz`
- **Blockscan Token** — `currencies-analysis-blockscan`
- **Breadcrumbs** — `currencies-analysis-breadcrumbs`
- **Crystal Explorer** — `currencies-analysis-crystal-exp`

### `facebook` (46)
- **About** — `facebook-profile-about`
- **Photo Albums** — `facebook-profile-albums`
- **Apps & Games** — `facebook-profile-apps`
- **Basic Info** — `facebook-profile-basic`
- **Biography** — `facebook-profile-bio`

### `phoneint` (44)
- **411.com** — `phoneint-411`
- **AQL Network (UK)** — `phoneint-aql`
- **Bing Search** — `phoneint-bing`
- **0Num Only** — `phoneint-dt-0numonly`
- **phoneint-dt-base** — `phoneint-dt-base`

### `videos` (39)
- **Account** — `videos-channel-account`
- **Metadata** — `videos-channel-metadata`
- **Profile** — `videos-channel-profile`
- **Search** — `videos-comments-search`
- **Age Bypass** — `videos-id-agebypass`

### `maps` (33)
- **AcreValue** — `maps-acrevalue`
- **Apple Maps** — `maps-apple`
- **Apple Maps Alt** — `maps-apple-alt`
- **Bing Map** — `maps-bing-map`
- **Bing Sat** — `maps-bing-sat`

### `x` (31)
- **Followers** — `x-account-followers`
- **Following** — `x-account-following`
- **Highlights** — `x-account-highlights`
- **Incoming Mentions** — `x-account-incoming`
- **Links** — `x-account-links`

### `docs` (30)
- **openAFRICA** — `docs-dataset-openafrica`
- **DOC/DOCX** — `docs-filetype-doc`
- **JPG/JPEG/PNG** — `docs-filetype-jpg`
- **MP3/WAV** — `docs-filetype-mp3`
- **MPG/MP4** — `docs-filetype-mpg`

### `vk` (30)
- **Checko.ru** — `vk-ext-checko`
- **Google Search** — `vk-ext-google`
- **Mail.Ru Search** — `vk-ext-mailru`
- **SMAT Search** — `vk-ext-smat`
- **WebArchive (RU)** — `vk-ext-webarchive`

### `searchengines` (28)
- **Ahmia (Clear)** — `searchengines-ahmia`
- **Ahmia (Onion)** — `searchengines-ahmiaonion`
- **Baidu** — `searchengines-baidu`
- **Bing** — `searchengines-bing`
- **Bing News** — `searchengines-bingnews`

### `phoneus` (27)
- **411** — `phoneus-411`
- **800 Notes** — `phoneus-800notes`
- **AdvBackground** — `phoneus-advbackground`
- **AmericaPhone** — `phoneus-americaphone`
- **Bing Search** — `phoneus-bing`

### `communities` (26)
- **Archive** — `communities-4chan-archive`
- **Boards** — `communities-4chan-boards`
- **Google** — `communities-4chan-google`
- **Threads** — `communities-4chan-threads`
- **Bee** — `communities-discord-bee`

### `email` (23)
- **AnalyzeID** — `email-analyzeid`
- **Bing** — `email-bing`
- **CleanTalk** — `email-cleantalk`
- **Cybernews** — `email-cybernews`
- **Dehashed** — `email-dehashed`

### `address` (22)
- **FastPeople EU** — `address-intl-fastpeople`
- **GISGraphy** — `address-intl-gisgraphy`
- **Google** — `address-intl-google`
- **Search Companies** — `address-it-paginebianche-companies`
- **Search People** — `address-it-paginebianche-people`

### `instagram` (18)
- **Bing Search** — `instagram-bing-search`
- **Channel** — `instagram-channel`
- **Associations (Google)** — `instagram-combo-associations`
- **User + Term (Google)** — `instagram-combo-user-term`
- **Dumpor Profile** — `instagram-dumpor-profile`

### `images` (16)
- **Bing** — `images-reverse-bing`
- **FaceCheck** — `images-reverse-facecheck`
- **Google Images** — `images-reverse-google`
- **Google Lens** — `images-reverse-lens`
- **Repost Sleuth** — `images-reverse-repostsleuth`

### `legal` (15)
- **CURIA (Case No.)** — `legal-eu-curia`
- **EUR-Lex** — `legal-eu-eurlex`
- **TMview** — `legal-eu-tmview`
- **VIES** — `legal-eu-vies`
- **Brocardi** — `legal-it-brocardi`

### `telegram` (14)
- **Jump Back in History** — `telegram-history`
- **Search in Channel** — `telegram-inchannel`
- **Invite Links** — `telegram-invites`
- **Lyzem** — `telegram-lyzem`
- **Link Mentions** — `telegram-mentions`

### `vehicles` (13)
- **CanadaVIN** — `vehicles-canadavin`
- **Launch Carnet.ai** — `vehicles-carnetai`
- **Carvana** — `vehicles-carvana`
- **CheckThatVIN** — `vehicles-checkthatvin`
- **CycleVIN** — `vehicles-cyclevin`

### `linkedin` (11)
- **Bing People** — `linkedin-ext-bing`
- **Google People** — `linkedin-ext-google`
- **Yandex People** — `linkedin-ext-yandex`
- **Bing Images** — `linkedin-images-bing`
- **Google Images** — `linkedin-images-google`

### `keybase` (6)
- **Team Profile** — `keybase-team-profile`
- **User Devices** — `keybase-user-devices`
- **User Graph** — `keybase-user-graph`
- **User Profile** — `keybase-user-profile`
- **User Sigchain** — `keybase-user-sigchain`

### `iban` (5)
- **Baidu Search** — `iban-search-baidu`
- **Bing Search** — `iban-search-bing`
- **Google Search** — `iban-search-google`
- **IBAN Calculator** — `iban-search-ibancalc`
- **Yandex Search** — `iban-search-yandex`

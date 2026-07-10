# Access requirements — do I need an account, a VPN, or Tor?

> Companion guide to the Exploratores query catalog. Last updated: 2026-07-10.

This guide tells you, for each source behind the catalog's queries, whether you need to **log in**, whether a **VPN** (and which country) helps or is required, and which sources are **Tor-only**. Requirements are per *source* (host); the **#q** column is how many catalog queries use that source.


## How to read this

| Tier | Meaning |
| --- | --- |
| 🔓 **Account — Not needed** | Works anonymously. |
| 👤 **Account — Recommended** | Usable without an account, but logging in unlocks more results / higher limits (e.g. OpenCorporates). |
| 🔑 **Account — Required** | No useful results without logging in — a normal account, a platform profile (a research *sock-puppet* for social networks), or a paid plan. |
| 🌍 **VPN — Required (country)** | The source only serves specific IP ranges; from elsewhere you need a VPN exit in that country. |
| 🧭 **VPN — Sometimes helps** | Bot-protection (Cloudflare / CAPTCHA) was seen during automated testing. A normal browser usually passes; if you are blocked, a different exit can help. |
| 🧅 **Tor — Required** | An .onion service; reachable only over Tor. |

> **Method & honesty.** Verdicts come from live probing of each source with neutral test inputs, from an EU IP and (for the geo checks) a US VPN exit. *Bot-protection* verdicts reflect **automated** access — a human in a regular browser is usually not blocked, so treat those as “may need a different exit”, not a hard requirement. Independently verify anything you rely on.


## At a glance

| Category | Sources | Queries |
| --- | --- | --- |
| Account required | 34 | 176 |
| Account recommended | 15 | 89 |
| Account not needed | 254 | 491 |
| VPN required (a country) | 19 | 26 |
| Tor required (.onion) | 9 | 9 |
| Bot-protection seen (VPN may help) | 40 | 86 |
| Unverified | 78 | 141 |

---

## 🔑 Account required  (34 sources, 176 queries)

| Source | Category | #q | Detail |
| --- | --- | --- | --- |
| www.facebook.com | facebook | 52 | Requires logged-in profile (FB session carried) |
| vk.com | usernames | 25 | Requires logged-in profile (VK) |
| x.com | usernames | 24 | Requires logged-in profile (X/Twitter) |
| search.censys.io | domains | 7 | Account/registration required |
| dehashed.com | domains | 6 | Paid account required |
| www.linkedin.com | linkedin | 6 | Requires logged-in profile (LinkedIn) |
| www.shodan.io | domains | 5 | A (free) account is required to run searches; results are global. |
| instagram.com | instagram | 4 | Requires logged-in profile (Instagram) |
| leakix.net | domains | 4 | Account required (redirect to /auth/login) |
| twitter.com | images | 4 | Requires logged-in profile (X / Twitter) |
| www.instagram.com | instagram | 4 | Requires logged-in profile (Instagram) |
| beta.shodan.io | ip | 3 | Account/login required |
| urlscan.io | domains | 3 | Account/login required |
| intelx.io | domains | 2 | Account required (registration) |
| maltiverse.com | domains | 2 | Account/login required |
| tria.ge | domains | 2 | Account required (registration) |
| vk.me | usernames | 2 | Requires logged-in profile (VK) |
| wigle.net | ip | 2 | Account/login required |
| www.domainiq.com | domains | 2 | Account/login required |
| www.googleapis.com | videos | 2 | API key required |
| www.tiktok.com | usernames | 2 | Requires logged-in profile (TikTok) |
| clarifiedby.diligenciagroup.com | publiccompanyrecords | 1 | Account/login required |
| facebook.com | usernames | 1 | Requires logged-in profile (Facebook) |
| mbasic.facebook.com | phoneus | 1 | Requires logged-in profile (Facebook) |
| mewe.com | usernames | 1 | Platform login: MeWe (profile 404 for test user) |
| myspace.com | email | 1 | Account/login required (password field present) |
| naijaplanet.com | usernames | 1 | Account/login required for full profile |
| portal.aql.com | phoneint | 1 | Account required |
| portal.spycloud.com | email | 1 | Account required (enterprise) |
| pulsedive.com | domains | 1 | Account/login required |
| scamsearch.io | email | 1 | Registration required |
| www.hybrid-analysis.com | domains | 1 | Account/login required |
| www.threads.net | instagram | 1 | Account/login required (Threads) |
| youtube.googleapis.com | videos | 1 | API key required (endpoint reachable) |

## 👤 Account recommended (works without, better with)  (15 sources, 89 queries)

| Source | Category | #q | Detail |
| --- | --- | --- | --- |
| viewdns.info | domains | 32 | Free (login optional for full results) |
| reversewhois.domaintools.com | names | 27 | Account for full results (preview no-login) |
| aleph.occrp.org | domains | 5 | Login optional (sign-in for some collections) |
| metasleuth.io | currencies | 4 | Free registration for full (partial no-login) |
| opencorporates.com | names | 3 | Public search works; a free account raises rate limits and unlocks full record history. |
| securitytrails.com | domains | 3 | No login (registration for extras) |
| t.me | communities | 3 | No login (public preview; login to interact) |
| whois.domaintools.com | domains | 3 | Basic WHOIS is public; historical/reverse data needs a paid account. |
| www.virustotal.com | domains | 3 | Basic lookups are public; a free account is needed for the full GUI and history. |
| discord.com | communities | 1 | No login to preview; Discord login to join |
| discord.gg | communities | 1 | No login to preview; Discord login to join |
| epieos.com | phoneint | 1 | Free registration for full results |
| hunter.io | email | 1 | No login for verifier UI; free registration for full results |
| kik.me | usernames | 1 | No login (deep-link splash); Kik app to chat |
| moz.com | domains | 1 | Free registration for full results |

## 🌍 VPN required — by country  (19 sources, 26 queries)


### US  (19 sources)

| Source | Category | #q | Detail |
| --- | --- | --- | --- |
| beta.shodan.io | ip | 3 | Loads via a US exit, then requires an account. |
| www.cyberbackgroundchecks.com | address | 3 | Restricted to US IP ranges; loads normally through a US exit. |
| www.411.com | phoneint | 2 | Restricted to US IP ranges; loads normally through a US exit. |
| www.peoplesearchnow.com | names | 2 | Restricted to US IP ranges; loads normally through a US exit. |
| www.zabasearch.com | names | 2 | Restricted to US IP ranges; loads normally through a US exit. |
| 800notes.com | phoneus | 1 | Restricted to US IP ranges; loads normally through a US exit. |
| b2bhint.com | publiccompanyrecords | 1 | Restricted to US IP ranges; loads normally through a US exit. |
| cash.app | usernames | 1 | Restricted to US IP ranges; loads normally through a US exit. |
| mysmsbox.ru | phoneint | 1 | Restricted to US IP ranges; loads normally through a US exit. |
| nerdydata.com | domains | 1 | Restricted to US IP ranges; loads normally through a US exit. |
| radaris.com | names | 1 | Restricted to US IP ranges; loads normally through a US exit. |
| rehold.com | address | 1 | Restricted to US IP ranges; loads normally through a US exit. |
| smartbackgroundchecks.com | address | 1 | Restricted to US IP ranges; loads normally through a US exit. |
| spam.org | domains | 1 | Restricted to US IP ranges; loads normally through a US exit. |
| telemetr.io | communities | 1 | Restricted to US IP ranges; loads normally through a US exit. |
| www.callersmart.com | phoneus | 1 | Restricted to US IP ranges; loads normally through a US exit. |
| www.usphonebook.com | phoneus | 1 | Restricted to US IP ranges; loads normally through a US exit. |
| www.wmtips.com | domains | 1 | Restricted to US IP ranges; loads normally through a US exit. |
| yandex.ru | videos | 1 | Restricted to US IP ranges; loads normally through a US exit. |

## 🧅 Tor required (.onion)  (9 sources, 9 queries)

| Source | Category | #q | Detail |
| --- | --- | --- | --- |
| 3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2jobad.onion | searchengines | 1 |  |
| 5qqrlc7hw3tsgokkqifb33p3mrlpnleka2bjg7n46vih2synghb6ycid.onion | searchengines | 1 |  |
| freshonifyfe4rmuh6qwpsexfhdrww7wnt5qmkoertwxmcuvm4woo4ad.onion | searchengines | 1 |  |
| juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion | searchengines | 1 |  |
| no6m4wzdexe3auiupv2zwif7rm6qwxcyhslkcnzisxgeiw6pvjsgafad.onion | searchengines | 1 |  |
| searchgf7gdtauh7bhnbyed4ivxqmuoat3nm6zfrg3ymkq6mtnpye3ad.onion | searchengines | 1 |  |
| u5lyidiw4lpkonoctpqzxgyk6xop7w7w3oho4dzzsi272rwnjhyx7ayd.onion | searchengines | 1 |  |
| www.tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion | searchengines | 1 |  |
| zb2jtkhnbvhkya3d46twv3g7lkobi4s62tjffqmafjibixk6pmq75did.onion | searchengines | 1 |  |

## 🧭 Bot-protection seen during testing (a VPN/other exit may help)  (40 sources, 86 queries)

| Source | Category | #q | Detail |
| --- | --- | --- | --- |
| yandex.com | domains | 15 | N/A |
| blockchair.com | currencies | 7 | No login |
| thatsthem.com | email | 6 | N/A |
| www.fastpeoplesearch.com | address | 4 | N/A |
| www.tineye.com | images | 4 | N/A |
| platform.arkhamintelligence.com | currencies | 3 | N/A |
| www.advancedbackgroundchecks.com | address | 3 | N/A |
| www.searchpeoplefree.com | address | 3 | N/A |
| www.truepeoplesearch.com | address | 3 | N/A |
| www.whitepages.com | address | 3 | N/A |
| nigeria24.me | publiccompanyrecords | 2 | N/A |
| nuwber.com | names | 2 | N/A |
| www.crunchbase.com | names | 2 | N/A |
| www.yandex.com | linkedin | 2 | N/A |
| www.zaubacorp.com | names | 2 | N/A |
| check.cybernews.com | email | 1 | N/A |
| check.spamhaus.org | domains | 1 | N/A |
| core.ac.uk | docs | 1 | N/A |
| dnpedia.com | domains | 1 | N/A |
| elephind.com | domains | 1 | N/A |
| iknowwhatyoudownload.com | ip | 1 | N/A |
| mrkoll.se | names | 1 | N/A |
| namechk.com | usernames | 1 | N/A |
| ng-check.com | publiccompanyrecords | 1 | N/A |
| numpi.com | phoneus | 1 | N/A |
| openpayrolls.com | publiccompanyrecords | 1 | N/A |
| search.cac.gov.ng | publiccompanyrecords | 1 | N/A |
| viz.greynoise.io | ip | 1 | N/A |
| voterrecords.com | publiccompanyrecords | 1 | N/A |
| www.familytreenow.com | names | 1 | N/A |
| www.faxvin.com | vehicles | 1 | N/A |
| www.infobyip.com | ip | 1 | N/A |
| www.ip-lookup.org | ip | 1 | N/A |
| www.ipaddress.com | ip | 1 | N/A |
| www.iplocation.net | ip | 1 | N/A |
| www.peoplebyname.com | names | 1 | N/A |
| www.skymem.info | domains | 1 | N/A |
| www.usa-people-search.com | address | 1 | N/A |
| www.vindecoderz.com | vehicles | 1 | N/A |
| zapper.fi | currencies | 1 | N/A |

## ✅ No account, no VPN — works as-is  (223 sources, 455 queries)

Distribution by catalog category:

| Category | Sources |
| --- | --- |
| domains | 53 |
| usernames | 22 |
| names | 18 |
| currencies | 17 |
| docs | 13 |
| communities | 12 |
| maps | 12 |
| publiccompanyrecords | 12 |
| searchengines | 10 |
| email | 10 |
| phoneint | 8 |
| videos | 7 |
| address | 6 |
| images | 5 |
| phoneus | 5 |
| ip | 4 |
| vehicles | 4 |
| instagram | 2 |
| keybase | 1 |
| iban | 1 |
| x | 1 |

<details><summary>Full list of open sources</summary>

| Source | Category | #q |
| --- | --- | --- |
| hudway.co | address | 1 |
| www.addresses.com | address | 2 |
| www.google.com | address | 81 |
| www.paginebianche.it | address | 3 |
| www.paginegialle.it | address | 2 |
| www.zillow.com | address | 2 |
| 4plebs.org | communities | 1 |
| api.pullpush.io | communities | 4 |
| boards.4chan.org | communities | 2 |
| disboard.org | communities | 1 |
| discord.me | communities | 1 |
| discordservers.com | communities | 1 |
| hn.algolia.com | communities | 1 |
| lyzem.com | communities | 1 |
| news.ycombinator.com | communities | 4 |
| telesco.pe | communities | 1 |
| tgstat.com | communities | 1 |
| www.reddit.com | communities | 9 |
| api.blockchair.com | currencies | 1 |
| bitcoinwhoswho.com | currencies | 1 |
| blockchain.info | currencies | 3 |
| blockchair.com | currencies | 7 |
| blockscan.com | currencies | 2 |
| debank.com | currencies | 1 |
| etherscan.io | currencies | 2 |
| explorer.crystalblockchain.com | currencies | 2 |
| mempool.space | currencies | 1 |
| phalcon.blocksec.com | currencies | 1 |
| polygonscan.com | currencies | 1 |
| solana.fm | currencies | 1 |
| tronscan.org | currencies | 3 |
| www.blockchain.com | currencies | 1 |
| www.breadcrumbs.app | currencies | 1 |
| www.oklink.com | currencies | 2 |
| www.walletexplorer.com | currencies | 2 |
| archive.org | docs | 5 |
| buckets.grayhatwarfare.com | docs | 1 |
| issuu.com | docs | 1 |
| learn.microsoft.com | docs | 1 |
| open.africa | docs | 1 |
| prezi.com | docs | 1 |
| search.wikileaks.org | docs | 1 |
| slidebean.com | docs | 1 |
| www.pdfdrive.com | docs | 1 |
| www.powershow.com | docs | 1 |
| www.refseek.com | docs | 1 |
| www.scribd.com | docs | 1 |
| www.slideshare.net | docs | 1 |
| analyzeid.com | domains | 4 |
| archive-it.org | domains | 1 |
| arquivo.pt | domains | 1 |
| builtwith.com | domains | 1 |
| carbondate.cs.odu.edu | domains | 1 |
| cavalier.hudsonrock.com | domains | 2 |
| centralops.net | domains | 1 |
| crt.sh | domains | 1 |
| dmns.app | domains | 1 |
| dnsdumpster.com | domains | 1 |
| dnslytics.com | domains | 5 |
| exchange.xforce.ibmcloud.com | domains | 1 |
| favicon-hash.kmsec.uk | domains | 1 |
| groups.google.com | domains | 2 |
| hackertarget.com | domains | 2 |
| host.io | domains | 3 |
| hypestat.com | domains | 1 |
| networksdb.io | domains | 6 |
| ofac.treasury.gov | domains | 5 |
| otx.alienvault.com | domains | 2 |
| publicwww.com | domains | 2 |
| research.domaintools.com | domains | 2 |
| searchdns.netcraft.com | domains | 1 |
| securityheaders.com | domains | 1 |
| sharedcount.com | domains | 1 |
| sitereport.netcraft.com | domains | 1 |
| themarkup.org | domains | 1 |
| threatintelligenceplatform.com | domains | 1 |
| tiny.cc | domains | 1 |
| web.archive.org | domains | 7 |
| whois.eurid.eu | domains | 1 |
| whoisology.com | domains | 2 |
| www.asa.org.uk | domains | 4 |
| www.baidu.com | domains | 3 |
| www.bing.com | domains | 26 |
| www.copyscape.com | domains | 1 |
| www.domaincodex.com | domains | 1 |
| www.expandurl.net | domains | 1 |
| www.fca.org.uk | domains | 3 |
| www.godaddy.com | domains | 1 |
| www.joesandbox.com | domains | 1 |
| www.linkody.com | domains | 1 |
| www.mywot.com | domains | 1 |
| www.robtex.com | domains | 2 |
| www.similarweb.com | domains | 1 |
| www.spyfu.com | domains | 1 |
| www.sra.org.uk | domains | 2 |
| www.stopforumspam.com | domains | 3 |
| www.who.is | domains | 2 |
| www.whois.com | domains | 3 |
| www.whoxy.com | domains | 2 |
| www.wipo.int | domains | 2 |
| {domain} | domains | 1 |
| api.protonmail.ch | email | 1 |
| bing.com | email | 3 |
| cleantalk.org | email | 1 |
| data.occrp.org | email | 1 |
| emailrep.io | email | 1 |
| flickr.com | email | 1 |
| gmail-osint.activetk.jp | email | 2 |
| google.com | email | 4 |
| gravatar.com | email | 1 |
| whoxy.com | email | 1 |
| www.ibancalculator.com | iban | 1 |
| facecheck.id | images | 1 |
| lens.google.com | images | 1 |
| www.flickr.com | images | 1 |
| www.repostsleuth.com | images | 1 |
| www.tumblr.com | images | 1 |
| dumpor.com | instagram | 2 |
| toolzu.com | instagram | 1 |
| app.ipapi.co | ip | 1 |
| dnschecker.org | ip | 1 |
| mxtoolbox.com | ip | 3 |
| www.maxmind.com | ip | 1 |
| keybase.io | keybase | 6 |
| beta.maps.apple.com | maps | 1 |
| eos.com | maps | 1 |
| kartaview.org | maps | 1 |
| livingatlas.arcgis.com | maps | 1 |
| nominatim.openstreetmap.org | maps | 2 |
| satellites.pro | maps | 1 |
| wego.here.com | maps | 1 |
| www.acrevalue.com | maps | 1 |
| www.mapillary.com | maps | 1 |
| www.realtor.com | maps | 1 |
| www.trulia.com | maps | 1 |
| zoom.earth | maps | 1 |
| 9jabook.com | names | 1 |
| publicrecords.searchsystems.net | names | 1 |
| rusfinder.pro | names | 1 |
| sanctionssearch.ofac.treas.gov | names | 2 |
| webmii.com | names | 1 |
| www.canada411.ca | names | 1 |
| www.classmates.com | names | 1 |
| www.eniro.se | names | 1 |
| www.hitta.se | names | 1 |
| www.idcrawl.com | names | 3 |
| www.intelius.com | names | 1 |
| www.interpol.int | names | 1 |
| www.opensanctions.org | names | 3 |
| www.ratsit.se | names | 1 |
| www.truthfinder.com | names | 1 |
| www.ukphonebook.com | names | 2 |
| www.yasni.com | names | 1 |
| yachtlycrew.com | names | 1 |
| freecarrierlookup.com | phoneint | 1 |
| nigeriaphonebook.com | phoneint | 1 |
| sync.me | phoneint | 2 |
| whatsapp.checkleaked.cc | phoneint | 2 |
| www.emobiletracker.com | phoneint | 1 |
| www.tellows.it | phoneint | 1 |
| www.truecaller.com | phoneint | 1 |
| www.vedbex.com | phoneint | 1 |
| infotracer.com | phoneus | 2 |
| people.yellowpages.com | phoneus | 1 |
| www.americaphonebook.com | phoneus | 1 |
| www.okcaller.com | phoneus | 1 |
| www.whoseno.com | phoneus | 1 |
| e-justice.europa.eu | publiccompanyrecords | 1 |
| find-and-update.company-information.service.gov.uk | publiccompanyrecords | 1 |
| littlesis.org | publiccompanyrecords | 2 |
| opencorporates.al | publiccompanyrecords | 1 |
| trellis.law | publiccompanyrecords | 2 |
| www.aihitdata.com | publiccompanyrecords | 4 |
| www.courtlistener.com | publiccompanyrecords | 2 |
| www.genealogybank.com | publiccompanyrecords | 1 |
| www.infobel.com | publiccompanyrecords | 2 |
| www.iosco.org | publiccompanyrecords | 2 |
| www.muckrock.com | publiccompanyrecords | 2 |
| www.opensecrets.org | publiccompanyrecords | 1 |
| ahmia.fi | searchengines | 1 |
| baidu.com | searchengines | 1 |
| baresearch.org | searchengines | 1 |
| duckduckgo.com | searchengines | 1 |
| patents.google.com | searchengines | 1 |
| scholar.google.com | searchengines | 1 |
| search.brave.com | searchengines | 1 |
| search.yahoo.com | searchengines | 1 |
| startpage.com | searchengines | 1 |
| www.qwant.com | searchengines | 1 |
| account.venmo.com | usernames | 1 |
| cse.google.com | usernames | 1 |
| en.gravatar.com | usernames | 1 |
| github.com | usernames | 1 |
| go.mail.ru | usernames | 2 |
| instantusername.com | usernames | 1 |
| krebsonsecurity.com | usernames | 1 |
| linktr.ee | usernames | 1 |
| medium.com | usernames | 1 |
| namevine.com | usernames | 1 |
| pastebin.com | usernames | 1 |
| remitano.com | usernames | 1 |
| steamcommunity.com | usernames | 1 |
| steamid.uk | usernames | 1 |
| usernamechecker.checkistan.com | usernames | 1 |
| usersearch.org | usernames | 1 |
| whatsmyname.app | usernames | 1 |
| www.namechecker.org | usernames | 1 |
| www.paypal.com | usernames | 1 |
| www.snapchat.com | usernames | 1 |
| xboxgamertag.com | usernames | 1 |
| {username}.tumblr.com | usernames | 1 |
| carnet.ai | vehicles | 1 |
| csps.con.rcmp-grc.gc.ca | vehicles | 1 |
| recordsfinder.com | vehicles | 2 |
| www.cyclevin.com | vehicles | 1 |
| i.ytimg.com | videos | 4 |
| image.baidu.com | videos | 1 |
| nsfwyoutube.com | videos | 1 |
| polsy.org.uk | videos | 1 |
| watannetwork.com | videos | 1 |
| www.youtube.com | videos | 4 |
| y2mate.is | videos | 1 |
| www.twitteraudit.com | x | 1 |

</details>

## ❔ Unverified (probe inconclusive — treat with caution)  (69 sources, 132 queries)

| Source | Category | #q | Detail |
| --- | --- | --- | --- |
| yandex.com | domains | 15 | N/A |
| community.riskiq.com | domains | 7 | Account likely (PassiveTotal/Microsoft) — manual |
| thatsthem.com | email | 6 | N/A |
| www.fastpeoplesearch.com | address | 4 | N/A |
| www.tineye.com | images | 4 | N/A |
| checko.ru | names | 3 | N/A |
| platform.arkhamintelligence.com | currencies | 3 | N/A |
| www.advancedbackgroundchecks.com | address | 3 | N/A |
| www.searchpeoplefree.com | address | 3 | N/A |
| www.truepeoplesearch.com | address | 3 | N/A |
| www.udrpsearch.com | domains | 3 | n/a (unreachable) |
| www.whitepages.com | address | 3 | N/A |
| ci-www.threatcrowd.org | domains | 2 | Unknown |
| memory.lol | x | 2 | Unknown |
| nigeria24.me | publiccompanyrecords | 2 | N/A |
| nuwber.com | names | 2 | N/A |
| psbdmp.ws | email | 2 | Unknown |
| resolve.rs | domains | 2 | Unknown |
| search.foia.gov | publiccompanyrecords | 2 | Unknown |
| search.uscourts.gov | publiccompanyrecords | 2 | Unknown |
| services.gisgraphy.com | address | 2 | Unknown |
| website.informer.com | domains | 2 | Unknown |
| www.crunchbase.com | names | 2 | N/A |
| www.judyrecords.com | publiccompanyrecords | 2 | Unknown |
| www.searchquarry.com | vehicles | 2 | Unknown |
| www.smat-app.com | usernames | 2 | Unknown |
| www.social-searcher.com | names | 2 | unknown (not probed) |
| www.spokeo.com | address | 2 | unknown (not probed) |
| www.yandex.com | linkedin | 2 | N/A |
| www.zaubacorp.com | names | 2 | N/A |
| check.cybernews.com | email | 1 | N/A |
| check.spamhaus.org | domains | 1 | N/A |
| core.ac.uk | docs | 1 | N/A |
| dnpedia.com | domains | 1 | N/A |
| elephind.com | domains | 1 | N/A |
| iknowwhatyoudownload.com | ip | 1 | N/A |
| mrkoll.se | names | 1 | N/A |
| namechk.com | usernames | 1 | N/A |
| ng-check.com | publiccompanyrecords | 1 | N/A |
| numpi.com | phoneus | 1 | N/A |
| openpayrolls.com | publiccompanyrecords | 1 | N/A |
| oxt.me | currencies | 1 | nav-error |
| phishcheck.me | domains | 1 | nav-error |
| phoneowner.com | phoneus | 1 | N/A |
| politicalmoneyline.com | publiccompanyrecords | 1 | nav-error |
| profilediscover.com | usernames | 1 | loaded-thin |
| search.cac.gov.ng | publiccompanyrecords | 1 | N/A |
| spyonweb.com | domains | 1 | nav-error |
| spytox.com | email | 1 | nav-blocked |
| timetravel.mementoweb.org | domains | 1 | nav-error |
| tinder.com | usernames | 1 | n/a (nav-blocked) |
| viz.greynoise.io | ip | 1 | N/A |
| voterrecords.com | publiccompanyrecords | 1 | N/A |
| www.carvana.com | vehicles | 1 | N/A |
| www.familytreenow.com | names | 1 | N/A |
| www.faxvin.com | vehicles | 1 | N/A |
| www.infobyip.com | ip | 1 | N/A |
| www.ip-lookup.org | ip | 1 | N/A |
| www.ipaddress.com | ip | 1 | N/A |
| www.iplocation.net | ip | 1 | N/A |
| www.merinfo.se | names | 1 | nav-blocked |
| www.peoplebyname.com | names | 1 | N/A |
| www.peoplefinders.com | address | 1 | nav-error |
| www.sitemapper.com | domains | 1 | nav-error |
| www.skymem.info | domains | 1 | N/A |
| www.spytox.com | phoneus | 1 | nav-error |
| www.usa-people-search.com | address | 1 | N/A |
| www.vindecoderz.com | vehicles | 1 | N/A |
| zapper.fi | currencies | 1 | N/A |

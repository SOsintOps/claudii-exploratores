#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Desk classification of the Exploratores catalog queries (Claudii-Exploratores)
by AUTHENTICATION requirements (dedicated Chrome profile) and VPN (country).

Method: desk analysis based on knowledge of each service, NOT live testing.
Every entry carries a confidence level (High/Medium/Low).
Four axes:
  - auth_access : login/registration TECHNICALLY needed to obtain the result
  - vpn_access  : country VPN / Tor technically needed or recommended for access
  - auth_opsec  : OPSEC recommendation on which identity/profile to use
  - vpn_opsec   : OPSEC recommendation on network attribution / exit
"""
import json, re, csv
from urllib.parse import urlparse
from collections import Counter

# Resolve catalog relative to this script so it works after the folder is moved.
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                      # Claudii-Exploratores/
SRC  = os.path.join(ROOT, "shared", "catalog.json")
OUT  = os.path.join(ROOT, "docs", "query_classification.csv")

def host_of(tpl):
    u2 = re.sub(r'\{[^}]*\}', 'X', tpl or '')
    try: h = urlparse(u2).netloc.lower()
    except Exception: h = ''
    return h.replace('www.', '')

LOGIN_PLATFORM = {
    'linkedin.com': ('LinkedIn','High'), 'facebook.com': ('Facebook','High'),
    'mbasic.facebook.com': ('Facebook','High'), 'instagram.com': ('Instagram','High'),
    'threads.net': ('Threads (Meta)','Medium'), 'vk.com': ('VK','High'), 'vk.me': ('VK','High'),
    'x.com': ('X / Twitter','High'), 'twitter.com': ('X / Twitter','High'),
    'tiktok.com': ('TikTok','Medium'), 'snapchat.com': ('Snapchat','Medium'),
    'tinder.com': ('Tinder','High'), 'kik.me': ('Kik','Medium'), 'mewe.com': ('MeWe','Medium'),
    'discord.com': ('Discord','High'), 'discord.gg': ('Discord','High'), 'discord.me': ('Discord','Medium'),
    't.me': ('Telegram (to join channels)','Medium'), 'go.mail.ru': ('VK / Mail.ru','Medium'),
}
SITE_ACCOUNT = {
    'shodan.io': ('Free registration for full search','Medium'), 'beta.shodan.io': ('Free registration','Medium'),
    'search.censys.io': ('Free registration','Medium'), 'dehashed.com': ('Paid account','High'),
    'intelx.io': ('Registration / account','Medium'), 'portal.spycloud.com': ('Account (enterprise)','High'),
    'portal.aql.com': ('Account','Medium'), 'hunter.io': ('Free registration for results','Medium'),
    'securitytrails.com': ('Free registration','Medium'), 'virustotal.com': ('Free registration for full features','Medium'),
    'maxmind.com': ('Account','Medium'), 'whoisology.com': ('Account / paywall','Medium'),
    'whoxy.com': ('Account / API for results','Medium'), 'domainiq.com': ('Account / paywall','Medium'),
    'research.domaintools.com': ('Account / paywall','Medium'), 'whois.domaintools.com': ('Account for details','Medium'),
    'reversewhois.domaintools.com': ('Account / paywall','Medium'), 'spyfu.com': ('Account / paywall','Medium'),
    'moz.com': ('Free registration','Medium'), 'similarweb.com': ('Registration for details','Medium'),
    'hybrid-analysis.com': ('Free registration','Medium'), 'joesandbox.com': ('Registration','Medium'),
    'tria.ge': ('Registration','Medium'), 'leakix.net': ('Account for some results','Medium'),
    'platform.arkhamintelligence.com': ('Free registration','Medium'), 'metasleuth.io': ('Free registration','Medium'),
    'breadcrumbs.app': ('Registration','Medium'), 'explorer.crystalblockchain.com': ('Account','Medium'),
    'viz.greynoise.io': ('Free registration','Medium'), 'facecheck.id': ('Registration / credits','Medium'),
    'scamsearch.io': ('Registration','Medium'), 'epieos.com': ('Free registration for full results','Medium'),
    'truecaller.com': ('Login / app required','Medium'), 'sync.me': ('Login / app','Medium'),
    'intelius.com': ('Paywall for reports','Medium'), 'crunchbase.com': ('Free registration for details','Medium'),
    'b2bhint.com': ('Registration for details','Medium'), 'aihitdata.com': ('Registration for details','Low'),
    'debank.com': ('Wallet login for features','Low'), 'zapper.fi': ('Wallet login for features','Low'),
}
LOW_SOFT_ACCOUNT = {
    'builtwith.com','urlscan.io','tineye.com','emailrep.io','psbdmp.ws','aleph.occrp.org',
    'social-searcher.com','phalcon.blocksec.com','check.cybernews.com','gmail-osint.activetk.jp',
}
GEO_HOST = {
    'eniro.se':'SE','hitta.se':'SE','merinfo.se':'SE','ratsit.se':'SE','mrkoll.se':'SE',
    'checko.ru':'RU','rusfinder.pro':'RU','mysmsbox.ru':'RU',
    'search.cac.gov.ng':'NG','ng-check.com':'NG','nigeria24.me':'NG','nigeriaphonebook.com':'NG',
    '9jabook.com':'NG','naijaplanet.com':'NG','canada411.ca':'CA','csps.con.rcmp-grc.gc.ca':'CA',
    'paginebianche.it':'IT','paginegialle.it':'IT','tellows.it':'IT','ukphonebook.com':'UK',
}
GEO_CONF = {'SE':'Medium','RU':'Medium','NG':'Low','CA':'Low','IT':'Low','UK':'Low','US':'Medium'}
GEO_LABEL = {'SE':'Sweden','RU':'Russia','NG':'Nigeria','CA':'Canada','IT':'Italy','UK':'United Kingdom','US':'United States'}
US_PEOPLE_HOSTS = {
    'whitepages.com','spokeo.com','radaris.com','truthfinder.com','nuwber.com','fastpeoplesearch.com',
    'truepeoplesearch.com','thatsthem.com','peoplefinders.com','familytreenow.com','advancedbackgroundchecks.com',
    'cyberbackgroundchecks.com','smartbackgroundchecks.com','searchpeoplefree.com','peoplesearchnow.com',
    'usphonebook.com','americaphonebook.com','usa-people-search.com','zabasearch.com','addresses.com','411.com',
    'whoseno.com','phoneowner.com','callersmart.com','okcaller.com','numpi.com','spytox.com','peoplebyname.com',
    'people.yellowpages.com','publicrecords.searchsystems.net','infotracer.com','recordsfinder.com','voterrecords.com',
    'openpayrolls.com','800notes.com','usa-official.com','searchquarry.com','checkthatvin.com','faxvin.com',
    'cyclevin.com','vincheck.info','vindecoderz.com','carvana.com','acrevalue.com','realtor.com','trulia.com',
    'zillow.com','idcrawl.com',
}
SEARCH_ENGINES = {
    'google.com','bing.com','duckduckgo.com','search.brave.com','startpage.com','qwant.com','search.yahoo.com',
    'yandex.com','yandex.ru','baidu.com','image.baidu.com','baresearch.org','cse.google.com','scholar.google.com',
    'patents.google.com','lens.google.com',
}

def classify(entry):
    tpl = entry.get('urlTemplate',''); host = host_of(tpl)
    cat = entry.get('category',''); sub = (entry.get('subcategory') or '')
    note=[]; cc=[]
    auth_access='No login'; auth_opsec='Dedicated research profile (non-attributable)'
    if host in LOGIN_PLATFORM:
        plat,c=LOGIN_PLATFORM[host]
        auth_access=f'Platform login: {plat} (to view content)'
        auth_opsec=f'Dedicated {plat} sock-puppet (never personal account)'; cc.append(c)
    elif host in SITE_ACCOUNT:
        desc,c=SITE_ACCOUNT[host]; auth_access=desc
        auth_opsec='Dedicated service account / non-personal API key'; cc.append(c)
    elif host in LOW_SOFT_ACCOUNT:
        auth_access='No (free; account only for volume/extras)'
        auth_opsec='Dedicated service account if registering'; cc.append('Low')
    is_onion=host.endswith('.onion')
    vpn_access='No (global access)'; vpn_opsec='Recommended (managed attribution)'
    if is_onion:
        vpn_access='Tor required (.onion, not on clearnet)'; vpn_opsec='Tor (no clearnet VPN)'; cc.append('High')
    else:
        country=None
        if host in GEO_HOST: country=GEO_HOST[host]
        elif host in US_PEOPLE_HOSTS or sub=='us' or cat=='phoneus': country='US'
        if country:
            lbl=GEO_LABEL[country]
            if country=='US': vpn_access=f'VPN {lbl} recommended (many sites limit/block EU IPs due to GDPR/CCPA)'
            elif country in ('SE','RU'): vpn_access=f'VPN {lbl} recommended (possible block/limit for foreign IPs)'
            else: vpn_access=f'Global access; {lbl} national data (VPN {lbl} only if blocked)'
            cc.append(GEO_CONF[country])
    if host in LOGIN_PLATFORM and not is_onion:
        vpn_opsec='Mandatory (direct visit to target profile, never real IP)'
    if host in SEARCH_ENGINES: note.append('search engine: no login; VPN/Tor may trigger captcha')
    if host in ('yandex.com','yandex.ru','baidu.com','image.baidu.com','go.mail.ru','checko.ru'):
        note.append('foreign service (RU/CN): consider isolated profile/exit')
    if is_onion: note.append('requires Tor Browser / OSINT VM with Tor')
    if cat=='currencies' and host not in SITE_ACCOUNT and host not in LOW_SOFT_ACCOUNT:
        note.append('public block explorer: no login')
    if host=='arquivo.pt': note.append('Portuguese web archive: global access, no login')
    order={'High':3,'Medium':2,'Low':1}
    conf=min(cc,key=lambda x:order[x]) if cc else 'High'
    return {'id':entry.get('id',''),'category':cat,'subcategory':sub,'label':entry.get('label',''),
            'host':host,'auth_access':auth_access,'vpn_access':vpn_access,'auth_opsec':auth_opsec,
            'vpn_opsec':vpn_opsec,'confidence':conf,'note':'; '.join(note)}

def main():
    cat=json.load(open(SRC,encoding='utf-8'))
    rows=[classify(e) for e in cat['entries']]
    cols=['id','category','subcategory','label','host','auth_access','vpn_access','auth_opsec','vpn_opsec','confidence','note']
    with open(OUT,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
    print('Rows:',len(rows),'-> CSV:',OUT)

if __name__=='__main__':
    main()

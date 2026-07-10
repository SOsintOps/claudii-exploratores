#!/usr/bin/env python3
"""build_verification_worklist.py — prepare the LIVE verification worklist.

Groups the 898 catalog queries by host (access behaviour is host-level, not
query-level), fills each representative query's placeholders with NEUTRAL test
values (no real PII), and joins the existing desk classification so the analyst
sees the predicted verdict next to each host to verify.

Output: a JSON worklist (one row per unique host) written to stdout or --out.
Consumed by the analyst during the live Chrome + VPN passes; raw results are
logged separately in the PRIVATE work repo (test-results/).
"""
import json
import csv
import sys
import argparse
from collections import defaultdict
from urllib.parse import urlparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Neutral, innocuous test values. Purpose is to exercise ACCESS (does the page
# load / login-wall / geo-block), NOT to query real targets. 555-prefix phones
# and reserved SSN/IBAN are deliberately non-real; BTC genesis address is public.
TEST_VALUES = {
    "{username}": "johnsmith", "{userid}": "123456", "{usera}": "johnsmith",
    "{userb}": "janesmith", "{realname}": "John Smith",
    "{domain}": "example.com", "{domain_nodots}": "example",
    "{url}": "https://example.com", "{favicon_url}": "https://example.com/favicon.ico",
    "{term}": "test", "{query}": "test", "{keyword}": "test",
    "{google_query}": "test", "{usa_address_query}": "1600 Amphitheatre Parkway",
    "{ip}": "8.8.8.8", "{start_ip}": "8.8.8.0", "{end_ip}": "8.8.8.255",
    "{fullname}": "John Smith", "{fullnamedash}": "john-smith",
    "{fullnamedashlower}": "john-smith", "{firstname}": "John", "{lastname}": "Smith",
    "{first}": "John", "{last}": "Smith", "{officername}": "John Smith",
    "{full}": "John Smith", "{full_dash}": "john-smith",
    "{email}": "test@example.com", "{localpart}": "test",
    "{companyname}": "Acme Corp", "{company}": "Acme Corp",
    "{lat}": "40.7128", "{lon}": "-74.0060", "{location}": "New York",
    "{state}": "NY", "{city}": "New York", "{street}": "Main Street",
    "{zip}": "10001", "{postalcode}": "10001", "{country}": "US",
    "{country_iso_lower}": "us", "{full_address}": "1600 Amphitheatre Parkway",
    "{videoid}": "aqz-KE-bpKQ", "{channelid}": "UC_x5XG1OV2P6uZZ5FSM9Ttw",
    "{btc_address}": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
    "{e164}": "+12025550123", "{nat_num}": "2025550123", "{phone}": "2025550123",
    "{number}": "2025550123", "{area}": "202", "{prefix}": "555", "{line}": "0123",
    "{dt_num_generic}": "2025550123", "{dt_enum_generic}": "2025550123",
    "{dt_num_only}": "2025550123", "{dt_0num_only}": "02025550123",
    "{dt_plus_cc_num}": "+12025550123", "{dt_plus_cc_0num}": "+102025550123",
    "{vin}": "1HGCM82633A004352", "{plate}": "ABC1234",
    "{iban}": "GB82WEST12345698765432", "{ssn}": "000-00-0000",
    "{md5_hash}": "d41d8cd98f00b204e9800998ecf8427e",
    "{shodan_hash}": "0", "{csp_string}": "default-src", "{ssid}": "linksys",
    "{hashtag}": "osint", "{tag}": "osint", "{amount}": "100",
    "{analyticsid}": "UA-000000-1", "{adsenseid}": "pub-0000000000000000",
    "{listid}": "123456", "{nat_num}": "2025550123",
    "{until}": "2024-12-31", "{since}": "2024-01-01",
    "{enddate}": "2024-12-31", "{startdate}": "2024-01-01",
    "{activity}": "running", "{searchQueryState}": "%7B%7D",
}


def fill(template, placeholders):
    url = template
    unresolved = []
    for p in placeholders:
        if p in TEST_VALUES:
            url = url.replace(p, TEST_VALUES[p])
        else:
            unresolved.append(p)
    # catch any placeholder not declared in the entry list
    for p, v in TEST_VALUES.items():
        url = url.replace(p, v)
    return url, unresolved


def load_desk(csv_path):
    """host -> representative desk verdict (mode of its rows)."""
    rows = defaultdict(list)
    with open(csv_path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows[r["host"]].append(r)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", default=str(ROOT / "shared/catalog.json"))
    ap.add_argument("--csv", default=str(ROOT / "docs/query_classification.csv"))
    ap.add_argument("--out", default="-")
    args = ap.parse_args()

    entries = json.load(open(args.catalog))["entries"]
    desk = load_desk(args.csv)

    by_host = defaultdict(list)
    for e in entries:
        h = urlparse(e["urlTemplate"]).netloc.lower()
        by_host[h].append(e)

    worklist = []
    for h in sorted(by_host):
        group = by_host[h]
        rep = group[0]
        test_url, unresolved = fill(rep["urlTemplate"], rep.get("placeholders", []))
        drows = desk.get(h, [])
        # desk prediction (take first row's axes as representative of the host)
        d = drows[0] if drows else {}
        worklist.append({
            "host": h,
            "query_count": len(group),
            "categories": sorted({e["category"] for e in group}),
            "representative_id": rep["id"],
            "representative_label": rep["label"],
            "test_url": test_url,
            "unresolved_placeholders": unresolved,
            "desk_auth_access": d.get("auth_access", ""),
            "desk_vpn_access": d.get("vpn_access", ""),
            "desk_confidence": d.get("confidence", ""),
            # to be filled during live passes:
            "live_auth_access": "",
            "live_vpn_access": "",
            "live_status": "",       # e.g. 200-ok / login-wall / geo-block / error
            "live_evidence": "",
            "verified": False,
        })

    out = {
        "meta": {
            "total_queries": len(entries),
            "unique_hosts": len(by_host),
            "onion_hosts": sum(1 for h in by_host if h.endswith(".onion")),
            "note": "Live-verification worklist. Neutral test values, host-level access behaviour.",
        },
        "hosts": worklist,
    }
    data = json.dumps(out, indent=2, ensure_ascii=False)
    if args.out == "-":
        print(data)
    else:
        Path(args.out).write_text(data, encoding="utf-8")
        print(f"Wrote {len(worklist)} hosts -> {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()

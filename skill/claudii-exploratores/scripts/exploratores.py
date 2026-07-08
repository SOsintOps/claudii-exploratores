#!/usr/bin/env python3
"""
exploratores.py — command-line entry point for the Exploratores OSINT skill.

Turns an investigation indicator (name, domain, email, IP, phone, username,
coordinates, IBAN, crypto address, ...) into a curated list of OSINT search URLs,
using the ported Exploratores catalog (898 tools). Also exposes the IBAN verifier
and the PII Redactor.

Everything runs offline: it only *builds* URLs — it never opens them. The analyst
(or a browser agent) decides which to open, applying OPSEC.

Examples
--------
  python exploratores.py classify "john.doe@example.com"
  python exploratores.py urls "exploratores.io"
  python exploratores.py urls "Mario Rossi" --type PERSON_NAME
  python exploratores.py urls "johndoe" --categories x,instagram,vk
  python exploratores.py urls "45.4642,9.1900" --format markdown
  python exploratores.py search "wayback"
  python exploratores.py iban "GB82 WEST 1234 5698 7654 32"
  python exploratores.py redact "Contact john@x.com from 8.8.8.8"
"""
import argparse
import json
import sys

import osint_core as core
import iban_tools
import redactor


def _print(obj, as_json=True):
    if as_json:
        print(json.dumps(obj, indent=2, ensure_ascii=False))
    else:
        print(obj)


def cmd_classify(a):
    _print(core.classify_indicator(a.value))


def cmd_urls(a):
    extra = {}
    for kv in (a.field or []):
        if "=" in kv:
            k, v = kv.split("=", 1)
            extra[k.strip()] = v.strip()
    cats = None
    if a.categories:
        cats = [] if a.categories.lower() == "all" else a.categories.split(",")
    res = core.render_urls(
        a.value,
        indicator_type=a.type,
        categories_filter=cats,
        extra=extra or None,
        include_onion=not a.no_onion,
        limit=a.limit,
    )
    if a.format == "json":
        _print(res)
    elif a.format == "urls":
        for r in res["results"]:
            print(r["url"])
    else:  # markdown
        print(f"# OSINT search set — `{res['value']}`  ({res['indicator_type']})")
        print(f"_{res['count']} tools · categories: {res['categories_used']}_\n")
        cur = None
        for r in res["results"]:
            if r["category"] != cur:
                cur = r["category"]
                print(f"\n## {cur}")
            print(f"- [{r['label']}]({r['url']})")


def cmd_search(a):
    _print(core.search_catalog(a.query, limit=a.limit))


def cmd_categories(a):
    _print(core.categories())


def cmd_iban(a):
    _print(iban_tools.verify_iban(a.value))


def cmd_redact(a):
    enabled = a.only.split(",") if a.only else None
    _print(redactor.redact(a.text, enabled=enabled))


def build_parser():
    p = argparse.ArgumentParser(prog="exploratores", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("classify", help="Detect the indicator type(s) of a value.")
    s.add_argument("value")
    s.set_defaults(func=cmd_classify)

    s = sub.add_parser("urls", help="Build a curated OSINT URL set for a value.")
    s.add_argument("value")
    s.add_argument("--type", help="Force an indicator type (e.g. PERSON_NAME, DOMAIN, COMPANY).")
    s.add_argument("--categories", help="Comma-separated category filter, or 'all'.")
    s.add_argument("--field", action="append",
                   help="Extra field key=value (repeatable): firstname=, lastname=, city=, "
                        "state=, street=, zip=, countrycode=, nationalnumber=, since=, until=, amount=.")
    s.add_argument("--limit", type=int, default=None)
    s.add_argument("--no-onion", action="store_true", help="Exclude .onion (Tor) results.")
    s.add_argument("--format", choices=["markdown", "json", "urls"], default="markdown")
    s.set_defaults(func=cmd_urls)

    s = sub.add_parser("search", help="Free-text search the tool catalog.")
    s.add_argument("query")
    s.add_argument("--limit", type=int, default=50)
    s.set_defaults(func=cmd_search)

    s = sub.add_parser("categories", help="List catalog categories and counts.")
    s.set_defaults(func=cmd_categories)

    s = sub.add_parser("iban", help="Validate an IBAN offline (ISO 13616 mod-97).")
    s.add_argument("value")
    s.set_defaults(func=cmd_iban)

    s = sub.add_parser("redact", help="Redact PII from text (reversible map).")
    s.add_argument("text")
    s.add_argument("--only", help="Comma-separated subset: EMAIL,IPV4,PHONE,IBAN,URL,...")
    s.set_defaults(func=cmd_redact)

    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())

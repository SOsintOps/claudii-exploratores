#!/usr/bin/env python3
"""Automated access check, one neutral request per catalog host.

Pass A (no VPN) checks every host from the current exit IP. Pass B rechecks only
the hosts that did not work in a previous pass (``--retry-from``), after the analyst
has switched the VPN to the candidate country (``--country`` filters the hosts
whose access map or desk classification points to that country).

Each host is requested once with neutral test values (see
``build_verification_worklist.TEST_VALUES``), slowly and in sequence, with a normal
browser User-Agent. CAPTCHAs and bot challenges are recorded, never solved. The
result is a plain HTTP view: a page that needs JavaScript or a login can still look
"ok" here, so a browser check remains the reference for anything ambiguous.

Usage::

    python scripts/check_links.py --out passA.json                      # all hosts
    python scripts/check_links.py --only-new old_catalog.json --out a.json
    python scripts/check_links.py --retry-from passA.json --country US --out passB-US.json
"""
from __future__ import annotations

import argparse
import json
import socket
import ssl
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_verification_worklist import TEST_VALUES  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "shared"))
import osint_core as core  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# Placeholders added after the 2026-07 verification.
TEST_VALUES.update({
    "{q}": "test", "{urn}": "urn:nir:stato:legge:1990-08-07;241", "{case}": "C-311/18",
    "{vat_country}": "IT", "{vat_number}": "00905811006", "{msgid}": "1",
    "{national_raw}": "0612345678", "{country_iso}": "US", "{searchQueryState}": "{}",
})

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")
CHALLENGE = ("cf-chl", "<title>just a moment", "attention required! | cloudflare",
             "verify you are human", "are you a robot", "ddos-guard", "captcha-delivery",
             "px-captcha", "_incapsula_resource")
GEO = ("not available in your country", "not available in your region", "unavailable in your country",
       "unavailable in your region", "access from your country", "your country is not",
       "outside the united states", "only available in the us", "not available outside")
LOGIN = ("log in to continue", "sign in to continue", "please log in", "login required",
         "you must be logged in")


def fill(template: str, placeholders) -> tuple:
    """Fill a template with neutral values, encoded exactly as the engine does."""
    fields = {k[1:-1]: v for k, v in TEST_VALUES.items()}
    unresolved = [p for p in placeholders if p[1:-1] not in fields]
    for p in unresolved:
        fields[p[1:-1]] = "test"
    return core.render_entry({"urlTemplate": template, "placeholders": placeholders}, fields), unresolved


def exit_ip() -> dict:
    try:
        with urllib.request.urlopen("https://ipinfo.io/json", timeout=10) as r:
            d = json.load(r)
        return {k: d.get(k) for k in ("ip", "country", "city", "org")}
    except Exception as exc:  # pragma: no cover - network
        return {"error": str(exc)}


def probe(url: str, timeout: float) -> dict:
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.9"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) as r:
            body = r.read(200_000).decode("utf-8", "replace").lower()
            code, final = r.status, r.geturl()
    except urllib.error.HTTPError as e:
        body = e.read(50_000).decode("utf-8", "replace").lower() if e.fp else ""
        code, final = e.code, url
    except urllib.error.URLError as e:
        reason = e.reason
        if isinstance(reason, socket.gaierror):
            return {"status": "dns-error", "detail": str(reason)}
        if isinstance(reason, (socket.timeout, TimeoutError)):
            return {"status": "timeout"}
        if isinstance(reason, ssl.SSLError):
            return {"status": "tls-error", "detail": str(reason)[:120]}
        return {"status": "connect-error", "detail": str(reason)[:120]}
    except (socket.timeout, TimeoutError):
        return {"status": "timeout"}
    except Exception as e:  # pragma: no cover - defensive
        return {"status": "error", "detail": f"{type(e).__name__}: {e}"[:120]}

    out = {"http": code, "final_host": urlparse(final).hostname, "ms": int((time.time() - t0) * 1000),
           "bytes": len(body)}
    if any(m in body for m in CHALLENGE):
        out["status"] = "bot-challenge"
    elif code == 451 or (code in (403, 401) and any(m in body for m in GEO)):
        out["status"] = "geo-block"
    elif any(m in body for m in GEO):
        out["status"] = "geo-block?"
    elif code in (403, 503) and "captcha" in body:
        out["status"] = "bot-challenge"
    elif code in (401,) or any(m in body for m in LOGIN):
        out["status"] = "login-wall"
    elif code == 429:
        out["status"] = "rate-limited"
    elif 200 <= code < 400:
        out["status"] = "ok"
    elif code == 404:
        out["status"] = "http-404"
    elif code == 403:
        out["status"] = "http-403"
    else:
        out["status"] = f"http-{code}"
    return out


OK = {"ok", "login-wall", "http-404"}  # host reachable; 404 = endpoint changed, not access


def hosts_for(entries, only_new=None):
    by_host = defaultdict(list)
    for e in entries:
        by_host[urlparse(e["urlTemplate"].replace("{", "").replace("}", "")).hostname or ""].append(e)
    if only_new:
        old = {e["id"] for e in json.loads(Path(only_new).read_text(encoding="utf-8"))["entries"]}
        by_host = {h: g for h, g in by_host.items() if any(e["id"] not in old for e in g)}
    return dict(sorted(by_host.items()))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--catalog", type=Path, default=ROOT / "shared" / "catalog.json")
    ap.add_argument("--only-new", help="old catalog.json: check only hosts with new entries")
    ap.add_argument("--retry-from", type=Path, help="previous result: recheck only failed hosts")
    ap.add_argument("--country", help="with --retry-from: only hosts tied to this country (US, RU, ...)")
    ap.add_argument("--delay", type=float, default=2.0, help="seconds between hosts")
    ap.add_argument("--timeout", type=float, default=20.0)
    args = ap.parse_args()

    entries = json.loads(args.catalog.read_text(encoding="utf-8"))["entries"]
    groups = hosts_for(entries, args.only_new)
    groups = {h: g for h, g in groups.items() if h and not h.endswith(".onion")}

    if args.retry_from:
        prev = json.loads(args.retry_from.read_text(encoding="utf-8"))["hosts"]
        failed = {h for h, r in prev.items() if r["status"] not in OK}
        groups = {h: g for h, g in groups.items() if h in failed}
        if args.country:
            cc = args.country.upper()
            groups = {h: g for h, g in groups.items()
                      if (core.access_for(g[0]["urlTemplate"]) or {}).get("country") == cc}

    ip = exit_ip()
    print(f"Exit: {ip}. Checking {len(groups)} hosts, {args.delay}s apart.", file=sys.stderr)
    results = {}
    for i, (host, group) in enumerate(groups.items(), 1):
        rep = group[0]
        url, unresolved = fill(rep["urlTemplate"], rep.get("placeholders", []))
        res = probe(url, args.timeout)
        res.update({"queries": len(group), "representative_id": rep["id"], "test_url": url})
        if unresolved:
            res["unresolved"] = unresolved
        results[host] = res
        print(f"[{i}/{len(groups)}] {res['status']:<14} {host}", file=sys.stderr)
        args.out.write_text(json.dumps({"meta": {"exit": ip}, "hosts": results}, indent=2), encoding="utf-8")
        time.sleep(args.delay)

    summary = defaultdict(int)
    for r in results.values():
        summary[r["status"]] += 1
    meta = {"exit": ip, "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "hosts": len(results), "summary": dict(sorted(summary.items()))}
    args.out.write_text(json.dumps({"meta": meta, "hosts": results}, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

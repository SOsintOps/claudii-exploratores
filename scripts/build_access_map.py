#!/usr/bin/env python3
"""Build ``shared/access.json``: per-host access requirements used by the engine.

For every host behind a catalog query it records whether a VPN exit in a given
country (or Tor) is needed, whether an account is needed, and where the verdict
comes from. The engine attaches this to each generated URL and raises a warning
for geo-locked links, so the analyst knows *before* opening a link that it needs
an exit IP in a specific country.

Sources, strongest first:
1. ``docs/access-requirements-guide.md`` -- live verification (browser probes from
   an Italian IP, then a VPN exit in the candidate country for the hosts that did
   not work). Verdict ``live``.
2. ``docs/query_classification.csv`` -- desk classification by
   ``scripts/classify_queries.py``. Verdict ``desk``.

Usage::

    python scripts/build_access_map.py
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUIDE = ROOT / "docs" / "access-requirements-guide.md"
CSV = ROOT / "docs" / "query_classification.csv"
OUT = ROOT / "shared" / "access.json"

COUNTRIES = {
    "united states": "US", "russia": "RU", "sweden": "SE", "nigeria": "NG",
    "italy": "IT", "canada": "CA", "united kingdom": "GB", "us": "US", "ru": "RU",
    "se": "SE", "ng": "NG", "it": "IT", "ca": "CA", "uk": "GB", "gb": "GB",
}


def norm_host(host: str) -> str:
    host = host.strip().lower()
    return host[4:] if host.startswith("www.") else host


def _guide_sections() -> dict[str, dict]:
    """Parse the live guide: section heading -> host rows."""
    live: dict[str, dict] = {}
    if not GUIDE.exists():
        return live
    section = sub = ""
    for line in GUIDE.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section, sub = line.lower(), ""
            continue
        if line.startswith("### "):
            sub = line[4:].split("(")[0].strip().lower()
            continue
        if not line.startswith("| ") or line.startswith("| ---") or line.startswith("| Source"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3 or "." not in cells[0]:
            continue
        host = norm_host(cells[0])
        detail = cells[-1] if cells[-1] not in ("", "N/A") else None
        rec = live.setdefault(host, {})
        if "vpn required" in section:
            rec.update(vpn="required", country=COUNTRIES.get(sub, sub.upper()), vpn_detail=detail)
        elif "tor required" in section:
            rec.update(vpn="tor")
        elif "bot-protection" in section:
            rec.update(bot_protection=True)
        elif "account required" in section:
            rec.update(account="required", account_detail=detail)
        elif "account recommended" in section:
            rec.update(account="recommended", account_detail=detail)
        elif "unverified" in section:
            rec.setdefault("unverified", True)
    return live


def _desk(row: dict) -> dict:
    vpn = row["vpn_access"]
    rec: dict = {}
    m = re.match(r"VPN (.+?) recommended", vpn)
    if vpn.startswith("Tor required"):
        rec.update(vpn="tor")
    elif m:
        rec.update(vpn="recommended", country=COUNTRIES.get(m.group(1).lower()), vpn_detail=vpn)
    auth = row["auth_access"]
    if auth.startswith(("Account", "Paid", "Platform login")):
        rec.update(account="required", account_detail=auth)
    elif "optional" in auth.lower():
        rec.update(account="recommended", account_detail=auth)
    return rec


def build() -> dict:
    live = _guide_sections()
    hosts: dict[str, dict] = {}
    for row in csv.DictReader(CSV.open(encoding="utf-8")):
        host = norm_host(row["host"])
        if not host or host in hosts:
            continue
        rec = _desk(row)
        rec["source"] = "desk"
        lv = live.get(host)
        if lv and not lv.get("unverified"):
            # Live verdict wins on every axis it covers.
            for axis in ("vpn", "account"):
                if axis not in lv:
                    rec.pop(axis, None)
                    rec.pop(f"{axis}_detail", None)
                    if axis == "vpn":
                        rec.pop("country", None)
            rec.update({k: v for k, v in lv.items() if v is not None})
            rec["source"] = "live"
        hosts[host] = {k: rec[k] for k in sorted(rec)}

    flagged = {h: r for h, r in sorted(hosts.items())
               if r.get("vpn") or r.get("account") or r.get("bot_protection")}
    return {
        "meta": {
            "description": "Per-host access requirements (VPN country, Tor, account). "
                           "'live' = verified in a browser; 'desk' = desk classification.",
            "hosts_total": len(hosts),
            "hosts_flagged": len(flagged),
            "geo_locked": sorted(h for h, r in flagged.items() if r.get("vpn") == "required"),
        },
        "hosts": flagged,
    }


def main() -> None:
    data = build()
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    m = data["meta"]
    print(f"Wrote {OUT}: {m['hosts_flagged']} of {m['hosts_total']} hosts flagged, "
          f"{len(m['geo_locked'])} geo-locked (VPN required).")


if __name__ == "__main__":
    main()

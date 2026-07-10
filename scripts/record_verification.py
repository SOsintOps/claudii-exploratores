#!/usr/bin/env python3
"""record_verification.py — merge live-probe results into the worklist.

Reads a JSON array of result records from stdin (or --in) and updates the
matching host rows in the verification worklist in place. Each record:

  {"host": "...", "live_status": "...", "live_auth_access": "...",
   "live_vpn_access": "...", "live_evidence": "...", "verified": true}

Only the provided fields are overwritten; unknown hosts are reported.
"""
import json
import sys
import argparse
from pathlib import Path

FIELDS = ("live_status", "live_auth_access", "live_vpn_access",
          "live_evidence", "verified", "pass_name")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--worklist", required=True)
    ap.add_argument("--in", dest="infile", default="-")
    args = ap.parse_args()

    data = sys.stdin.read() if args.infile == "-" else Path(args.infile).read_text()
    records = json.loads(data)

    wl = json.loads(Path(args.worklist).read_text())
    index = {h["host"]: h for h in wl["hosts"]}

    updated, unknown = 0, []
    for rec in records:
        h = rec.get("host")
        if h not in index:
            unknown.append(h)
            continue
        row = index[h]
        for f in FIELDS:
            if f in rec:
                row[f] = rec[f]
        updated += 1

    Path(args.worklist).write_text(json.dumps(wl, indent=2, ensure_ascii=False))
    done = sum(1 for h in wl["hosts"] if h.get("verified"))
    print(f"Updated {updated} host(s). Verified so far: {done}/{len(wl['hosts'])}.",
          file=sys.stderr)
    if unknown:
        print(f"Unknown hosts (skipped): {unknown}", file=sys.stderr)


if __name__ == "__main__":
    main()

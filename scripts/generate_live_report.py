#!/usr/bin/env python3
"""generate_live_report.py — render the LIVE verification worklist as Markdown.

Reads the verification worklist JSON (raw live-probe results, host-level) and
produces a human-readable Markdown page: methodology, headline coverage, and
per-host tables grouped by outcome (verified access, auth-gated, geo/VPN
candidates, blocked/inconclusive). Intended for the private work repo while the
pass is in progress; the verified subset later folds into the public catalog.
"""
import json
import argparse
from collections import Counter
from pathlib import Path


def esc(s):
    return (s or "").replace("|", "\\|").replace("\n", " ")


def table(rows, headers):
    out = ["| " + " | ".join(headers) + " |",
           "| " + " | ".join("---" for _ in headers) + " |"]
    for r in rows:
        out.append("| " + " | ".join(esc(str(c)) for c in r) + " |")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--worklist", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--date", default="")
    args = ap.parse_args()

    wl = json.loads(Path(args.worklist).read_text())
    hosts = wl["hosts"]
    meta = wl["meta"]

    probed = [h for h in hosts if h.get("live_status")]
    verified = [h for h in probed if h.get("verified")]
    q_total = sum(h["query_count"] for h in hosts)
    q_probed = sum(h["query_count"] for h in probed)
    q_verified = sum(h["query_count"] for h in verified)

    # buckets by live status / access
    def bucket(h):
        s = (h.get("live_status") or "").lower()
        a = (h.get("live_auth_access") or "").lower()
        v = (h.get("live_vpn_access") or "").lower()
        if any(k in s for k in ("blocked", "403", "429", "captcha", "challenge",
                                "cf-", "js-denied", "ratelimit")):
            if "candidate" in v or "us-" in v or ("vpn" in v and "none" not in v):
                return "geo"
            return "blocked"
        if "candidate" in v or ("vpn" in v and "none" not in v):
            return "geo"
        anon = "no login" in a or "login optional" in a
        gated = (not anon) and any(k in a for k in (
            "profile", "account", "paid", "registration", "requires",
            "platform login", "login required"))
        return "auth" if gated else "open"

    buckets = {"open": [], "auth": [], "geo": [], "blocked": []}
    for h in probed:
        buckets[bucket(h)].append(h)

    status_counts = Counter(h.get("live_status") for h in probed)

    L = []
    L.append("# Live access verification — auth / profile / VPN\n")
    if args.date:
        L.append(f"> Live-verification pass. Last updated: {args.date}. "
                 "Method: authenticated Chrome automation + probe, neutral test inputs.\n")
    L.append("> **Status: IN PROGRESS.** Host-level results. Access behaviour is "
             "determined per host (all queries on a host share the same access "
             "gate), then propagated to the queries on that host.\n")

    L.append("\n## Method\n")
    L.append("- **Driver:** Claude-for-Chrome automation over the analyst's real "
             "Chrome profile (sessions for Facebook, Instagram, X, LinkedIn, VK "
             "carried into the automation tab).")
    L.append("- **Probe:** each host's representative query is opened with neutral "
             "test values (e.g. `example.com`, `John Smith`, `8.8.8.8`); the page "
             "is inspected for content, login-walls, CAPTCHAs and geo/HTTP blocks.")
    L.append("- **Baseline exit:** analyst home IP (Italy). Hosts that block or "
             "challenge from the home IP are flagged as VPN candidates for a "
             "country-specific retry pass.")
    L.append("- **Not solved:** CAPTCHAs and bot-challenges are recorded, never "
             "bypassed (policy).")
    L.append("- **Axes:** (1) *auth* — works anonymously vs needs a logged-in "
             "profile / account / paid plan; (2) *vpn* — works from any exit vs "
             "needs a specific country / Tor.\n")

    L.append("\n## Coverage\n")
    L.append(table([
        ["Unique hosts", meta["unique_hosts"]],
        ["Hosts probed", f"{len(probed)} ({len(probed)*100//meta['unique_hosts']}%)"],
        ["Hosts verified", len(verified)],
        ["Queries represented by probed hosts", f"{q_probed} / {q_total} ({q_probed*100//q_total}%)"],
        ["Queries represented by verified hosts", f"{q_verified} / {q_total} ({q_verified*100//q_total}%)"],
    ], ["Metric", "Value"]))

    titles = {
        "open": "### ✅ Open — works without login, any exit",
        "auth": "### 🔑 Auth-gated — needs a logged-in profile / account / paid plan",
        "geo": "### 🌍 Geo / VPN candidates — blocked or challenged from home IP",
        "blocked": "### ⛔ Blocked / inconclusive — CAPTCHA, rate-limit, or unprobeable",
    }
    for key in ("open", "auth", "geo", "blocked"):
        rows = sorted(buckets[key], key=lambda h: -h["query_count"])
        if not rows:
            continue
        L.append(f"\n{titles[key]}  ({len(rows)} hosts, "
                 f"{sum(h['query_count'] for h in rows)} queries)\n")
        L.append(table(
            [[h["host"], h["query_count"], h.get("live_auth_access", ""),
              h.get("live_vpn_access", ""), h.get("live_status", ""),
              "✓" if h.get("verified") else "—", h.get("live_evidence", "")]
             for h in rows],
            ["Host", "#q", "Auth", "VPN", "Status", "Verified", "Evidence"]))

    L.append("\n## Status legend\n")
    L.append(table([[k, v] for k, v in sorted(status_counts.items())],
                   ["live_status", "count"]))

    Path(args.out).write_text("\n".join(L) + "\n")
    print(f"Wrote report -> {args.out} ({len(probed)} probed, {len(verified)} verified)")


if __name__ == "__main__":
    main()

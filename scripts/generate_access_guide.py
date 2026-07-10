#!/usr/bin/env python3
"""generate_access_guide.py — user-facing access-requirements guide.

Turns the live-verification worklist into a clean public page that tells an
Exploratores user, per source, whether a query needs a login/account (required
vs recommended), a VPN (required + which country, or recommended), or Tor.

Honest by design:
- Access behaviour is host-level; the query counts show how many catalog
  queries each source backs.
- "Bot-protection" verdicts come from AUTOMATED probing. A normal human browser
  usually passes a Cloudflare / CAPTCHA interstitial, so those are surfaced as a
  caveat ("may work in a normal browser"), NOT as a hard requirement.
- A small, documented OVERRIDES table fixes a handful of well-known sources whose
  automated probe was inconclusive (e.g. opencorporates account-recommended).
"""
import json
import argparse
from collections import defaultdict, Counter
from pathlib import Path

# --- curated overrides: host -> (account_tier, vpn_tier, note) --------------
# Used only where automated probing was inconclusive but the real requirement is
# well established. Kept small and explicit for auditability.
OVERRIDES = {
    "opencorporates.com": ("recommended", "none",
        "Public search works; a free account raises rate limits and unlocks full record history."),
    "www.virustotal.com": ("recommended", "none",
        "Basic lookups are public; a free account is needed for the full GUI and history."),
    "www.shodan.io": ("required", "none",
        "A (free) account is required to run searches; results are global."),
    "scholar.google.com": ("none", "none",
        "Public; heavy automated use triggers a CAPTCHA, but normal browsing is fine."),
    "whois.domaintools.com": ("recommended", "none",
        "Basic WHOIS is public; historical/reverse data needs a paid account."),
    "opencorporates.al": ("none", "none", "Public company register."),
}

ACCOUNT_LABEL = {
    "none": "Not needed",
    "recommended": "Recommended",
    "required": "Required",
    "unknown": "Unverified",
}
VPN_LABEL = {
    "none": "Not needed",
    "recommended": "Sometimes helps",
    "required": "Required",
    "tor": "Tor required",
    "unknown": "Unverified",
}


def account_tier(h):
    a = (h.get("live_auth_access") or "").lower()
    s = (h.get("live_status") or "").lower()
    if not a or a in ("n/a", "unknown", "unknown (not probed)"):
        return "unknown"
    if "no login" in a or a.startswith("free (login optional") or "login optional" in a:
        # some "no login ... for full/extras" cases are really 'recommended'
        if any(k in a for k in ("for full", "for extras", "to interact", "to join",
                                "to chat", "for some", "registration for", "login to")):
            return "recommended"
        return "none"
    if any(k in a for k in ("paid", "required", "requires logged-in profile",
                            "registration required", "api key", "platform login")):
        return "required"
    if any(k in a for k in ("for full", "preview no-login", "partial no-login",
                            "for some collections", "recommend", "for extra")):
        return "recommended"
    if s in ("login-wall", "redirect-login", "login-paywall", "200-ok-authed"):
        return "required"
    if a.startswith("account likely") or "manual" in a:
        return "unknown"
    return "unknown"


def vpn_tier(h):
    v = (h.get("live_vpn_access") or "").lower()
    s = (h.get("live_status") or "").lower()
    if h["host"].endswith(".onion"):
        return "tor", None
    if "required" in v or v.startswith("loads from us"):
        # extract country
        for c, name in (("us", "US"), ("united states", "US"), ("sweden", "Sweden"),
                        ("russia", "Russia"), ("nigeria", "Nigeria"), ("canada", "Canada"),
                        ("uk", "UK")):
            if c in v:
                return "required", name
        return "required", None
    if "anti-bot" in v or s in ("cf-challenge", "captcha-blocked", "403-blocked"):
        return "recommended", None  # bot-protection: may help, not guaranteed
    if v.startswith("none") or v == "":
        return "none", None
    return "unknown", None


def primary_category(h):
    cats = h.get("categories") or []
    return cats[0] if cats else "-"


def esc(s):
    return (s or "").replace("|", "\\|").replace("\n", " ")


def row(cells):
    return "| " + " | ".join(esc(str(c)) for c in cells) + " |"


def table(rows, headers):
    out = [row(headers), "| " + " | ".join("---" for _ in headers) + " |"]
    out += [row(r) for r in rows]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--worklist", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--date", default="")
    args = ap.parse_args()

    wl = json.loads(Path(args.worklist).read_text())
    hosts = [h for h in wl["hosts"] if h["host"]]  # drop the empty edge host

    recs = []
    for h in hosts:
        at = account_tier(h)
        vt, country = vpn_tier(h)
        note = ""
        if h["host"] in OVERRIDES:
            at, vt, note = OVERRIDES[h["host"]]
            country = "US" if vt == "required" else country
        recs.append({
            "host": h["host"], "cat": primary_category(h), "n": h["query_count"],
            "account": at, "vpn": vt, "country": country,
            "note": note, "status": h.get("live_status", ""),
            "auth_raw": h.get("live_auth_access", ""),
        })

    q_total = sum(r["n"] for r in recs)

    L = []
    L.append("# Access requirements — do I need an account, a VPN, or Tor?\n")
    if args.date:
        L.append(f"> Companion guide to the Exploratores query catalog. Last updated: {args.date}.\n")
    L.append(
        "This guide tells you, for each source behind the catalog's queries, whether "
        "you need to **log in**, whether a **VPN** (and which country) helps or is "
        "required, and which sources are **Tor-only**. Requirements are per *source* "
        "(host); the **#q** column is how many catalog queries use that source.\n")

    L.append("\n## How to read this\n")
    L.append(table([
        ["🔓 **Account — Not needed**", "Works anonymously."],
        ["👤 **Account — Recommended**", "Usable without an account, but logging in unlocks more results / higher limits (e.g. OpenCorporates)."],
        ["🔑 **Account — Required**", "No useful results without logging in — a normal account, a platform profile (a research *sock-puppet* for social networks), or a paid plan."],
        ["🌍 **VPN — Required (country)**", "The source only serves specific IP ranges; from elsewhere you need a VPN exit in that country."],
        ["🧭 **VPN — Sometimes helps**", "Bot-protection (Cloudflare / CAPTCHA) was seen during automated testing. A normal browser usually passes; if you are blocked, a different exit can help."],
        ["🧅 **Tor — Required**", "An .onion service; reachable only over Tor."],
    ], ["Tier", "Meaning"]))

    L.append("\n> **Method & honesty.** Verdicts come from live probing of each source "
             "with neutral test inputs, from an EU IP and (for the geo checks) a US VPN "
             "exit. *Bot-protection* verdicts reflect **automated** access — a human in a "
             "regular browser is usually not blocked, so treat those as “may need a "
             "different exit”, not a hard requirement. Independently verify anything you "
             "rely on.\n")

    # ---- counts ----
    ac = Counter(r["account"] for r in recs)
    vc = Counter(r["vpn"] for r in recs)
    L.append("\n## At a glance\n")
    L.append(table([
        ["Account required", ac["required"], sum(r["n"] for r in recs if r["account"] == "required")],
        ["Account recommended", ac["recommended"], sum(r["n"] for r in recs if r["account"] == "recommended")],
        ["Account not needed", ac["none"], sum(r["n"] for r in recs if r["account"] == "none")],
        ["VPN required (a country)", vc["required"], sum(r["n"] for r in recs if r["vpn"] == "required")],
        ["Tor required (.onion)", vc["tor"], sum(r["n"] for r in recs if r["vpn"] == "tor")],
        ["Bot-protection seen (VPN may help)", vc["recommended"], sum(r["n"] for r in recs if r["vpn"] == "recommended")],
        ["Unverified", ac["unknown"], sum(r["n"] for r in recs if r["account"] == "unknown")],
    ], ["Category", "Sources", "Queries"]))

    def sect(title, pred, cols=("host", "cat", "n", "detail")):
        rows = sorted([r for r in recs if pred(r)], key=lambda r: (-r["n"], r["host"]))
        if not rows:
            return
        L.append(f"\n## {title}  ({len(rows)} sources, {sum(r['n'] for r in rows)} queries)\n")
        trows = []
        for r in rows:
            detail = r["note"] or r["auth_raw"] or r["status"]
            trows.append([r["host"], r["cat"], r["n"], detail])
        L.append(table(trows, ["Source", "Category", "#q", "Detail"]))

    L.append("\n---")
    sect("🔑 Account required", lambda r: r["account"] == "required")
    sect("👤 Account recommended (works without, better with)",
         lambda r: r["account"] == "recommended")

    # VPN required, grouped by country
    vreq = [r for r in recs if r["vpn"] == "required"]
    if vreq:
        bycc = defaultdict(list)
        for r in vreq:
            bycc[r["country"] or "?"].append(r)
        L.append(f"\n## 🌍 VPN required — by country  ({len(vreq)} sources, "
                 f"{sum(r['n'] for r in vreq)} queries)\n")
        def vpn_detail(r):
            if r["note"]:
                return r["note"]
            s = r["status"]
            cc = r["country"] or "the target"
            if s == "login-wall":
                return f"Loads via a {cc} exit, then requires an account."
            if s == "200-ok-us" or s.startswith("200-ok"):
                return f"Restricted to {cc} IP ranges; loads normally through a {cc} exit."
            return f"Reachable only through a {cc} exit."
        for cc in sorted(bycc, key=lambda c: -sum(x["n"] for x in bycc[c])):
            rows = sorted(bycc[cc], key=lambda r: -r["n"])
            L.append(f"\n### {cc}  ({len(rows)} sources)\n")
            L.append(table([[r["host"], r["cat"], r["n"], vpn_detail(r)]
                            for r in rows], ["Source", "Category", "#q", "Detail"]))

    sect("🧅 Tor required (.onion)", lambda r: r["vpn"] == "tor")
    sect("🧭 Bot-protection seen during testing (a VPN/other exit may help)",
         lambda r: r["vpn"] == "recommended" and r["account"] != "required")

    # Open sources: summarise by category (large list)
    openr = [r for r in recs if r["account"] == "none" and r["vpn"] in ("none", "recommended")]
    if openr:
        bycat = Counter(r["cat"] for r in openr)
        L.append(f"\n## ✅ No account, no VPN — works as-is  ({len(openr)} sources, "
                 f"{sum(r['n'] for r in openr)} queries)\n")
        L.append("Distribution by catalog category:\n")
        L.append(table([[c, n] for c, n in bycat.most_common()], ["Category", "Sources"]))
        L.append("\n<details><summary>Full list of open sources</summary>\n")
        L.append(table([[r["host"], r["cat"], r["n"]] for r in
                        sorted(openr, key=lambda r: (r["cat"], r["host"]))],
                       ["Source", "Category", "#q"]))
        L.append("\n</details>")

    # Unverified
    sect("❔ Unverified (probe inconclusive — treat with caution)",
         lambda r: r["account"] == "unknown" and r["vpn"] not in ("required", "tor"))

    Path(args.out).write_text("\n".join(L) + "\n")
    print(f"Wrote guide -> {args.out}: {len(recs)} sources, {q_total} queries")
    print("account:", dict(ac), "| vpn:", dict(vc))


if __name__ == "__main__":
    main()

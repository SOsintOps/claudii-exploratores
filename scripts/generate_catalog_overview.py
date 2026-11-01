#!/usr/bin/env python3
"""Render skill/claudii-exploratores/references/catalog_overview.md from catalog.json."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "shared" / "catalog.json"
OUT = ROOT / "skill" / "claudii-exploratores" / "references" / "catalog_overview.md"

DESCRIPTIONS = {
    "domains": "Domain intelligence: WHOIS/history, DNS, tech profiling, screenshots, archives, subdomains.",
    "usernames": "Pivot a username/handle across dozens of platforms and enumeration services.",
    "names": "Search a person by full name across people-search, directories and social platforms.",
    "ip": "IP-address intelligence: geolocation, reputation, ports/services, WiFi (WiGLE), ranges.",
    "publiccompanyrecords": "Corporate registries and officer/company records across jurisdictions.",
    "currencies": "Cryptocurrency address analysis and blockchain explorers (BTC/ETH/XMR).",
    "facebook": "Facebook-specific search by name, username or numeric ID.",
    "phoneint": "International phone number lookups (E.164 variants, reverse WHOIS, messaging apps).",
    "videos": "Video platform search and analysis (YouTube, Vimeo, TikTok, etc.).",
    "communities": "Forums and community platforms (Reddit, Discord, Hacker News, 4chan, etc.).",
    "maps": "Geolocation and mapping tools by coordinates/address.",
    "x": "X/Twitter search by handle, ID, list, real name, date range.",
    "docs": "Document and file search (leaks, pastes, code, scribd-style repositories).",
    "vk": "VKontakte search by username, ID, tag.",
    "searchengines": "General clear-web and Tor search engines (Google dorks, Yandex, Bing, DuckDuckGo, Wayback, Ahmia, .onion engines).",
    "phoneus": "US phone number lookups (reverse phone, carrier, people search).",
    "email": "Investigate an email address: breach/exposure lookups, reverse email, validators.",
    "address": "Physical-address lookups (US and international property/people directories).",
    "instagram": "Instagram-specific search by username, user ID, hashtag.",
    "images": "Reverse image search and image analysis.",
    "vehicles": "Vehicle intelligence by VIN or licence plate.",
    "linkedin": "LinkedIn people/company/content search.",
    "keybase": "Keybase identity lookups.",
    "iban": "IBAN-related lookups and validation.",
    "legal": "Italian and European Union legal sources: legislation (Normattiva URN), case law, regulators, registers, trade marks, VAT check (VIES).",
    "telegram": "Telegram channels, groups, users and messages: previews, in-channel search, message history, search engines and archives."
}


def main() -> None:
    cat = json.loads(CATALOG.read_text(encoding="utf-8"))
    meta, entries = cat["meta"], cat["entries"]
    counts = sorted(meta["categories"].items(), key=lambda kv: (-kv[1], kv[0]))
    lines = [
        "# Catalog Overview",
        "",
        f"The catalog holds **{meta['total']} OSINT tools** across **{len(counts)} categories** "
        f"(source: {meta['source']}). Each entry is a URL template filled from the classified "
        "indicator and URL-encoded, exactly as the original toolkit does.",
        "",
        "Use `python scripts/exploratores.py categories` for live counts and "
        "`... search \"<keyword>\"` to find a specific tool. Access requirements per source "
        "(VPN country, Tor, account) are in `scripts/access.json` and appear as warnings in "
        "the `urls` output.",
        "",
        "| Category | Tools | What it covers |",
        "|---|---|---|",
    ]
    for c, n in counts:
        lines.append(f"| `{c}` | {n} | {DESCRIPTIONS.get(c, '')} |")
    lines += ["", "## Example: sample tools per category (first 5)", ""]
    for c, n in counts:
        lines.append(f"### `{c}` ({n})")
        for e in [e for e in entries if e["category"] == c][:5]:
            lines.append(f"- **{e['label']}** — `{e['id']}`")
        lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Regenerate ``shared/catalog.json`` from a local checkout of Exploratores.

Exploratores publishes its catalogue as ``assets/data/search-library.json`` with a
companion ``catalogue-meta.json`` (version, entry count, SHA-256). This script reads
that export -- no JavaScript is evaluated -- checks the hash, and enriches every
entry with the button label shown on the toolkit pages (``pages/*.html``), falling
back to the label in ``assets/js/janua-search-map.js``.

Disabled entries (``"disabled": true`` upstream, confirmed-dead hosts) are skipped.

The output is deterministic: running it twice on the same upstream commit gives a
byte-identical file, so the weekly sync workflow only opens a pull request when
upstream has really changed.

Usage::

    python scripts/sync_catalog.py /path/to/Exploratores [--out shared/catalog.json]
    python scripts/sync_catalog.py /path/to/Exploratores --check   # exit 1 if out of date
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "shared" / "catalog.json"
UPSTREAM_URL = "https://github.com/SOsintOps/Exploratores"

_PLACEHOLDER = re.compile(r"\{([a-zA-Z0-9_]+)\}")
_HTML_LABEL = re.compile(r'data-search-id="([^"]+)"[^>]*>([^<]*)<')
_JANUA_LABEL = re.compile(r'"([a-z0-9-]+)"\s*:\s*\{\s*"label"\s*:\s*"([^"]*)"')


def _html_labels(pages: Path) -> dict[str, str]:
    labels: dict[str, str] = {}
    for page in sorted(pages.glob("*.html")):
        for sid, text in _HTML_LABEL.findall(page.read_text(encoding="utf-8")):
            text = re.sub(r"\s+", " ", html.unescape(text)).strip()
            if text and sid not in labels:
                labels[sid] = text
    return labels


def _janua_labels(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    return dict(_JANUA_LABEL.findall(path.read_text(encoding="utf-8")))


def build(src: Path) -> dict:
    data_dir = src / "assets" / "data"
    raw = (data_dir / "search-library.json").read_bytes()
    meta = json.loads((data_dir / "catalogue-meta.json").read_text(encoding="utf-8"))

    digest = hashlib.sha256(raw).hexdigest()
    if meta.get("sha256") and meta["sha256"] != digest:
        sys.exit(f"search-library.json SHA-256 {digest} does not match catalogue-meta.json "
                 f"({meta['sha256']}); run the upstream build-meta script first.")

    library = json.loads(raw)
    html_labels = _html_labels(src / "pages")
    janua_labels = _janua_labels(src / "assets" / "js" / "janua-search-map.js")

    entries, categories, skipped = [], {}, 0
    for sid in sorted(library):
        cfg = library[sid]
        if not isinstance(cfg, dict) or not cfg.get("urlTemplate"):
            continue
        if cfg.get("disabled"):
            skipped += 1
            continue
        parts = sid.split("-")
        category = parts[0]
        template = cfg["urlTemplate"]
        entries.append({
            "id": sid,
            "category": category,
            "subcategory": parts[1] if len(parts) > 2 else None,
            "label": html_labels.get(sid) or janua_labels.get(sid) or sid,
            "urlTemplate": template,
            "validator": cfg.get("validator"),
            "placeholders": list(dict.fromkeys(f"{{{p}}}" for p in _PLACEHOLDER.findall(template))),
        })
        categories[category] = categories.get(category, 0) + 1

    return {
        "meta": {
            "source": f"Exploratores OSINT Toolkit {meta.get('version', '?')} ({UPSTREAM_URL})",
            "upstream_version": meta.get("version"),
            "upstream_sha256": digest,
            "generated": meta.get("updated_at"),
            "total": len(entries),
            "disabled_skipped": skipped,
            "categories": dict(sorted(categories.items())),
        },
        "entries": entries,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("source", type=Path, help="path to a checkout of Exploratores (branch v3)")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--check", action="store_true", help="do not write; exit 1 if --out is stale")
    args = ap.parse_args()

    catalog = build(args.source)
    text = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
    m = catalog["meta"]
    unlabelled = sum(1 for e in catalog["entries"] if e["label"] == e["id"])

    if args.check:
        current = args.out.read_text(encoding="utf-8") if args.out.exists() else ""
        if current != text:
            print(f"{args.out} is out of date with Exploratores {m['upstream_version']}.")
            return 1
        print(f"{args.out} matches Exploratores {m['upstream_version']}.")
        return 0

    args.out.write_text(text, encoding="utf-8", newline="\n")
    print(f"Wrote {m['total']} entries in {len(m['categories'])} categories "
          f"(Exploratores {m['upstream_version']}, {m['disabled_skipped']} disabled skipped, "
          f"{unlabelled} without a label) to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

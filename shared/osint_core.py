"""
osint_core.py — shared engine for the Exploratores OSINT Suite.

Pure-Python port of the Exploratores toolkit logic:
  * classify_indicator()  — port of indicator-classifier.js
  * build_fields()        — port of the placeholder-producing validators.js logic
  * render_urls()         — port of main.js URL substitution (encodeURIComponent-equivalent)

The catalog (catalog.json) is data-only and language-neutral, generated from the
toolkit's search-library.js + the human-readable labels in pages/*.html.

No third-party dependencies. Python 3.9+.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

# --------------------------------------------------------------------------- #
# Catalog loading
# --------------------------------------------------------------------------- #
_CATALOG_CACHE: Optional[Dict[str, Any]] = None


def catalog_path() -> Path:
    """catalog.json is expected next to this module."""
    return Path(__file__).with_name("catalog.json")


def load_catalog(path: Optional[str | Path] = None) -> Dict[str, Any]:
    global _CATALOG_CACHE
    if path is not None:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    if _CATALOG_CACHE is None:
        with open(catalog_path(), "r", encoding="utf-8") as fh:
            _CATALOG_CACHE = json.load(fh)
    return _CATALOG_CACHE


def entries() -> List[Dict[str, Any]]:
    return load_catalog()["entries"]


def categories() -> Dict[str, int]:
    return load_catalog()["meta"]["categories"]


# --------------------------------------------------------------------------- #
# encodeURIComponent-equivalent (matches main.js behaviour)
# --------------------------------------------------------------------------- #
# encodeURIComponent leaves these unescaped: A-Z a-z 0-9 - _ . ! ~ * ' ( )
_ENCODE_SAFE = "-_.!~*'()"


def encode_uri_component(value: str) -> str:
    out = []
    for ch in value:
        if ch.isalnum() and ch.isascii():
            out.append(ch)
        elif ch in _ENCODE_SAFE:
            out.append(ch)
        else:
            out.append("".join(f"%{b:02X}" for b in ch.encode("utf-8")))
    return "".join(out)


# --------------------------------------------------------------------------- #
# Indicator classifier  (port of indicator-classifier.js)
# --------------------------------------------------------------------------- #
_ROBUST_DOMAIN = re.compile(
    r"^([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$"
)

_PLATFORM_RULES = {
    "vk.com": ("VK_USERNAME", re.compile(r"^([\w.-]+)")),
    "x.com": ("X_USERNAME", re.compile(r"^([\w.-]+)")),
    "twitter.com": ("X_USERNAME", re.compile(r"^([\w.-]+)")),
    "instagram.com": ("INSTAGRAM_USERNAME", re.compile(r"^([\w.-]+)")),
    "t.me": ("TELEGRAM_USERNAME", re.compile(r"^([\w.-]+)")),
    "facebook.com": ("FACEBOOK_USERNAME", re.compile(r"^([\w.-]+)")),
    "linkedin.com/in": ("LINKEDIN_PROFILE", re.compile(r"in/([\w.-]+)")),
}


def _parse_url_subtypes(query: str) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    try:
        from urllib.parse import urlparse

        u = urlparse(query if "://" in query else "http://" + query)
        hostname = (u.hostname or "").replace("www.", "", 1)
        path = (u.path or "").lstrip("/")
        for key, (typ, rgx) in _PLATFORM_RULES.items():
            if (hostname + "/" + path).startswith(key):
                m = rgx.search(key + "/" + path)
                if m and m.group(1):
                    val = m.group(1)
                    results.append({"type": typ, "score": 0.9, "value": val})
                    if "USERNAME" in typ or "PROFILE" in typ:
                        results.append({"type": "USERNAME", "score": 0.85, "value": val})
    except Exception:
        pass
    return results


# (type, compiled pattern, score, optional precheck)
_UNIQUE_RULES = [
    ("IBAN", re.compile(r"^[A-Z]{2}\d{2}[A-Z\d]{11,30}$", re.I), 1.0, None),
    ("BTC_ADDRESS", re.compile(r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$"), 1.0, None),
    ("CRYPTO_ETH", re.compile(r"^0x[a-fA-F0-9]{40}$"), 1.0, None),
    ("CRYPTO_XMR", re.compile(r"^[48][0-9AB][1-9A-HJ-NP-Za-km-z]{93,105}$"), 1.0, None),
    ("HASH_SHA256", re.compile(r"^[a-f0-9]{64}$", re.I), 1.0, None),
    ("HASH_SHA1", re.compile(r"^[a-f0-9]{40}$", re.I), 1.0, None),
    ("HASH_MD5", re.compile(r"^[a-f0-9]{32}$", re.I), 1.0, None),
    ("SSN", re.compile(r"^\d{3}-?\d{2}-?\d{4}$"), 1.0, None),
    ("ADSENSE_ID", re.compile(r"^pub-\d{16}$", re.I), 1.0, None),
    ("ANALYTICS_ID", re.compile(r"^(UA-\d{4,}-\d{1,}|G-[A-Z0-9]{10})$", re.I), 1.0, None),
    ("IPV4", re.compile(r"^(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)$"), 0.95, None),
    ("EMAIL", re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$"), 0.95, None),
    ("PHONE_E164", re.compile(r"^\+\d{7,15}$"), 0.9, None),
    ("YOUTUBE_CHANNEL_ID", re.compile(r"^UC[a-zA-Z0-9_-]{22}$"), 0.9, None),
    ("VEHICLE_VIN", re.compile(r"^[A-HJ-NPR-Z0-9]{17}$", re.I), 0.85, None),
    ("URL", re.compile(r"^(https?://)?([\da-z\.-]+)\.([a-z\.]{2,6})([/\w \.-]*)*/?$", re.I), 0.8,
        lambda q: "." in q and " " not in q),
    ("DOMAIN", _ROBUST_DOMAIN, 0.8, lambda q: " " not in q and "@" not in q),
]

_AMBIGUOUS_RULES = [
    ("COORDINATES", re.compile(r"^-?\d{1,3}(?:\.\d+)?,\s*-?\d{1,3}(?:\.\d+)?$"), 0.75, None),
    ("YOUTUBE_VIDEO_ID", re.compile(r"^[a-zA-Z0-9_-]{11}$"), 0.7, None),
    ("USERNAME", re.compile(r"^[a-zA-Z0-9_.-]{3,24}$"), 0.6, lambda q: " " not in q),
    ("PERSON_NAME", re.compile(r"^[A-Z][a-z']+(\s[A-Z][a-z']{1,})+$"), 0.55, lambda q: " " in q),
    ("NUMERIC_ID", re.compile(r"^\d{5,20}$"), 0.5, None),
    ("PHONE_NATIONAL", re.compile(r"^[\d\s\-()]{7,15}$"), 0.5,
        lambda q: not q.startswith("+") and any(c.isdigit() for c in q)),
]


def classify_indicator(query: str) -> List[Dict[str, Any]]:
    """Return a sorted list of {type, score, value} candidates for an input string."""
    q = (query or "").strip()
    if not q:
        return []

    for typ, pat, score, precheck in _UNIQUE_RULES:
        if pat.match(q):
            if precheck and not precheck(q):
                continue
            results = [{"type": typ, "score": score, "value": q}]
            if typ == "URL":
                results += _parse_url_subtypes(q)
            return results

    results: List[Dict[str, Any]] = []
    for typ, pat, score, precheck in _AMBIGUOUS_RULES:
        if (precheck is None or precheck(q)) and pat.match(q):
            results.append({"type": typ, "score": score, "value": q})

    generic = 0.1 if results else 0.5
    results.append({"type": "GENERIC_TEXT", "score": generic, "value": q})
    results.sort(key=lambda r: r["score"], reverse=True)

    seen, unique = set(), []
    for r in results:
        if r["type"] not in seen:
            seen.add(r["type"])
            unique.append(r)
    return unique


# --------------------------------------------------------------------------- #
# Field builder — produces the placeholder dict consumed by URL templates.
# --------------------------------------------------------------------------- #
# Maps a classifier type to the catalog categories it can drive.
TYPE_TO_CATEGORIES: Dict[str, List[str]] = {
    "DOMAIN": ["domains"],
    "URL": ["domains", "images"],
    "EMAIL": ["email"],
    "IPV4": ["ip"],
    "USERNAME": ["usernames", "facebook", "instagram", "x", "vk", "linkedin",
                 "communities", "keybase", "videos"],
    "VK_USERNAME": ["vk", "usernames"],
    "X_USERNAME": ["x", "usernames"],
    "INSTAGRAM_USERNAME": ["instagram", "usernames"],
    "FACEBOOK_USERNAME": ["facebook", "usernames"],
    "TELEGRAM_USERNAME": ["communities", "usernames"],
    "LINKEDIN_PROFILE": ["linkedin", "usernames"],
    "PERSON_NAME": ["names", "publiccompanyrecords"],
    "COORDINATES": ["maps"],
    "IBAN": ["iban"],
    "BTC_ADDRESS": ["currencies"],
    "CRYPTO_ETH": ["currencies"],
    "CRYPTO_XMR": ["currencies"],
    "VEHICLE_VIN": ["vehicles"],
    "PHONE_E164": ["phoneint"],
    "PHONE_NATIONAL": ["phoneint", "phoneus"],
    "COMPANY": ["publiccompanyrecords"],
    "GENERIC_TEXT": ["searchengines", "docs"],
    "NUMERIC_ID": ["searchengines"],
    "YOUTUBE_VIDEO_ID": ["videos"],
    "YOUTUBE_CHANNEL_ID": ["videos"],
}


def _host_of(value: str) -> str:
    from urllib.parse import urlparse

    u = urlparse(value if "://" in value else "http://" + value)
    return (u.hostname or value).replace("www.", "", 1)


def build_fields(value: str, indicator_type: str,
                 extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """Build the placeholder->value mapping for a given value and indicator type.

    `extra` lets callers supply structured/optional fields (firstname, lastname,
    city, state, street, zip, countrycode, since, until, amount, etc.). Extra
    values always win over derived defaults.
    """
    v = (value or "").strip()
    f: Dict[str, str] = {"term": v, "query": v, "keyword": v}
    t = indicator_type.upper()

    if t in ("DOMAIN",):
        f["domain"] = v
        f["domain_nodots"] = v.replace(".", "")
        f["url"] = v if "://" in v else "http://" + v
    elif t == "URL":
        f["url"] = v
        f["domain"] = _host_of(v)
        f["domain_nodots"] = _host_of(v).replace(".", "")
    elif t == "EMAIL":
        f["email"] = v
        f["localpart"] = v.split("@")[0]
        f["domain"] = v.split("@")[-1]
    elif t == "IPV4":
        f["ip"] = v
    elif "USERNAME" in t or t in ("LINKEDIN_PROFILE",):
        f["username"] = v
        f["usera"] = v
    elif t == "PERSON_NAME":
        parts = v.split()
        first = parts[0] if parts else ""
        last = parts[-1] if len(parts) > 1 else ""
        dash = "-".join(parts)
        f.update({
            "firstname": first, "lastname": last, "first": first, "last": last,
            "fullname": v, "fullnamedash": dash, "fullnamedashlower": dash.lower(),
            "officername": v, "realname": v,
        })
    elif t == "COORDINATES":
        lat, _, lon = v.partition(",")
        f["lat"] = lat.strip()
        f["lon"] = lon.strip()
    elif t == "IBAN":
        f["iban"] = v.replace(" ", "").upper()
    elif t in ("BTC_ADDRESS", "CRYPTO_ETH", "CRYPTO_XMR"):
        f["btc_address"] = v  # currencies templates route the address through {query}
    elif t == "VEHICLE_VIN":
        f["vin"] = v
    elif t == "COMPANY":
        f["companyname"] = v
        f["company"] = v
        f["officername"] = v
    elif t in ("YOUTUBE_VIDEO_ID",):
        f["videoid"] = v
    elif t in ("YOUTUBE_CHANNEL_ID",):
        f["channelid"] = v
    elif t in ("PHONE_E164", "PHONE_NATIONAL"):
        f.update(_phone_fields(v, extra or {}))

    if extra:
        f.update({k: str(val) for k, val in extra.items() if val is not None})
    return f


def _phone_fields(value: str, extra: Dict[str, str]) -> Dict[str, str]:
    """Best-effort port of the phone validators' derived fields."""
    cc = str(extra.get("countrycode", "")).lstrip("+").lstrip("0")
    nat = re.sub(r"\D", "", str(extra.get("nationalnumber", "")))
    digits = re.sub(r"\D", "", value)

    if not cc and value.startswith("+"):
        # Heuristic split: 1-3 digit country code. Prefer explicit extra fields.
        cc = digits[:2] if len(digits) > 10 else digits[:1]
        nat = digits[len(cc):]
    elif not nat:
        nat = digits.lstrip("0")

    e164 = f"{cc}{nat}" if cc else nat
    out = {
        "e164": e164, "countrycode": cc, "nat_num": nat,
        "dt_num_only": nat, "dt_0num_only": f"0{nat}", "dt_num_generic": nat,
        "dt_enum_generic": f"e{nat}",
        "google_query": f'"+{cc}{nat}" OR "+{cc} {nat}"' if cc else f'"{nat}"',
    }
    if cc:
        out["dt_plus_cc_num"] = f"+{cc}.{nat}"
        out["dt_plus_cc_0num"] = f"+{cc}.0{nat}"
    # US-style 10-digit breakdown
    if len(digits) >= 10:
        d = digits[-10:]
        out.update({"area": d[:3], "prefix": d[3:6], "line": d[6:], "full": d})
    return out


# --------------------------------------------------------------------------- #
# URL rendering
# --------------------------------------------------------------------------- #
_PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z0-9_]+)\}")


def _applicable(entry: Dict[str, Any], fields: Dict[str, str]) -> bool:
    for ph in entry["placeholders"]:
        key = ph[1:-1]
        if not fields.get(key):
            return False
    return True


def render_entry(entry: Dict[str, Any], fields: Dict[str, str]) -> Optional[str]:
    if not _applicable(entry, fields):
        return None
    url = entry["urlTemplate"]

    def repl(m: "re.Match") -> str:
        return encode_uri_component(fields[m.group(1)])

    return _PLACEHOLDER_RE.sub(repl, url)


def render_urls(value: str,
                indicator_type: Optional[str] = None,
                categories_filter: Optional[List[str]] = None,
                extra: Optional[Dict[str, str]] = None,
                include_onion: bool = True,
                limit: Optional[int] = None) -> Dict[str, Any]:
    """Produce a curated list of OSINT search URLs for `value`.

    - indicator_type: force a type; if None, auto-classified (top candidate).
    - categories_filter: restrict to these catalog categories; if None, uses the
      type->categories map. Pass [] or ['all'] to consider every category.
    - extra: structured/optional fields (firstname, city, countrycode, since...).
    - include_onion: keep .onion (Tor) results.
    - limit: cap the number of URLs returned.
    """
    candidates = classify_indicator(value)
    if indicator_type:
        chosen = indicator_type.upper()
    elif candidates:
        chosen = candidates[0]["type"]
    else:
        chosen = "GENERIC_TEXT"

    fields = build_fields(value, chosen, extra)

    if categories_filter in (None,):
        cats = TYPE_TO_CATEGORIES.get(chosen, ["searchengines"])
    elif categories_filter == [] or [c.lower() for c in categories_filter] == ["all"]:
        cats = None  # every category
    else:
        cats = [c.lower() for c in categories_filter]

    results = []
    for e in entries():
        if cats is not None and e["category"] not in cats:
            continue
        if not include_onion and ".onion" in e["urlTemplate"]:
            continue
        url = render_entry(e, fields)
        if url:
            results.append({
                "id": e["id"],
                "category": e["category"],
                "label": e["label"],
                "url": url,
            })

    if limit:
        results = results[:limit]

    return {
        "value": value,
        "indicator_type": chosen,
        "candidates": candidates,
        "categories_used": cats if cats is not None else "all",
        "count": len(results),
        "results": results,
    }


def search_catalog(query: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Free-text search across entry ids, labels and categories."""
    q = query.lower()
    out = []
    for e in entries():
        hay = f"{e['id']} {e['label']} {e['category']} {e.get('subcategory') or ''}".lower()
        if q in hay:
            out.append({"id": e["id"], "category": e["category"],
                        "label": e["label"], "urlTemplate": e["urlTemplate"],
                        "placeholders": e["placeholders"]})
        if len(out) >= limit:
            break
    return out

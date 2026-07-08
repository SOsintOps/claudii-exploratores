"""
redactor.py — browser-side-equivalent PII redaction with a reversible map.

Mirrors the Exploratores 'Redactor' concept: replace PII with numbered
placeholders (e.g. [EMAIL_1]) before sending case text to an external model,
and restore it afterwards using the returned redaction map.

Built-in patterns cover emails, IPv4/IPv6, phone numbers, IBANs, credit-card-like
numbers, URLs, and common crypto addresses. Callers may add custom patterns.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple

_BUILTIN: List[Tuple[str, "re.Pattern[str]"]] = [
    ("EMAIL", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("URL", re.compile(r"\bhttps?://[^\s<>\"]+", re.I)),
    ("IBAN", re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{10,30}\b")),
    ("CRYPTO_ETH", re.compile(r"\b0x[a-fA-F0-9]{40}\b")),
    ("CRYPTO_BTC", re.compile(r"\b(?:bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}\b")),
    ("IPV4", re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b")),
    ("IPV6", re.compile(r"\b(?:[A-F0-9]{1,4}:){2,7}[A-F0-9]{1,4}\b", re.I)),
    ("CREDIT_CARD", re.compile(r"\b(?:\d[ -]?){13,19}\b")),
    ("PHONE", re.compile(r"(?<!\w)\+?\d[\d\s().-]{6,}\d(?!\w)")),
    ("SSN", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
]


def redact(text: str,
           enabled: List[str] | None = None,
           custom_patterns: Dict[str, str] | None = None) -> Dict[str, Any]:
    """Redact PII from `text`. Returns {redacted, map}.

    `map` maps each placeholder ([TYPE_N]) back to the original substring so the
    output of an external model can be de-redacted with `restore()`.
    """
    patterns = list(_BUILTIN)
    if custom_patterns:
        for name, rgx in custom_patterns.items():
            patterns.append((name.upper(), re.compile(rgx)))
    if enabled is not None:
        allow = {e.upper() for e in enabled}
        patterns = [p for p in patterns if p[0] in allow]

    redaction_map: Dict[str, str] = {}
    counters: Dict[str, int] = {}
    seen: Dict[str, str] = {}  # original -> placeholder (dedupe identical values)
    out = text

    for name, rgx in patterns:
        def _sub(m: "re.Match") -> str:
            original = m.group(0)
            if original in seen:
                return seen[original]
            counters[name] = counters.get(name, 0) + 1
            ph = f"[{name}_{counters[name]}]"
            redaction_map[ph] = original
            seen[original] = ph
            return ph
        out = rgx.sub(_sub, out)

    return {"redacted": out, "map": redaction_map, "count": len(redaction_map)}


def restore(text: str, redaction_map: Dict[str, str]) -> str:
    """Reverse a redaction using its map."""
    out = text
    # Restore longer placeholders first to avoid partial clobbering.
    for ph in sorted(redaction_map, key=len, reverse=True):
        out = out.replace(ph, redaction_map[ph])
    return out

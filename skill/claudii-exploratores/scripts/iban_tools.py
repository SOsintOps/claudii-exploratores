"""
iban_tools.py — offline IBAN structural validation (ISO 13616 mod-97).

Ports the country length/name table from the Exploratores toolkit (ibankit v1.6.5).
Validates length-by-country and the mod-97 check digits. Does NOT resolve the
bank name offline (that dataset lives in the web toolkit's bankDatabases/*.js);
instead it returns the bank/branch identifier substring where the layout is known.
"""
from __future__ import annotations

import re
from typing import Any, Dict

try:  # generated table
    from ._iban_countries import IBAN_COUNTRIES  # type: ignore
except Exception:  # pragma: no cover - allow flat-dir import
    from _iban_countries import IBAN_COUNTRIES  # type: ignore


def _mod97(iban: str) -> int:
    # Move first 4 chars to the end, convert letters to numbers (A=10..Z=35).
    rearranged = iban[4:] + iban[:4]
    digits = "".join(str(int(c, 36)) if c.isalpha() else c for c in rearranged)
    # Piecewise mod to avoid big ints
    rem = 0
    for ch in digits:
        rem = (rem * 10 + int(ch)) % 97
    return rem


def verify_iban(value: str) -> Dict[str, Any]:
    raw = (value or "").strip()
    iban = re.sub(r"\s+", "", raw).upper()
    result: Dict[str, Any] = {"input": raw, "normalised": iban, "valid": False}

    if not re.match(r"^[A-Z]{2}\d{2}[A-Z0-9]+$", iban):
        result["error"] = "Format not IBAN-like (expected 2 letters, 2 digits, then alphanumerics)."
        return result

    country = iban[:2]
    info = IBAN_COUNTRIES.get(country)
    if not info:
        result["error"] = f"Unknown / unsupported IBAN country code '{country}'."
        result["country"] = country
        return result

    expected_len, country_name = info
    result["country"] = country
    result["country_name"] = country_name
    result["expected_length"] = expected_len
    result["actual_length"] = len(iban)

    if len(iban) != expected_len:
        result["error"] = f"Length {len(iban)} != expected {expected_len} for {country_name}."
        return result

    if _mod97(iban) != 1:
        result["error"] = "Failed mod-97 check-digit validation (ISO 13616)."
        return result

    result["valid"] = True
    result["bban"] = iban[4:]
    result["check_digits"] = iban[2:4]
    result["note"] = ("Structurally valid. Bank-name resolution for supported countries is "
                      "available in the Exploratores web toolkit (offline bankDatabases).")
    return result

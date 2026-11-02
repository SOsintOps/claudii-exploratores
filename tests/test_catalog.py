"""Catalog integrity: one source of truth, copied unchanged into skill/ and mcp/."""
import json
import re
from collections import Counter

import pytest

from conftest import ROOT

SHARED = ROOT / "shared"
COPIES = [ROOT / "skill" / "claudii-exploratores" / "scripts", ROOT / "mcp" / "exploratores_osint_mcp"]
ENGINE_FILES = ["osint_core.py", "iban_tools.py", "redactor.py", "_iban_countries.py",
                "catalog.json", "access.json"]


@pytest.fixture(scope="module")
def catalog():
    return json.loads((SHARED / "catalog.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("copy", COPIES, ids=["skill", "mcp"])
@pytest.mark.parametrize("name", ENGINE_FILES)
def test_copies_identical(copy, name):
    assert (copy / name).read_bytes() == (SHARED / name).read_bytes(), (
        f"{copy / name} differs from shared/: run scripts/build_release.sh")


def test_ids_unique(catalog):
    dup = [i for i, n in Counter(e["id"] for e in catalog["entries"]).items() if n > 1]
    assert dup == []


def test_meta_matches_entries(catalog):
    meta, entries = catalog["meta"], catalog["entries"]
    assert meta["total"] == len(entries)
    assert meta["categories"] == dict(Counter(e["category"] for e in entries))


def test_placeholders_listed(catalog):
    for e in catalog["entries"]:
        found = list(dict.fromkeys(re.findall(r"\{[a-zA-Z0-9_]+\}", e["urlTemplate"])))
        assert e["placeholders"] == found, e["id"]


# Inherited from upstream as-is: Bitly's "+" suffix shows a short link's stats page,
# so the template is the short link itself.
NOT_HTTP = {"domains-shorturl-bitly"}


def test_templates_are_http(catalog):
    for e in catalog["entries"]:
        if e["id"] in NOT_HTTP:
            continue
        assert e["urlTemplate"].startswith(("http://", "https://")), e["id"]

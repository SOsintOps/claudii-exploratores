"""Geo-locked / Tor / account warnings attached to generated links."""
import json

import osint_core as core
from conftest import ROOT

ACCESS = json.loads((ROOT / "shared" / "access.json").read_text(encoding="utf-8"))


def test_access_map_shape():
    assert ACCESS["meta"]["hosts_flagged"] == len(ACCESS["hosts"])
    for host, rec in ACCESS["hosts"].items():
        assert not host.startswith("www."), host
        assert rec["source"] in ("live", "desk")
        assert rec.get("vpn") in (None, "required", "recommended", "tor")
        if rec.get("vpn") in ("required", "recommended"):
            assert rec.get("country"), host


def _geo_locked_entry():
    for e in core.entries():
        acc = core.access_for(e["urlTemplate"])
        if acc and acc.get("vpn") == "required":
            return e
    raise AssertionError("no catalog entry on a geo-locked host")


def test_geo_locked_link_warns_and_can_be_excluded():
    e = _geo_locked_entry()
    acc = core.access_for(e["urlTemplate"])
    note = core.access_note(acc)
    assert note.startswith("GEO-LOCKED") and acc["country"] in note

    fields = {p[1:-1]: "test" for p in e["placeholders"]}
    kw = dict(indicator_type="GENERIC_TEXT", categories_filter=[e["category"]], extra=fields)
    res = core.render_urls("test", **kw)
    hit = [r for r in res["results"] if r["id"] == e["id"]]
    assert hit and hit[0]["access"]["vpn"] == "required"
    assert any("geo-locked" in w for w in res["warnings"])

    res2 = core.render_urls("test", exclude_geo_locked=True, **kw)
    assert e["id"] not in {r["id"] for r in res2["results"]}


def test_tor_warning():
    res = core.render_urls("osint", categories_filter=["searchengines"])
    if any(".onion" in r["url"] for r in res["results"]):
        assert any("Tor Browser" in w for w in res["warnings"])

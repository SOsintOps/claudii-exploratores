"""scripts/sync_catalog.py on a tiny Exploratores-shaped tree."""
import hashlib
import json
import subprocess
import sys

from conftest import ROOT

SCRIPT = ROOT / "scripts" / "sync_catalog.py"


def _fixture(base):
    lib = {
        "names-a": {"urlTemplate": "https://a.example/?q={fullname}", "validator": "v"},
        "legal-it-x": {"urlTemplate": "https://x.example/{urn}"},
        "ip-dead": {"urlTemplate": "https://dead.example/{ip}", "disabled": True},
    }
    raw = json.dumps(lib).encode()
    for d in ("assets/data", "assets/js", "pages"):
        (base / d).mkdir(parents=True)
    (base / "assets/data/search-library.json").write_bytes(raw)
    (base / "assets/data/catalogue-meta.json").write_text(json.dumps({
        "version": "9.9.9", "updated_at": "2026-01-01T00:00:00Z",
        "sha256": hashlib.sha256(raw).hexdigest()}))
    (base / "pages/names.html").write_text('<button data-search-id="names-a">A Search</button>')
    (base / "assets/js/janua-search-map.js").write_text(
        '"legal-it-x": { "label": "X", "page": "Legal"},')


def test_sync_and_check(tmp_path):
    src = tmp_path / "Exploratores"
    _fixture(src)
    out = tmp_path / "catalog.json"
    run = [sys.executable, str(SCRIPT), str(src), "--out", str(out)]
    subprocess.run(run, check=True, capture_output=True)
    cat = json.loads(out.read_text(encoding="utf-8"))
    assert cat["meta"]["upstream_version"] == "9.9.9"
    assert cat["meta"]["disabled_skipped"] == 1
    assert {e["id"]: e["label"] for e in cat["entries"]} == {"legal-it-x": "X", "names-a": "A Search"}
    assert subprocess.run(run + ["--check"], capture_output=True).returncode == 0
    out.write_text("{}")
    assert subprocess.run(run + ["--check"], capture_output=True).returncode == 1


def test_hash_mismatch_fails(tmp_path):
    src = tmp_path / "Exploratores"
    _fixture(src)
    meta = src / "assets/data/catalogue-meta.json"
    meta.write_text(json.dumps({"version": "1", "sha256": "0" * 64}))
    r = subprocess.run([sys.executable, str(SCRIPT), str(src), "--out", str(tmp_path / "c.json")],
                       capture_output=True, text=True)
    assert r.returncode != 0 and "SHA-256" in r.stderr

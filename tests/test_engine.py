"""Classifier, field builder and URL rendering."""
import re

import pytest

import osint_core as core

# Placeholders that no classifier type derives: the caller passes them in `fields`
# (MCP) or `--field` (CLI). Documented in the README and the FAQ.
EXTRA_ONLY = {
    "full_address", "postalcode", "street", "city", "state", "zip", "country",
    "countrycode", "nationalnumber", "country_iso", "country_iso_lower",
    "since", "until", "enddate", "startdate", "amount", "listid", "userb", "ssn",
    "activity", "location", "csp_string", "favicon_url", "shodan_hash", "start_ip",
    "end_ip", "ssid", "usa_address_query", "searchQueryState", "msgid", "number", "plate",
}

SAMPLES = {
    "DOMAIN": "example.com", "URL": "https://example.com/a", "EMAIL": "a@example.com",
    "IPV4": "8.8.8.8", "USERNAME": "johndoe", "PERSON_NAME": "John Smith",
    "COORDINATES": "45.46,9.19", "IBAN": "GB82WEST12345698765432",
    "BTC_ADDRESS": "1BoatSLRHtKNngkdXEeobR76b53LETtpyT", "VEHICLE_VIN": "1HGCM82633A004352",
    "PHONE_E164": "+12025550123", "PHONE_NATIONAL": "2025550123", "COMPANY": "Acme",
    "YOUTUBE_VIDEO_ID": "dQw4w9WgXcQ", "YOUTUBE_CHANNEL_ID": "UC" + "a" * 22,
    "NUMERIC_ID": "123456789", "HASH_MD5": "d41d8cd98f00b204e9800998ecf8427e",
    "ADSENSE_ID": "pub-1234567890123456", "ANALYTICS_ID": "UA-1234-1", "HASHTAG": "#osint",
    "NORMATTIVA_URN": "urn:nir:stato:legge:1990-08-07;241", "CURIA_CASE": "C-311/18",
    "EU_VAT": "IT00905811006", "ADDRESS": "1 Main St, Springfield",
}


def test_every_placeholder_reachable():
    """Each placeholder is built by some indicator type or is a documented extra field."""
    built = set()
    for typ, value in SAMPLES.items():
        built |= set(core.build_fields(value, typ))
    used = {p[1:-1] for e in core.entries() for p in e["placeholders"]}
    missing = sorted(used - built - EXTRA_ONLY)
    assert missing == [], f"placeholders nobody fills: {missing}"


@pytest.mark.parametrize("value,expected", [
    ("example.com", "URL"),  # the URL rule matches first; it drives domains + images
    ("john.doe@example.com", "EMAIL"),
    ("8.8.8.8", "IPV4"),
    ("GB82WEST12345698765432", "IBAN"),
    ("urn:nir:stato:legge:1990-08-07;241", "NORMATTIVA_URN"),
    ("C-311/18", "CURIA_CASE"),
    ("#osint", "HASHTAG"),
    ("d41d8cd98f00b204e9800998ecf8427e", "HASH_MD5"),
    ("+393331234567", "PHONE_E164"),
])
def test_classifier_top(value, expected):
    assert core.classify_indicator(value)[0]["type"] == expected


def test_eu_vat_does_not_hide_usernames():
    types = [c["type"] for c in core.classify_indicator("DEADBEEF123")]
    assert "USERNAME" in types
    assert "EU_VAT" in [c["type"] for c in core.classify_indicator("IT00905811006")]


def test_urn_keeps_reserved_characters():
    res = core.render_urls("urn:nir:stato:legge:1990-08-07;241")
    urls = {r["id"]: r["url"] for r in res["results"]}
    assert urls["legal-it-normattiva-urn"].endswith("N2Ls?urn:nir:stato:legge:1990-08-07;241")
    assert "%3A" in urls["legal-eu-eurlex"]  # {q} is fully encoded


def test_encoding_matches_encodeuricomponent():
    assert core.encode_uri_component("Mário Rossi & co/1") == "M%C3%A1rio%20Rossi%20%26%20co%2F1"


def test_eu_vat_fields():
    f = core.build_fields("GR 123.456.789", "EU_VAT")
    assert (f["vat_country"], f["vat_number"]) == ("EL", "123456789")


def test_us_phone_fields():
    f = core.build_fields("(202) 555-0123", "PHONE_NATIONAL")
    assert f["full_dash"] == "202-555-0123"
    assert f["national_raw"] == "2025550123"


@pytest.mark.parametrize("value", ["example.com", "John Smith", "johndoe", "+12025550123",
                                   "8.8.8.8", "IT00905811006", "#osint", "C-311/18"])
def test_no_unfilled_placeholders_in_output(value):
    for r in core.render_urls(value, categories_filter=["all"])["results"]:
        assert not re.search(r"\{[a-zA-Z0-9_]+\}", r["url"]), r["id"]


def test_onion_filter():
    res = core.render_urls("osint", include_onion=False, categories_filter=["searchengines"])
    assert all(".onion" not in r["url"] for r in res["results"])

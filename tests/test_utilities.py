"""IBAN verifier and PII redactor."""
import iban_tools
import redactor


def test_iban_valid():
    r = iban_tools.verify_iban("GB82 WEST 1234 5698 7654 32")
    assert r["valid"] and r["country"] == "GB"


def test_iban_bad_checksum():
    assert not iban_tools.verify_iban("GB83 WEST 1234 5698 7654 32")["valid"]


def test_redact_restore_round_trip():
    text = "Mail john@example.com from 8.8.8.8, IBAN GB82WEST12345698765432."
    red = redactor.redact(text)
    assert "john@example.com" not in red["redacted"] and red["count"] >= 3
    assert redactor.restore(red["redacted"], red["map"]) == text

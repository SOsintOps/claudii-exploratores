"""MCP server: tools registered, read-only annotations, same output as the engine."""
import asyncio
import sys

import pytest

from conftest import ROOT

pytest.importorskip("mcp")
sys.path.insert(0, str(ROOT / "mcp"))
from exploratores_osint_mcp import server  # noqa: E402
import osint_core as core  # noqa: E402

EXPECTED = {"classify_indicator", "build_osint_urls", "search_catalog", "list_categories",
            "verify_iban", "redact_pii", "restore_pii"}


def test_tools_registered_read_only():
    tools = asyncio.run(server.mcp.list_tools())
    assert {t.name for t in tools} == EXPECTED
    for t in tools:
        a = t.annotations.model_dump(by_alias=True)  # camelCase on mcp 1.x and 2.x
        assert a["readOnlyHint"] is True, t.name
        assert a["openWorldHint"] is False, t.name
        assert t.title, t.name


def test_server_matches_engine():
    assert server.build_osint_urls("example.com") == core.render_urls("example.com")
    assert server.list_categories() == core.categories()

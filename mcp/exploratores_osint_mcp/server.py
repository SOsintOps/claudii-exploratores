"""
Exploratores OSINT — MCP server (FastMCP).

Exposes the ported Exploratores toolkit (the OSINT tool catalog) as MCP tools so any MCP
client (Claude Desktop, etc.) can classify indicators, build curated OSINT search
URL sets, verify IBANs and redact PII — all offline, without a browser.

The server never *opens* URLs; it only builds them. Opening/reading is left to the
client, so OPSEC (VPN, sterile profile) stays under the operator's control.

Run:
    python -m exploratores_osint_mcp.server         # stdio (default)
    # or via the console script:  claudii-exploratores-mcp
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from mcp.types import ToolAnnotations

try:  # mcp 2.x renamed FastMCP to MCPServer
    from mcp.server.mcpserver import MCPServer
    _MCP2 = True
except ImportError:  # mcp 1.x
    from mcp.server.fastmcp import FastMCP as MCPServer  # type: ignore[no-redef]
    _MCP2 = False

__version__ = "1.1.0a1"

# Support both `python -m exploratores_osint_mcp.server` (package) and a flat run.
try:
    from . import osint_core as core
    from . import iban_tools, redactor
except ImportError:  # pragma: no cover
    import osint_core as core  # type: ignore
    import iban_tools, redactor  # type: ignore

_N_TOOLS = len(core.entries())
_N_CATS = len(core.categories())

# Every tool is offline and side-effect free: it reads the bundled catalog and
# computes a result. No network call, no state, nothing the target can see.
_OFFLINE = ToolAnnotations(readOnlyHint=True, destructiveHint=False,
                           idempotentHint=True, openWorldHint=False)

mcp = MCPServer(
    "claudii-exploratores",
    **({"version": __version__} if _MCP2 else {}),
    instructions=(
        f"OSINT investigation tools ported from the Exploratores toolkit ({_N_TOOLS} curated "
        f"tools across {_N_CATS} categories). Use classify_indicator to detect what a value is, "
        "build_osint_urls to get a curated set of search links for an indicator, "
        "search_catalog / list_categories to explore the catalog, verify_iban for "
        "offline IBAN validation, and redact_pii before sending case text to an "
        "external model. These tools BUILD search URLs — they do not fetch pages; the "
        "client decides which to open, applying OPSEC. Opening a link reveals the "
        "operator's IP address to that service. build_osint_urls returns 'warnings' and a "
        "per-link 'access_note': always show them to the user before any link is opened, "
        "above all the geo-locked links that only work through a VPN exit in a given "
        "country, and the .onion links that need Tor Browser. Use only for authorised, lawful "
        "investigation. Treat results as leads to verify, never as conclusions."
    ),
)


@mcp.tool(title="Classify an OSINT indicator", annotations=_OFFLINE)
def classify_indicator(value: str) -> List[Dict[str, Any]]:
    """Detect the likely type(s) of an OSINT indicator string.

    Returns a confidence-ranked list of candidates, e.g.
    [{"type": "EMAIL", "score": 0.95, "value": "a@b.com"}]. Types include DOMAIN,
    URL, EMAIL, IPV4, USERNAME, PERSON_NAME, COORDINATES, IBAN, BTC_ADDRESS,
    CRYPTO_ETH/XMR, VEHICLE_VIN, PHONE_E164/NATIONAL, YOUTUBE_*, SSN, HASH_*,
    HASHTAG, NORMATTIVA_URN, CURIA_CASE, EU_VAT, ADSENSE_ID, ANALYTICS_ID.

    Args:
        value: The raw indicator (name, email, domain, IP, username, phone, ...).
    """
    return core.classify_indicator(value)


@mcp.tool(title="Build OSINT search URLs", annotations=_OFFLINE)
def build_osint_urls(
    value: str,
    indicator_type: Optional[str] = None,
    categories: Optional[List[str]] = None,
    fields: Optional[Dict[str, str]] = None,
    include_onion: bool = True,
    limit: Optional[int] = None,
    exclude_geo_locked: bool = False,
) -> Dict[str, Any]:
    """Build a curated set of OSINT search URLs for an indicator.

    URLs are generated from the catalog's templates and URL-encoded exactly as the
    original toolkit. Only entries whose placeholders can be filled are returned, so
    the set is automatically scoped to what the indicator supports.

    Args:
        value: The indicator to investigate.
        indicator_type: Force a type (e.g. "PERSON_NAME", "DOMAIN", "COMPANY").
            If omitted, the top classifier candidate is used.
        categories: Restrict to these catalog categories (e.g. ["x","instagram"]).
            Pass ["all"] to consider every category; omit to use the type's default
            category mapping.
        fields: Extra/structured inputs that some tools need, e.g.
            {"firstname":"Mario","lastname":"Rossi"}, {"city":"Milano","state":"MI"},
            {"countrycode":"39","nationalnumber":"3331234567"},
            {"since":"2020-01-01","until":"2020-12-31"}, {"amount":"100"}.
        include_onion: Keep Tor (.onion) hidden-service results (default True).
        limit: Optional cap on the number of URLs returned.
        exclude_geo_locked: Drop links verified to need an exit IP in a specific
            country (default False: they are kept and flagged).

    Returns:
        {value, indicator_type, candidates, categories_used, count, warnings[],
        results[]} where each result is {id, category, label, url} plus, when the
        source has known requirements, "access" ({vpn: required|recommended|tor,
        country, account, bot_protection, source: live|desk}) and "access_note".
        Show "warnings" to the user before any link is opened.
    """
    cats: Optional[List[str]]
    if categories is None:
        cats = None
    elif [c.lower() for c in categories] == ["all"]:
        cats = []
    else:
        cats = categories
    return core.render_urls(
        value,
        indicator_type=indicator_type,
        categories_filter=cats,
        extra=fields,
        include_onion=include_onion,
        limit=limit,
        exclude_geo_locked=exclude_geo_locked,
    )


@mcp.tool(title="Search the OSINT catalog", annotations=_OFFLINE)
def search_catalog(query: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Free-text search the OSINT tool catalog by id, label or category.

    Args:
        query: Keyword to match (e.g. "wayback", "whois", "reddit").
        limit: Maximum results (default 50).
    """
    return core.search_catalog(query, limit=limit)


@mcp.tool(title="List catalog categories", annotations=_OFFLINE)
def list_categories() -> Dict[str, int]:
    """List the catalog's categories and how many tools each contains."""
    return core.categories()


@mcp.tool(title="Verify an IBAN offline", annotations=_OFFLINE)
def verify_iban(value: str) -> Dict[str, Any]:
    """Validate an IBAN offline (ISO 13616: country length table + mod-97 check).

    Args:
        value: The IBAN, with or without spaces.

    Returns a dict with validity, country, expected/actual length, check digits and
    BBAN. Bank-name resolution is only available in the Exploratores web toolkit.
    """
    return iban_tools.verify_iban(value)


@mcp.tool(title="Redact personal data", annotations=_OFFLINE)
def redact_pii(
    text: str,
    only: Optional[List[str]] = None,
    custom_patterns: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Redact PII from case text before sending it to an external model.

    Replaces emails, IPs, phones, IBANs, cards, URLs and crypto addresses with
    numbered placeholders (e.g. [EMAIL_1]) and returns a reversible map. Use
    restore_pii to de-redact the model's response.

    Args:
        text: The text to redact.
        only: Optional subset of pattern names to apply
            (EMAIL, URL, IBAN, CRYPTO_ETH, CRYPTO_BTC, IPV4, IPV6, CREDIT_CARD,
            PHONE, SSN).
        custom_patterns: Optional {name: regex} extra patterns.

    Returns:
        {redacted, map, count}.
    """
    return redactor.redact(text, enabled=only, custom_patterns=custom_patterns)


@mcp.tool(title="Restore redacted data", annotations=_OFFLINE)
def restore_pii(text: str, redaction_map: Dict[str, str]) -> str:
    """Reverse a redaction produced by redact_pii using its map.

    Args:
        text: Text containing placeholders (typically an external model's output).
        redaction_map: The map returned by redact_pii.
    """
    return redactor.restore(text, redaction_map)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

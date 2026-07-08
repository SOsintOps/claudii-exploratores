# Claudii Exploratores — MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io) server exposing the
Exploratores OSINT toolkit (898 tools) to any MCP client (Claude Desktop, etc.).
Built with **FastMCP**. Offline — it builds search URLs, it does not fetch pages.

## Install

```bash
cd mcp
pip install -e .          # or: uv pip install -e .
```

Requires Python 3.9+ and the `mcp` package (installed automatically).

## Run

```bash
python -m exploratores_osint_mcp.server     # stdio transport
# or, after install, the console script:
claudii-exploratores-mcp
```

## Configure a client

Claude Desktop (`claude_desktop_config.json`) — see `config.example.json`:

```json
{
  "mcpServers": {
    "claudii-exploratores": {
      "command": "python",
      "args": ["-m", "exploratores_osint_mcp.server"]
    }
  }
}
```

If installed in a virtualenv, point `command` at that interpreter, or use
`"command": "claudii-exploratores-mcp"` if the console script is on PATH.

## Tools

| Tool | Purpose |
|---|---|
| `classify_indicator(value)` | Detect the indicator type(s) with confidence scores. |
| `build_osint_urls(value, indicator_type?, categories?, fields?, include_onion?, limit?)` | Curated OSINT search-URL set for the indicator. |
| `search_catalog(query, limit?)` | Free-text search across the 898-tool catalog. |
| `list_categories()` | Categories and tool counts. |
| `verify_iban(value)` | Offline IBAN validation (ISO 13616 mod-97). |
| `redact_pii(text, only?, custom_patterns?)` | Redact PII, returning a reversible map. |
| `restore_pii(text, redaction_map)` | Reverse a redaction. |

### Example call

```jsonc
// build_osint_urls
{
  "value": "Mario Rossi",
  "indicator_type": "PERSON_NAME",
  "fields": { "firstname": "Mario", "lastname": "Rossi" },
  "limit": 20
}
```

Returns `{ value, indicator_type, candidates, categories_used, count, results[] }`
where each result is `{ id, category, label, url }`.

## Notes

- `categories: ["all"]` considers every catalog category; omit the argument to use
  the indicator type's default mapping.
- `.onion` (Tor) results are included by default; set `include_onion: false` to drop
  them. They require Tor Browser.
- Use only for authorised, lawful investigation. Results are leads to verify.

Licensed AGPL-3.0 (see repository `LICENSE`).

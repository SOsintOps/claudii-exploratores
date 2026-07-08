#!/usr/bin/env bash
# build_release.sh — regenerate the catalog and sync the shared engine into both
# deliverables (skill + MCP), then package the skill as a .skill zip.
#
# Usage:  scripts/build_release.sh [/path/to/Exploratores-3.4.1]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${1:-}"
SHARED="$ROOT/shared"
SKILL_SCRIPTS="$ROOT/skill/claudii-exploratores/scripts"
MCP_PKG="$ROOT/mcp/exploratores_osint_mcp"
DIST="$ROOT/dist"

# 1. (Optional) regenerate catalog.json from the original toolkit
if [[ -n "$SRC" && -f "$SRC/assets/js/search-library.js" ]]; then
  echo "==> Regenerating catalog.json from $SRC"
  node "$ROOT/scripts/extract_catalog.js" "$SRC" "$SHARED/catalog.json"
fi

CORE_FILES=(osint_core.py iban_tools.py redactor.py _iban_countries.py catalog.json)

echo "==> Syncing shared engine into skill/"
mkdir -p "$SKILL_SCRIPTS"
for f in "${CORE_FILES[@]}"; do cp "$SHARED/$f" "$SKILL_SCRIPTS/$f"; done

echo "==> Syncing shared engine into mcp/ package"
mkdir -p "$MCP_PKG"
for f in "${CORE_FILES[@]}"; do cp "$SHARED/$f" "$MCP_PKG/$f"; done

echo "==> Packaging .skill archive"
mkdir -p "$DIST"
( cd "$ROOT/skill" && zip -rq "$DIST/claudii-exploratores.skill" claudii-exploratores \
    -x '*/__pycache__/*' '*.pyc' )

echo "==> Done."
echo "    Skill package : $DIST/claudii-exploratores.skill"
echo "    MCP package   : $MCP_PKG"

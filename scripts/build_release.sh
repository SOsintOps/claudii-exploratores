#!/usr/bin/env bash
# build_release.sh — (optionally) re-sync the catalog from Exploratores, rebuild the
# access map and the docs, copy the shared engine into both deliverables (skill +
# MCP), then package the skill as a .skill zip.
#
# Usage:  scripts/build_release.sh [/path/to/Exploratores]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${1:-}"
PY="${PYTHON:-python3}"
command -v "$PY" >/dev/null 2>&1 || PY=python
SHARED="$ROOT/shared"
SKILL_SCRIPTS="$ROOT/skill/claudii-exploratores/scripts"
MCP_PKG="$ROOT/mcp/exploratores_osint_mcp"
DIST="$ROOT/dist"

# 1. (Optional) regenerate catalog.json from the Exploratores export
if [[ -n "$SRC" ]]; then
  echo "==> Syncing catalog.json from $SRC"
  "$PY" "$ROOT/scripts/sync_catalog.py" "$SRC"
fi

# 2. Desk classification, its page, and the per-host access map
echo "==> Rebuilding access classification and access map"
"$PY" "$ROOT/scripts/classify_queries.py"
"$PY" "$ROOT/scripts/generate_docs.py"
"$PY" "$ROOT/scripts/build_access_map.py"
"$PY" "$ROOT/scripts/generate_catalog_overview.py"

CORE_FILES=(osint_core.py iban_tools.py redactor.py _iban_countries.py catalog.json access.json)

echo "==> Syncing shared engine into skill/ and mcp/"
mkdir -p "$SKILL_SCRIPTS" "$MCP_PKG"
for f in "${CORE_FILES[@]}"; do
  cp "$SHARED/$f" "$SKILL_SCRIPTS/$f"
  cp "$SHARED/$f" "$MCP_PKG/$f"
done

echo "==> Packaging .skill archive"
mkdir -p "$DIST"
rm -f "$DIST/claudii-exploratores.skill"
( cd "$ROOT/skill" && "$PY" - <<'EOF'
import os, zipfile
with zipfile.ZipFile("../dist/claudii-exploratores.skill", "w", zipfile.ZIP_DEFLATED) as z:
    for base, dirs, files in os.walk("claudii-exploratores"):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for f in sorted(files):
            if not f.endswith(".pyc"):
                z.write(os.path.join(base, f))
EOF
)

echo "==> Done."
echo "    Skill package : $DIST/claudii-exploratores.skill"
echo "    MCP package   : $MCP_PKG"

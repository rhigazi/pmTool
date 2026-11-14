#!/usr/bin/env bash
# Verifiziert ein Projekt-Setup auf Vollständigkeit und Funktion.
# Nach einem Container-Neustart ausführen: bash definitions/verify.sh
#
# Aufruf: ./verify.sh [ZIELPROJEKT]   (Default: aktuelles Verzeichnis)
# Exit 0 = Setup vollständig; Exit 1 = Befunde vorhanden.
set -uo pipefail

TARGET="${1:-$(pwd)}"
[ -e "$TARGET" ] || { echo "Ziel nicht gefunden: $TARGET" >&2; exit 1; }
TARGET="$(cd "$TARGET" && pwd)"

FAIL=0
ok()   { echo "  ✓ $1"; }
warn() { echo "  ! $1"; }
bad()  { echo "  ✗ $1"; FAIL=1; }

echo "→ Prüfe Setup in: $TARGET"

echo "1) Projektdateien"
for f in AGENTS.md opencode.jsonc \
         tools/telegram_send.py tools/tests/test_telegram_send.py \
         wissen/index.md wissen/features.md wissen/log.md \
         wissen/entscheidungen/log.md wissen/aufgaben/index.md \
         wissen/projekt/phasen.md wissen/projekt/konzept.md \
         wissen/projekt/technische-spec.md; do
  [ -e "$TARGET/$f" ] && ok "$f" || bad "$f fehlt"
done

echo "2) Subagenten"
for a in planner coder reviewer tester documenter; do
  [ -e "$TARGET/.opencode/agents/$a.md" ] && ok ".opencode/agents/$a.md" || bad ".opencode/agents/$a.md fehlt"
done

echo "3) Werkzeuge & Laufzeit"
if command -v python3 >/dev/null 2>&1; then
  ok "python3 $(python3 --version 2>&1 | cut -d' ' -f2)"
else
  bad "python3 fehlt"
fi
if python3 -m pytest --version >/dev/null 2>&1; then
  ok "pytest $(python3 -m pytest --version 2>&1 | head -1 | awk '{print $2}')"
else
  bad "pytest fehlt (setup.sh ausführen oder: python3 -m pip install pytest)"
fi

echo "4) Unit-Tests"
if [ -d "$TARGET/tools/tests" ] && python3 -m pytest "$TARGET/tools/tests/" -q >/dev/null 2>&1; then
  ok "Test-Suite bestanden"
else
  bad "Test-Suite fehlgeschlagen oder nicht vorhanden"
fi

echo "5) CLI-Smoke"
python3 "$TARGET/tools/telegram_send.py" --help >/dev/null 2>&1 \
  && ok "--help → Exit 0" || bad "--help schlägt fehl"
if python3 "$TARGET/tools/telegram_send.py" >/dev/null 2>&1; then
  bad "ohne Argument sollte Exit != 0 sein"
else
  ok "ohne Argument → Exit 1"
fi

echo "6) Globale Umgebung (Hinweise)"
[ -e "$HOME/.agents/skills/okf-knowledge-base/SKILL.md" ] \
  && ok "Skill okf-knowledge-base" || warn "Skill okf-knowledge-base nicht installiert (setup.sh --global)"
[ -e "$HOME/.agents/skills/duckdb-docs/SKILL.md" ] \
  && ok "Skill duckdb-docs" || warn "Skill duckdb-docs nicht installiert (setup.sh --global)"
[ -e "$HOME/.config/opencode/agents/coder.md" ] \
  && ok "globale Subagenten" || warn "globale Subagenten nicht installiert (setup.sh --global)"
command -v moli >/dev/null 2>&1 && ok "moli Browser" || warn "moli nicht im PATH (optional, wird von container.sh installiert)"

echo ""
if [ "$FAIL" -eq 0 ]; then
  echo "✓ Setup vollständig und funktionsfähig."
else
  echo "✗ Setup unvollständig — siehe Befunde oben."
fi
exit "$FAIL"

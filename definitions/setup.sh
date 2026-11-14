#!/usr/bin/env bash
# Installiert die OpenCode-Definitionen aus diesem Verzeichnis in ein Projekt.
#
# Aufruf:
#   ./setup.sh                       installiert in das aktuelle Verzeichnis
#   ./setup.sh /pfad/zum/projekt     installiert in das angegebene Projekt
#
# Optionen:
#   --wissen   legt zusätzlich das OKF-Wissensdatenbank-Gerüst in <projekt>/wissen/ an
#   --global   installiert die Subagenten nach ~/.config/opencode/agents/
#              und die Skill-Snapshots nach ~/.agents/skills/
#   --force    überschreibt vorhandene Dateien (sonst: vorhandene bleiben unangetastet)
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$(pwd)"
FORCE=0
GLOBAL=0
WISSEN=0

for arg in "$@"; do
  case "$arg" in
    --force)  FORCE=1 ;;
    --global) GLOBAL=1 ;;
    --wissen) WISSEN=1 ;;
    -*) echo "Unbekannte Option: $arg" >&2; exit 1 ;;
    *)  TARGET="$arg" ;;
  esac
done

mkdir -p "$TARGET"
TARGET="$(cd "$TARGET" && pwd)"

install_file() {  # $1 = Quelle, $2 = Ziel
  if [ -e "$2" ] && [ "$FORCE" -eq 0 ]; then
    echo "  übersprungen (vorhanden): $2"
    return
  fi
  mkdir -p "$(dirname "$2")"
  cp "$1" "$2"
  echo "  installiert: $2"
}

echo "→ Zielprojekt: $TARGET"

echo "1) Projektregeln (AGENTS.md)"
install_file "$SRC/AGENTS.md" "$TARGET/AGENTS.md"

echo "2) Subagenten (.opencode/agents/)"
for f in "$SRC"/agents/*.md; do
  install_file "$f" "$TARGET/.opencode/agents/$(basename "$f")"
done

echo "3) Projekt-Konfiguration (opencode.jsonc)"
install_file "$SRC/opencode.jsonc" "$TARGET/opencode.jsonc"

echo "4) Werkzeuge (tools/)"
if [ -d "$SRC/tools" ]; then
  for f in "$SRC"/tools/*; do
    [ -e "$f" ] || continue
    if [ -d "$f" ]; then
      if [ -e "$TARGET/tools/$(basename "$f")" ] && [ "$FORCE" -eq 0 ]; then
        echo "  übersprungen (vorhanden): tools/$(basename "$f")"
      else
        mkdir -p "$TARGET/tools"
        cp -r "$f" "$TARGET/tools/$(basename "$f")"
        echo "  installiert: tools/$(basename "$f")"
      fi
    else
      install_file "$f" "$TARGET/tools/$(basename "$f")"
    fi
  done
  if ! grep -q '^config\.json$' "$TARGET/.gitignore" 2>/dev/null; then
    echo "config.json" >> "$TARGET/.gitignore"
    echo "  config.json zu .gitignore hinzugefügt"
  fi
fi

if [ "$WISSEN" -eq 1 ]; then
  echo "5) OKF-Wissensdatenbank (wissen/)"
  if [ -e "$TARGET/wissen/index.md" ] && [ "$FORCE" -eq 0 ]; then
    echo "  übersprungen (vorhanden): $TARGET/wissen/"
  else
    mkdir -p "$TARGET/wissen"
    cp -r "$SRC/wissen-vorlage/." "$TARGET/wissen/"
    echo "  installiert: $TARGET/wissen/"
  fi
fi

if [ "$GLOBAL" -eq 1 ]; then
  echo "6) Global: Subagenten (~/.config/opencode/agents/)"
  for f in "$SRC"/agents/*.md; do
    install_file "$f" "$HOME/.config/opencode/agents/$(basename "$f")"
  done

  echo "7) Global: Skill-Snapshots (~/.agents/skills/)"
  for d in "$SRC"/skills/*/; do
    name="$(basename "$d")"
    if [ -e "$HOME/.agents/skills/$name" ] && [ "$FORCE" -eq 0 ]; then
      echo "  übersprungen (vorhanden): $name"
    else
      mkdir -p "$HOME/.agents/skills"
      cp -r "$d" "$HOME/.agents/skills/$name"
      echo "  installiert: $name"
    fi
  done
fi

echo "8) Dev-Abhängigkeiten (pytest)"
if python3 -m pytest --version >/dev/null 2>&1; then
  echo "  übersprungen (vorhanden): pytest"
else
  python3 -m pip install --quiet pytest && echo "  installiert: pytest" || echo "  Warnung: pytest konnte nicht installiert werden"
fi

echo "✓ Fertig."

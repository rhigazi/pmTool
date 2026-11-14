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

copy_tree() {  # $1 = Quellverzeichnis, $2 = Zielverzeichnis (ohne __pycache__/*.pyc)
  mkdir -p "$2"
  find "$1" -type d ! -name '__pycache__' -print0 |
    while IFS= read -r -d '' verzeichnis; do
      mkdir -p "$2${verzeichnis#"$1"}"
    done
  find "$1" -type f ! -path '*/__pycache__/*' ! -name '*.pyc' -print0 |
    while IFS= read -r -d '' datei; do
      ziel="$2${datei#"$1"}"
      mkdir -p "$(dirname "$ziel")"
      cp "$datei" "$ziel"
    done
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

  echo "8) Global: Wichtige Skills & Browser (npx/curl)"
  if command -v npx >/dev/null 2>&1; then
    ( cd "$HOME" && npx skills add https://github.com/inkeep/open-knowledge-skills --skill okf-knowledge-base ) \
      || echo "  Warnung: okf-knowledge-base konnte nicht installiert werden"
  else
    echo "  Warnung: npx nicht gefunden – okf-knowledge-base übersprungen"
  fi

  curl --proto '=https' --tlsv1.2 -fsSL \
    https://github.com/lexmount/moli/releases/latest/download/moli-installer.sh | sh \
    || echo "  Warnung: moli-Installer fehlgeschlagen"
fi

echo "8) Dev-Abhängigkeiten (pytest)"
if python3 -m pytest --version >/dev/null 2>&1; then
  echo "  übersprungen (vorhanden): pytest"
else
  python3 -m pip install --quiet pytest && echo "  installiert: pytest" || echo "  Warnung: pytest konnte nicht installiert werden"
fi

echo "9) App (app/)"
if [ -d "$SRC/app" ]; then
  for f in "$SRC"/app/*; do
    [ -e "$f" ] || continue
    name="$(basename "$f")"
    case "$name" in
      __pycache__|.pytest_cache) continue ;;
    esac
    if [ -d "$f" ]; then
      if [ -e "$TARGET/app/$name" ] && [ "$FORCE" -eq 0 ]; then
        echo "  übersprungen (vorhanden): app/$name"
      else
        copy_tree "$f" "$TARGET/app/$name"
        echo "  installiert: app/$name"
      fi
    else
      install_file "$f" "$TARGET/app/$name"
    fi
  done
fi

echo "✓ Fertig."

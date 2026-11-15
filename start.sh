#!/usr/bin/env bash
# Stellt die Arbeitsumgebung wieder her: Pakete prüfen, Projektstruktur prüfen,
# Setup verifizieren und den App-Server starten.
#
# Aufruf:
#   bash start.sh            lokal: Server auf http://localhost:5000 (BUNDLE_ROOT=$PROJEKT/wissen, absolut)
#   bash start.sh --colab    Colab: startet definitions/app/start_colab.py (Port-Freigabe im Browser)
#   bash start.sh --neu      wissen/ auf die leere Vorlage zurücksetzen (mit Backup), dann starten
#
# Optionen:
#   --neu           Reset ohne Rückfrage über tools/neues_projekt.py (Backup), dann Start
#   --skip-verify   überspringt die Setup-Prüfung (verify.sh)
#   --dry-run       zeigt nur, was getan würde — installiert, löscht und startet nichts; verify.sh wird dabei still übersprungen
#   -h, --help      zeigt diese Hilfe
#
# Bei vorbefülltem wissen/ fragt der Start interaktiv nach einem neuen, leeren
# Projekt. Ohne TTY oder Bestätigung wird nichts gelöscht (fail-safe).
set -euo pipefail

PROJEKT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Reset-Ziel ist immer <Projekt>/wissen: tools/neues_projekt.py ignoriert BUNDLE_ROOT.
RESET_ZIEL="$PROJEKT/wissen"
BUNDLE_ROOT="${BUNDLE_ROOT:-$RESET_ZIEL}"
PORT="${PORT:-5000}"
MODUS="lokal"
DRY_RUN=0
MIT_VERIFY=1
NEU=0
PORT_BELEGT=0
HINWEIS_GEZEIGT=0

# (pip-Paket, Importname) — geprüft wird der Importname.
PAKETE=("flask:flask" "pyyaml:yaml" "pytest:pytest")

# Marker des mitgelieferten pmTool-Projekts: Dateien, die nur der Referenzstand
# mitbringt — die Vorlage (definitions/wissen-vorlage/) legt sie nie an. Eine
# Liste statt einer Einzeldatei, damit eine Umbenennung die Erkennung nicht
# still abschaltet.
PROJEKT_MARKER=(
  "aufgaben/a1-okf-bundle.md"
  "features/okf-projekt-manager-spa.md"
)

# Einzige Reset-Implementierung ist tools/neues_projekt.py (A24), von setup.sh
# dorthin installiert. Die Quelle definitions/tools/ dient bewusst nicht als
# Fallback: ein Reset darf nie mit einem nicht installierten Werkzeug laufen.
NEUES_PROJEKT="$PROJEKT/tools/neues_projekt.py"

info()   { printf '%s\n' "$*"; }
ok()     { printf '  ✓ %s\n' "$*"; }
warn()   { printf '  ! %s\n' "$*"; }
fehler() { printf '  ✗ %s\n' "$*" >&2; }

hilfe() {
  sed -n '2,17p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

for arg in "$@"; do
  case "$arg" in
    --colab)       MODUS="colab" ;;
    --neu)         NEU=1 ;;
    --dry-run)     DRY_RUN=1 ;;
    --skip-verify) MIT_VERIFY=0 ;;
    -h|--help)     hilfe; exit 0 ;;
    *) echo "Unbekannte Option: $arg (bash start.sh --help)" >&2; exit 1 ;;
  esac
done

pruefe_python() {
  if command -v python3 >/dev/null 2>&1; then
    ok "python3 $(python3 --version 2>&1 | cut -d' ' -f2)"
  else
    warn "python3 fehlt — bitte Python 3 installieren (in Colab vorhanden)."
    exit 1
  fi
}

pruefe_struktur() {
  local fehlt=0 verzeichnis
  for verzeichnis in wissen definitions; do
    if [ "$verzeichnis" = "wissen" ] && [ "$NEU" -eq 1 ]; then
      # --neu legt ein fehlendes Bundle aus der Vorlage an (tools/neues_projekt.py).
      continue
    fi
    if [ -d "$PROJEKT/$verzeichnis" ]; then
      ok "$verzeichnis/"
    else
      warn "$verzeichnis/ fehlt — falsches Verzeichnis oder unvollständiger Clone?"
      fehlt=1
    fi
  done
  [ "$fehlt" -eq 0 ] || {
    info "Abbruch: bitte im Projektwurzelverzeichnis arbeiten (git clone https://github.com/rhigazi/pmTool → cd pmTool)."
    exit 1
  }
}

installiere_pakete() {
  local fehlend=() eintrag paket modul
  for eintrag in "${PAKETE[@]}"; do
    paket="${eintrag%%:*}"
    modul="${eintrag##*:}"
    if python3 -c 'import importlib.util, sys; sys.exit(0 if importlib.util.find_spec(sys.argv[1]) else 1)' "$modul"; then
      ok "$paket vorhanden"
    else
      fehlend+=("$paket")
    fi
  done

  if [ "${#fehlend[@]}" -eq 0 ]; then
    return 0
  fi
  if [ "$DRY_RUN" -eq 1 ]; then
    warn "würde installieren: ${fehlend[*]}"
    return 0
  fi
  info "→ Installiere fehlende Pakete: ${fehlend[*]}"
  python3 -m pip install --quiet "${fehlend[@]}"
}

pruefe_telegram() {
  if [ -f "$PROJEKT/config.json" ]; then
    ok "config.json vorhanden (Telegram)"
  else
    warn "config.json fehlt (gitignored) — Telegram-Benachrichtigungen sind deaktiviert."
    info "   Anlegen über die Colab-Secrets-Zelle, siehe docs/colab-start.md (nicht committen)."
  fi
}

wissen_vorbefuellt() {
  local marker
  for marker in "${PROJEKT_MARKER[@]}"; do
    # Marker am Reset-Ziel prüfen, nicht am (abweichend möglichen) BUNDLE_ROOT.
    if [ -f "$RESET_ZIEL/$marker" ]; then
      return 0
    fi
  done
  return 1
}

warnung_reset_ziel() {
  if [ "$BUNDLE_ROOT" != "$RESET_ZIEL" ]; then
    info "    Achtung: BUNDLE_ROOT=$BUNDLE_ROOT weicht ab — der Reset wirkt auf $RESET_ZIEL, nicht auf $BUNDLE_ROOT."
  fi
}

neues_projekt_hinweis() {
  local art="$1"
  warn "Dieses Repo enthält die Projekt-Daten des pmTool-Vorbilds in $RESET_ZIEL."
  warnung_reset_ziel
  HINWEIS_GEZEIGT=1
  case "$art" in
    tty)
      info "    Ein neues, leeres Projekt setzt $RESET_ZIEL auf die Vorlage zurück."
      info "    Werkzeug: tools/neues_projekt.py — vorher entsteht ein Backup"
      info "    wissen-backup-YYYYMMDD-HHMMSS.tar.gz im Projekt-Root."
      info "    Ohne Zustimmung wird nichts gelöscht."
      ;;
    dry-run)
      info "    Trockenlauf: Es wird nichts zurückgesetzt und nichts gelöscht."
      info "    Plan ansehen:    bash start.sh --neu --dry-run"
      info "    Reset ausführen: bash start.sh --neu"
      ;;
    *)
      info "    Kein interaktives Terminal — es wird nichts gelöscht (fail-safe)."
      info "    Neues leeres Projekt:  bash start.sh --neu"
      info "    Nur den Plan ansehen:  bash start.sh --neu --dry-run"
      info "    Direkt:                python3 tools/neues_projekt.py --ja"
      ;;
  esac
}

ist_zustimmung() {
  case "$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')" in
    j|ja|y|yes) return 0 ;;
    *) return 1 ;;
  esac
}

starte_neues_projekt() {
  local ausfuehren="$1"
  if [ ! -f "$NEUES_PROJEKT" ]; then
    fehler "Werkzeug fehlt: tools/neues_projekt.py — Reset nicht möglich (es wird nichts gelöscht)."
    exit 1
  fi

  if [ "$HINWEIS_GEZEIGT" -eq 0 ]; then
    warnung_reset_ziel
  fi

  if [ "$ausfuehren" -eq 1 ]; then
    info "→ Neues Projekt beginnen (Backup + Vorlage): python3 $NEUES_PROJEKT --ja"
    if ! python3 "$NEUES_PROJEKT" --ja; then
      fehler "Reset fehlgeschlagen — Start abgebrochen, damit kein Halbzustand startet."
      exit 1
    fi
  else
    info "→ Neues Projekt — Plan (ändert nichts): python3 $NEUES_PROJEKT"
    if ! python3 "$NEUES_PROJEKT"; then
      fehler "Plan des Resets fehlgeschlagen — Start abgebrochen."
      exit 1
    fi
  fi
}

pruefe_projektstand() {
  # K7: Port zuerst prüfen — ein laufender Server soll keinen Reset auslösen,
  # den der Nutzer nur wegen des zweiten Starts begonnen hätte.
  if [ "$DRY_RUN" -eq 0 ] && port_belegt; then
    PORT_BELEGT=1
    info "→ Port $PORT ist bereits belegt — der Server läuft vermutlich schon: http://localhost:$PORT"
    info "→ Kein zweiter Start, kein Projekt-Reset."
    return 0
  fi

  if [ "$NEU" -eq 1 ]; then
    if [ "$DRY_RUN" -eq 1 ]; then
      starte_neues_projekt 0
    else
      starte_neues_projekt 1
    fi
    return 0
  fi

  wissen_vorbefuellt || return 0

  if [ "$DRY_RUN" -eq 1 ]; then
    neues_projekt_hinweis "dry-run"
    return 0
  fi
  if [ ! -t 0 ]; then
    neues_projekt_hinweis "kein-tty"
    return 0
  fi

  neues_projekt_hinweis "tty"
  printf '  Neues leeres Projekt beginnen? [j/N] '
  local antwort=""
  if ! read -r antwort; then
    antwort=""
  fi
  if ist_zustimmung "$antwort"; then
    starte_neues_projekt 1
  else
    info "→ Nein: Start unverändert, wissen/ bleibt bestehen."
  fi
}

fuehre_verify_aus() {
  local verify="$PROJEKT/definitions/verify.sh"
  if [ "$MIT_VERIFY" -eq 0 ] || [ "$DRY_RUN" -eq 1 ]; then
    return 0
  fi
  if [ ! -f "$verify" ]; then
    warn "definitions/verify.sh nicht gefunden — Prüfung übersprungen."
    return 0
  fi
  info "→ Setup-Prüfung (definitions/verify.sh):"
  bash "$verify" "$PROJEKT" || warn "verify.sh meldet Befunde — Start wird trotzdem fortgesetzt."
}

port_belegt() {
  python3 - "$PORT" <<'PY'
import socket
import sys

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
    probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        probe.bind(("127.0.0.1", int(sys.argv[1])))
    except OSError:
        sys.exit(0)
sys.exit(1)
PY
}

starte_server() {
  local server="$PROJEKT/app/server.py"
  [ -f "$server" ] || server="$PROJEKT/definitions/app/server.py"
  if [ ! -f "$server" ]; then
    warn "server.py nicht gefunden (app/ oder definitions/app/) — bitte zuerst setup.sh ausführen."
    exit 1
  fi

  local url="http://localhost:$PORT"
  if [ "$DRY_RUN" -eq 1 ]; then
    info "→ würde starten: BUNDLE_ROOT=$BUNDLE_ROOT PORT=$PORT python3 $server"
    info "→ URL: $url"
    return 0
  fi

  if [ "$PORT_BELEGT" -eq 1 ]; then
    info "→ Kein zweiter Start: Port $PORT ist belegt."
    return 0
  fi

  if port_belegt; then
    info "Port $PORT ist bereits belegt — der Server läuft vermutlich schon: $url"
    info "Kein zweiter Start."
    return 0
  fi

  info "→ Server startet: $url  (Beenden mit Strg+C)"
  BUNDLE_ROOT="$BUNDLE_ROOT" PORT="$PORT" python3 "$server" &
  local pid=$!
  trap 'kill "$pid" 2>/dev/null || true' INT TERM

  local status=0
  wait "$pid" || status=$?
  trap - INT TERM

  if [ "$status" -ne 0 ] && [ "$status" -ne 130 ]; then
    warn "Server wurde mit Status $status beendet."
    return "$status"
  fi
  info "→ Server beendet."
}

starte_colab() {
  local start="$PROJEKT/definitions/app/start_colab.py"
  if [ ! -f "$start" ]; then
    warn "definitions/app/start_colab.py nicht gefunden — bitte im Projektwurzelverzeichnis arbeiten."
    exit 1
  fi
  if [ "$PORT_BELEGT" -eq 1 ]; then
    info "→ Kein zweiter Start: Port $PORT ist belegt (in Colab bei Bedarf die Runtime neu starten)."
    return 0
  fi
  if [ "$DRY_RUN" -eq 1 ]; then
    info "→ würde aufrufen: python3 $start"
    return 0
  fi
  info "→ Colab-Start: python3 definitions/app/start_colab.py (gibt Port $PORT im Browser frei)"
  # Kein eigener Trap: Strg+C erreicht die Prozessgruppe; start_colab.py beendet
  # sich per KeyboardInterrupt und der Server-Subprozess erhält das Signal ebenfalls.
  PORT="$PORT" python3 "$start"
}

info "→ Umgebung wiederherstellen (Modus: $MODUS, Projekt: $PROJEKT)"

echo "1) Python"
pruefe_python

echo "2) Projektstruktur"
pruefe_struktur

echo "3) Abhängigkeiten"
installiere_pakete

echo "4) Telegram-Konfiguration"
pruefe_telegram

echo "5) Projektstand"
pruefe_projektstand

echo "6) Setup-Prüfung"
fuehre_verify_aus

if [ "$MODUS" = "colab" ]; then
  echo "7) App starten"
  starte_colab
else
  echo "7) App starten"
  starte_server
fi

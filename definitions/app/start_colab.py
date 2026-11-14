#!/usr/bin/env python3
"""Colab-Startzelle für den OKF Projekt-Manager (Aufgabe A16).

Prüft/installiert die Laufzeitpakete ``flask`` und ``pyyaml`` nur bei Bedarf,
startet ``server.py`` als Subprozess auf dem Bundle und gibt den Port über die
eingebaute Colab-Funktion im Browser frei. Ohne Colab wird die lokale URL
ausgegeben. Das Bundle wird ausschließlich lesend verwendet.
"""

from __future__ import annotations

import importlib.util
import os
import socket
import subprocess
import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
SERVER = APP_DIR / "server.py"

BUNDLE_ROOT = "/content/pmTool/wissen"
PORT_STANDARD = 5000
# Wie ``server.HOST``: geprüft wird die Adresse, an die der Server bindet.
HOST = "0.0.0.0"

# (pip-Paket, Importname) — geprüft wird der Importname.
PAKETE = (("flask", "flask"), ("pyyaml", "yaml"))


def main() -> int:
    """Startet den Server, falls nötig, und gibt den Port frei; Rückgabe: Exit-Code."""
    fehlende = _fehlende_pakete()
    if fehlende and not _installiere(fehlende):
        return 1

    weiter_fehlen = _fehlende_pakete()
    if weiter_fehlen:
        print(
            "Start abgebrochen: Benötigte Pakete fehlen weiterhin: "
            f"{', '.join(weiter_fehlen)}. Bitte manuell installieren.",
            file=sys.stderr,
        )
        return 1

    port = _port_aus_umgebung()
    url = f"http://localhost:{port}"

    if _port_belegt(port):
        print(f"OKF Projekt-Manager läuft bereits unter {url} — kein zweiter Start.", flush=True)
        return 0

    prozess = _starte_server(port)
    print(f"Server gestartet (PID {prozess.pid}) für {BUNDLE_ROOT}", flush=True)

    if _oeffne_colab_fenster(port):
        print(f"Colab-Fenster für Port {port} geöffnet: {url}", flush=True)
    else:
        print(f"Colab-Port-Freigabe nicht verfügbar — bitte im Browser öffnen: {url}", flush=True)
    return 0


def _fehlende_pakete() -> list[str]:
    """pip-Pakete, deren Importmodul nicht auffindbar ist."""
    return [paket for paket, modul in PAKETE if importlib.util.find_spec(modul) is None]


def _installiere(pakete: list[str]) -> bool:
    """Installiert die Pakete per pip; ``False``, wenn pip scheitert."""
    print(f"Installiere fehlende Pakete: {', '.join(pakete)}", flush=True)
    ergebnis = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--quiet", *pakete],
        check=False,
    )
    if ergebnis.returncode != 0:
        print(
            f"Paketinstallation fehlgeschlagen (pip-Exit {ergebnis.returncode}): "
            f"{', '.join(pakete)}",
            file=sys.stderr,
        )
        return False
    return True


def _port_aus_umgebung() -> int:
    """``PORT`` aus der Umgebung, sonst :data:`PORT_STANDARD`."""
    roh = os.environ.get("PORT", "").strip()
    if not roh:
        return PORT_STANDARD
    try:
        port = int(roh)
    except ValueError:
        print(f"PORT ist keine Zahl ({roh!r}) — verwende {PORT_STANDARD}.", file=sys.stderr)
        return PORT_STANDARD
    if not 1 <= port <= 65535:
        print(f"PORT liegt außerhalb von 1–65535 ({port}) — verwende {PORT_STANDARD}.", file=sys.stderr)
        return PORT_STANDARD
    return port


def _port_belegt(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            probe.bind((HOST, port))
        except OSError:
            return True
    return False


def _starte_server(port: int) -> subprocess.Popen:
    umgebung = {**os.environ, "BUNDLE_ROOT": BUNDLE_ROOT, "PORT": str(port)}
    return subprocess.Popen([sys.executable, str(SERVER)], env=umgebung)


def _oeffne_colab_fenster(port: int) -> bool:
    """Gibt den Port in Colab frei; ``False``, wenn die Freigabe nicht verfügbar ist."""
    try:
        from google.colab import output  # nur in Colab vorhanden
    except ImportError:
        return False

    try:
        output.serve_kernel_port_as_window(port)
    except Exception as fehler:
        print(f"Colab-Port-Freigabe fehlgeschlagen: {fehler}", file=sys.stderr)
        return False
    return True


if __name__ == "__main__":
    sys.exit(main())

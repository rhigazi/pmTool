#!/usr/bin/env python3
"""Colab-Startzelle für den OKF Projekt-Manager (Aufgabe A16).

Prüft/installiert die Laufzeitpakete ``flask`` und ``pyyaml`` nur bei Bedarf,
startet ``server.py`` als Subprozess auf dem Bundle und zeigt die App über den
Kernel-Kanal in der Notebook-Zelle (``serve_kernel_port_as_iframe``). Nur als
Fallback dient das veraltete ``serve_kernel_port_as_window``; ohne Colab wird
die lokale URL ausgegeben. Das Bundle wird ausschließlich lesend verwendet.

Die Port-Freigabe funktioniert nur im Notebook-Kernel, deshalb ist der
Kernel-Aufruf mit absolutem Pfad der vorgesehene Weg::

    %run /content/pmTool/definitions/app/start_colab.py

Ein Start als Unterprozess (``!python3 start_colab.py``) hat keinen
Kernel-Kanal; das Skript erklärt dann, wie die Freigabe nachzuholen ist.
"""

from __future__ import annotations

import builtins
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

# Ergebnis-Arten der Port-Freigabe (siehe ``_gib_port_frei``).
FREIGABE_IFRAME = "iframe"
FREIGABE_FENSTER = "fenster"


def _hinweis_port_freigabe(port: int) -> str:
    """Handlungsanweisung mit absolutem Skriptpfad.

    Relativ (`%run definitions/app/start_colab.py`) schlägt der Aufruf in Colab
    fehl, weil das Notebook-Verzeichnis `/content` ist, nicht die Projektwurzel.
    """
    skript = Path(__file__).resolve()
    return (
        f"Port-Freigabe nur aus einer Notebook-Zelle möglich — bitte "
        f"`%run {skript}` in einer Code-Zelle ausführen "
        f"(alternativ in laufender Sitzung: "
        f"`from google.colab import output; output.serve_kernel_port_as_iframe({port})`)."
    )


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
        print(f"OKF Projekt-Manager läuft bereits auf Port {port} — kein zweiter Start.", flush=True)
        return 0

    prozess = _starte_server(port)
    print(f"Server gestartet (PID {prozess.pid}) für {BUNDLE_ROOT}", flush=True)

    freigabe = _gib_port_frei(port)
    if freigabe == FREIGABE_IFRAME:
        print(f"App wird in der Notebook-Zelle angezeigt (Port {port}).", flush=True)
    elif freigabe == FREIGABE_FENSTER:
        print(
            f"App wird im Browserfenster geöffnet (Port {port}) — "
            "serve_kernel_port_as_window ist veraltet.",
            flush=True,
        )
    elif _colab_output() is not None:
        # Colab-Laufzeit vorhanden, aber kein Kernel-Kanal: Freigabe nachholbar.
        print(f"Port-Freigabe nicht verfügbar — Server läuft (Port {port}).", flush=True)
        print(_hinweis_port_freigabe(port), flush=True)
    else:
        print(f"Lokaler Modus (kein Colab) — bitte im Browser öffnen: {url}", flush=True)
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


def _colab_output():
    """``google.colab.output``, falls vorhanden, sonst ``None``."""
    try:
        from google.colab import output  # nur in Colab vorhanden
    except ImportError:
        return None
    return output


def _gib_port_frei(port: int) -> str | None:
    """Zeigt die App über den Kernel-Kanal; Rückgabe: Art der Freigabe oder ``None``.

    Primär ``serve_kernel_port_as_iframe`` (App erscheint in der Zelle). Nur wenn
    die Funktion fehlt oder scheitert, folgt das veraltete
    ``serve_kernel_port_as_window``. Beide wirken nur im Notebook-Kernel — im
    Unterprozess fehlt der Kanal und der Aufruf scheitert.
    """
    output = _colab_output()
    if output is None:
        return None

    iframe = getattr(output, "serve_kernel_port_as_iframe", None)
    if iframe is not None:
        try:
            iframe(port)
            return FREIGABE_IFRAME
        except Exception as fehler:
            print(f"Colab-Port-Freigabe als iframe fehlgeschlagen: {fehler}", file=sys.stderr)

    fenster = getattr(output, "serve_kernel_port_as_window", None)
    if fenster is None:
        return None

    print(
        "Fallback auf das veraltete serve_kernel_port_as_window (Deprecation-Warnung in Colab).",
        file=sys.stderr,
    )
    try:
        fenster(port)
    except Exception as fehler:
        print(f"Colab-Port-Freigabe als Fenster fehlgeschlagen: {fehler}", file=sys.stderr)
        return None
    return FREIGABE_FENSTER


def _laeuft_im_kernel() -> bool:
    """``True``, wenn der Code im Notebook-Kernel läuft (dort gibt es einen Kernel-Kanal)."""
    get_ipython = getattr(builtins, "get_ipython", None)
    return get_ipython is not None and get_ipython() is not None


if __name__ == "__main__":
    # Im Kernel (``%run``) kein ``sys.exit``: ein SystemExit bliebe dort als Fehlerzeile stehen.
    if _laeuft_im_kernel():
        main()
    else:
        sys.exit(main())

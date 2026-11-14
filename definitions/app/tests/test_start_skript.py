"""TDD-Tests für das Startskript ``start.sh`` (Aufgabe A18).

``start.sh`` ist ein Repo-Werkzeug im Projektwurzelverzeichnis (neben
``definitions/``) und wird von ``setup.sh`` **nicht** verteilt. Im verteilten
Zielprojekt fehlt es daher; dort überspringt sich dieses Modul selbst.

Das Skript wird ausschließlich im ``--dry-run``-Modus aufgerufen: Es werden
keine Pakete installiert und keine Serverprozesse gestartet.
"""

import os
import subprocess
from pathlib import Path

import pytest

PROJEKT = Path(__file__).resolve().parents[3]
START = PROJEKT / "start.sh"

pytestmark = pytest.mark.skipif(
    not (PROJEKT / "definitions" / "setup.sh").is_file(),
    reason="start.sh ist ein Repo-Root-Werkzeug und wird nicht mitverteilt",
)


def starte(*argumente: str) -> subprocess.CompletedProcess:
    """Führt ``start.sh`` mit Argumenten im Projektwurzelverzeichnis aus."""
    return subprocess.run(
        ["bash", str(START), *argumente],
        cwd=PROJEKT,
        capture_output=True,
        text=True,
        timeout=120,
    )


def test_skript_existiert_ausfuehrbar_und_nutzt_bash():
    assert START.is_file()
    assert os.access(START, os.X_OK)
    assert START.read_text(encoding="utf-8").startswith("#!/usr/bin/env bash")


def test_bash_syntax_ist_gueltig():
    pruefung = subprocess.run(["bash", "-n", str(START)], capture_output=True, text=True)
    assert pruefung.returncode == 0, pruefung.stderr


def test_colab_modus_ruft_start_colab_auf():
    ergebnis = starte("--colab", "--dry-run")

    assert ergebnis.returncode == 0, ergebnis.stderr
    assert "definitions/app/start_colab.py" in ergebnis.stdout


def test_lokal_modus_bereitet_serverstart_vor():
    ergebnis = starte("--dry-run")

    assert ergebnis.returncode == 0, ergebnis.stderr
    assert "server.py" in ergebnis.stdout
    assert "würde starten" in ergebnis.stdout
    assert "http://localhost:5000" in ergebnis.stdout
    assert "BUNDLE_ROOT" in ergebnis.stdout


def test_dry_run_startet_keinen_server():
    ergebnis = starte("--dry-run")

    assert "Server startet" not in ergebnis.stdout


def test_telegram_hinweis_wird_gegeben():
    ergebnis = starte("--dry-run")

    assert "config.json" in ergebnis.stdout
    assert "docs/colab-start.md" in ergebnis.stdout


def test_unbekannte_option_bricht_ab():
    ergebnis = starte("--gibt-es-nicht")

    assert ergebnis.returncode != 0
    assert "Unbekannte Option" in ergebnis.stderr

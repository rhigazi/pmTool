"""Tests für die App-Verteilung über ``setup.sh``/``verify.sh`` (Aufgabe A15).

Die Tests führen die Skripte aus ``definitions/`` gegen ``tmp_path``-Projekte aus
und prüfen Erstinstallation, Idempotenz, ``--force``, Bestandsschutz, die
Verify-Prüfungen und den Erhalt der bestehenden Setup-Abschnitte.

Im verteilten Zielprojekt liegt diese Datei unter ``<ziel>/app/tests/``; dort
fehlt ``setup.sh`` im Projektwurzelverzeichnis, weshalb das Modul sich selbst
überspringt. So ruft kein verteilter Testlauf die Skripte erneut auf.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

DEFINITIONS = Path(__file__).resolve().parents[2]
SETUP = DEFINITIONS / "setup.sh"
VERIFY = DEFINITIONS / "verify.sh"

pytestmark = pytest.mark.skipif(
    not (SETUP.is_file() and VERIFY.is_file()),
    reason="Setup-Skripte nur im Definitions-Repo vorhanden",
)


def _laeuft(befehl: list[str], ziel: Path | None = None) -> subprocess.CompletedProcess:
    """Führt ein Skript mit Prozessumgebung aus und fängt die Ausgabe ab."""
    return subprocess.run(
        befehl,
        cwd=str(ziel) if ziel else None,
        env=dict(os.environ),
        capture_output=True,
        text=True,
        check=False,
    )


def _setup(ziel: Path, *optionen: str) -> subprocess.CompletedProcess:
    return _laeuft(["bash", str(SETUP), str(ziel), *optionen])


def _verify(ziel: Path) -> subprocess.CompletedProcess:
    return _laeuft(["bash", str(VERIFY), str(ziel)])


def _pytest(tests: Path) -> subprocess.CompletedProcess:
    return _laeuft(
        [sys.executable, "-m", "pytest", str(tests), "-q", "-p", "no:cacheprovider"]
    )


# --- T1: Erstinstallation -------------------------------------------------


def test_t1_erstinstallation(tmp_path):
    ziel = tmp_path / "projekt"

    ergebnis = _setup(ziel)

    assert ergebnis.returncode == 0, ergebnis.stderr
    for datei in (
        "app/server.py",
        "app/okf_bundle.py",
        "app/static/index.html",
        "app/static/style.css",
        "app/tests/test_server.py",
        "app/tests/conftest.py",
        "app/tests/fixtures/bundle_min/index.md",
    ):
        assert (ziel / datei).is_file(), f"{datei} fehlt nach der Installation"


def test_t1b_keine_cache_artefakte(tmp_path):
    ziel = tmp_path / "projekt"
    (DEFINITIONS / "app" / "__pycache__").mkdir(exist_ok=True)

    ergebnis = _setup(ziel)

    assert ergebnis.returncode == 0, ergebnis.stderr
    assert not list(ziel.rglob("__pycache__"))
    assert not list(ziel.rglob("*.pyc"))
    assert not list(ziel.rglob(".pytest_cache"))


# --- T2: Idempotenz -------------------------------------------------------


def test_t2_idempotenz(tmp_path):
    ziel = tmp_path / "projekt"
    assert _setup(ziel).returncode == 0
    server = ziel / "app/server.py"
    vorher = server.read_bytes()

    ergebnis = _setup(ziel)

    assert ergebnis.returncode == 0, ergebnis.stderr
    assert "übersprungen (vorhanden): app/server.py" in ergebnis.stdout
    assert server.read_bytes() == vorher


# --- T3: --force ----------------------------------------------------------


def test_t3_force_setzt_datei_zurueck(tmp_path):
    ziel = tmp_path / "projekt"
    assert _setup(ziel).returncode == 0
    server = ziel / "app/server.py"
    original = server.read_bytes()
    server.write_text("# lokal verändert\n", encoding="utf-8")

    ergebnis = _setup(ziel, "--force")

    assert ergebnis.returncode == 0, ergebnis.stderr
    assert server.read_bytes() == original


def test_t3b_force_setzt_verzeichnis_zurueck(tmp_path):
    ziel = tmp_path / "projekt"
    assert _setup(ziel).returncode == 0
    conftest = ziel / "app/tests/conftest.py"
    original = conftest.read_bytes()
    conftest.write_text("# lokal verändert\n", encoding="utf-8")

    ergebnis = _setup(ziel, "--force")

    assert ergebnis.returncode == 0, ergebnis.stderr
    assert conftest.read_bytes() == original
    assert not (ziel / "app/tests/tests").exists()


# --- T4: Bestandsschutz ---------------------------------------------------


def test_t4_bestandsschutz(tmp_path):
    ziel = tmp_path / "projekt"
    ziel.mkdir()
    agents = ziel / "AGENTS.md"
    agents.write_text("# Eigene Regeln\n\nMARKER-4711\n", encoding="utf-8")
    eigener_anhang = ziel / "app/tests/test_eigen.py"
    eigener_anhang.parent.mkdir(parents=True)
    eigener_anhang.write_text("# eigener Test\n", encoding="utf-8")

    ergebnis = _setup(ziel)

    assert ergebnis.returncode == 0, ergebnis.stderr
    assert "MARKER-4711" in agents.read_text(encoding="utf-8")
    assert eigener_anhang.read_text(encoding="utf-8") == "# eigener Test\n"


# --- T5: Verify grün ------------------------------------------------------


def test_t5_verify_gruen(tmp_path):
    ziel = tmp_path / "projekt"
    assert _setup(ziel, "--wissen").returncode == 0

    ergebnis = _verify(ziel)

    assert ergebnis.returncode == 0, ergebnis.stdout + ergebnis.stderr
    assert "app/server.py" in ergebnis.stdout
    assert "app/static/index.html" in ergebnis.stdout


# --- T6: Verify rot -------------------------------------------------------


def test_t6_verify_nennt_fehlende_app_datei(tmp_path):
    ziel = tmp_path / "projekt"
    assert _setup(ziel, "--wissen").returncode == 0
    (ziel / "app/server.py").unlink()

    ergebnis = _verify(ziel)

    assert ergebnis.returncode == 1
    assert "app/server.py" in ergebnis.stdout


def test_t6b_verify_rot_ohne_app_verzeichnis(tmp_path):
    ziel = tmp_path / "projekt"
    assert _setup(ziel, "--wissen").returncode == 0
    (ziel / "app/static/index.html").unlink(missing_ok=True)

    ergebnis = _verify(ziel)

    assert ergebnis.returncode == 1
    assert "app/static/index.html" in ergebnis.stdout


# --- T7: Tests mitverteilt ------------------------------------------------


def test_t7_tests_mitverteilt(tmp_path):
    ziel = tmp_path / "projekt"
    assert _setup(ziel).returncode == 0

    ergebnis = _pytest(ziel / "app/tests")

    assert ergebnis.returncode == 0, ergebnis.stdout + ergebnis.stderr


# --- T8: Keine Regression der bestehenden Abschnitte ----------------------


def test_t8_bestehende_abschnitte(tmp_path):
    ziel = tmp_path / "projekt"

    ergebnis = _setup(ziel, "--wissen")

    assert ergebnis.returncode == 0, ergebnis.stderr
    for nummer in ("1)", "2)", "3)", "4)", "5)", "8)", "9)"):
        assert f"{nummer} " in ergebnis.stdout, f"Abschnitt {nummer} fehlt"
    quelle = SETUP.read_text(encoding="utf-8")
    assert "6) Global: Subagenten" in quelle
    assert "7) Global: Skill-Snapshots" in quelle

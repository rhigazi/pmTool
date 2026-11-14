"""Tests für die App-Verteilung über ``setup.sh``/``verify.sh`` (Aufgabe A15).

Die Tests führen die Skripte aus ``definitions/`` gegen ``tmp_path``-Projekte aus
und prüfen Erstinstallation, Idempotenz, ``--force``, Bestandsschutz, die
Verify-Prüfungen und den Erhalt der bestehenden Setup-Abschnitte.

Eine Session-Installation dient als Vorlage; jeder Test arbeitet auf einer zügig
kopierten Arbeitskopie. Die Subprozesse laufen ohne Plugin-Autoload, damit der
Start von ``pytest`` in langsamen Container-Dateisystemen nicht dominiert.

Im verteilten Zielprojekt liegt diese Datei unter ``<ziel>/app/tests/``; dort
fehlt ``setup.sh`` im Projektwurzelverzeichnis, weshalb das Modul sich selbst
überspringt. So ruft kein verteilter Testlauf die Skripte erneut auf.
"""

import os
import shutil
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


def _laeuft(befehl: list[str]) -> subprocess.CompletedProcess:
    """Führt einen Befehl mit Prozessumgebung aus und fängt die Ausgabe ab."""
    env = dict(os.environ)
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    return subprocess.run(befehl, env=env, capture_output=True, text=True, check=False)


def _setup(ziel: Path, *optionen: str) -> subprocess.CompletedProcess:
    return _laeuft(["bash", str(SETUP), str(ziel), *optionen])


def _verify(ziel: Path) -> subprocess.CompletedProcess:
    return _laeuft(["bash", str(VERIFY), str(ziel)])


def _pytest(tests: Path) -> subprocess.CompletedProcess:
    return _laeuft(
        [sys.executable, "-m", "pytest", str(tests), "-q", "-p", "no:cacheprovider"]
    )


@pytest.fixture(scope="module")
def installation(tmp_path_factory):
    """Einmalige Installation mit ``--wissen`` als Vorlage für alle Tests."""
    # Cache-Artefakt der lokalen Testläufe sicherstellen (darf nicht mitverteilt werden).
    (DEFINITIONS / "app" / "__pycache__").mkdir(exist_ok=True)
    ziel = tmp_path_factory.mktemp("vorlage") / "projekt"
    ergebnis = _setup(ziel, "--wissen")
    assert ergebnis.returncode == 0, ergebnis.stderr
    return ziel, ergebnis.stdout


@pytest.fixture()
def ziel(tmp_path, installation):
    """Arbeitskopie der Session-Installation unter ``tmp_path``."""
    vorlage, _ = installation
    kopie = tmp_path / "projekt"
    shutil.copytree(vorlage, kopie)
    return kopie


# --- T1: Erstinstallation -------------------------------------------------


def test_t1_erstinstallation(installation):
    ziel, _ = installation

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


def test_t1b_keine_cache_artefakte(installation):
    ziel, _ = installation

    assert not list(ziel.rglob("__pycache__"))
    assert not list(ziel.rglob("*.pyc"))
    assert not list(ziel.rglob(".pytest_cache"))


# --- T2: Idempotenz -------------------------------------------------------


def test_t2_idempotenz(ziel):
    server = ziel / "app/server.py"
    vorher = server.read_bytes()

    ergebnis = _setup(ziel)

    assert ergebnis.returncode == 0, ergebnis.stderr
    assert "übersprungen (vorhanden):" in ergebnis.stdout
    assert "app/server.py" in ergebnis.stdout
    assert server.read_bytes() == vorher


# --- T3: --force ----------------------------------------------------------


def test_t3_force_setzt_zurueck(ziel):
    server = ziel / "app/server.py"
    conftest = ziel / "app/tests/conftest.py"
    original = server.read_bytes()
    original_conftest = conftest.read_bytes()
    server.write_text("# lokal verändert\n", encoding="utf-8")
    conftest.write_text("# lokal verändert\n", encoding="utf-8")

    ergebnis = _setup(ziel, "--force")

    assert ergebnis.returncode == 0, ergebnis.stderr
    assert server.read_bytes() == original
    assert conftest.read_bytes() == original_conftest
    assert not (ziel / "app/tests/tests").exists()


# --- T4: Bestandsschutz ---------------------------------------------------


def test_t4_bestandsschutz(ziel):
    agents = ziel / "AGENTS.md"
    agents.write_text("# Eigene Regeln\n\nMARKER-4711\n", encoding="utf-8")
    eigener_anhang = ziel / "app/tests/test_eigen.py"
    eigener_anhang.write_text("# eigener Test\n", encoding="utf-8")

    ergebnis = _setup(ziel)

    assert ergebnis.returncode == 0, ergebnis.stderr
    assert "MARKER-4711" in agents.read_text(encoding="utf-8")
    assert eigener_anhang.read_text(encoding="utf-8") == "# eigener Test\n"


# --- T5: Verify grün ------------------------------------------------------


def test_t5_verify_gruen(ziel):
    ergebnis = _verify(ziel)

    assert ergebnis.returncode == 0, ergebnis.stdout + ergebnis.stderr
    assert "app/server.py" in ergebnis.stdout
    assert "app/static/index.html" in ergebnis.stdout


# --- T6: Verify rot -------------------------------------------------------


def test_t6_verify_nennt_fehlende_app_datei(ziel):
    (ziel / "app/server.py").unlink()

    ergebnis = _verify(ziel)

    assert ergebnis.returncode == 1
    assert "app/server.py" in ergebnis.stdout


# --- T7: Tests mitverteilt ------------------------------------------------


def test_t7_tests_mitverteilt(ziel):
    ergebnis = _pytest(ziel / "app/tests")

    assert ergebnis.returncode == 0, ergebnis.stdout + ergebnis.stderr


# --- T8: Keine Regression der bestehenden Abschnitte ----------------------


def test_t8_bestehende_abschnitte(installation):
    _, ausgabe = installation

    for nummer in ("1)", "2)", "3)", "4)", "5)", "8)", "9)"):
        assert f"{nummer} " in ausgabe, f"Abschnitt {nummer} fehlt"
    quelle = SETUP.read_text(encoding="utf-8")
    assert "6) Global: Subagenten" in quelle
    assert "7) Global: Skill-Snapshots" in quelle

"""Tests für die Verteilung der Werkzeuge über ``setup.sh`` (Aufgabe A26).

Quelle ist ``definitions/tools/`` (Single Source of Truth); ``<projekt>/tools/``
ist die von ``setup.sh`` installierte Kopie. Die Tests führen die Skripte aus
``definitions/`` gegen ``tmp_path``-Projekte aus und prüfen Verteilung,
Aufruffähigkeit, Idempotenz, Cache-Freiheit, die ``verify.sh``-Kompatibilität
sowie die Drift-Freiheit von Quelle und Spiegel im Entwicklungs-Repo.

Im verteilten Zielprojekt liegt diese Datei unter ``<ziel>/tools/tests/``; dort
fehlt ``definitions/setup.sh``, weshalb das Modul sich selbst überspringt. So
ruft kein verteilter Testlauf die Skripte erneut auf.

Das echte ``wissen/`` des Repositories wird nie angefasst: alle Läufe arbeiten
auf ``tmp_path``-Kopien.
"""

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

HIER = Path(__file__).resolve()
QUELLE = HIER.parents[1]  # definitions/tools bzw. <ziel>/tools
DEFINITIONS = QUELLE.parent
SETUP = DEFINITIONS / "setup.sh"
VERIFY = DEFINITIONS / "verify.sh"
VORLAGE = DEFINITIONS / "wissen-vorlage"
SPIEGEL = DEFINITIONS.parent / "tools"

CACHE_TEILE = frozenset({"__pycache__", ".pytest_cache"})

pytestmark = pytest.mark.skipif(
    not (SETUP.is_file() and VERIFY.is_file()),
    reason="Setup-Skripte nur im Definitions-Repo vorhanden",
)


def _laeuft(befehl, cwd=None):
    """Führt einen Befehl mit Prozessumgebung aus und fängt die Ausgabe ab."""
    env = dict(os.environ)
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    return subprocess.run(
        befehl, cwd=cwd, env=env, capture_output=True, text=True, check=False
    )


def _setup(ziel, *optionen):
    return _laeuft(["bash", str(SETUP), str(ziel), *optionen])


def _verify(ziel):
    return _laeuft(["bash", str(VERIFY), str(ziel)])


def _pytest(tests, cwd=None):
    return _laeuft(
        [sys.executable, "-m", "pytest", str(tests), "-q", "-p", "no:cacheprovider"],
        cwd=cwd,
    )


def baum(wurzel):
    """Inhalt eines Baums als ``{relativer Pfad: Inhalt-Hash}`` ohne Cache-Artefakte."""
    ergebnis = {}
    for pfad in sorted(wurzel.rglob("*")):
        rel = pfad.relative_to(wurzel)
        if CACHE_TEILE.intersection(rel.parts) or rel.suffix == ".pyc":
            continue
        if pfad.is_dir():
            ergebnis[rel.as_posix()] = "<verzeichnis>"
        else:
            ergebnis[rel.as_posix()] = hashlib.sha256(pfad.read_bytes()).hexdigest()
    return ergebnis


@pytest.fixture(scope="module")
def installation(tmp_path_factory):
    """Vollständige Installation (``--wissen``) als Vorlage für alle Tests."""
    ziel = tmp_path_factory.mktemp("verteilung") / "projekt"
    ergebnis = _setup(ziel, "--wissen")
    assert ergebnis.returncode == 0, ergebnis.stderr
    return ziel


@pytest.fixture()
def ziel(tmp_path, installation):
    """Arbeitskopie der Installation unter ``tmp_path`` (Tests bleiben isoliert)."""
    kopie = tmp_path / "projekt"
    shutil.copytree(installation, kopie)
    return kopie


# --- T1: Verteilung -------------------------------------------------------


def test_t1_werkzeug_und_test_verteilt(installation):
    assert (installation / "tools" / "neues_projekt.py").is_file()
    assert (installation / "tools" / "tests" / "test_neues_projekt.py").is_file()


def test_t1b_vorlage_und_verify_verteilt(installation):
    # Das Werkzeug liest definitions/wissen-vorlage/ und verweist auf verify.sh.
    assert (installation / "definitions" / "wissen-vorlage" / "index.md").is_file()
    assert (installation / "definitions" / "verify.sh").is_file()


# --- T2: Werkzeug läuft im Zielprojekt ------------------------------------


def test_t2_plan_lauf_im_zielprojekt_aendert_nichts(ziel):
    vorher = baum(ziel)

    ergebnis = _laeuft(
        [sys.executable, "tools/neues_projekt.py"],
        cwd=ziel,
    )

    assert ergebnis.returncode == 0, ergebnis.stderr
    assert "Plan" in ergebnis.stdout
    assert baum(ziel) == vorher
    assert not list(ziel.glob("wissen-backup-*.tar.gz"))


# --- T3: verteilte Werkzeug-Tests laufen ----------------------------------


def test_t3_verteilte_tools_tests_laufen(ziel):
    ergebnis = _pytest(ziel / "tools" / "tests")

    assert ergebnis.returncode == 0, ergebnis.stdout + ergebnis.stderr
    assert "passed" in ergebnis.stdout
    assert "failed" not in ergebnis.stdout


# --- T4/T5: Verify und Idempotenz -----------------------------------------


def test_t4_verify_vollinstallation_gruen(ziel):
    ergebnis = _verify(ziel)

    assert ergebnis.returncode == 0, ergebnis.stdout + ergebnis.stderr
    assert "Setup vollständig" in ergebnis.stdout


def test_t5_zweiter_lauf_ueberschreibt_nicht(ziel):
    werkzeug = ziel / "tools" / "neues_projekt.py"
    test = ziel / "tools" / "tests" / "test_neues_projekt.py"
    vorher = (werkzeug.read_bytes(), test.read_bytes())

    ergebnis = _setup(ziel)

    assert ergebnis.returncode == 0, ergebnis.stderr
    assert "übersprungen (vorhanden):" in ergebnis.stdout
    assert str(werkzeug) in ergebnis.stdout
    assert (werkzeug.read_bytes(), test.read_bytes()) == vorher


def test_t5b_force_ersetzt_die_kopie(ziel):
    werkzeug = ziel / "tools" / "neues_projekt.py"
    original = werkzeug.read_bytes()
    werkzeug.write_text("# lokal verändert\n", encoding="utf-8")

    ergebnis = _setup(ziel, "--force")

    assert ergebnis.returncode == 0, ergebnis.stderr
    assert werkzeug.read_bytes() == original


# --- T6: keine Cache-Artefakte -------------------------------------------


def test_t6_keine_cache_artefakte_in_tools(installation):
    tools = installation / "tools"

    assert not list(tools.rglob("__pycache__"))
    assert not list(tools.rglob("*.pyc"))
    assert not list(tools.rglob(".pytest_cache"))


# --- T7: Single Source / Drift -------------------------------------------


@pytest.mark.skipif(not SPIEGEL.is_dir(), reason="Spiegel tools/ nur im Dev-Repo")
def test_t7_quelle_und_spiegel_sind_inhaltsgleich():
    """Quelle ist ``definitions/tools/``; ``tools/`` ist nur die installierte Kopie."""
    assert baum(QUELLE) == baum(SPIEGEL), (
        "definitions/tools/ und tools/ laufen auseinander — Änderungen nur in "
        "definitions/tools/ vornehmen und den Spiegel per setup.sh --force erneuern"
    )


# --- T8: Root-Suite ohne doppelte Basisnamen -----------------------------


@pytest.mark.skipif(not SPIEGEL.is_dir(), reason="Dev-Repo-Wurzel nicht vorhanden")
def test_t8_root_suite_kollektiert_ohne_konflikt():
    ergebnis = _laeuft(
        [sys.executable, "-m", "pytest", "-q", "--collect-only", "-p", "no:cacheprovider"],
        cwd=DEFINITIONS.parent,
    )

    ausgabe = ergebnis.stdout + ergebnis.stderr
    assert ergebnis.returncode == 0, ausgabe
    assert "import file mismatch" not in ausgabe
    assert "ERROR collecting" not in ausgabe
    # Der Spiegel wird nicht zusätzlich kollektiert (jede Testdatei genau einmal).
    gesammelt = ergebnis.stdout.splitlines()
    assert not [zeile for zeile in gesammelt if zeile.startswith("tools/")]
    assert any(zeile.startswith("definitions/tools/tests/") for zeile in gesammelt)

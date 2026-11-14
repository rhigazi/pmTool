"""TDD-Tests für die Colab-Startzelle ``start_colab.py`` (Aufgabe A16).

Alle externen Wirkungen sind gemockt: Colab-Port-Freigabe, ``subprocess`` und
die Portprüfung. Ein echter ``server.py``-Prozess wird nie gestartet.
"""

import hashlib
import socket
import subprocess
import sys
import types
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import start_colab  # noqa: E402


class FakePopen:
    """Ersatz für ``subprocess.Popen``: merkt Aufrufe, startet keinen Prozess."""

    def __init__(self):
        self.aufrufe = []

    def __call__(self, befehl, env=None, **optionen):
        self.aufrufe.append({"befehl": befehl, "env": env})
        return types.SimpleNamespace(pid=4242)


@pytest.fixture()
def popen(monkeypatch):
    fake = FakePopen()
    monkeypatch.setattr(subprocess, "Popen", fake)
    return fake


@pytest.fixture()
def port_frei(monkeypatch):
    monkeypatch.setattr(start_colab, "_port_belegt", lambda port: False)


@pytest.fixture()
def colab(monkeypatch):
    """Fake-``google.colab.output``; die Rückgabe sammelt die Port-Aufrufe."""
    aufrufe = []

    modul_google = types.ModuleType("google")
    modul_colab = types.ModuleType("google.colab")
    modul_output = types.ModuleType("google.colab.output")
    modul_output.serve_kernel_port_as_window = aufrufe.append
    modul_google.colab = modul_colab
    modul_colab.output = modul_output
    monkeypatch.setitem(sys.modules, "google", modul_google)
    monkeypatch.setitem(sys.modules, "google.colab", modul_colab)
    monkeypatch.setitem(sys.modules, "google.colab.output", modul_output)
    return aufrufe


@pytest.fixture()
def ohne_colab(monkeypatch):
    """Erzwingt einen fehlgeschlagenen ``google.colab``-Import."""
    for name in ("google", "google.colab", "google.colab.output"):
        monkeypatch.setitem(sys.modules, name, None)


def _baum_hash(wurzel: Path) -> str:
    """Hash über Pfade und Inhalte aller Dateien (ohne ``__pycache__``)."""
    pruefer = hashlib.sha256()
    for pfad in sorted(wurzel.rglob("*")):
        if "__pycache__" in pfad.parts or not pfad.is_file():
            continue
        pruefer.update(str(pfad.relative_to(wurzel)).encode())
        pruefer.update(pfad.read_bytes())
    return pruefer.hexdigest()


# --- T1 Port-Freigabe -----------------------------------------------------


def test_t1_port_freigabe_genau_einmal(popen, port_frei, colab, monkeypatch):
    monkeypatch.delenv("PORT", raising=False)

    assert start_colab.main() == 0
    assert colab == [5000]
    assert len(popen.aufrufe) == 1


# --- T2 Subprozess-Env ----------------------------------------------------


def test_t2_subprozess_erhaelt_bundle_root_und_port(popen, port_frei, ohne_colab, monkeypatch):
    monkeypatch.setenv("PORT", "8123")

    assert start_colab.main() == 0
    aufruf = popen.aufrufe[0]
    assert aufruf["env"]["BUNDLE_ROOT"] == "/content/pmTool/wissen"
    assert aufruf["env"]["PORT"] == "8123"
    assert aufruf["befehl"][0] == sys.executable
    assert Path(aufruf["befehl"][1]).name == "server.py"


def test_t2_standard_port_ist_5000(popen, port_frei, ohne_colab, monkeypatch):
    monkeypatch.delenv("PORT", raising=False)

    assert start_colab.main() == 0
    assert popen.aufrufe[0]["env"]["PORT"] == "5000"


# --- T3 Ohne Colab --------------------------------------------------------


def test_t3_ohne_colab_exit_null_und_url(popen, port_frei, ohne_colab, monkeypatch, capsys):
    monkeypatch.delenv("PORT", raising=False)

    assert start_colab.main() == 0
    assert "http://localhost:5000" in capsys.readouterr().out
    assert len(popen.aufrufe) == 1


# --- T4 Port belegt -------------------------------------------------------


def test_t4_belegter_port_meldet_laeuft_bereits(popen, ohne_colab, monkeypatch, capsys):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as belegung:
        belegung.bind(("127.0.0.1", 0))
        belegung.listen(1)
        monkeypatch.setenv("PORT", str(belegung.getsockname()[1]))

        assert start_colab.main() == 0

    assert "läuft bereits" in capsys.readouterr().out
    assert popen.aufrufe == []


# --- T5 Fehlende Pakete ---------------------------------------------------


def test_t5_fehlende_pakete_loesen_pip_install_aus(popen, port_frei, ohne_colab, monkeypatch):
    monkeypatch.setattr(start_colab.importlib.util, "find_spec", lambda name: None)
    installiert = []
    monkeypatch.setattr(subprocess, "run", lambda befehl, **optionen: installiert.append(befehl))

    assert start_colab.main() == 0

    assert len(installiert) == 1
    befehl = installiert[0]
    assert befehl[:2] == [sys.executable, "-m"]
    assert "pip" in befehl
    assert "install" in befehl
    assert "flask" in befehl
    assert "pyyaml" in befehl


def test_t5_vorhandene_pakete_loesen_kein_pip_aus(popen, port_frei, ohne_colab, monkeypatch):
    monkeypatch.setattr(start_colab.importlib.util, "find_spec", lambda name: object())
    installiert = []
    monkeypatch.setattr(subprocess, "run", lambda befehl, **optionen: installiert.append(befehl))

    assert start_colab.main() == 0
    assert installiert == []


# --- T6 Kein Bundle-Schreibzugriff ---------------------------------------


def test_t6_bundle_wird_nicht_beschrieben(popen, port_frei, colab, monkeypatch):
    bundle = Path(start_colab.BUNDLE_ROOT)
    if not bundle.is_dir():
        pytest.skip(f"Bundle fehlt: {bundle}")
    monkeypatch.delenv("PORT", raising=False)
    vorher = _baum_hash(bundle)

    assert start_colab.main() == 0

    assert _baum_hash(bundle) == vorher

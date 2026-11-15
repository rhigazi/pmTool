"""TDD-Tests für das Startskript ``start.sh`` (Aufgaben A18, A32).

``start.sh`` ist ein Repo-Werkzeug im Projektwurzelverzeichnis (neben
``definitions/``) und wird von ``setup.sh`` **nicht** verteilt. Im verteilten
Zielprojekt fehlt es daher; dort überspringt sich dieses Modul selbst.

Die Tests zu A32 (Neues-Projekt-Flow) laufen ausschließlich in ``tmp_path``:
Dort wird ein vollständiges Mini-Projekt (``wissen/``, ``tools/neues_projekt.py``,
``definitions/wissen-vorlage/``, Dummy-Server) aufgebaut. Das echte ``wissen/``
des Repositories wird nie angefasst — der Reset löscht es.
"""

import os
import pty
import shutil
import socket
import subprocess
import sys
import threading
from pathlib import Path

import pytest

PROJEKT = Path(__file__).resolve().parents[3]
START = PROJEKT / "start.sh"
VORLAGE = PROJEKT / "definitions" / "wissen-vorlage"

# Marker des mitgelieferten pmTool-Projekts (siehe start.sh) — die Vorlage
# legt keinen davon an.
MARKER = (
    Path("aufgaben") / "a1-okf-bundle.md",
    Path("features") / "okf-projekt-manager-spa.md",
)

pytestmark = pytest.mark.skipif(
    not (PROJEKT / "definitions" / "setup.sh").is_file(),
    reason="start.sh ist ein Repo-Root-Werkzeug und wird nicht mitverteilt",
)


def starte(
    *argumente: str, umgebung: dict[str, str] | None = None
) -> subprocess.CompletedProcess:
    """Führt ``start.sh`` mit Argumenten im Projektwurzelverzeichnis aus."""
    return subprocess.run(
        ["bash", str(START), *argumente],
        cwd=PROJEKT,
        capture_output=True,
        text=True,
        timeout=120,
        env=umgebung,
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


def test_help_zeigt_hilfe_ohne_shelloptionen():
    ergebnis = starte("--help")

    assert ergebnis.returncode == 0, ergebnis.stderr
    assert "--colab" in ergebnis.stdout
    assert "--neu" in ergebnis.stdout
    assert "--dry-run" in ergebnis.stdout
    # Die Hilfe endet mit der letzten Kommentarzeile, nicht mit dem Skriptkopf.
    assert "set -euo" not in ergebnis.stdout


def test_dry_run_installiert_keine_pakete(tmp_path):
    """Der Dry-Run zeigt fehlende Pakete nur an und ruft pip nicht auf."""
    protokoll = tmp_path / "pip-aufrufe.txt"
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_python = fake_bin / "python3"
    fake_python.write_text(
        "#!/usr/bin/env bash\n"
        'case "$*" in\n'
        f'  *"-m pip install"*) printf "%s\\n" "$*" >> "{protokoll}"; exit 0 ;;\n'
        "  *importlib.util*) exit 1 ;;\n"
        "esac\n"
        'exec "$ECHTES_PYTHON" "$@"\n',
        encoding="utf-8",
    )
    fake_python.chmod(0o755)
    umgebung = {
        **os.environ,
        "PATH": f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}",
        "ECHTES_PYTHON": sys.executable,
    }

    ergebnis = starte("--dry-run", umgebung=umgebung)

    assert ergebnis.returncode == 0, ergebnis.stderr
    assert "würde installieren: flask pyyaml pytest" in ergebnis.stdout
    assert not protokoll.exists(), protokoll.read_text(encoding="utf-8")


# --- A32: Neues-Projekt-Flow ----------------------------------------------
#
# Testisolation: Jedes Szenario bekommt ein eigenes Mini-Projekt unter
# ``tmp_path``. Der Reset löscht dort ``wissen/`` — nie das des Repositories.


def _werkzeug_quelle() -> Path:
    """``neues_projekt.py`` aus der Quelle (dev: definitions/tools) oder dem Spiegel."""
    for kandidat in (
        PROJEKT / "definitions" / "tools" / "neues_projekt.py",
        PROJEKT / "tools" / "neues_projekt.py",
    ):
        if kandidat.is_file():
            return kandidat
    raise AssertionError("neues_projekt.py nicht gefunden")


def _freier_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


def _umgebung() -> dict[str, str]:
    """Umgebung ohne geerbtes ``BUNDLE_ROOT``/``PORT``; freier Port für den Dummy-Server."""
    geerbt = {"BUNDLE_ROOT", "PORT"}
    umgebung = {schlüssel: wert for schlüssel, wert in os.environ.items() if schlüssel not in geerbt}
    umgebung["PORT"] = str(_freier_port())
    return umgebung


def baue_testprojekt(tmp_path: Path, *, vorbefuellt: bool = True, mit_werkzeug: bool = True) -> Path:
    """Baut ein startfähiges Mini-Projekt (Dummy-Server, echte Vorlage, tmp-``wissen/``)."""
    projekt = tmp_path / "projekt"
    app = projekt / "definitions" / "app"
    app.mkdir(parents=True)
    (projekt / "definitions" / "setup.sh").write_text("#!/usr/bin/env bash\n", encoding="utf-8")
    (app / "server.py").write_text("raise SystemExit(0)\n", encoding="utf-8")
    (app / "start_colab.py").write_text("raise SystemExit(0)\n", encoding="utf-8")

    shutil.copy2(START, projekt / "start.sh")
    (projekt / "start.sh").chmod(0o755)

    if mit_werkzeug:
        (projekt / "tools").mkdir()
        shutil.copy2(_werkzeug_quelle(), projekt / "tools" / "neues_projekt.py")

    shutil.copytree(VORLAGE, projekt / "definitions" / "wissen-vorlage")
    shutil.copytree(VORLAGE, projekt / "wissen")

    if vorbefuellt:
        _marker_anlegen(projekt / "wissen", MARKER[0])
    return projekt


def _marker_anlegen(wissen: Path, marker: Path) -> None:
    ziel = wissen / marker
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text("---\ntype: Task\ntitle: A1\n---\n", encoding="utf-8")


def starte_im(projekt: Path, *argumente: str, eingabe: str = "") -> subprocess.CompletedProcess:
    """Führt ``start.sh`` im Mini-Projekt aus; stdin ist eine Pipe (kein TTY)."""
    return subprocess.run(
        ["bash", str(projekt / "start.sh"), *argumente],
        cwd=projekt,
        capture_output=True,
        text=True,
        timeout=120,
        input=eingabe,
        env=_umgebung(),
    )


def starte_mit_tty(
    projekt: Path, *argumente: str, eingabe: str | None
) -> subprocess.CompletedProcess:
    """Führt ``start.sh`` an einem echten Terminal aus (``read`` sieht ein TTY).

    ``eingabe=None`` sendet Strg+D (Eingabe-Abbruch/EOF).
    """
    master, slave = pty.openpty()
    prozess = subprocess.Popen(
        ["bash", str(projekt / "start.sh"), *argumente],
        cwd=projekt,
        stdin=slave,
        stdout=slave,
        stderr=slave,
        env=_umgebung(),
        close_fds=True,
    )
    os.close(slave)
    os.write(master, b"\x04" if eingabe is None else eingabe.encode("utf-8"))

    gesammelt: list[bytes] = []

    def lesen() -> None:
        while True:
            try:
                daten = os.read(master, 4096)
            except OSError:
                break
            if not daten:
                break
            gesammelt.append(daten)

    leser = threading.Thread(target=lesen)
    leser.start()
    try:
        status = prozess.wait(timeout=120)
    finally:
        leser.join(timeout=30)
        os.close(master)

    ausgabe = b"".join(gesammelt).decode("utf-8", errors="replace").replace("\r\n", "\n")
    return subprocess.CompletedProcess(prozess.args, status, ausgabe, "")


def _backups(projekt: Path) -> list[Path]:
    return sorted(projekt.glob("wissen-backup-*.tar.gz"))


def test_erststart_hinweis_ohne_tty_setzt_nichts_zurueck(tmp_path):
    """Vorbefülltes wissen/ + kein TTY: nur Hinweis, kein Prompt, keine Löschung."""
    projekt = baue_testprojekt(tmp_path)

    ergebnis = starte_im(projekt, "--skip-verify")

    assert ergebnis.returncode == 0, ergebnis.stderr
    assert "Projekt-Daten" in ergebnis.stdout
    assert "Kein interaktives Terminal" in ergebnis.stdout
    assert "--neu" in ergebnis.stdout
    assert "beginnen? [j/N]" not in ergebnis.stdout
    assert (projekt / "wissen" / MARKER[0]).is_file()
    assert _backups(projekt) == []
    assert "Server startet" in ergebnis.stdout


def test_dry_run_zeigt_nie_einen_prompt(tmp_path):
    """Der Trockenlauf fragt nicht und löscht nichts — auch mit vorbefülltem wissen/."""
    projekt = baue_testprojekt(tmp_path)

    ergebnis = starte_im(projekt, "--dry-run")

    assert ergebnis.returncode == 0, ergebnis.stderr
    assert "Projekt-Daten" in ergebnis.stdout
    assert "würde starten" in ergebnis.stdout
    assert "beginnen? [j/N]" not in ergebnis.stdout
    assert (projekt / "wissen" / MARKER[0]).is_file()
    assert _backups(projekt) == []


def test_frische_vorlage_zeigt_keinen_hinweis(tmp_path):
    """Ein bereits leeres Vorlagen-wissen/ löst weder Hinweis noch Rückfrage aus."""
    projekt = baue_testprojekt(tmp_path, vorbefuellt=False)

    ergebnis = starte_im(projekt, "--dry-run")

    assert ergebnis.returncode == 0, ergebnis.stderr
    assert "Projekt-Daten" not in ergebnis.stdout
    assert "start.sh --neu" not in ergebnis.stdout


@pytest.mark.parametrize("marker", MARKER)
def test_jeder_marker_erkennt_vorbefuelltes_wissen(tmp_path, marker):
    """Die Marker-Liste bleibt stabil, wenn eine der Referenzdateien fehlt."""
    projekt = baue_testprojekt(tmp_path, vorbefuellt=False)
    _marker_anlegen(projekt / "wissen", marker)

    ergebnis = starte_im(projekt, "--dry-run")

    assert "Projekt-Daten" in ergebnis.stdout


def test_interaktiv_nein_startet_unveraendert(tmp_path):
    """Antwort Nein: nichts wird gelöscht, die App startet normal."""
    projekt = baue_testprojekt(tmp_path)

    ergebnis = starte_mit_tty(projekt, "--skip-verify", eingabe="nein\n")

    assert ergebnis.returncode == 0
    assert "beginnen? [j/N]" in ergebnis.stdout
    assert "Nein" in ergebnis.stdout
    assert (projekt / "wissen" / MARKER[0]).is_file()
    assert _backups(projekt) == []
    assert "Server startet" in ergebnis.stdout


def test_interaktiv_abbruch_ist_wie_nein(tmp_path):
    """Eingabe-Abbruch (Strg+D) zählt als Nein — fail-safe ohne Löschung."""
    projekt = baue_testprojekt(tmp_path)

    ergebnis = starte_mit_tty(projekt, "--skip-verify", eingabe=None)

    assert ergebnis.returncode == 0
    assert (projekt / "wissen" / MARKER[0]).is_file()
    assert _backups(projekt) == []
    assert "Server startet" in ergebnis.stdout


def test_interaktiv_ja_setzt_zurueck_und_startet(tmp_path):
    """Antwort Ja: Reset über neues_projekt.py (mit Backup), dann Start mit leerem Projekt."""
    projekt = baue_testprojekt(tmp_path)

    ergebnis = starte_mit_tty(projekt, "--skip-verify", eingabe="ja\n")

    assert ergebnis.returncode == 0
    assert "wissen/ zurückgesetzt auf Vorlage" in ergebnis.stdout
    assert not (projekt / "wissen" / MARKER[0]).exists()
    assert (projekt / "wissen" / "index.md").is_file()
    backups = _backups(projekt)
    assert len(backups) == 1
    assert "Server startet" in ergebnis.stdout


def test_neu_setzt_ohne_rueckfrage_zurueck_und_startet(tmp_path):
    """``--neu``: Reset ohne Rückfrage (Backup-Pflicht), danach Start."""
    projekt = baue_testprojekt(tmp_path)
    eigene = projekt / "wissen" / "aufgaben" / "eigene-aufgabe.md"
    eigene.write_text("---\ntype: Task\ntitle: Eigene\n---\n", encoding="utf-8")

    ergebnis = starte_im(projekt, "--neu", "--skip-verify")

    assert ergebnis.returncode == 0, ergebnis.stderr
    assert "wissen/ zurückgesetzt auf Vorlage" in ergebnis.stdout
    assert "beginnen? [j/N]" not in ergebnis.stdout
    assert not eigene.exists()
    assert _backups(projekt), "Backup ist Pflicht"
    assert "Server startet" in ergebnis.stdout


def test_neu_dry_run_zeigt_nur_den_plan(tmp_path):
    """``--neu --dry-run`` ruft das Werkzeug ohne ``--ja``: Plan, keine Änderung."""
    projekt = baue_testprojekt(tmp_path)

    ergebnis = starte_im(projekt, "--neu", "--dry-run")

    assert ergebnis.returncode == 0, ergebnis.stderr
    assert "Neues Projekt beginnen — Plan (nichts wurde verändert)" in ergebnis.stdout
    assert "wissen/ zurückgesetzt" not in ergebnis.stdout
    assert (projekt / "wissen" / MARKER[0]).is_file()
    assert _backups(projekt) == []
    assert "würde starten" in ergebnis.stdout


def test_neu_ist_mit_colab_kombinierbar(tmp_path):
    projekt = baue_testprojekt(tmp_path)

    ergebnis = starte_im(projekt, "--neu", "--colab", "--dry-run")

    assert ergebnis.returncode == 0, ergebnis.stderr
    assert "Neues Projekt beginnen — Plan" in ergebnis.stdout
    assert "definitions/app/start_colab.py" in ergebnis.stdout
    assert _backups(projekt) == []


def test_reset_fehler_bricht_den_start_ab(tmp_path):
    """Fehler des Reset-Werkzeugs: fail-loud, kein Start, kein Halbzustand."""
    projekt = baue_testprojekt(tmp_path)
    shutil.rmtree(projekt / "definitions" / "wissen-vorlage")

    ergebnis = starte_im(projekt, "--neu", "--skip-verify")

    assert ergebnis.returncode != 0
    assert "Fehler" in ergebnis.stderr
    assert (projekt / "wissen" / MARKER[0]).is_file()
    assert _backups(projekt) == []
    assert "Server startet" not in ergebnis.stdout


def test_ohne_reset_werkzeug_kein_loeschen(tmp_path):
    """Ohne ``tools/neues_projekt.py`` gibt es keine zweite Lösch-Implementierung."""
    projekt = baue_testprojekt(tmp_path, mit_werkzeug=False)

    ergebnis = starte_im(projekt, "--neu", "--skip-verify")

    assert ergebnis.returncode != 0
    assert "neues_projekt.py" in ergebnis.stderr
    assert (projekt / "wissen" / MARKER[0]).is_file()
    assert _backups(projekt) == []
    assert "Server startet" not in ergebnis.stdout

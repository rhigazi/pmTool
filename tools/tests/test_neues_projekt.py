"""Tests für das CLI-Werkzeug neues_projekt.py (Arbeit ausschließlich auf tmp-Kopien).

Alle Tests bauen die Projektstruktur (``definitions/wissen-vorlage/``, ``wissen/``,
``definitions/verify.sh``) in ``tmp_path`` nach und übergeben die Wurzel per
``root=`` an :func:`neues_projekt.main`. Das echte ``wissen/`` des Repositories
wird nie angefasst.
"""

import hashlib
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import neues_projekt  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
VORLAGE_QUELLE = REPO_ROOT / "definitions" / "wissen-vorlage"
VERIFY_QUELLE = REPO_ROOT / "definitions" / "verify.sh"

ALTE_DATEI = "aufgaben/a1-alt.md"
ALTE_VERSTECKTE_DATEI = ".alt-geheim"


def baum(wurzel):
    """Inhalt eines Baums als ``{relativer Pfad: Inhalt-Hash}`` (inkl. Verzeichnisse)."""
    ergebnis = {}
    for pfad in sorted(wurzel.rglob("*")):
        rel = pfad.relative_to(wurzel).as_posix()
        if pfad.is_dir():
            ergebnis[rel] = "<verzeichnis>"
        else:
            ergebnis[rel] = hashlib.sha256(pfad.read_bytes()).hexdigest()
    return ergebnis


def alte_wissen_struktur(wissen):
    """Legt einen realistischen Altbestand an (inkl. versteckter Dateien)."""
    dateien = {
        "index.md": "# Altbestand\n",
        "features.md": "# Features\n",
        "log.md": "# Log\n",
        "entscheidungen/log.md": "# Entscheidungen\n",
        "aufgaben/index.md": "# Aufgaben\n",
        ALTE_DATEI: "# Alte Aufgabe\n",
        "projekt/konzept.md": "# Altes Konzept\n",
        ALTE_VERSTECKTE_DATEI: "geheim\n",
        ".versteckt/notiz.md": "# versteckte Notiz\n",
    }
    for rel, inhalt in dateien.items():
        ziel = wissen / rel
        ziel.parent.mkdir(parents=True, exist_ok=True)
        ziel.write_text(inhalt, encoding="utf-8")
    (wissen / "leerer-ordner").mkdir()


def projekt_bauen(root):
    """Baut eine Projektkopie mit Vorlage, verify.sh und Altbestand in ``wissen/``."""
    vorlage = root / "definitions" / "wissen-vorlage"
    shutil.copytree(VORLAGE_QUELLE, vorlage)
    # Versteckte Datei: muss beim Reset mitkommen.
    (vorlage / ".vorlage-versteckt").write_text("versteckt\n", encoding="utf-8")
    shutil.copy2(VERIFY_QUELLE, root / "definitions" / "verify.sh")

    wissen = root / "wissen"
    wissen.mkdir()
    alte_wissen_struktur(wissen)
    return root


@pytest.fixture
def projekt(tmp_path):
    root = tmp_path / "projekt"
    root.mkdir()
    return projekt_bauen(root)


def backups(root):
    return sorted(root.glob("wissen-backup-*.tar.gz"))


def reset(root, *argumente):
    return neues_projekt.main(list(argumente), root=root)


# --- T1: Plan-Lauf ohne --ja verändert nichts ---------------------------------


def test_plan_ohne_ja_aendert_nichts(projekt, capsys):
    vorher = baum(projekt)

    exit_code = reset(projekt)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert baum(projekt) == vorher
    assert backups(projekt) == []
    assert captured.err == ""


def test_plan_nennt_umfang_vorlage_und_backupziel(projekt, capsys):
    reset(projekt)

    ausgabe = capsys.readouterr().out
    assert "Plan" in ausgabe
    assert "wissen/" in ausgabe
    assert "Dateien" in ausgabe
    assert "Ordner" in ausgabe
    assert "definitions/wissen-vorlage/" in ausgabe
    assert "Backup" in ausgabe
    assert "wissen-backup-" in ausgabe
    assert "--ja" in ausgabe


def test_plan_weist_auf_loeschung_hin(projekt, capsys):
    reset(projekt)

    ausgabe = capsys.readouterr().out
    assert "löscht" in ausgabe or "gelöscht" in ausgabe
    assert "nichts" in ausgabe.lower()


# --- T2: --ja sichert alten Stand und setzt auf die Vorlage -------------------


def test_ja_erzeugt_backup_mit_alten_dateien(projekt, capsys):
    exit_code = reset(projekt, "--ja")

    angelegte_backups = backups(projekt)
    assert exit_code == 0
    assert len(angelegte_backups) == 1

    with tarfile.open(angelegte_backups[0]) as archiv:
        namen = archiv.getnames()
        inhalt = archiv.extractfile(f"wissen/{ALTE_DATEI}").read().decode("utf-8")
    assert f"wissen/{ALTE_DATEI}" in namen
    assert f"wissen/{ALTE_VERSTECKTE_DATEI}" in namen
    assert inhalt == "# Alte Aufgabe\n"
    assert capsys.readouterr().out.count("Backup") >= 1


def test_ja_setzt_wissen_auf_vorlage(projekt, capsys):
    reset(projekt, "--ja")

    wissen = projekt / "wissen"
    vorlage = projekt / "definitions" / "wissen-vorlage"
    assert not (wissen / ALTE_DATEI).exists()
    assert not (wissen / ALTE_VERSTECKTE_DATEI).exists()
    assert baum(wissen) == baum(vorlage)
    assert "zurückgesetzt auf Vorlage" in capsys.readouterr().out


def test_ja_nennt_naechste_schritte_und_sicherheitshinweis(projekt, capsys):
    reset(projekt, "--ja")

    ausgabe = capsys.readouterr().out
    assert "Nächste Schritte" in ausgabe
    assert "start.sh" in ausgabe
    assert "Projekt" in ausgabe
    assert "leer" in ausgabe
    assert "verify.sh" in ausgabe


def test_eigener_backup_pfad_wird_genutzt(projekt, capsys):
    ziel = projekt / "sicherungen" / "stand.tar.gz"

    exit_code = reset(projekt, "--ja", "--backup", str(ziel))

    assert exit_code == 0
    assert ziel.is_file()
    assert backups(projekt) == []
    assert str(ziel) in capsys.readouterr().out


def test_backup_pfad_ausserhalb_des_repos_wird_abgelehnt(projekt, tmp_path_factory, capsys):
    vorher = baum(projekt / "wissen")
    aussen = tmp_path_factory.mktemp("aussen") / "backup.tar.gz"

    exit_code = reset(projekt, "--ja", "--backup", str(aussen))

    assert exit_code == 1
    assert not aussen.exists()
    assert baum(projekt / "wissen") == vorher
    assert "Fehler" in capsys.readouterr().err


def test_backup_pfad_im_wissen_verzeichnis_wird_abgelehnt(projekt, capsys):
    vorher = baum(projekt / "wissen")
    ziel = projekt / "wissen" / "backup.tar.gz"

    exit_code = reset(projekt, "--ja", "--backup", str(ziel))

    assert exit_code == 1
    assert baum(projekt / "wissen") == vorher
    assert "Fehler" in capsys.readouterr().err


def test_wissen_als_datei_wird_abgelehnt(projekt, capsys):
    shutil.rmtree(projekt / "wissen")
    (projekt / "wissen").write_text("keine Struktur\n", encoding="utf-8")

    exit_code = reset(projekt, "--ja")

    assert exit_code == 1
    assert (projekt / "wissen").read_text(encoding="utf-8") == "keine Struktur\n"
    assert "Verzeichnis" in capsys.readouterr().err


def test_wissen_als_symlink_wird_abgelehnt(projekt, tmp_path_factory, capsys):
    ziel = tmp_path_factory.mktemp("aussen") / "wissen"
    ziel.mkdir()
    (ziel / "wichtig.md").write_text("bleibt\n", encoding="utf-8")
    shutil.rmtree(projekt / "wissen")
    (projekt / "wissen").symlink_to(ziel, target_is_directory=True)

    exit_code = reset(projekt, "--ja")

    assert exit_code == 1
    assert (ziel / "wichtig.md").is_file()
    assert "Symlink" in capsys.readouterr().err


# --- T3: Backup-Fehler verhindert das Löschen ---------------------------------


def test_backup_fehler_verhindert_loeschen(projekt, capsys, monkeypatch):
    vorher = baum(projekt / "wissen")

    def kaputtes_backup(*args, **kwargs):
        raise OSError("Speicher voll")

    monkeypatch.setattr(neues_projekt.tarfile, "open", kaputtes_backup)

    exit_code = reset(projekt, "--ja")

    captured = capsys.readouterr()
    assert exit_code != 0
    assert baum(projekt / "wissen") == vorher
    assert "Backup" in captured.err
    assert "Speicher voll" in captured.err
    assert backups(projekt) == []


def test_backup_fehler_laesst_kein_halbfertiges_archiv_zurueck(projekt, capsys, monkeypatch):
    def kaputtes_backup(pfad, *args, **kwargs):
        Path(pfad).write_bytes(b"halb")
        raise OSError("Schreiben fehlgeschlagen")

    monkeypatch.setattr(neues_projekt.tarfile, "open", kaputtes_backup)

    reset(projekt, "--ja")

    assert backups(projekt) == []


def test_backup_ziel_als_verzeichnis_wird_abgelehnt(projekt, capsys):
    vorher = baum(projekt / "wissen")
    ziel = projekt / "backup-verzeichnis"
    ziel.mkdir()

    exit_code = reset(projekt, "--ja", "--backup", str(ziel))

    assert exit_code == 1
    assert baum(projekt / "wissen") == vorher
    assert "Verzeichnis" in capsys.readouterr().err


# --- T4: fehlende oder unvollständige Vorlage --------------------------------


def test_fehlende_vorlage_bricht_ohne_loeschung_ab(projekt, capsys):
    vorher = baum(projekt / "wissen")
    shutil.rmtree(projekt / "definitions" / "wissen-vorlage")

    exit_code = reset(projekt, "--ja")

    captured = capsys.readouterr()
    assert exit_code == 1
    assert baum(projekt / "wissen") == vorher
    assert "Vorlage" in captured.err
    assert backups(projekt) == []


def test_unvollstaendige_vorlage_nennt_fehlende_datei(projekt, capsys):
    vorher = baum(projekt / "wissen")
    (projekt / "definitions" / "wissen-vorlage" / "features.md").unlink()

    exit_code = reset(projekt, "--ja")

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "features.md" in captured.err
    assert baum(projekt / "wissen") == vorher
    assert backups(projekt) == []


def test_leere_vorlage_bricht_ohne_loeschung_ab(projekt, capsys):
    vorher = baum(projekt / "wissen")
    vorlage = projekt / "definitions" / "wissen-vorlage"
    shutil.rmtree(vorlage)
    vorlage.mkdir()

    exit_code = reset(projekt, "--ja")

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Vorlage" in captured.err
    assert baum(projekt / "wissen") == vorher
    assert backups(projekt) == []


def test_plan_meldet_fehlende_vorlage_ebenfalls(projekt, capsys):
    shutil.rmtree(projekt / "definitions" / "wissen-vorlage")

    exit_code = reset(projekt)

    assert exit_code == 1
    assert "Vorlage" in capsys.readouterr().err


# --- T5: keine Cache-Artefakte, keine Reste ----------------------------------


def test_reset_enthaelt_keine_cache_artefakte(projekt, capsys):
    vorlage = projekt / "definitions" / "wissen-vorlage"
    (vorlage / "__pycache__").mkdir()
    (vorlage / "__pycache__" / "modul.cpython-313.pyc").write_bytes(b"cache")
    (vorlage / ".pytest_cache" / "v" / "cache").mkdir(parents=True)
    (vorlage / ".pytest_cache" / "v" / "cache" / "nodeids").write_text("x", encoding="utf-8")
    (vorlage / "alt.pyc").write_bytes(b"cache")

    exit_code = reset(projekt, "--ja")

    inhalte = baum(projekt / "wissen")
    assert exit_code == 0
    assert not any("__pycache__" in pfad for pfad in inhalte)
    assert not any(".pytest_cache" in pfad for pfad in inhalte)
    assert not any(pfad.endswith(".pyc") for pfad in inhalte)


def test_reset_laesst_keine_temporaeren_verzeichnisse_zurueck(projekt, capsys):
    reset(projekt, "--ja")

    reste = [
        pfad.name
        for pfad in projekt.iterdir()
        if pfad.is_dir() and pfad.name.startswith(".")
    ]
    assert reste == []


def test_vorlage_bleibt_unveraendert(projekt, capsys):
    vorlage = projekt / "definitions" / "wissen-vorlage"
    vorher = baum(vorlage)

    reset(projekt, "--ja")

    assert baum(vorlage) == vorher


# --- T6: E2E — Reset auf Testkopie, danach verify.sh -------------------------


def verify_kopie_bauen(root):
    """Ergänzt die Projektkopie um alles, was ``definitions/verify.sh`` prüft.

    Die App wird als Minimal-Stub angelegt: ``verify.sh`` prüft nur Existenz und
    eine grüne Test-Suite. Die echte App-Suite bleibt den App-Tests vorbehalten
    (und würde hier nur zusätzlich Zeit kosten); die eigene Testdatei wird
    bewusst NICHT kopiert, weil ``verify.sh`` sonst rekursiv diesen Test startet.
    """
    shutil.copy2(REPO_ROOT / "AGENTS.md", root / "AGENTS.md")
    shutil.copy2(REPO_ROOT / "opencode.jsonc", root / "opencode.jsonc")
    agenten = root / ".opencode" / "agents"
    agenten.mkdir(parents=True)
    for quelle in sorted((REPO_ROOT / "definitions" / "agents").glob("*.md")):
        shutil.copy2(quelle, agenten / quelle.name)

    (root / "tools" / "tests").mkdir(parents=True)
    shutil.copy2(REPO_ROOT / "tools" / "telegram_send.py", root / "tools" / "telegram_send.py")
    shutil.copy2(
        REPO_ROOT / "tools" / "tests" / "test_telegram_send.py",
        root / "tools" / "tests" / "test_telegram_send.py",
    )

    (root / "app" / "static").mkdir(parents=True)
    (root / "app" / "server.py").write_text("", encoding="utf-8")
    (root / "app" / "static" / "index.html").write_text("", encoding="utf-8")
    (root / "app" / "tests").mkdir()
    (root / "app" / "tests" / "test_smoke.py").write_text(
        "def test_smoke():\n    assert True\n", encoding="utf-8"
    )


def test_verify_nach_reset_ist_gruen(projekt, capsys):
    verify_kopie_bauen(projekt)

    assert reset(projekt, "--ja") == 0

    ergebnis = subprocess.run(
        ["bash", str(projekt / "definitions" / "verify.sh"), str(projekt)],
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert ergebnis.returncode == 0, ergebnis.stdout + ergebnis.stderr
    assert "Setup vollständig" in ergebnis.stdout


# --- T7: zweiter Aufruf ist idempotent ---------------------------------------


def test_zweiter_aufruf_ist_idempotent(projekt, capsys):
    reset(projekt, "--ja")
    erster_stand = baum(projekt / "wissen")

    exit_code = reset(projekt, "--ja")

    assert exit_code == 0
    assert baum(projekt / "wissen") == erster_stand
    assert baum(projekt / "wissen") == baum(projekt / "definitions" / "wissen-vorlage")
    assert len(backups(projekt)) == 2


def test_zweites_backup_ueberschreibt_das_erste_nicht(projekt, capsys):
    reset(projekt, "--ja")
    erstes = backups(projekt)[0]
    groesse = erstes.stat().st_size

    reset(projekt, "--ja")

    assert erstes.is_file()
    assert erstes.stat().st_size == groesse
    assert len(backups(projekt)) == 2

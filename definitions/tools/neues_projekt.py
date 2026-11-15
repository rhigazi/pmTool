#!/usr/bin/env python3
"""Startet ein neues, leeres Projekt: setzt ``wissen/`` auf die OKF-Vorlage zurück.

Der gesamte Inhalt von ``wissen/`` wird gelöscht (auch versteckte Dateien) und
durch ``definitions/wissen-vorlage/`` ersetzt. Ohne ``--ja`` wird nur der Plan
ausgegeben und nichts verändert; mit ``--ja`` entsteht vorher ein Backup
``wissen-backup-YYYYMMDD-HHMMSS.tar.gz`` im Projekt-Root. Ein bereits
vorhandenes Backup-Ziel wird abgelehnt, nie überschrieben.

Aufruf:
    python3 tools/neues_projekt.py
    python3 tools/neues_projekt.py --ja
    python3 tools/neues_projekt.py --ja --backup PFAD

Exit-Codes: 0 bei Erfolg bzw. Plan-Lauf, 1 bei jedem Fehler (Meldung auf stderr).
"""

import argparse
import os
import shutil
import sys
import tarfile
import tempfile
from datetime import datetime
from pathlib import Path

WISSEN = "wissen"
VORLAGE = Path("definitions") / "wissen-vorlage"
BACKUP_PRAEFIX = "wissen-backup"
BACKUP_ENDUNG = ".tar.gz"

# mkdtemp legt Verzeichnisse mit 0700 an; wissen/ muss für die App lesbar bleiben.
WISSEN_MODUS = 0o755

# Artefakte, die nie in ein frisches Projekt gehören.
CACHE_ORDNER = frozenset({"__pycache__", ".pytest_cache"})
CACHE_ENDUNGEN = frozenset({".pyc"})

# Pflichtdateien der Vorlage — muss ``definitions/verify.sh .`` erfüllen.
PFLICHTDATEIEN = (
    "index.md",
    "features.md",
    "log.md",
    "entscheidungen/log.md",
    "aufgaben/index.md",
    "projekt/phasen.md",
    "projekt/konzept.md",
    "projekt/technische-spec.md",
)

PLAN_TITEL = "Neues Projekt beginnen — Plan (nichts wurde verändert)"
ERFOLG_MELDUNG = "wissen/ zurückgesetzt auf Vorlage"


class NeuesProjektFehler(Exception):
    """Basisfehler des Werkzeugs; die Meldung ist für die CLI-Ausgabe gedacht."""


class PfadFehler(NeuesProjektFehler):
    """Pfad liegt außerhalb des Projekts oder ist als Ziel unzulässig."""


class VorlageFehler(NeuesProjektFehler):
    """Die Vorlage fehlt oder ist unvollständig."""


class BackupFehler(NeuesProjektFehler):
    """Das Backup konnte nicht erstellt werden; es wurde nichts gelöscht."""


# --- Pfadschutz -----------------------------------------------------------


def _wurzel(root=None):
    """Projekt-Root als realer Pfad (Default: zwei Ebenen über diesem Skript)."""
    basis = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    return Path(os.path.realpath(basis))


def _im_repo(root, pfad):
    """Prüft, dass ``pfad`` innerhalb von ``root`` liegt, und gibt den realen Pfad."""
    ziel = Path(os.path.realpath(pfad))
    if not ziel.is_relative_to(root):
        raise PfadFehler(f"Pfad liegt außerhalb des Projekts: {pfad}")
    return ziel


def _pruefe_backup_ziel(root, wissen, vorlage, backup):
    """Ermittelt das Backup-Ziel und stellt sicher, dass es sicher beschreibbar ist."""
    if backup is None:
        ziel = root / _backup_name(root)
    else:
        kandidat = Path(backup)
        if not kandidat.is_absolute():
            kandidat = root / kandidat
        if kandidat.is_symlink():
            raise PfadFehler(f"Backup-Ziel ist ein Symlink: {kandidat}")
        ziel = _im_repo(root, kandidat)

    if ziel.is_relative_to(wissen) or ziel.is_relative_to(vorlage):
        raise PfadFehler("Backup-Ziel darf nicht in wissen/ oder in der Vorlage liegen")
    if ziel.exists():
        if ziel.is_dir():
            raise PfadFehler(f"Backup-Ziel ist ein Verzeichnis: {ziel}")
        raise PfadFehler(
            f"Backup-Ziel existiert bereits: {ziel} — bestehende Sicherungen werden nie "
            "überschrieben. Bitte einen freien Pfad angeben."
        )
    return ziel


def _backup_name(root, zeitpunkt=None):
    """Zeitgestempelter Backup-Name; vorhandene Backups werden nie überschrieben."""
    stempel = (zeitpunkt or datetime.now()).strftime("%Y%m%d-%H%M%S")
    ziel = root / f"{BACKUP_PRAEFIX}-{stempel}{BACKUP_ENDUNG}"
    nummer = 2
    while ziel.exists():
        ziel = root / f"{BACKUP_PRAEFIX}-{stempel}-{nummer}{BACKUP_ENDUNG}"
        nummer += 1
    return ziel.name


# --- Bestandsaufnahme -----------------------------------------------------


def umfang(pfad):
    """Zählt ``(Dateien, Ordner, versteckte Einträge)`` unterhalb von ``pfad``."""
    if not pfad.is_dir():
        return 0, 0, 0
    dateien = ordner = versteckt = 0
    for eintrag in pfad.rglob("*"):
        if eintrag.is_dir():
            ordner += 1
        else:
            dateien += 1
        if any(teil.startswith(".") for teil in eintrag.relative_to(pfad).parts):
            versteckt += 1
    return dateien, ordner, versteckt


def ist_cache_artefakt(rel):
    """``__pycache__``/``.pytest_cache``/``*.pyc`` gehören nicht ins neue Projekt."""
    return any(teil in CACHE_ORDNER for teil in rel.parts) or rel.suffix in CACHE_ENDUNGEN


def pruefe_vorlage(vorlage):
    """Prüft die Vorlage vollständig, bevor irgendetwas gelöscht wird."""
    if not vorlage.is_dir():
        raise VorlageFehler(f"Vorlage fehlt: {VORLAGE.as_posix()}/ — es wurde nichts gelöscht.")
    fehlend = [rel for rel in PFLICHTDATEIEN if not (vorlage / rel).is_file()]
    if fehlend:
        raise VorlageFehler(
            f"Vorlage unvollständig: {VORLAGE.as_posix()}/ — fehlt {', '.join(fehlend)}. "
            "Es wurde nichts gelöscht."
        )
    for eintrag in vorlage.rglob("*"):
        if eintrag.is_symlink():
            rel = eintrag.relative_to(vorlage).as_posix()
            # Symlinks würden beim Kopieren dereferenziert und aus der Vorlage
            # hinauszeigen — die Vorlage muss ein reiner Dateibaum sein.
            raise VorlageFehler(
                f"Vorlage enthält einen Symlink: {VORLAGE.as_posix()}/{rel}. "
                "Es wurde nichts gelöscht."
            )
    return umfang(vorlage)[:2]


# --- Backup und Reset -----------------------------------------------------


def backup_erstellen(wissen, ziel):
    """Packt ``wissen/`` in ein tar.gz; bei jedem Fehler bleibt der Altstand erhalten.

    Ein bereits vorhandenes Ziel wird abgelehnt: ``tarfile`` würde es sonst
    truncaten und damit eine frühere Sicherung vernichten.
    """
    if ziel.exists():
        raise BackupFehler(
            f"Backup-Ziel existiert bereits ({ziel}). Es wurde nichts gelöscht."
        )
    try:
        ziel.parent.mkdir(parents=True, exist_ok=True)
        with tarfile.open(ziel, "w:gz") as archiv:
            archiv.add(wissen, arcname=wissen.name, recursive=True)
    except (OSError, tarfile.TarError) as fehler:
        try:
            ziel.unlink(missing_ok=True)
        except OSError:
            pass
        raise BackupFehler(
            f"Backup fehlgeschlagen ({fehler}). Es wurde nichts gelöscht."
        ) from fehler
    return ziel


def kopiere_vorlage(quelle, ziel):
    """Kopiert die Vorlage inklusive versteckter Dateien, ohne Cache-Artefakte.

    Symlinks werden nicht dereferenziert: sie werden als Fehler gemeldet, damit
    die Kopie nie aus der Vorlage hinauszeigt.
    """
    for eintrag in quelle.rglob("*"):
        rel = eintrag.relative_to(quelle)
        if eintrag.is_symlink():
            raise VorlageFehler(f"Vorlage enthält einen Symlink: {rel.as_posix()}")
        if ist_cache_artefakt(rel):
            continue
        ablage = ziel / rel
        if eintrag.is_dir():
            ablage.mkdir(parents=True, exist_ok=True)
        else:
            ablage.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(eintrag, ablage)


def _ersetze(quelle, ziel):
    """Kapselt ``os.replace`` (eigener Testhaken für den Rollback-Zweig)."""
    os.replace(quelle, ziel)


def tausche_gegen_vorlage(root, wissen, vorlage):
    """Baut die neue Struktur daneben auf und tauscht sie atomar gegen ``wissen/``.

    So gibt es keinen Halbzustand: schlägt der Aufbau oder der Tausch fehl, bleibt
    ``wissen/`` unverändert und das temporäre Verzeichnis wird entfernt. Scheitert
    auch der Rollback, bleibt der Altbestand unter ``.wissen-alt-*`` liegen und
    wird gemeldet — gelöscht wird er nie, solange er nicht zurückgetauscht ist.
    """
    neu = Path(tempfile.mkdtemp(dir=root, prefix=".wissen-neu-"))
    alt = None
    alt_erhalten = False
    try:
        kopiere_vorlage(vorlage, neu)

        if wissen.exists():
            alt = Path(tempfile.mkdtemp(dir=root, prefix=".wissen-alt-"))
            alt.rmdir()
            _ersetze(wissen, alt)
            alt_erhalten = True

        try:
            _ersetze(neu, wissen)
        except OSError:
            if alt is not None and not wissen.exists():
                _ersetze(alt, wissen)
                alt_erhalten = False
                alt = None
            raise

        os.chmod(wissen, WISSEN_MODUS)
        alt_erhalten = False
    except OSError as fehler:
        raise NeuesProjektFehler(
            f"Zurücksetzen fehlgeschlagen ({fehler.strerror or fehler})."
        ) from fehler
    finally:
        if neu.exists():
            shutil.rmtree(neu, ignore_errors=True)
        if alt is not None and alt.exists():
            if alt_erhalten:
                print(f"Altbestand unter {alt} gesichert.", file=sys.stderr)
            else:
                try:
                    shutil.rmtree(alt)
                except OSError:
                    # Der Reset ist bereits erfolgreich; das Backup bleibt die Absicherung.
                    print(f"Warnung: Altbestand blieb liegen: {alt}", file=sys.stderr)


# --- Ausgaben -------------------------------------------------------------


def _umfang_text(dateien, ordner, versteckt=0):
    text = f"{dateien} Dateien, {ordner} Ordner"
    if versteckt:
        text += f" (davon {versteckt} versteckt)"
    return text


def plan_text(root, wissen, backup_ziel, wissen_umfang, vorlage_umfang):
    if wissen.is_dir():
        bestand = f"{WISSEN}/ — {_umfang_text(*wissen_umfang)}"
    else:
        bestand = f"{WISSEN}/ — nicht vorhanden (wird aus der Vorlage angelegt)"

    return "\n".join(
        [
            PLAN_TITEL,
            "",
            f"  Projekt:   {root}",
            f"  Betroffen: {bestand}",
            f"  Vorlage:   {VORLAGE.as_posix()}/ — {_umfang_text(*vorlage_umfang)}",
            f"  Backup:    {backup_ziel}",
            "  Danach:    wissen/ enthält nur noch die Vorlage — das Projekt ist leer",
            "",
            "Dieser Lauf hat nichts verändert. Ausführen mit:",
            "  python3 tools/neues_projekt.py --ja",
            "",
            "--ja löscht den gesamten Inhalt von wissen/ — erst nach erfolgreichem Backup.",
        ]
    )


def erfolgs_text(backup_ziel, vorlage_umfang):
    zeilen = [
        "Neues Projekt beginnen",
        "",
        f"1) Vorlage geprüft: {VORLAGE.as_posix()}/ ({vorlage_umfang[0]} Dateien)",
    ]
    if backup_ziel is None:
        zeilen.append("2) Backup: nicht nötig (wissen/ war nicht vorhanden)")
    else:
        zeilen.append(f"2) Backup: {backup_ziel}")
    zeilen += [
        f"3) {ERFOLG_MELDUNG}",
        f"4) Pflichtdateien aus der geprüften Vorlage übernommen ({len(PFLICHTDATEIEN)}/{len(PFLICHTDATEIEN)})",
        "",
        f"✓ {ERFOLG_MELDUNG}.",
        "",
        "Nächste Schritte:",
        "  - App starten: bash start.sh",
        "  - Neues Projekt anlegen: App öffnen und in der Projekt-Ansicht anlegen",
        "  - Setup prüfen: bash definitions/verify.sh .",
        "",
        "Sicherheitshinweis: Das Projekt ist jetzt leer. Alle bisherigen Wissensdateien",
        f"liegen ausschließlich im Backup: {backup_ziel or '(kein Backup nötig)'}",
        "Dieses Backup jetzt sichern oder an einen sicheren Ort verschieben.",
    ]
    return "\n".join(zeilen)


# --- CLI ------------------------------------------------------------------


def _build_parser():
    parser = argparse.ArgumentParser(
        description="Setzt wissen/ auf die OKF-Vorlage zurück (neues, leeres Projekt).",
    )
    parser.add_argument(
        "--ja",
        action="store_true",
        help="Reset wirklich ausführen (ohne dieses Flag wird nur der Plan gezeigt)",
    )
    parser.add_argument(
        "--backup",
        metavar="PFAD",
        default=None,
        help="Ziel des Backups (Standard: wissen-backup-YYYYMMDD-HHMMSS.tar.gz im Projekt-Root)",
    )
    return parser


def main(argv=None, root=None):
    parser = _build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exit_signal:
        # argparse beendet sich bei Argumentfehlern mit 2 und bei --help mit 0.
        return 0 if exit_signal.code == 0 else 1

    try:
        wurzel = _wurzel(root)
        if not wurzel.is_dir():
            raise PfadFehler(f"Projektverzeichnis nicht gefunden: {wurzel}")
        wissen_roh = wurzel / WISSEN
        if wissen_roh.is_symlink():
            raise PfadFehler(f"{WISSEN}/ darf kein Symlink sein")
        if wissen_roh.exists() and not wissen_roh.is_dir():
            raise PfadFehler(f"{WISSEN}/ ist kein Verzeichnis")
        wissen = _im_repo(wurzel, wissen_roh)
        vorlage = _im_repo(wurzel, wurzel / VORLAGE)
        if wissen == vorlage or vorlage.is_relative_to(wissen):
            raise PfadFehler("Vorlage und wissen/ dürfen nicht ineinander liegen")
        vorlage_umfang = pruefe_vorlage(vorlage)
        backup_ziel = _pruefe_backup_ziel(wurzel, wissen, vorlage, args.backup)
    except NeuesProjektFehler as fehler:
        print(f"Fehler: {fehler}", file=sys.stderr)
        return 1

    if not args.ja:
        print(plan_text(wurzel, wissen, backup_ziel, umfang(wissen), vorlage_umfang))
        return 0

    backup = None
    if wissen.is_dir():
        try:
            backup = backup_erstellen(wissen, backup_ziel)
        except NeuesProjektFehler as fehler:
            print(f"Fehler: {fehler}", file=sys.stderr)
            return 1

    try:
        tausche_gegen_vorlage(wurzel, wissen, vorlage)
    except NeuesProjektFehler as fehler:
        zusatz = f" Das Backup liegt unter: {backup}." if backup is not None else ""
        print(f"Fehler: {fehler}{zusatz}", file=sys.stderr)
        return 1

    print(erfolgs_text(backup, vorlage_umfang))
    return 0


if __name__ == "__main__":
    sys.exit(main())

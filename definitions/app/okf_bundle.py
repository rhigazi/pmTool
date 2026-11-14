"""Zugriffsschicht auf das OKF-Bundle (framework-frei).

Enthält Pfadschutz, Frontmatter-/Datei-I/O mit atomarem Schreiben und den
Bundle-Scan. Wird von ``server.py`` und den Fachmodulen genutzt.
"""

from __future__ import annotations

import os
import re
import stat
import tempfile
from pathlib import Path
from urllib.parse import unquote

import yaml

# Wurzel des Bundles; im Betrieb per Umgebungsvariable gesetzt, in Tests ersetzt.
BUNDLE_ROOT = os.environ.get("BUNDLE_ROOT", "/content/pmTool/wissen")

RESERVIERTE_DATEIEN = frozenset({"index.md", "log.md", "features.md"})

_SCHLUESSEL = re.compile(r"([A-Za-z0-9_.-]+)\s*:")


class BundlePfadFehler(ValueError):
    """Pfad liegt außerhalb von ``BUNDLE_ROOT`` oder ist unzulässig."""


class FrontmatterFehler(ValueError):
    """Datei hat kein lesbares YAML-Frontmatter."""


class EingabeFehler(ValueError):
    """Ungültige Eingabe; keine Datei wurde angelegt/verändert."""


class ReservierteDateiFehler(ValueError):
    """Ziel ist eine reservierte KI-Datei und für die App schreibgeschützt."""


# --- Pfadschutz -----------------------------------------------------------


def _wurzel() -> Path:
    return Path(os.path.realpath(BUNDLE_ROOT))


def resolve_path(rel: str | os.PathLike[str]) -> Path:
    """Bundle-relativen Pfad prüfen und als absoluten Pfad zurückgeben.

    Die Rückgabe ist ein absoluter Pfad und darf nicht wieder als Eingabe für
    :func:`lesen`, :func:`schreiben` oder :func:`set_meta` verwendet werden —
    diese erwarten einen bundle-relativen Pfad.
    """
    if rel is None:
        raise BundlePfadFehler("Pfad fehlt")
    text = unquote(str(rel)).strip()
    if not text or "\x00" in text:
        raise BundlePfadFehler("Pfad ist leer oder unzulässig")

    kandidat = Path(text)
    if kandidat.is_absolute():
        raise BundlePfadFehler(f"Absoluter Pfad nicht erlaubt: {text}")
    if ".." in kandidat.parts:
        raise BundlePfadFehler(f"Pfadausbruch nicht erlaubt: {text}")

    wurzel = _wurzel()
    ziel = Path(os.path.realpath(wurzel / kandidat))
    if not ziel.is_relative_to(wurzel):
        raise BundlePfadFehler(f"Pfad verlässt das Bundle: {text}")
    return ziel


def ist_reserviert(pfad: str | os.PathLike[str]) -> bool:
    """Reservierte KI-Dateien (``index.md``, ``log.md``, ``features.md``)."""
    return Path(str(pfad)).name in RESERVIERTE_DATEIEN


def _pruefe_schreibziel(pfad: str | os.PathLike[str]) -> Path:
    """Löst den Pfad auf und weist reservierte Ziele vor jedem Zugriff ab."""
    ziel = resolve_path(pfad)
    if ist_reserviert(pfad) or ist_reserviert(ziel):
        name = Path(str(pfad)).name
        raise ReservierteDateiFehler(f"Reservierte Datei ist schreibgeschützt: {name}")
    return ziel


# --- Frontmatter ----------------------------------------------------------


def _zerlege(text: str) -> tuple[list[str] | None, str, str]:
    """Zerlegt Text in (Frontmatter-Zeilen, Body, Zeilenende).

    Ohne Frontmatter: ``(None, text, Zeilenende)``.
    """
    ende = "\r\n" if "\r\n" in text else "\n"
    if not text.startswith("---"):
        return None, text, ende
    zeilen = text.split(ende)
    if zeilen[0].strip() != "---":
        return None, text, ende
    for index in range(1, len(zeilen)):
        if zeilen[index].strip() == "---":
            return zeilen[1:index], ende.join(zeilen[index + 1 :]), ende
    return None, text, ende


def _lies_text(ziel: Path) -> str:
    with open(ziel, encoding="utf-8", newline="") as datei:
        return datei.read()


def _parse_frontmatter(zeilen: list[str]) -> dict:
    try:
        daten = yaml.safe_load("\n".join(zeilen))
    except yaml.YAMLError as fehler:
        raise FrontmatterFehler(f"Frontmatter ist kein gültiges YAML: {fehler}") from fehler
    if daten is None:
        return {}
    if not isinstance(daten, dict):
        raise FrontmatterFehler("Frontmatter ist keine Schlüssel-Wert-Struktur")
    return daten


def lesen(pfad: str | os.PathLike[str]) -> tuple[dict, str]:
    """Datei strikt lesen: ``(frontmatter, body)``; ohne Frontmatter Fehler."""
    ziel = resolve_path(pfad)
    zeilen, body, _ = _zerlege(_lies_text(ziel))
    if zeilen is None:
        raise FrontmatterFehler(f"Frontmatter fehlt: {ziel.name}")
    return _parse_frontmatter(zeilen), body


def lesen_tolerant(pfad: str | os.PathLike[str]) -> tuple[dict, str]:
    """Wie :func:`lesen`, aber ohne Frontmatter ``({}, volltext)`` statt Fehler."""
    ziel = resolve_path(pfad)
    text = _lies_text(ziel)
    zeilen, body, _ = _zerlege(text)
    if zeilen is None:
        return {}, text
    try:
        return _parse_frontmatter(zeilen), body
    except FrontmatterFehler:
        return {}, text


def _yaml_zeilen(schluessel: str, wert: object) -> list[str]:
    try:
        return yaml.safe_dump(
            {schluessel: wert},
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        ).splitlines()
    except yaml.YAMLError as fehler:
        raise FrontmatterFehler(f"Wert für {schluessel!r} nicht schreibbar: {fehler}") from fehler


def _setze_zeilen(zeilen: list[str], schluessel: str, wert: object) -> list[str]:
    """Ersetzt einen Top-Level-Key samt Folgezeilen, sonst anhängen."""
    if not isinstance(schluessel, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+", schluessel):
        raise FrontmatterFehler(f"Ungültiger Frontmatter-Schlüssel: {schluessel!r}")

    ergebnis = list(zeilen)
    start = None
    for index, zeile in enumerate(ergebnis):
        treffer = _SCHLUESSEL.match(zeile)
        if treffer and treffer.group(1) == schluessel:
            start = index
            break

    if start is None:
        return ergebnis + _yaml_zeilen(schluessel, wert)

    ende = start + 1
    while ende < len(ergebnis) and ergebnis[ende][:1] in (" ", "\t", "-"):
        ende += 1
    return ergebnis[:start] + _yaml_zeilen(schluessel, wert) + ergebnis[ende:]


def set_meta(pfad: str | os.PathLike[str], updates: dict) -> dict:
    """Setzt ausschließlich die angegebenen Frontmatter-Keys; Body bleibt unverändert."""
    ziel = _pruefe_schreibziel(pfad)
    text = _lies_text(ziel)
    zeilen, body, ende = _zerlege(text)
    if zeilen is None:
        raise FrontmatterFehler(f"Frontmatter fehlt: {ziel.name}")
    _parse_frontmatter(zeilen)

    for schluessel, wert in updates.items():
        zeilen = _setze_zeilen(zeilen, schluessel, wert)

    aktualisiert = _parse_frontmatter(zeilen)
    _schreibe_atomar(ziel, ende.join(["---", *zeilen, "---"]) + ende + body)
    return aktualisiert


# --- Schreiben und Scan ---------------------------------------------------


def _schreibe_atomar(ziel: Path, inhalt: str) -> None:
    """Schreibt über eine Temporärdatei und ``os.replace`` — nie halbe Dateien."""
    ziel.parent.mkdir(parents=True, exist_ok=True)
    modus = stat.S_IMODE(ziel.stat().st_mode) if ziel.exists() else None

    fd, temp = tempfile.mkstemp(dir=ziel.parent, prefix=".tmp-", suffix=ziel.suffix)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as datei:
            datei.write(inhalt)
            datei.flush()
            os.fsync(datei.fileno())
        if modus is not None:
            os.chmod(temp, modus)
        os.replace(temp, ziel)
    except BaseException:
        Path(temp).unlink(missing_ok=True)
        raise


def schreiben(pfad: str | os.PathLike[str], inhalt: str) -> Path:
    """Schreibt ``inhalt`` atomar in die (bundle-relative) Datei und liefert deren Pfad."""
    ziel = _pruefe_schreibziel(pfad)
    _schreibe_atomar(ziel, inhalt)
    return ziel


def scan() -> list[str]:
    """Alle ``.md``-Dateien des Bundles außer reservierten, als relative Pfade."""
    wurzel = _wurzel()
    ergebnis: list[str] = []
    for treffer in sorted(wurzel.rglob("*.md")):
        if not treffer.is_file():
            continue
        rel = treffer.relative_to(wurzel).as_posix()
        if ist_reserviert(rel) or treffer.name.startswith(".tmp-"):
            continue
        try:
            resolve_path(rel)
        except BundlePfadFehler:
            continue
        ergebnis.append(rel)
    return ergebnis

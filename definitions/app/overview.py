"""Lese-API-Logik: Übersichtsliste, Dateidetail und Nachträge (framework-frei).

Basis sind :mod:`okf_bundle` (Pfadschutz, Frontmatter-I/O, Scan) und
:mod:`status` (UI-Status, owner-Default). Die Übersicht listet alle
nicht-reservierten ``.md``-Dateien, absteigend nach ``zuletzt_geaendert``
(Datei-Mtime, ISO 8601) und bei Gleichstand aufsteigend nach ``path``.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

import okf_bundle
import status

UNBEKANNTER_TYP = "unbekannt"

# Markerzeile laut Technischer Spec; Folgezeilen eines Nachtrags beginnen mit ``> ``.
_MARKER = re.compile(
    r"^>\s*\*\*Nachtrag\s*\((?P<autor>[^,)]+),\s*(?P<datum>\d{4}-\d{2}-\d{2})\):\*\*\s*"
    r"(?P<text>.*)$"
)
_FOLGEZEILE = re.compile(r"^>\s?(?P<text>.*)$")


def liste(praefix: str | None = None) -> list[dict]:
    """Übersichtseinträge aller Punkte; ``praefix`` grenzt auf einen Ordner ein.

    ``praefix="aufgaben"`` liefert nur ``aufgaben/*``, ``praefix="wellen"`` nur
    ``wellen/*``. Ohne Präfix erscheinen alle nicht-reservierten ``.md``-Dateien.
    """
    pfade = okf_bundle.scan()
    if praefix:
        pfade = [pfad for pfad in pfade if pfad.startswith(f"{praefix}/")]

    eintraege = [_eintrag(pfad) for pfad in pfade]
    eintraege.sort(key=lambda eintrag: eintrag["path"])
    eintraege.sort(key=lambda eintrag: eintrag["zuletzt_geaendert"], reverse=True)
    return eintraege


def details(pfad: str) -> dict:
    """Dateiinhalt als ``{frontmatter, markdown, nachtraege}``.

    Wirft :class:`okf_bundle.BundlePfadFehler` bei Pfadausbruch und
    :class:`FileNotFoundError`, wenn die Datei fehlt.
    """
    ziel = okf_bundle.resolve_path(pfad)
    if not ziel.is_file():
        raise FileNotFoundError(f"Datei nicht gefunden: {pfad}")

    frontmatter, markdown = okf_bundle.lesen_tolerant(pfad)
    return {"frontmatter": frontmatter, "markdown": markdown, "nachtraege": nachtraege(markdown)}


def nachtraege(markdown: str) -> list[dict]:
    """Parst die Markerzeilen ``> **Nachtrag (Autor, YYYY-MM-DD):** Text``.

    Mehrzeilige Nachträge werden über die folgenden ``> ``-Zeilen ergänzt.
    """
    ergebnis: list[dict] = []
    aktuell: dict | None = None

    for zeile in markdown.splitlines():
        marker = _MARKER.match(zeile)
        if marker:
            aktuell = {
                "autor": marker.group("autor").strip(),
                "datum": marker.group("datum"),
                "text": marker.group("text").strip(),
            }
            ergebnis.append(aktuell)
            continue

        folge = _FOLGEZEILE.match(zeile)
        if aktuell is not None and folge:
            text = folge.group("text").strip()
            if text:
                aktuell["text"] = f"{aktuell['text']}\n{text}" if aktuell["text"] else text
            continue

        aktuell = None

    return ergebnis


def _eintrag(pfad: str) -> dict:
    frontmatter, _ = okf_bundle.lesen_tolerant(pfad)
    ui_status, hinweis = status.ui_status(frontmatter)

    eintrag = {
        "path": pfad,
        "typ": _text(frontmatter.get("type")) or UNBEKANNTER_TYP,
        "titel": _text(frontmatter.get("title")) or "",
        "status": ui_status,
        "owner": status.owner_default(frontmatter),
        "zuletzt_geaendert": _zeitstempel(pfad),
    }
    if hinweis:
        eintrag["hinweis"] = hinweis
    welle = _text(frontmatter.get("welle"))
    if welle:
        eintrag["welle"] = welle
    return eintrag


def _zeitstempel(pfad: str) -> str:
    """Mtime der Datei als ISO-8601-Zeitstempel in UTC."""
    mtime = okf_bundle.resolve_path(pfad).stat().st_mtime
    return datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()


def _text(wert: object) -> str | None:
    if wert is None:
        return None
    text = str(wert).strip()
    return text or None

"""Lese-API-Logik: Übersichtsliste, Dateidetail und Nachträge (framework-frei).

Basis sind :mod:`okf_bundle` (Pfadschutz, Frontmatter-I/O, Scan) und
:mod:`status` (UI-Status, owner-Default). Die Übersicht listet alle
nicht-reservierten ``.md``-Dateien, absteigend nach ``zuletzt_geaendert``
(Datei-Mtime, ISO 8601) und bei Gleichstand aufsteigend nach ``path``.

Eine einzelne unlesbare Datei darf die Übersicht nicht scheitern lassen;
Fehlermeldungen nennen nie Dateipfade oder OS-Details.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

import okf_bundle
import status

UNBEKANNTER_TYP = "unbekannt"
HINWEIS_NICHT_LESBAR = "nicht lesbar"
# Einzige Quelle der neutralen Meldungen ist okf_bundle (keine Pfade/OS-Details).
MELDUNG_NICHT_GEFUNDEN = okf_bundle.MELDUNG_NICHT_GEFUNDEN
MELDUNG_NICHT_LESBAR = okf_bundle.MELDUNG_NICHT_LESBAR

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
    praefix = praefix.strip("/") if praefix else None
    if praefix:
        pfade = [pfad for pfad in pfade if pfad.startswith(f"{praefix}/")]

    eintraege = []
    for pfad in pfade:
        eintrag = _eintrag(pfad)
        if eintrag is not None:
            eintraege.append(eintrag)
    eintraege.sort(key=lambda eintrag: eintrag["path"])
    eintraege.sort(key=lambda eintrag: eintrag["zuletzt_geaendert"], reverse=True)
    return eintraege


def details(pfad: str) -> dict:
    """Dateiinhalt als ``{frontmatter, markdown, nachtraege}``.

    Wirft :class:`okf_bundle.BundlePfadFehler` bei Pfadausbruch oder nicht
    zulässiger Endung, :class:`FileNotFoundError`, wenn die Datei fehlt, und
    :class:`PermissionError`, wenn sie nicht lesbar ist. Die Meldungen sind
    neutral und nennen keinen Dateipfad.
    """
    ziel = okf_bundle.resolve_path(pfad)
    if ziel.suffix.lower() != ".md":
        raise okf_bundle.BundlePfadFehler("Nur .md-Dateien sind lesbar")
    if not ziel.is_file():
        raise FileNotFoundError(MELDUNG_NICHT_GEFUNDEN)

    frontmatter, markdown = _lesen(pfad)
    return {"frontmatter": frontmatter, "markdown": markdown, "nachtraege": nachtraege(markdown)}


def nachtraege(markdown: str) -> list[dict]:
    """Parst die Markerzeilen ``> **Nachtrag (Autor, YYYY-MM-DD):** Text``.

    Folgezeilen mit ``> `` werden übernommen; eine leere ``>``-Zeile steht für
    einen Absatzumbruch und bleibt als Leerzeile im Text erhalten.
    """
    roh: list[dict] = []
    aktuell: dict | None = None

    for zeile in markdown.splitlines():
        marker = _MARKER.match(zeile)
        if marker:
            aktuell = {
                "autor": marker.group("autor").strip(),
                "datum": marker.group("datum"),
                "zeilen": [marker.group("text")],
            }
            roh.append(aktuell)
            continue

        folge = _FOLGEZEILE.match(zeile)
        if aktuell is not None and folge:
            aktuell["zeilen"].append(folge.group("text"))
            continue

        aktuell = None

    return [
        {
            "autor": eintrag["autor"],
            "datum": eintrag["datum"],
            "text": _nachtrag_text(eintrag["zeilen"]),
        }
        for eintrag in roh
    ]


def _nachtrag_text(zeilen: list[str]) -> str:
    """Zeilen eines Nachtrags als Text mit Leerzeilen als Absatzumbruch."""
    return "\n".join(zeile.strip() for zeile in zeilen).strip()


def _lesen(pfad: str) -> tuple[dict, str]:
    """Liest tolerant; OS- und Encoding-Fehler werden neutral übersetzt."""
    try:
        return okf_bundle.lesen_tolerant(pfad)
    except FileNotFoundError:
        raise FileNotFoundError(MELDUNG_NICHT_GEFUNDEN) from None
    except (OSError, UnicodeDecodeError):
        raise PermissionError(MELDUNG_NICHT_LESBAR) from None


def _eintrag(pfad: str) -> dict | None:
    """Übersichtseintrag einer Datei; ``None``, wenn sie inzwischen gelöscht ist."""
    try:
        frontmatter, _ = okf_bundle.lesen_tolerant(pfad)
        zeitstempel = _zeitstempel(pfad)
    except FileNotFoundError:
        return None
    except (OSError, UnicodeDecodeError):
        return _nicht_lesbarer_eintrag(pfad)

    ui_status, hinweis = status.ui_status(frontmatter)

    eintrag = {
        "path": pfad,
        "typ": _text(frontmatter.get("type")) or UNBEKANNTER_TYP,
        "titel": _text(frontmatter.get("title")) or "",
        "status": ui_status,
        "owner": status.owner_default(frontmatter),
        "zuletzt_geaendert": zeitstempel,
    }
    if hinweis:
        eintrag["hinweis"] = hinweis
    welle = _text(frontmatter.get("welle"))
    if welle:
        eintrag["welle"] = welle
    return eintrag


def _nicht_lesbarer_eintrag(pfad: str) -> dict | None:
    """Ersatzzeile für eine unlesbare Datei; ``None``, wenn auch ``stat`` scheitert."""
    try:
        zeitstempel = _zeitstempel(pfad)
    except OSError:
        return None

    return {
        "path": pfad,
        "typ": UNBEKANNTER_TYP,
        "titel": "",
        "status": status.OFFEN,
        "owner": None,
        "zuletzt_geaendert": zeitstempel,
        "hinweis": HINWEIS_NICHT_LESBAR,
    }



def _zeitstempel(pfad: str) -> str:
    """Mtime der Datei als ISO-8601-Zeitstempel in UTC."""
    mtime = okf_bundle.resolve_path(pfad).stat().st_mtime
    return datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()


def _text(wert: object) -> str | None:
    if wert is None:
        return None
    text = str(wert).strip()
    return text or None

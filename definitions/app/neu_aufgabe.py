"""Neue Aufgaben-Datei im Phasen-Format anlegen.

Erzeugt ``aufgaben/<slug>.md`` aus den Formulardaten der App: Frontmatter nach
dem Phasenmodell (ergänzt um ``owner: ai``), Body mit allen sechs Abschnitten
und ein freier, lesbarer ASCII-Slug (Entscheidung R2). Vorhandene Dateien
werden nie überschrieben — Kollisionen bekommen ein Suffix (``-2``, ``-3``, …).
"""

from __future__ import annotations

import re
import unicodedata

import yaml

import okf_bundle
from okf_bundle import EingabeFehler

AUFGABEN_ORDNER = "aufgaben"
MAX_SLUG_LAENGE = 60
MAX_KURZBESCHREIBUNG = 160
MAX_KANDIDATEN = 1000

PRIORITAETEN = ("hoch", "mittel", "niedrig")

_UMLAUTE = str.maketrans(
    {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "Ä": "Ae",
        "Ö": "Oe",
        "Ü": "Ue",
        "ß": "ss",
    }
)
_NICHT_SLUG = re.compile(r"[^a-z0-9]+")

ERGEBNIS_PLATZHALTER = (
    "Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, "
    "Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege."
)


# --- Öffentliche Schnittstelle --------------------------------------------


def anlegen(daten: dict) -> str:
    """Legt eine neue Aufgaben-Datei an und liefert ihren bundle-relativen Pfad.

    Erwartet ``{titel, ziel, akzeptanz[], prioritaet, welle?, user_story?}``.
    Unzulässige Daten führen zu :class:`EingabeFehler`, ohne dass eine Datei
    entsteht.
    """
    felder = _pruefe(daten)
    pfad = _freier_pfad(felder["slug"])
    okf_bundle.schreiben(pfad, _inhalt(felder))
    return pfad


def slug_aus_titel(titel: str) -> str:
    """ASCII-Slug aus dem Titel: Umlaute → ASCII, Sonderzeichen → ``-``, max. 60."""
    text = str(titel).translate(_UMLAUTE).lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(zeichen for zeichen in text if not unicodedata.combining(zeichen))

    slug = _NICHT_SLUG.sub("-", text).strip("-")
    if len(slug) > MAX_SLUG_LAENGE:
        slug = slug[:MAX_SLUG_LAENGE].rstrip("-")
    return slug


# --- Eingabeprüfung -------------------------------------------------------


def _pruefe(daten: dict) -> dict:
    """Validiert und normalisiert die Formulardaten; wirft sonst ``EingabeFehler``."""
    if not isinstance(daten, dict):
        raise EingabeFehler("Formulardaten fehlen")

    titel = _text(daten.get("titel"), "Titel", einzeilig=True)
    ziel = _text(daten.get("ziel"), "Ziel")
    akzeptanz = _akzeptanzliste(daten.get("akzeptanz"))

    prioritaet = daten.get("prioritaet")
    if not isinstance(prioritaet, str) or not prioritaet.strip():
        raise EingabeFehler("Priorität fehlt")
    prioritaet = prioritaet.strip()
    if prioritaet not in PRIORITAETEN:
        raise EingabeFehler(
            f"Unzulässige Priorität {prioritaet!r} "
            f"(erlaubt: {', '.join(PRIORITAETEN)})"
        )

    slug = slug_aus_titel(titel)
    if not slug:
        raise EingabeFehler("Titel enthält keine verwendbaren Zeichen für ein Kürzel")

    return {
        "titel": titel,
        "ziel": ziel,
        "akzeptanz": akzeptanz,
        "prioritaet": prioritaet,
        "slug": slug,
        "user_story": _verweis(daten.get("user_story"), "user_story"),
        "welle": _verweis(daten.get("welle"), "welle"),
    }


def _text(wert: object, feldname: str, einzeilig: bool = False) -> str:
    if not isinstance(wert, str) or not wert.strip():
        raise EingabeFehler(f"{feldname} fehlt")
    return " ".join(wert.split()) if einzeilig else wert.strip()


def _akzeptanzliste(wert: object) -> list[str]:
    if not isinstance(wert, (list, tuple)):
        raise EingabeFehler("Akzeptanzkriterien müssen als Liste übergeben werden")

    eintraege: list[str] = []
    for eintrag in wert:
        if not isinstance(eintrag, str):
            raise EingabeFehler("Akzeptanzkriterien müssen Text sein")
        if eintrag.strip():
            eintraege.append(" ".join(eintrag.split()))
    if not eintraege:
        raise EingabeFehler("Mindestens ein Akzeptanzkriterium ist nötig")
    return eintraege


def _verweis(wert: object, feldname: str) -> str | None:
    """Optionaler Bundle-Verweis; leer oder fehlend ergibt ``None``."""
    if wert is None:
        return None
    if not isinstance(wert, str):
        raise EingabeFehler(f"{feldname} muss ein Pfad sein")
    text = " ".join(wert.split())
    return text or None


# --- Dateiname ------------------------------------------------------------


def _freier_pfad(slug: str) -> str:
    """Erster freier Dateiname im Aufgaben-Ordner; reservierte Dateien bleiben frei."""
    for nummer in range(1, MAX_KANDIDATEN + 1):
        name = f"{slug}.md" if nummer == 1 else f"{slug}-{nummer}.md"
        if okf_bundle.ist_reserviert(name):
            continue
        pfad = f"{AUFGABEN_ORDNER}/{name}"
        if not okf_bundle.resolve_path(pfad).exists():
            return pfad
    raise EingabeFehler(f"Kein freier Dateiname für {slug!r} gefunden")


# --- Dateiinhalt ----------------------------------------------------------


def _inhalt(felder: dict) -> str:
    frontmatter = {
        "type": "Task",
        "title": felder["titel"],
        "description": _kurzbeschreibung(felder["ziel"]),
        "task_status": "offen",
        "phase": "2 Planung",
        "priority": felder["prioritaet"],
        "assigned_to": "coder",
    }
    for feld in ("user_story", "welle"):
        if felder[feld]:
            frontmatter[feld] = felder[feld]
    frontmatter["owner"] = "ai"

    kopf = yaml.safe_dump(
        frontmatter,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    ).rstrip("\n")
    return f"---\n{kopf}\n---\n{_body(felder)}"


def _body(felder: dict) -> str:
    akzeptanz = "".join(f"- {eintrag}\n" for eintrag in felder["akzeptanz"])
    return (
        "\n# Ziel\n\n"
        f"{felder['ziel']}\n\n"
        "# Akzeptanzkriterien\n\n"
        f"{akzeptanz}\n"
        "# Testfälle (TDD)\n\n"
        "Noch keine Einträge — der `planner` ergänzt die Testfälle.\n\n"
        "# Kontext\n\n"
        f"{_kontext(felder)}\n\n"
        "# Betroffene Dateien\n\n"
        "Noch keine Einträge — die Planung ergänzt die betroffenen Dateien.\n\n"
        "# Ergebnisse\n\n"
        f"{ERGEBNIS_PLATZHALTER}\n"
    )


def _kontext(felder: dict) -> str:
    zeilen = []
    if felder["user_story"]:
        zeilen.append(f"- User Story: {_verweis_zeile(felder['user_story'])}")
    if felder["welle"]:
        zeilen.append(f"- Welle: {_verweis_zeile(felder['welle'])}")
    return "\n".join(zeilen) or "Kein zusätzlicher Kontext angegeben."


def _verweis_zeile(pfad: str) -> str:
    name = pfad.rstrip("/").rsplit("/", 1)[-1].removesuffix(".md")
    return f"[{name}]({pfad})"


def _kurzbeschreibung(ziel: str) -> str:
    """Erste Zeile des Ziels als OKF-``description`` (max. 160 Zeichen)."""
    erste = ziel.splitlines()[0].strip() or ziel.strip()
    if len(erste) <= MAX_KURZBESCHREIBUNG:
        return erste
    return erste[: MAX_KURZBESCHREIBUNG - 1].rstrip() + "…"

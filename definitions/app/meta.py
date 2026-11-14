"""``owner`` und die erlaubten UI-Status setzen — mit serverseitiger Rechteprüfung.

Die App darf ``owner`` umschalten und den Status ausschließlich auf ``Klarung``
und ``Geschlossen`` setzen (Entscheidung R1); Pipeline-Status bleiben der KI
vorbehalten. Geschrieben wird immer in einem einzigen, atomaren Vorgang über
:func:`okf_bundle.set_meta`.
"""

from __future__ import annotations

from typing import Any

import okf_bundle

OWNER_WERTE = ("mensch", "ai")
STATUS_WERTE = ("Klarung", "Geschlossen")

# Erlaubter UI-Status -> zu schreibender ``task_status`` (Technische Spec, R1).
TASK_STATUS_ZIELE = {"Klarung": "in Klärung", "Geschlossen": "abgeschlossen"}


class RechteFehler(PermissionError):
    """Die App darf diesen Zielwert bzw. diese Datei nicht schreiben (HTTP 403)."""


def setzen(pfad: str, owner: str | None = None, status: str | None = None) -> dict:
    """Setzt ``owner`` und/oder ``status`` und liefert das neue Frontmatter.

    Ohne Zielwerte wird nichts geschrieben. Reservierte Dateien, unbekannte
    Zielwerte und Dateien ohne Frontmatter werden abgewiesen, bevor geschrieben
    wird; der Body bleibt unverändert.
    """
    ziel = okf_bundle.resolve_path(pfad)
    if okf_bundle.ist_reserviert(pfad) or okf_bundle.ist_reserviert(ziel):
        raise RechteFehler(f"Reservierte Datei ist schreibgeschützt: {ziel.name}")

    if owner is not None:
        owner = _pruefe_owner(owner)
    if status is not None:
        status = _pruefe_status(status)

    # Validierung vollständig vor dem Lesen: nur bestehende .md-Dateien.
    okf_bundle.pruefe_zieldatei(pfad)
    frontmatter, _ = okf_bundle.lesen(pfad)

    updates: dict[str, Any] = {}
    if owner is not None:
        updates["owner"] = owner
    if status is not None:
        if _hat_task_status(frontmatter):
            updates["task_status"] = TASK_STATUS_ZIELE[status]
        else:
            updates["status"] = status

    if not updates:
        return frontmatter
    return okf_bundle.set_meta(pfad, updates)


def _pruefe_owner(owner: Any) -> str:
    if owner not in OWNER_WERTE:
        raise RechteFehler(f"owner darf nur 'mensch' oder 'ai' sein, nicht {owner!r}")
    return owner


def _pruefe_status(status: Any) -> str:
    if status not in STATUS_WERTE:
        raise RechteFehler(
            "Status darf die App nur auf 'Klarung' oder 'Geschlossen' setzen, "
            f"nicht {status!r} — Pipeline-Status bleibt der KI vorbehalten"
        )
    return status


def _hat_task_status(frontmatter: dict) -> bool:
    """Punkte mit ``task_status`` (Aufgaben) werden darüber gesteuert, sonst ``status``."""
    wert = frontmatter.get("task_status")
    return wert is not None and str(wert).strip() != ""

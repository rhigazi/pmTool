"""TDD-Tests für die Lese-API ``GET /api/overview|file|aufgaben|wellen`` (Aufgabe A8)."""

import os
import sys
from datetime import datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import server

AUFGABE = "aufgaben/a1.md"
ZWEITE_AUFGABE = "aufgaben/a2.md"
WELLE = "wellen/w1.md"

ZEIT_FRUEH = 1_700_000_000
ZEIT_SPAET = 1_700_100_000


@pytest.fixture()
def client(bundle):
    return server.create_app(bundle).test_client()


def _schreibe(bundle, pfad: str, text: str) -> Path:
    ziel = bundle / pfad
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(text, encoding="utf-8")
    return ziel


def _aufgabe(bundle, pfad: str, titel: str, task_status: str = "offen") -> Path:
    return _schreibe(
        bundle,
        pfad,
        f"---\ntype: Task\ntitle: {titel!r}\ntask_status: {task_status}\nowner: ai\n---\n\n"
        "# Ziel\n\nFixture.\n",
    )


def _setze_mtime(ziel: Path, zeit: int) -> None:
    os.utime(ziel, (zeit, zeit))


def _pfade(antwort) -> list[str]:
    return [eintrag["path"] for eintrag in antwort.get_json()]


# --- Overview -------------------------------------------------------------


def test_t1_overview_liste(client, bundle):
    _aufgabe(bundle, ZWEITE_AUFGABE, "A2: Zweite Aufgabe")

    antwort = client.get("/api/overview")

    assert antwort.status_code == 200
    assert antwort.mimetype == "application/json"
    assert isinstance(antwort.get_json(), list)
    assert len(antwort.get_json()) == 3


def test_t2_feldschema(client):
    eintraege = client.get("/api/overview").get_json()

    assert eintraege
    for eintrag in eintraege:
        assert {
            "path",
            "typ",
            "titel",
            "status",
            "owner",
            "zuletzt_geaendert",
        } <= set(eintrag)


def test_t2_zeitstempel_ist_iso_8601(client):
    for eintrag in client.get("/api/overview").get_json():
        zeit = datetime.fromisoformat(eintrag["zuletzt_geaendert"])

        assert zeit.tzinfo is not None


def test_t2_welle_feld_wird_durchgereicht(client, bundle):
    _schreibe(
        bundle,
        ZWEITE_AUFGABE,
        "---\ntype: Task\ntitle: \"A2: In Welle\"\ntask_status: offen\n"
        "welle: /wellen/w1.md\n---\n\n# Ziel\n",
    )

    eintraege = {eintrag["path"]: eintrag for eintrag in client.get("/api/overview").get_json()}

    assert eintraege[ZWEITE_AUFGABE]["welle"] == "/wellen/w1.md"


def test_t3_status_mapping_in_umsetzung(client, bundle):
    _aufgabe(bundle, ZWEITE_AUFGABE, "A2: In Umsetzung", task_status="in Umsetzung")

    eintraege = {eintrag["path"]: eintrag for eintrag in client.get("/api/overview").get_json()}

    assert eintraege[ZWEITE_AUFGABE]["status"] == "In Arbeit"
    assert eintraege[ZWEITE_AUFGABE]["owner"] == "ai"
    assert "hinweis" not in eintraege[ZWEITE_AUFGABE]


def test_t3_owner_aus_status_default(client):
    eintraege = {eintrag["path"]: eintrag for eintrag in client.get("/api/overview").get_json()}

    assert eintraege[AUFGABE]["owner"] == "ai"
    assert eintraege[WELLE]["owner"] == "ai"


def test_t3_pausiert_hat_hinweis(client, bundle):
    _aufgabe(bundle, ZWEITE_AUFGABE, "A2: Pausiert", task_status="pausiert")

    eintraege = {eintrag["path"]: eintrag for eintrag in client.get("/api/overview").get_json()}

    assert eintraege[ZWEITE_AUFGABE]["hinweis"] == "pausiert"


def test_t4_sortierung_absteigend_mit_pfad_tiebreaker(client, bundle):
    _aufgabe(bundle, ZWEITE_AUFGABE, "A2: Gleich alt")
    _setze_mtime(bundle / ZWEITE_AUFGABE, ZEIT_SPAET)
    _setze_mtime(bundle / WELLE, ZEIT_SPAET)
    _setze_mtime(bundle / AUFGABE, ZEIT_FRUEH)

    antwort = client.get("/api/overview")

    assert _pfade(antwort) == [ZWEITE_AUFGABE, WELLE, AUFGABE]


def test_t5_reservierte_dateien_sind_nicht_gelistet(client):
    pfade = _pfade(client.get("/api/overview"))

    for reserviert in ("index.md", "log.md", "features.md", "aufgaben/index.md"):
        assert reserviert not in pfade


# --- Dateidetail ----------------------------------------------------------


def test_t6_detaildatei(client):
    antwort = client.get("/api/file", query_string={"path": AUFGABE})

    assert antwort.status_code == 200
    daten = antwort.get_json()
    assert daten["frontmatter"]["type"] == "Task"
    assert daten["frontmatter"]["title"] == "A1: Mini-Aufgabe"
    assert daten["markdown"].lstrip().startswith("# Ziel")
    assert "type: Task" not in daten["markdown"]
    assert daten["nachtraege"] == []


def test_t6_reservierte_datei_ist_lesbar(client):
    antwort = client.get("/api/file", query_string={"path": "log.md"})

    assert antwort.status_code == 200
    assert antwort.get_json()["frontmatter"]["type"] == "Log"


@pytest.mark.parametrize(
    "pfad",
    [
        "../../etc/passwd",
        "/etc/passwd",
        "aufgaben/../../etc/passwd",
        "a/%2e%2e/b.md",
    ],
)
def test_t7_traversal_ist_400_ohne_inhalt(client, pfad):
    antwort = client.get("/api/file", query_string={"path": pfad})

    assert antwort.status_code == 400
    assert antwort.mimetype == "application/json"
    assert antwort.get_json()["error"]
    assert "root:" not in antwort.get_data(as_text=True)


def test_t7_fehlender_path_parameter_ist_400(client):
    antwort = client.get("/api/file")

    assert antwort.status_code == 400
    assert antwort.get_json()["error"]


def test_t8_fehlende_datei_ist_404(client):
    antwort = client.get("/api/file", query_string={"path": "aufgaben/gibt-es-nicht.md"})

    assert antwort.status_code == 404
    assert antwort.get_json()["error"]


# --- Gefilterte Listen ----------------------------------------------------


def test_t9_nur_aufgaben(client, bundle):
    _aufgabe(bundle, ZWEITE_AUFGABE, "A2: Zweite Aufgabe")

    antwort = client.get("/api/aufgaben")

    assert antwort.status_code == 200
    pfade = _pfade(antwort)
    assert set(pfade) == {AUFGABE, ZWEITE_AUFGABE}
    assert all(pfad.startswith("aufgaben/") for pfad in pfade)


def test_t10_nur_wellen(client):
    antwort = client.get("/api/wellen")

    assert antwort.status_code == 200
    assert _pfade(antwort) == [WELLE]


def test_t10_leeres_wellenverzeichnis(client, bundle):
    (bundle / WELLE).unlink()

    antwort = client.get("/api/wellen")

    assert antwort.status_code == 200
    assert antwort.get_json() == []


# --- Randfälle ------------------------------------------------------------


def test_t11_datei_ohne_frontmatter(client, bundle):
    _schreibe(bundle, "aufgaben/ohne.md", "# Nur Text\n\nkein Frontmatter\n")

    eintraege = {eintrag["path"]: eintrag for eintrag in client.get("/api/overview").get_json()}
    detail = client.get("/api/file", query_string={"path": "aufgaben/ohne.md"})

    assert eintraege["aufgaben/ohne.md"]["typ"] == "unbekannt"
    assert eintraege["aufgaben/ohne.md"]["status"] == "Offen"
    assert detail.status_code == 200
    assert detail.get_json()["frontmatter"] == {}
    assert "kein Frontmatter" in detail.get_json()["markdown"]


def test_t12_nachtrag_parsing(client, bundle):
    _schreibe(
        bundle,
        "aufgaben/mit-nachtraegen.md",
        "---\ntype: Task\ntitle: Mit Nachträgen\ntask_status: offen\n---\n\n"
        "# Ziel\n\nText.\n\n# Nachträge\n\n"
        "> **Nachtrag (Mensch, 2026-11-14):** Bitte prüfen.\n\n"
        "> **Nachtrag (Mensch, 2026-11-15):** Zweiter Eintrag\n"
        "> mit Folgezeile.\n",
    )

    antwort = client.get("/api/file", query_string={"path": "aufgaben/mit-nachtraegen.md"})

    assert antwort.status_code == 200
    assert antwort.get_json()["nachtraege"] == [
        {"autor": "Mensch", "datum": "2026-11-14", "text": "Bitte prüfen."},
        {"autor": "Mensch", "datum": "2026-11-15", "text": "Zweiter Eintrag\nmit Folgezeile."},
    ]

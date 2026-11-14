"""TDD-Tests für die Schreib-API ``POST /api/nachtrag|task|welle|meta`` (Aufgabe A9)."""

import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import server

AUFGABE = "aufgaben/a1.md"
WELLE = "wellen/w1.md"

ENDPUNKTE = ("/api/nachtrag", "/api/task", "/api/welle", "/api/meta")
RESERVIERTE = ("index.md", "log.md", "features.md", "aufgaben/index.md")
TRAVERSAL = (
    "../fremd.md",
    "../../etc/passwd",
    "/etc/passwd",
    "aufgaben/../../etc/passwd",
    "a/%2e%2e/b.md",
)


@pytest.fixture()
def client(bundle):
    return server.create_app(bundle).test_client()


def _aufgabe_daten(**abweichungen) -> dict:
    daten = {
        "titel": "A99: Neue Aufgabe",
        "ziel": "Ziel der neuen Aufgabe.",
        "akzeptanz": ["Erstes Kriterium.", "Zweites Kriterium."],
        "prioritaet": "hoch",
    }
    daten.update(abweichungen)
    return daten


def _welle_daten(**abweichungen) -> dict:
    daten = {
        "titel": "Welle 2: Neu",
        "ziel": "Ziel der neuen Welle.",
        "status": "Offen",
        "owner": "ai",
    }
    daten.update(abweichungen)
    return daten


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _lies(bundle, pfad: str) -> str:
    with open(bundle / pfad, encoding="utf-8", newline="") as datei:
        return datei.read()


def _datei_hash(bundle, pfad: str) -> str:
    return _hash(_lies(bundle, pfad))


def _bestand(bundle) -> list[str]:
    """Alle Dateien und Verzeichnisse im Bundle (Teilzustand wäre hier sichtbar)."""
    return sorted(pfad.relative_to(bundle).as_posix() for pfad in bundle.rglob("*"))


def _aussen(bundle) -> list[str]:
    """Alles neben dem Bundle-Verzeichnis (dort darf nie etwas entstehen)."""
    return sorted(pfad.name for pfad in bundle.parent.iterdir() if pfad.name != bundle.name)


# --- T1/T2: Nachtrag ------------------------------------------------------


def test_t1_nachtrag_anfuegen(client, bundle):
    antwort = client.post("/api/nachtrag", json={"path": AUFGABE, "text": "Bitte präzisieren."})

    assert antwort.status_code == 200
    assert antwort.mimetype == "application/json"
    daten = antwort.get_json()
    assert daten["path"] == AUFGABE
    assert "Bitte präzisieren." in daten["markdown"]
    assert daten["frontmatter"]["type"] == "Task"
    letzter = daten["nachtraege"][-1]
    assert letzter["autor"] == "Mensch"
    assert letzter["text"] == "Bitte präzisieren."
    assert letzter["datum"] == datetime.now(timezone.utc).date().isoformat()

    inhalt = _lies(bundle, AUFGABE)
    assert inhalt.startswith("---\ntype: Task")
    assert "> **Nachtrag (Mensch, " in inhalt
    assert "Bitte präzisieren." in inhalt


@pytest.mark.parametrize("text", [None, "", "   ", "\n\t\n"])
def test_t2_nachtrag_leer_ist_400(client, bundle, text):
    hash_vorher = _datei_hash(bundle, AUFGABE)

    antwort = client.post("/api/nachtrag", json={"path": AUFGABE, "text": text})

    assert antwort.status_code == 400
    assert antwort.mimetype == "application/json"
    assert antwort.get_json()["error"]
    assert _datei_hash(bundle, AUFGABE) == hash_vorher


# --- T3/T4: Aufgabe ------------------------------------------------------


def test_t3_aufgabe_anlegen(client):
    antwort = client.post("/api/task", json=_aufgabe_daten())

    assert antwort.status_code == 200
    assert antwort.mimetype == "application/json"
    pfad = antwort.get_json()["path"]
    assert pfad == "aufgaben/a99-neue-aufgabe.md"

    eintraege = {eintrag["path"]: eintrag for eintrag in client.get("/api/overview").get_json()}
    assert eintraege[pfad]["typ"] == "Task"
    assert eintraege[pfad]["status"] == "Offen"
    assert eintraege[pfad]["owner"] == "ai"


@pytest.mark.parametrize("feld", ["titel", "ziel", "akzeptanz", "prioritaet"])
def test_t4_aufgabe_unvollstaendig_ist_400(client, bundle, feld):
    daten = _aufgabe_daten()
    del daten[feld]
    bestand_vorher = _bestand(bundle)

    antwort = client.post("/api/task", json=daten)

    assert antwort.status_code == 400
    assert antwort.get_json()["error"]
    assert _bestand(bundle) == bestand_vorher


def test_t4_aufgabe_ungueltige_prioritaet_ist_400(client, bundle):
    bestand_vorher = _bestand(bundle)

    antwort = client.post("/api/task", json=_aufgabe_daten(prioritaet="dringend"))

    assert antwort.status_code == 400
    assert antwort.get_json()["error"]
    assert _bestand(bundle) == bestand_vorher


# --- T5/T6: Welle --------------------------------------------------------


def test_t5_welle_anlegen(client):
    antwort = client.post("/api/welle", json=_welle_daten())

    assert antwort.status_code == 200
    assert antwort.mimetype == "application/json"
    pfad = antwort.get_json()["path"]
    assert pfad == "wellen/welle-2-neu.md"

    pfade = [eintrag["path"] for eintrag in client.get("/api/wellen").get_json()]
    assert pfad in pfade


def test_welle_legt_wellen_ordner_bei_erstanlage(client, bundle):
    (bundle / WELLE).unlink()
    (bundle / "wellen").rmdir()

    antwort = client.post("/api/welle", json=_welle_daten())

    assert antwort.status_code == 200
    assert antwort.get_json()["path"].startswith("wellen/")
    assert (bundle / "wellen").is_dir()


@pytest.mark.parametrize("status_wert", ["In Umsetzung", "offen", "Unbekannt", "", None])
def test_t6_welle_ungueltiger_status_ist_400(client, bundle, status_wert):
    bestand_vorher = _bestand(bundle)

    antwort = client.post("/api/welle", json=_welle_daten(status=status_wert))

    assert antwort.status_code == 400
    assert antwort.mimetype == "application/json"
    assert antwort.get_json()["error"]
    assert _bestand(bundle) == bestand_vorher


# --- T7/T8/T9: Meta ------------------------------------------------------


@pytest.mark.parametrize("owner", ["mensch", "ai"])
def test_t7_meta_owner(client, bundle, owner):
    antwort = client.post("/api/meta", json={"path": AUFGABE, "owner": owner})

    assert antwort.status_code == 200
    assert antwort.mimetype == "application/json"
    daten = antwort.get_json()
    assert daten["path"] == AUFGABE
    assert daten["frontmatter"]["owner"] == owner
    assert f"owner: {owner}" in _lies(bundle, AUFGABE)


def test_t8_meta_erlaubter_status(client, bundle):
    antwort = client.post("/api/meta", json={"path": AUFGABE, "status": "Klarung"})

    assert antwort.status_code == 200
    assert antwort.get_json()["frontmatter"]["task_status"] == "in Klärung"
    assert "task_status: in Klärung" in _lies(bundle, AUFGABE)


@pytest.mark.parametrize("verboten", ["Testing", "In Arbeit", "Offen", "Dokumentation"])
def test_t8_meta_pipeline_status_ist_403(client, bundle, verboten):
    hash_vorher = _datei_hash(bundle, AUFGABE)

    antwort = client.post("/api/meta", json={"path": AUFGABE, "status": verboten})

    assert antwort.status_code == 403
    assert antwort.mimetype == "application/json"
    assert antwort.get_json()["error"]
    assert _datei_hash(bundle, AUFGABE) == hash_vorher


@pytest.mark.parametrize("pfad", RESERVIERTE)
def test_t9_meta_reserviert_ist_geschuetzt(client, bundle, pfad):
    hash_vorher = _datei_hash(bundle, pfad)

    antwort = client.post("/api/meta", json={"path": pfad, "owner": "mensch"})

    assert antwort.status_code in (400, 403)
    assert antwort.get_json()["error"]
    assert _datei_hash(bundle, pfad) == hash_vorher


@pytest.mark.parametrize("pfad", RESERVIERTE)
def test_t9_nachtrag_reserviert_ist_403(client, bundle, pfad):
    hash_vorher = _datei_hash(bundle, pfad)

    antwort = client.post("/api/nachtrag", json={"path": pfad, "text": "Eintrag der App."})

    assert antwort.status_code == 403
    assert antwort.get_json()["error"]
    assert _datei_hash(bundle, pfad) == hash_vorher


# --- T10: Pfadausbruch ---------------------------------------------------


@pytest.mark.parametrize("pfad", TRAVERSAL)
@pytest.mark.parametrize(
    ("endpunkt", "nutzlast"),
    [
        ("/api/nachtrag", {"text": "Text"}),
        ("/api/meta", {"owner": "ai"}),
    ],
)
def test_t10_traversal_ist_400(client, bundle, endpunkt, nutzlast, pfad):
    aussen_vorher = _aussen(bundle)

    antwort = client.post(endpunkt, json={"path": pfad, **nutzlast})

    assert antwort.status_code == 400
    assert antwort.mimetype == "application/json"
    assert antwort.get_json()["error"]
    assert "root:" not in antwort.get_data(as_text=True)
    assert _aussen(bundle) == aussen_vorher


@pytest.mark.parametrize("pfad", TRAVERSAL)
@pytest.mark.parametrize(
    ("endpunkt", "daten"),
    [
        ("/api/task", _aufgabe_daten),
        ("/api/welle", _welle_daten),
    ],
)
def test_t10_traversal_anlegen_ist_400(client, bundle, endpunkt, daten, pfad):
    bestand_vorher = _bestand(bundle)
    aussen_vorher = _aussen(bundle)

    antwort = client.post(endpunkt, json={**daten(), "path": pfad})

    assert antwort.status_code == 400
    assert antwort.get_json()["error"]
    assert _bestand(bundle) == bestand_vorher
    assert _aussen(bundle) == aussen_vorher


# --- T11: JSON-Fehlerformat ----------------------------------------------


@pytest.mark.parametrize("endpunkt", ENDPUNKTE)
def test_t11_leerer_body_ist_json_400(client, endpunkt):
    antwort = client.post(endpunkt, json={})

    assert antwort.status_code == 400
    assert antwort.mimetype == "application/json"
    assert antwort.get_json()["error"].strip()


@pytest.mark.parametrize("endpunkt", ENDPUNKTE)
def test_t11_ungueltiges_json_ist_400(client, endpunkt):
    antwort = client.post(endpunkt, data="kein json", content_type="application/json")

    assert antwort.status_code == 400
    assert antwort.mimetype == "application/json"
    assert antwort.get_json()["error"].strip()


@pytest.mark.parametrize("endpunkt", ENDPUNKTE)
def test_t11_body_kein_objekt_ist_400(client, endpunkt):
    antwort = client.post(endpunkt, json=["keine", "objekt"])

    assert antwort.status_code == 400
    assert antwort.mimetype == "application/json"
    assert antwort.get_json()["error"].strip()


# --- T12: Kein Teilzustand ------------------------------------------------


@pytest.mark.parametrize(
    ("endpunkt", "daten", "code"),
    [
        ("/api/task", {"titel": "Ohne Ziel", "akzeptanz": ["Kriterium."], "prioritaet": "hoch"}, 400),
        ("/api/task", {"titel": "Ohne Akzeptanz", "ziel": "Ziel.", "prioritaet": "hoch"}, 400),
        (
            "/api/task",
            {"titel": "Falsche Priorität", "ziel": "Ziel.", "akzeptanz": ["K."], "prioritaet": "dringend"},
            400,
        ),
        ("/api/welle", {"titel": "Ohne Status", "ziel": "Ziel.", "owner": "ai"}, 400),
        ("/api/welle", {"titel": "Ohne owner", "ziel": "Ziel.", "status": "Offen"}, 400),
        ("/api/welle", {"titel": "  ", "ziel": "Ziel.", "status": "Offen", "owner": "ai"}, 400),
        ("/api/nachtrag", {"path": AUFGABE, "text": ""}, 400),
        ("/api/meta", {"path": AUFGABE, "status": "Testing"}, 403),
    ],
)
def test_t12_kein_teilzustand(client, bundle, endpunkt, daten, code):
    bestand_vorher = _bestand(bundle)
    aussen_vorher = _aussen(bundle)

    antwort = client.post(endpunkt, json=daten)

    assert antwort.status_code == code
    assert antwort.get_json()["error"]
    assert _bestand(bundle) == bestand_vorher
    assert _aussen(bundle) == aussen_vorher


def test_t12_welle_fehler_legt_keinen_ordner_an(client, bundle):
    (bundle / WELLE).unlink()
    (bundle / "wellen").rmdir()

    antwort = client.post("/api/welle", json=_welle_daten(status="In Umsetzung"))

    assert antwort.status_code == 400
    assert not (bundle / "wellen").exists()


# --- Randfälle -----------------------------------------------------------


@pytest.mark.parametrize(
    ("endpunkt", "nutzlast"),
    [
        ("/api/nachtrag", {"text": "Text"}),
        ("/api/meta", {"owner": "ai"}),
    ],
)
def test_fehlende_datei_ist_404(client, bundle, endpunkt, nutzlast):
    antwort = client.post(endpunkt, json={"path": "aufgaben/gibt-es-nicht.md", **nutzlast})

    assert antwort.status_code == 404
    assert antwort.mimetype == "application/json"
    assert antwort.get_json()["error"]
    assert not (bundle / "aufgaben/gibt-es-nicht.md").exists()


@pytest.mark.parametrize(
    ("endpunkt", "nutzlast"),
    [
        ("/api/nachtrag", {"text": "Text"}),
        ("/api/meta", {"owner": "ai"}),
    ],
)
def test_fehlender_path_ist_400(client, endpunkt, nutzlast):
    antwort = client.post(endpunkt, json=nutzlast)

    assert antwort.status_code == 400
    assert antwort.get_json()["error"]

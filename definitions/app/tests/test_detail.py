"""Prüfungen für die Detailansicht (A12).

Die UI-Szenarien T1–T10 spielt der ``tester`` mit dem Moli-Browser durch; hier
werden ``detail.js`` und seine Verdrahtung ohne Browser geprüft. Die reine
Markdown-/Metadaten-Logik läuft über Node (keine neue Abhängigkeit).
"""

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

STATIC_DIR = Path(__file__).resolve().parents[1] / "static"
DETAIL_JS = STATIC_DIR / "js" / "detail.js"
APP_JS = STATIC_DIR / "js" / "app.js"
API_JS = STATIC_DIR / "js" / "api.js"
NODE = shutil.which("node")

ohne_node = pytest.mark.skipif(NODE is None, reason="node nicht verfügbar")

# Nur diese beiden UI-Status darf die App setzen (R1); Pipeline-Status fehlen.
ERLAUBTE_STATUS_KNOEPFE = ["Klarung", "Geschlossen"]


def lies(pfad: Path) -> str:
    assert pfad.is_file(), f"{pfad} fehlt"
    return pfad.read_text(encoding="utf-8")


def js(ausdruck: str, daten=None):
    """Wertet einen Ausdruck im Kontext von ``detail.js`` über Node aus."""
    assert NODE is not None
    skript = (
        f"import * as detail from {json.dumps(DETAIL_JS.as_uri())};\n"
        f"const daten = {json.dumps(daten, ensure_ascii=False)};\n"
        f"console.log(JSON.stringify({ausdruck}));"
    )
    ergebnis = subprocess.run(
        [NODE, "--input-type=module", "-e", skript],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert ergebnis.returncode == 0, ergebnis.stderr
    return json.loads(ergebnis.stdout)


# --- Statische Prüfungen ---------------------------------------------------


def test_detail_js_vorhanden():
    assert DETAIL_JS.is_file()


def test_app_js_importiert_detail():
    assert re.search(r'from\s+"\./detail\.js"', lies(APP_JS))


def test_app_js_verdrahtet_detail():
    assert 'registriereAnsicht("detail"' in lies(APP_JS)


def test_app_js_oeffnet_detail_bei_zeilenklick():
    js_quelle = lies(APP_JS)
    assert "data-path" in js_quelle
    assert "closest" in js_quelle
    assert "#/detail/" in js_quelle


@pytest.mark.parametrize("endpunkt", ["/api/file", "/api/nachtrag", "/api/meta"])
def test_detail_js_nutzt_endpunkt(endpunkt):
    assert endpunkt in lies(DETAIL_JS)


def test_detail_js_nutzt_api_helper():
    js_quelle = lies(DETAIL_JS)
    assert re.search(r"import\s*\{[^}]*\bgetJson\b[^}]*\}\s*from\s*\"\./api\.js\"", js_quelle)
    assert re.search(r"import\s*\{[^}]*\bpostJson\b[^}]*\}\s*from\s*\"\./api\.js\"", js_quelle)
    assert "zeigeMeldung" in js_quelle
    assert "zeigeFehler" in js_quelle


def test_detail_js_verwendet_container_id():
    assert '"detail"' in lies(DETAIL_JS)


def test_detail_js_rendert_ohne_innerhtml():
    js_quelle = lies(DETAIL_JS)
    assert "textContent" in js_quelle
    assert "innerHTML" not in js_quelle


@pytest.mark.parametrize(
    "senke",
    ["outerHTML", "insertAdjacentHTML", "document.write(", "eval("],
)
def test_detail_js_vermeidet_weitere_html_senken(senke):
    assert senke not in lies(DETAIL_JS)


def test_detail_js_hat_nachtrag_formular():
    js_quelle = lies(DETAIL_JS)
    assert '"nachtrag-formular"' in js_quelle
    assert '"nachtrag-text"' in js_quelle
    assert '"nachtrag-fehler"' in js_quelle
    assert "addEventListener(\"submit\"" in js_quelle


def test_detail_js_hat_owner_umschalter():
    js_quelle = lies(DETAIL_JS)
    assert '"detail-owner"' in js_quelle
    assert "OWNER_WERTE" in js_quelle


def test_detail_js_zeigt_status_als_marke():
    js_quelle = lies(DETAIL_JS)
    assert '"status"' in js_quelle
    assert "status--klarung" in js_quelle
    assert "status--geschlossen" in js_quelle


def test_detail_js_laedt_nach_schreiben_neu():
    # Nach POST wird der gespeicherte Stand erneut geladen (Sofortanzeige/Persistenz).
    js_quelle = lies(DETAIL_JS)
    treffer = re.search(r'postJson\("/api/nachtrag"[\s\S]{0,600}?ladeDetail\(', js_quelle)
    assert treffer, "Nachtrag-Handler lädt die Datei nach dem Speichern nicht neu"


def test_detail_js_meldet_erfolg():
    js_quelle = lies(DETAIL_JS)
    assert "zeigeMeldung(NACHRAG_ERFOLG)" in js_quelle
    assert "zeigeMeldung(erfolgsmeldung)" in js_quelle
    assert re.search(r"speichereMeta\([^)]*OWNER_ERFOLG\)", js_quelle)
    assert re.search(r"speichereMeta\([^)]*STATUS_ERFOLG\)", js_quelle)


def test_detail_js_hat_zurueck_link():
    js_quelle = lies(DETAIL_JS)
    assert '"#/uebersicht"' in js_quelle


def test_detail_js_fragt_ohne_cache_ab():
    # ``cache: "no-store"`` kommt zentral aus api.js und gilt damit auch hier.
    assert 'cache: "no-store"' in lies(API_JS)


# --- Reine Logik über Node -------------------------------------------------


@ohne_node
def test_status_knoepfe_sind_genau_klarung_und_geschlossen():
    assert js("detail.STATUS_KNOEPFE") == ERLAUBTE_STATUS_KNOEPFE


@ohne_node
@pytest.mark.parametrize("verboten", ["Offen", "In Arbeit", "Testing", "Dokumentation"])
def test_status_knoepfe_ohne_pipeline_status(verboten):
    assert verboten not in js("detail.STATUS_KNOEPFE")


@ohne_node
def test_parse_ueberschrift_und_absatz():
    bloecke = js("detail.parseMarkdown('# Ziel\\n\\nEin Absatz.')")
    assert bloecke == [
        {"art": "ueberschrift", "ebene": 1, "text": "Ziel"},
        {"art": "absatz", "text": "Ein Absatz."},
    ]


@ohne_node
def test_parse_absatz_ueber_mehrere_zeilen():
    bloecke = js("detail.parseMarkdown('Erste Zeile\\nzweite Zeile')")
    assert bloecke == [{"art": "absatz", "text": "Erste Zeile zweite Zeile"}]


@ohne_node
def test_parse_ungeordnete_liste():
    bloecke = js("detail.parseMarkdown('- eins\\n- zwei')")
    assert bloecke == [{"art": "liste", "geordnet": False, "eintraege": ["eins", "zwei"]}]


@ohne_node
def test_parse_geordnete_liste():
    bloecke = js("detail.parseMarkdown('1. eins\\n2. zwei')")
    assert bloecke == [{"art": "liste", "geordnet": True, "eintraege": ["eins", "zwei"]}]


@ohne_node
def test_parse_getrennte_listen():
    bloecke = js("detail.parseMarkdown('- eins\\n\\n1. zwei')")
    assert [block["geordnet"] for block in bloecke] == [False, True]


@ohne_node
def test_parse_codeblock():
    bloecke = js("detail.parseMarkdown('```python\\nprint(1)\\n```')")
    assert bloecke == [{"art": "code", "text": "print(1)"}]


@ohne_node
def test_parse_blockquote():
    bloecke = js("detail.parseMarkdown('> Zeile eins\\n> Zeile zwei')")
    assert bloecke == [{"art": "zitat", "text": "Zeile eins\nZeile zwei"}]


@ohne_node
def test_parse_nachtrag_marker_als_zitat():
    bloecke = js(
        "detail.parseMarkdown('> **Nachtrag (Mensch, 2026-11-14):** Bitte prüfen')",
    )
    assert bloecke == [
        {
            "art": "zitat",
            "text": "**Nachtrag (Mensch, 2026-11-14):** Bitte prüfen",
        }
    ]


@ohne_node
def test_parse_html_bleibt_text():
    bloecke = js(
        "detail.parseMarkdown('<script>alert(1)</script>')",
    )
    assert bloecke == [{"art": "absatz", "text": "<script>alert(1)</script>"}]


@ohne_node
def test_parse_leer_und_crlf():
    assert js("detail.parseMarkdown('')") == []
    assert js("detail.parseMarkdown(null)") == []
    assert js("detail.parseMarkdown('# A\\r\\n\\r\\ntext')") == [
        {"art": "ueberschrift", "ebene": 1, "text": "A"},
        {"art": "absatz", "text": "text"},
    ]


@ohne_node
def test_meta_payload_nur_pfad():
    assert js("detail.erstelleMetaPayload('aufgaben/a1.md', {})") == {"path": "aufgaben/a1.md"}


@ohne_node
def test_meta_payload_laesst_leere_felder_weg():
    assert js("detail.erstelleMetaPayload('a.md', { owner: '', status: '   ' })") == {
        "path": "a.md"
    }


@ohne_node
def test_meta_payload_nimmt_einzelwerte():
    assert js("detail.erstelleMetaPayload('a.md', { owner: 'ai' })") == {
        "path": "a.md",
        "owner": "ai",
    }
    assert js("detail.erstelleMetaPayload('a.md', { status: 'Klarung' })") == {
        "path": "a.md",
        "status": "Klarung",
    }


@ohne_node
def test_meta_payload_trimmt_werte():
    assert js("detail.erstelleMetaPayload('a.md', { owner: '  mensch  ' })") == {
        "path": "a.md",
        "owner": "mensch",
    }


@ohne_node
def test_nachtrag_payload_leer_ist_null():
    assert js("detail.erstelleNachtragPayload('a.md', '   ')") is None
    assert js("detail.erstelleNachtragPayload('a.md', '')") is None


@ohne_node
def test_nachtrag_payload_trimmt():
    assert js("detail.erstelleNachtragPayload('a.md', '  Text  ')") == {
        "path": "a.md",
        "text": "Text",
    }


@ohne_node
def test_status_aus_task_status():
    assert js("detail.ermittleStatus({ task_status: 'in Umsetzung' })") == {
        "status": "In Arbeit",
        "hinweis": None,
    }
    assert js("detail.ermittleStatus({ task_status: 'in Klärung' })")["status"] == "Klarung"
    assert js("detail.ermittleStatus({ task_status: 'abgeschlossen' })")["status"] == "Geschlossen"


@ohne_node
def test_status_ohne_feld():
    assert js("detail.ermittleStatus({})") == {"status": "Offen", "hinweis": "ohne Status"}


@ohne_node
def test_status_nimmt_status_feld():
    assert js("detail.ermittleStatus({ status: 'Geschlossen' })") == {
        "status": "Geschlossen",
        "hinweis": None,
    }


@ohne_node
def test_status_unbekannt_bleibt_offen_mit_hinweis():
    assert js("detail.ermittleStatus({ status: 'kaputt' })") == {
        "status": "Offen",
        "hinweis": "kaputt",
    }


@ohne_node
def test_owner_explizit_hat_vorrang():
    assert js("detail.ermittleOwner({ owner: 'mensch', task_status: 'in Umsetzung' })") == "mensch"


@ohne_node
def test_owner_default_aus_status():
    assert js("detail.ermittleOwner({ task_status: 'in Klärung' })") == "mensch"
    assert js("detail.ermittleOwner({ status: 'Offen' })") == "ai"
    assert js("detail.ermittleOwner({ status: 'Geschlossen' })") is None


@ohne_node
def test_owner_ohne_angabe_ist_null():
    assert js("detail.ermittleOwner({})") is None

"""Prüfungen für die Detailansicht (A12).

Die UI-Szenarien T1–T10 spielt der ``tester`` mit dem Moli-Browser durch; hier
werden ``detail.js`` und seine Verdrahtung ohne Browser geprüft. Die reine
Markdown-/Metadaten-Logik läuft über Node (keine neue Abhängigkeit). T10
(403-Pfad) ist zusätzlich hier direkt belegt: Mini-DOM in Node, der
``fetch``-Proxy erzwingt die 403 am echten Server.
"""

import hashlib
import json
import re
import shutil
import subprocess
import sys
import threading
from pathlib import Path

import pytest
from werkzeug.serving import make_server

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import server

STATIC_DIR = Path(__file__).resolve().parents[1] / "static"
DETAIL_JS = STATIC_DIR / "js" / "detail.js"
APP_JS = STATIC_DIR / "js" / "app.js"
API_JS = STATIC_DIR / "js" / "api.js"
NODE = shutil.which("node")

ohne_node = pytest.mark.skipif(NODE is None, reason="node nicht verfügbar")

# Nur diese beiden UI-Status darf die App setzen (R1); Pipeline-Status fehlen.
ERLAUBTE_STATUS_KNOEPFE = ["Klarung", "Geschlossen"]

# T10: Die UI zeigt "In Arbeit" an, darf ihn aber nie setzen (R1).
T10_DATEI = "aufgaben/a1.md"
T10_VERBOTENER_STATUS = "In Arbeit"


def lies(pfad: Path) -> str:
    assert pfad.is_file(), f"{pfad} fehlt"
    return pfad.read_text(encoding="utf-8")


def node_ausfuehren(skript: str) -> dict:
    """Führt ein Node-Skript aus und liest das JSON-Ergebnis aus stdout."""
    assert NODE is not None
    ergebnis = subprocess.run(
        [NODE, "--input-type=module", "-e", skript],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert ergebnis.returncode == 0, ergebnis.stderr
    return json.loads(ergebnis.stdout)


def js(ausdruck: str, daten=None):
    """Wertet einen Ausdruck im Kontext von ``detail.js`` über Node aus."""
    skript = (
        f"import * as detail from {json.dumps(DETAIL_JS.as_uri())};\n"
        f"const daten = {json.dumps(daten, ensure_ascii=False)};\n"
        f"console.log(JSON.stringify({ausdruck}));"
    )
    return node_ausfuehren(skript)


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


# --- UI-Läufe in Node (Mini-DOM + fetch-Proxy) ----------------------------

MINI_DOM = r"""
// Mini-DOM für Node: nur so viel, wie detail.js und api.js benutzen.
const REGISTRIERT = new Map();

class Knoten {
  constructor(marke, art) {
    this.marke = marke;
    this.art = art;
    this.kinder = [];
    this.attribute = {};
    this.dataset = {};
    this.hoerer = {};
    this.textContent = "";
    this.hidden = false;
    this.disabled = false;
    this.value = "";
    const knoten = this;
    this.classList = {
      add: (...namen) => {
        const vorhanden = new Set(knoten.klassen());
        for (const name of namen) vorhanden.add(name);
        knoten.attribute.class = [...vorhanden].join(" ");
      },
      contains: (name) => knoten.klassen().includes(name),
    };
  }

  klassen() {
    return (this.attribute.class || "").split(/\s+/).filter(Boolean);
  }

  get className() {
    return this.attribute.class || "";
  }

  set className(wert) {
    this.attribute.class = wert;
  }

  get id() {
    return this.attribute.id || "";
  }

  set id(wert) {
    this.attribute.id = wert;
    REGISTRIERT.set(wert, this);
  }

  setAttribute(name, wert) {
    this.attribute[name] = wert;
  }

  getAttribute(name) {
    return this.attribute[name] ?? null;
  }

  addEventListener(art, hoerer) {
    if (!this.hoerer[art]) this.hoerer[art] = [];
    this.hoerer[art].push(hoerer);
  }

  async ausloesen(art, ereignis = { preventDefault() {} }) {
    const rueckgaben = (this.hoerer[art] || []).map((hoerer) => hoerer(ereignis));
    await Promise.all(rueckgaben);
  }

  append(...kinder) {
    for (const kind of kinder) {
      if (kind.art === "fragment") this.kinder.push(...kind.kinder);
      else this.kinder.push(kind);
    }
  }

  replaceChildren(...kinder) {
    this.kinder = [];
    this.append(...kinder);
  }

  focus() {}

  alleKnoten() {
    const liste = [this];
    for (const kind of this.kinder) liste.push(...kind.alleKnoten());
    return liste;
  }
}

globalThis.document = {
  createElement: (marke) => new Knoten(marke, "element"),
  createDocumentFragment: () => new Knoten("#fragment", "fragment"),
  getElementById: (id) => REGISTRIERT.get(id) || null,
};
"""

UI_UMGEBUNG = r"""
// Fehler-/Erfolgsbereich und Detail-Container wie in index.html.
const fehler = document.createElement("div");
fehler.id = "fehler";
fehler.hidden = true;
const meldung = document.createElement("div");
meldung.id = "meldung";
meldung.hidden = true;
const ziel = document.createElement("div");
ziel.id = "detail";

// Sperrzustand der Bedienelemente (A12-2): sichtbar während laufender Requests.
function gesperrtZustand() {
  const alle = ziel.alleKnoten();
  const absenden = alle.find((knoten) => knoten.type === "submit");
  return {
    absenden: Boolean(absenden && absenden.disabled),
    status: alle
      .filter((knoten) => knoten.dataset.status)
      .map((knoten) => Boolean(knoten.disabled)),
  };
}

function zustand() {
  const alle = ziel.alleKnoten();
  const marke = alle.find((knoten) => knoten.classList.contains("status"));
  return {
    statusMarke: marke ? marke.textContent : null,
    aktiv: alle
      .filter((knoten) => knoten.dataset.status && knoten.classList.contains("knopf--primaer"))
      .map((knoten) => knoten.dataset.status),
    gesperrt: gesperrtZustand(),
  };
}

// fetch-Proxy an den echten Server; mit VERBOTENER_STATUS wird der Status im
// POST /api/meta ersetzt und so die 403 erzwungen (T10).
const echtesFetch = globalThis.fetch;
const anfragen = [];

globalThis.fetch = async (pfad, optionen = {}) => {
  const anfrageZiel = new URL(String(pfad), BASIS);
  const methode = optionen.method || "GET";
  const aufzeichnung = {
    methode,
    pfad: anfrageZiel.pathname,
    status: null,
    payload: null,
    gesperrt: methode === "GET" ? null : gesperrtZustand(),
  };
  let koerper = optionen.body;
  if (methode !== "GET" && koerper !== undefined) {
    aufzeichnung.payload = JSON.parse(koerper);
    if (VERBOTENER_STATUS && anfrageZiel.pathname === "/api/meta") {
      aufzeichnung.payload.status = VERBOTENER_STATUS;
      koerper = JSON.stringify(aufzeichnung.payload);
    }
  }
  const antwort = await echtesFetch(anfrageZiel, { ...optionen, body: koerper });
  aufzeichnung.status = antwort.status;
  anfragen.push(aufzeichnung);
  return antwort;
};
"""

SZENARIO_403 = r"""
await detail.ladeDetail({ unterpunkt: DATEI });
const klarung = ziel.alleKnoten().find((knoten) => knoten.dataset.status === "Klarung");
const vorher = zustand();

await klarung.ausloesen("click");

console.log(JSON.stringify({
  anfragen,
  fehler: { sichtbar: !fehler.hidden, text: fehler.textContent },
  meldung: { sichtbar: !meldung.hidden, text: meldung.textContent },
  vorher,
  nachher: zustand(),
  dateiLadungen: anfragen.filter((a) => a.methode === "GET" && a.pfad === "/api/file").length,
}));
"""

SZENARIO_DOPPELT_ABSENDEN = r"""
await detail.ladeDetail({ unterpunkt: DATEI });
document.getElementById("nachtrag-text").value = "Bitte prüfen.";
const formular = document.getElementById("nachtrag-formular");

// Zweimal schnell hintereinander — wie ein Doppelklick, nur ohne die
// browserseitige Klick-Unterdrückung (strengerer Fall).
const erstes = formular.ausloesen("submit");
const zweites = formular.ausloesen("submit");
await Promise.all([erstes, zweites]);

console.log(JSON.stringify({
  anfragen,
  nachher: zustand(),
}));
"""

SZENARIO_DOPPELKLICK_STATUS = r"""
await detail.ladeDetail({ unterpunkt: DATEI });
const klarung = ziel.alleKnoten().find((knoten) => knoten.dataset.status === "Klarung");

const erstes = klarung.ausloesen("click");
const zweites = klarung.ausloesen("click");
await Promise.all([erstes, zweites]);

console.log(JSON.stringify({
  anfragen,
  nachher: zustand(),
}));
"""


def ui_lauf(basis: str, szenario: str, verbotener_status: str | None = None) -> dict:
    """Spielt ein UI-Szenario in Node gegen den echten Server unter ``basis`` aus."""
    skript = (
        f"import * as detail from {json.dumps(DETAIL_JS.as_uri())};\n"
        + MINI_DOM
        + f"const BASIS = {json.dumps(basis)};\n"
        + f"const DATEI = {json.dumps(T10_DATEI)};\n"
        + f"const VERBOTENER_STATUS = {json.dumps(verbotener_status)};\n"
        + UI_UMGEBUNG
        + szenario
    )
    return node_ausfuehren(skript)


@pytest.fixture()
def app_server(bundle):
    """Echter HTTP-Server auf einem freien Port für die UI-Läufe."""
    httpd = make_server("127.0.0.1", 0, server.create_app(bundle), threaded=True)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{httpd.server_port}"
    finally:
        httpd.shutdown()
        thread.join(timeout=5)


# --- T10: 403-Pfad (verbotener Status) -----------------------------------


def _sha256(pfad: Path) -> str:
    return hashlib.sha256(pfad.read_bytes()).hexdigest()


def _bestand(wurzel: Path) -> list[str]:
    return sorted(pfad.relative_to(wurzel).as_posix() for pfad in wurzel.rglob("*"))


@ohne_node
def test_t10_verbotener_status_403_zeigt_fehler_ohne_zustandswechsel(bundle, app_server):
    datei = bundle / T10_DATEI
    inhalt_vorher = _sha256(datei)
    bestand_vorher = _bestand(bundle)

    ergebnis = ui_lauf(app_server, SZENARIO_403, T10_VERBOTENER_STATUS)

    # Der Proxy hat den verbotenen Status wirklich geschickt und 403 erzwungen.
    meta = [
        eintrag
        for eintrag in ergebnis["anfragen"]
        if eintrag["methode"] == "POST" and eintrag["pfad"] == "/api/meta"
    ]
    assert meta, "UI hat /api/meta nicht aufgerufen"
    assert meta[0]["payload"]["status"] == T10_VERBOTENER_STATUS
    assert meta[0]["status"] == 403

    # Fail-loud wie im Fehlerzustand-Design (A11/A12): sichtbar und verständlich.
    assert ergebnis["fehler"]["sichtbar"] is True
    assert "Status" in ergebnis["fehler"]["text"]

    # Kein falscher Zustand: kein Erfolg, Ansicht ohne Zustandswechsel, Datei unverändert.
    assert ergebnis["meldung"] == {"sichtbar": False, "text": ""}
    assert ergebnis["nachher"] == ergebnis["vorher"]
    assert ergebnis["nachher"]["statusMarke"] == "Offen"
    assert ergebnis["nachher"]["aktiv"] == []
    assert ergebnis["dateiLadungen"] == 1
    assert _sha256(datei) == inhalt_vorher
    assert _bestand(bundle) == bestand_vorher


# --- A12-2: Sperren bei laufenden Requests -------------------------------


@ohne_node
def test_a12_2_doppeltes_absenden_erzeugt_genau_einen_eintrag(bundle, app_server):
    datei = bundle / T10_DATEI

    ergebnis = ui_lauf(app_server, SZENARIO_DOPPELT_ABSENDEN)

    schreibungen = [
        eintrag
        for eintrag in ergebnis["anfragen"]
        if eintrag["methode"] == "POST" and eintrag["pfad"] == "/api/nachtrag"
    ]
    assert len(schreibungen) == 1
    assert schreibungen[0]["gesperrt"]["absenden"] is True
    assert ergebnis["nachher"]["gesperrt"]["absenden"] is False
    assert datei.read_text(encoding="utf-8").count("**Nachtrag (") == 1


@ohne_node
def test_a12_2_doppelklick_status_schreibt_nur_einmal(bundle, app_server):
    ergebnis = ui_lauf(app_server, SZENARIO_DOPPELKLICK_STATUS)

    schreibungen = [
        eintrag
        for eintrag in ergebnis["anfragen"]
        if eintrag["methode"] == "POST" and eintrag["pfad"] == "/api/meta"
    ]
    assert len(schreibungen) == 1
    assert schreibungen[0]["gesperrt"]["status"] == [True, True]
    assert ergebnis["nachher"]["gesperrt"]["status"] == [False, False]

"""Prüfungen für die Entscheidungen- und Projekt-Ansicht (A14).

Die UI-Szenarien T1–T5 spielt der ``tester`` mit dem Moli-Browser durch; hier
werden ``projekt.js`` und seine Verdrahtung ohne Browser geprüft. Der Parser
der Log-Einträge läuft über Node (keine neue Abhängigkeit); die Ansichten
laufen im Node-DOM-Harness — einmal mit Antworten aus dem Fetch-Stab und
einmal per HTTP gegen ein Test-Bundle unter ``tmp_path`` (nie gegen das echte
Projekt-Bundle). Genutzt wird ausschließlich ``GET /api/file``.
"""

import json
import re
import shutil
import subprocess
import sys
import threading
from pathlib import Path
from urllib.parse import unquote

import pytest
from werkzeug.serving import make_server

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import server

STATIC_DIR = Path(__file__).resolve().parents[1] / "static"
PROJEKT_JS = STATIC_DIR / "js" / "projekt.js"
APP_JS = STATIC_DIR / "js" / "app.js"
API_JS = STATIC_DIR / "js" / "api.js"
DETAIL_JS = STATIC_DIR / "js" / "detail.js"
NODE = shutil.which("node")

ohne_node = pytest.mark.skipif(NODE is None, reason="node nicht verfügbar")

ENTSCHEIDUNGEN_PFAD = "entscheidungen/log.md"
DETAIL_VORSCHLAG = "#/detail/"
PROJEKT_VORSCHLAG = "#/projekt/"

# Die fünf Projekt-Unterpunkte laut Navigation (index.html, A10).
PROJEKT_ERWARTET = [
    {"unterpunkt": "konzept", "titel": "Konzept", "pfad": "projekt/konzept.md"},
    {"unterpunkt": "technische-spec", "titel": "Technische Spec", "pfad": "projekt/technische-spec.md"},
    {"unterpunkt": "user-stories", "titel": "User Stories", "pfad": "projekt/user-stories/index.md"},
    {"unterpunkt": "phasen", "titel": "Phasen", "pfad": "projekt/phasen.md"},
    {"unterpunkt": "log", "titel": "Log", "pfad": "log.md"},
]

# Log-Fixture für die Stub-Läufe (Format `## YYYY-MM-DD: Titel`).
LOG_MD = (
    "# Entscheidungslog\n"
    "\n"
    "## 2026-11-14: Moli-Frage — Standardentscheidung Harness\n"
    "\n"
    "**Entscheidung:** Harness bleibt.\n"
    "\n"
    "## 2026-11-13: Navigation mit fünf Hauptpunkten\n"
    "\n"
    "**Entscheidung:** Fünf Punkte.\n"
)

LOG_ERWARTET = [
    {"datum": "2026-11-14", "titel": "Moli-Frage — Standardentscheidung Harness"},
    {"datum": "2026-11-13", "titel": "Navigation mit fünf Hauptpunkten"},
]

SPEC_MD = "# Technische Spec\n\nSpec-Absatz zur Prüfung.\n\n- Erster Punkt\n"

# Test-Bundle für die HTTP-Läufe (relativ zum Bundle-Root, wie in A14 vorgegeben).
BUNDLE_DATEIEN = {
    "projekt/konzept.md": "# Konzept\n\nKonzept-Absatz.\n",
    "projekt/technische-spec.md": "# Technische Spec\n\nSpec-Absatz.\n",
    "projekt/user-stories/index.md": "# User Stories\n\nStories-Absatz.\n",
    "projekt/phasen.md": "# Phasen\n\nPhasen-Absatz.\n",
    "log.md": "---\ntype: Log\ntitle: Projekt-Log (Test)\n---\n\n# Projekt-Log\n\nLog-Absatz.\n",
}

BUNDLE_LOG = (
    "# Entscheidungslog\n"
    "\n"
    "## 2026-11-14: Erste Entscheidung\n"
    "\n"
    "**Entscheidung:** Text eins.\n"
    "\n"
    "## 2026-11-13: Zweite Entscheidung\n"
    "\n"
    "**Entscheidung:** Text zwei.\n"
)


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
    """Wertet einen Ausdruck im Kontext von ``projekt.js`` über Node aus."""
    skript = (
        f"import * as projekt from {json.dumps(PROJEKT_JS.as_uri())};\n"
        f"const daten = {json.dumps(daten, ensure_ascii=False)};\n"
        f"console.log(JSON.stringify({ausdruck}));"
    )
    return node_ausfuehren(skript)


# --- Statische Prüfungen ---------------------------------------------------


def test_projekt_js_vorhanden():
    assert PROJEKT_JS.is_file()


def test_app_js_importiert_projekt():
    assert re.search(r'from\s+"\./projekt\.js"', lies(APP_JS))


def test_app_js_verdrahtet_projekt():
    js_quelle = lies(APP_JS)
    assert 'registriereAnsicht("entscheidungen"' in js_quelle
    assert 'registriereAnsicht("projekt"' in js_quelle


def test_projekt_js_nutzt_nur_den_file_endpunkt():
    # A14: kein neuer Server-Endpunkt, ausschließlich GET /api/file.
    js_quelle = lies(PROJEKT_JS)
    assert set(re.findall(r"/api/[a-z_-]+", js_quelle)) == {"/api/file"}
    assert "postJson" not in js_quelle


def test_projekt_js_nutzt_api_helper():
    js_quelle = lies(PROJEKT_JS)
    assert re.search(r"import\s*\{[^}]*\bgetJson\b[^}]*\}\s*from\s*\"\./api\.js\"", js_quelle)


def test_projekt_js_nutzt_detail_renderer():
    # R6: der Minimal-Renderer aus detail.js wird wiederverwendet.
    js_quelle = lies(PROJEKT_JS)
    assert re.search(r"import\s*\{[^}]*\brendereMarkdown\b[^}]*\}\s*from\s*\"\./detail\.js\"", js_quelle)


def test_projekt_js_rendert_ohne_innerhtml():
    js_quelle = lies(PROJEKT_JS)
    assert "textContent" in js_quelle
    assert "innerHTML" not in js_quelle


@pytest.mark.parametrize(
    "senke",
    ["outerHTML", "insertAdjacentHTML", "document.write(", "eval("],
)
def test_projekt_js_vermeidet_weitere_html_senken(senke):
    assert senke not in lies(PROJEKT_JS)


def test_projekt_js_nutzt_classlist_statt_classname():
    js_quelle = lies(PROJEKT_JS)
    assert "classList" in js_quelle
    assert "className" not in js_quelle


@pytest.mark.parametrize("container_id", ["liste-entscheidungen", "liste-projekt"])
def test_projekt_js_verwendet_container_id(container_id):
    assert f'"{container_id}"' in lies(PROJEKT_JS)


@pytest.mark.parametrize(
    "pfad",
    [
        "entscheidungen/log.md",
        "projekt/konzept.md",
        "projekt/technische-spec.md",
        "projekt/user-stories/index.md",
        "projekt/phasen.md",
    ],
)
def test_projekt_js_pfade_relativ_zum_bundle(pfad):
    assert pfad in lies(PROJEKT_JS)


# --- Reine Logik über Node -------------------------------------------------


@ohne_node
def test_parse_entscheidungen_datum_und_titel():
    assert js("projekt.parseEntscheidungen(daten)", LOG_MD) == LOG_ERWARTET


@ohne_node
@pytest.mark.parametrize("trennzeichen", ["", ": ", ":", " - ", "-", " – ", "–", " — ", "—"])
def test_parse_entscheidungen_trennzeichen_tolerant(trennzeichen):
    markdown = f"## 2026-11-14{trennzeichen}Titel der Entscheidung"
    assert js("projekt.parseEntscheidungen(daten)", markdown) == [
        {"datum": "2026-11-14", "titel": "Titel der Entscheidung"}
    ]


@ohne_node
def test_parse_entscheidungen_titel_mit_sonderzeichen():
    markdown = "## 2026-11-14: Titel — mit Bindestrich: und Doppelpunkt"
    assert js("projekt.parseEntscheidungen(daten)", markdown) == [
        {"datum": "2026-11-14", "titel": "Titel — mit Bindestrich: und Doppelpunkt"}
    ]


@ohne_node
def test_parse_entscheidungen_ignoriert_unpassende_zeilen():
    markdown = (
        "# Entscheidungslog\n"
        "\n"
        "## Übersicht\n"
        "\n"
        "### 2026-01-01: Zu tief\n"
        "\n"
        "2026-01-02: Ohne Raute\n"
        "\n"
        "## 2026-01-03\n"
        "\n"
        "## 2026-01-05: Gültig\n"
    )
    assert js("projekt.parseEntscheidungen(daten)", markdown) == [
        {"datum": "2026-01-05", "titel": "Gültig"}
    ]


@ohne_node
def test_parse_entscheidungen_leer_und_crlf():
    assert js("projekt.parseEntscheidungen(daten)", "") == []
    assert js("projekt.parseEntscheidungen(daten)", "\n  \n") == []
    assert js("projekt.parseEntscheidungen(daten)", None) == []
    assert js("projekt.parseEntscheidungen(daten)", 42) == []
    assert js("projekt.parseEntscheidungen(daten)", "# Titel\r\n\r\n## 2026-11-14: Eins\r\n") == [
        {"datum": "2026-11-14", "titel": "Eins"}
    ]


@ohne_node
def test_projekt_punkte_genau_fuenf():
    assert js("projekt.PROJEKT_PUNKTE") == PROJEKT_ERWARTET


@ohne_node
def test_projekt_punkt_findet_unterpunkt():
    assert js("projekt.projektPunkt('log')") == {
        "unterpunkt": "log",
        "titel": "Log",
        "pfad": "log.md",
    }
    assert js("projekt.projektPunkt('technische-spec')")["pfad"] == "projekt/technische-spec.md"


@ohne_node
def test_projekt_punkt_unbekannt_ist_null():
    assert js("projekt.projektPunkt('gibtsnicht')") is None
    assert js("projekt.projektPunkt('')") is None


# --- UI-Läufe im DOM-Stab (Fetch-Antworten simuliert) ----------------------

MINI_DOM = r"""
// Mini-DOM für Node: nur so viel, wie projekt.js, detail.js und api.js benutzen.
const REGISTRIERT = new Map();

class Knoten {
  constructor(marke, art) {
    this.marke = marke;
    this.art = art;
    this.kinder = [];
    this.attribute = {};
    this.dataset = {};
    this.hoerer = {};
    this.hidden = false;
    this.disabled = false;
    this.value = "";
    this._text = "";
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

  get textContent() {
    if (this.kinder.length === 0) return this._text;
    return this.kinder.map((kind) => kind.textContent).join("");
  }

  set textContent(wert) {
    this._text = String(wert);
    this.kinder = [];
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

  append(...kinder) {
    for (const kind of kinder) {
      if (kind.art === "fragment") this.kinder.push(...kind.kinder);
      else this.kinder.push(kind);
    }
  }

  replaceChildren(...kinder) {
    this.kinder = [];
    this._text = "";
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

// Fehler-/Erfolgsbereich und Ansichtscontainer wie in index.html (A10).
for (const id of ["fehler", "meldung", "liste-entscheidungen", "liste-projekt"]) {
  const bereich = document.createElement("div");
  bereich.id = id;
  if (id === "fehler" || id === "meldung") bereich.hidden = true;
}

const sammle = (el) => [el, ...(el.kinder ?? []).flatMap(sammle)];
const bei = (id) => document.getElementById(id);
const sichtbar = (id) => document.getElementById(id)?.hidden === false;
const links = (id) => sammle(bei(id)).filter((k) => k.marke === "a").map((k) => ({ text: k.textContent, href: k.href }));
"""

FETCH_STAB = r"""
// Fetch-Stab: protokolliert jeden Aufruf und liefert Antworten je Bundle-Pfad.
const aufrufe = [];
const antworten = __ANTWORTEN__;
globalThis.fetch = async (pfad, optionen = {}) => {
  const ziel = new URL(String(pfad), __BASIS__);
  const datei = ziel.searchParams.get("path") ?? ziel.pathname;
  aufrufe.push({ endpunkt: ziel.pathname, datei, methode: optionen.method ?? "GET" });
  const vorgabe = antworten[datei] ?? { status: 404, koerper: { error: "Nicht gefunden." } };
  return {
    ok: vorgabe.status < 400,
    status: vorgabe.status,
    headers: { get: () => "application/json" },
    text: async () => JSON.stringify(vorgabe.koerper ?? null),
  };
};
"""

FETCH_PROXY = r"""
// Proxy an den echten Server: macht Pfade absolut und protokolliert die Aufrufe.
const echtesFetch = globalThis.fetch;
const aufrufe = [];
globalThis.fetch = async (pfad, optionen = {}) => {
  const ziel = new URL(String(pfad), __BASIS__);
  const datei = ziel.searchParams.get("path") ?? ziel.pathname;
  aufrufe.push({ endpunkt: ziel.pathname, datei, methode: optionen.method ?? "GET" });
  return echtesFetch(ziel, optionen);
};
"""


def _harness(ablauf: str, fetch_skript: str) -> dict:
    skript = (
        MINI_DOM
        + fetch_skript
        + f"\nimport * as projekt from {json.dumps(PROJEKT_JS.as_uri())};\n"
        + "const ergebnis = await (async () => {\n"
        + ablauf
        + "\n})();\n"
        + "console.log(JSON.stringify(ergebnis));\n"
    )
    return node_ausfuehren(skript)


def dom(ablauf: str, antworten: dict | None = None) -> dict:
    """Führt einen Ablauf im DOM-Stab aus; Antworten kommen aus dem Fetch-Stab."""
    fetch_skript = (
        FETCH_STAB.replace("__ANTWORTEN__", json.dumps(antworten or {}, ensure_ascii=False))
        .replace("__BASIS__", json.dumps("http://lokal"))
    )
    return _harness(ablauf, fetch_skript)


def ui_lauf(basis: str, ablauf: str) -> dict:
    """Führt einen Ablauf im DOM-Harness gegen den echten Server unter ``basis`` aus."""
    return _harness(ablauf, FETCH_PROXY.replace("__BASIS__", json.dumps(basis)))


SZENARIO_T1 = r"""
await projekt.ladeEntscheidungenAnsicht();
return {
  eintraege: links("liste-entscheidungen"),
  abgerufen: aufrufe.map((a) => a.endpunkt + " " + a.datei),
};
"""

SZENARIO_T3 = r"""
await projekt.ladeProjektAnsicht({ unterpunkt: "" });
return {
  punkte: links("liste-projekt"),
  abgerufen: aufrufe.map((a) => a.endpunkt + " " + a.datei),
};
"""

SZENARIO_T4 = r"""
await projekt.ladeProjektAnsicht({ unterpunkt: "technische-spec" });
const alle = bei("liste-projekt").alleKnoten();
return {
  ueberschriften: alle.filter((k) => k.marke === "h1").map((k) => k.textContent),
  absaetze: alle.filter((k) => k.marke === "p").map((k) => k.textContent),
  listenpunkte: alle.filter((k) => k.marke === "li").map((k) => k.textContent),
  links: links("liste-projekt"),
  abgerufen: aufrufe.map((a) => a.endpunkt + " " + a.datei),
};
"""

SZENARIO_FEHLER = r"""
__AUFRUF__
return {
  text: bei("__CONTAINER__").textContent,
  kinder: bei("__CONTAINER__").kinder.length,
  links: links("__CONTAINER__").length,
  fehler: { sichtbar: sichtbar("fehler"), text: bei("fehler").textContent },
  abgerufen: aufrufe.map((a) => a.endpunkt + " " + a.datei),
};
"""


def szenario_fehler(aufruf: str, container: str) -> str:
    return SZENARIO_FEHLER.replace("__AUFRUF__", aufruf).replace("__CONTAINER__", container)


@ohne_node
def test_t1_entscheidungen_zeigen_datum_und_titel():
    ergebnis = dom(
        SZENARIO_T1,
        antworten={ENTSCHEIDUNGEN_PFAD: {"status": 200, "koerper": {"frontmatter": {}, "markdown": LOG_MD}}},
    )
    assert ergebnis["eintraege"] == [
        {"text": f"{eintrag['datum']}: {eintrag['titel']}", "href": f"{DETAIL_VORSCHLAG}entscheidungen%2Flog.md"}
        for eintrag in LOG_ERWARTET
    ]
    assert ergebnis["abgerufen"] == [f"/api/file {ENTSCHEIDUNGEN_PFAD}"]


@ohne_node
def test_t2_eintrag_oeffnet_detail_der_log_datei():
    # Jeder Klick öffnet das Detail der Log-Datei (die Einträge sind keine Dateien).
    ergebnis = dom(
        SZENARIO_T1,
        antworten={ENTSCHEIDUNGEN_PFAD: {"status": 200, "koerper": {"frontmatter": {}, "markdown": LOG_MD}}},
    )
    assert len(ergebnis["eintraege"]) == len(LOG_ERWARTET)
    for eintrag in ergebnis["eintraege"]:
        assert eintrag["href"].startswith(DETAIL_VORSCHLAG)
        ziel = unquote(eintrag["href"][len(DETAIL_VORSCHLAG):])
        assert ziel == ENTSCHEIDUNGEN_PFAD


@ohne_node
def test_t3_projekt_zeigt_fuenf_unterpunkte():
    ergebnis = dom(SZENARIO_T3)
    assert ergebnis["punkte"] == [
        {"text": punkt["titel"], "href": f"{PROJEKT_VORSCHLAG}{punkt['unterpunkt']}"}
        for punkt in PROJEKT_ERWARTET
    ]
    # Die Liste ist statisch: kein Request nötig.
    assert ergebnis["abgerufen"] == []


@ohne_node
def test_t4_spec_oeffnet_detail_mit_gerendertem_inhalt():
    ergebnis = dom(
        SZENARIO_T4,
        antworten={
            "projekt/technische-spec.md": {
                "status": 200,
                "koerper": {"frontmatter": {}, "markdown": SPEC_MD},
            }
        },
    )
    # Gerendert und nicht als Rohtext: Überschrift, Absatz und Liste sind Knoten.
    assert ergebnis["ueberschriften"] == ["Technische Spec"]
    assert ergebnis["absaetze"] == ["Spec-Absatz zur Prüfung."]
    assert ergebnis["listenpunkte"] == ["Erster Punkt"]
    assert ergebnis["links"] == [{"text": "← Zurück zum Projekt", "href": "#/projekt"}]
    assert ergebnis["abgerufen"] == ["/api/file projekt/technische-spec.md"]


@ohne_node
def test_t5_fehlende_datei_entscheidungen_zeigt_fehlermeldung():
    ergebnis = dom(
        szenario_fehler("await projekt.ladeEntscheidungenAnsicht();", "liste-entscheidungen"),
        antworten={ENTSCHEIDUNGEN_PFAD: {"status": 404, "koerper": {"error": "Nicht gefunden."}}},
    )
    # Fehlermeldung statt leerem Screen (fail-loud wie A11/A12).
    assert ergebnis["text"]
    assert ergebnis["kinder"] > 0
    assert ergebnis["links"] == 0
    assert ergebnis["fehler"]["sichtbar"] is True
    assert ergebnis["fehler"]["text"]


@ohne_node
def test_t5_fehlende_datei_projekt_zeigt_fehlermeldung():
    ergebnis = dom(
        szenario_fehler('await projekt.ladeProjektAnsicht({ unterpunkt: "phasen" });', "liste-projekt"),
        antworten={"projekt/phasen.md": {"status": 404, "koerper": {"error": "Nicht gefunden."}}},
    )
    assert ergebnis["text"]
    assert ergebnis["kinder"] > 0
    assert ergebnis["links"] == 0
    assert ergebnis["fehler"]["sichtbar"] is True
    assert ergebnis["fehler"]["text"]


@ohne_node
def test_unerwartetes_format_ist_fail_loud():
    ergebnis = dom(
        szenario_fehler("await projekt.ladeEntscheidungenAnsicht();", "liste-entscheidungen"),
        antworten={ENTSCHEIDUNGEN_PFAD: {"status": 200, "koerper": {"markdown": 42}}},
    )
    assert "Format" in ergebnis["text"]
    assert ergebnis["fehler"]["sichtbar"] is True
    assert "Format" in ergebnis["fehler"]["text"]


@ohne_node
def test_unbekannter_unterpunkt_ist_fail_loud():
    ergebnis = dom(
        szenario_fehler('await projekt.ladeProjektAnsicht({ unterpunkt: "gibtsnicht" });', "liste-projekt"),
    )
    assert ergebnis["text"]
    assert ergebnis["fehler"]["sichtbar"] is True
    assert ergebnis["abgerufen"] == []


@ohne_node
def test_ohne_container_ist_robust():
    # Robustheit: ohne Container aus index.html passiert nichts und nichts crasht.
    ergebnis = dom(
        "for (const id of [\"liste-entscheidungen\", \"liste-projekt\"]) REGISTRIERT.delete(id);\n"
        "await projekt.ladeEntscheidungenAnsicht();\n"
        "await projekt.ladeProjektAnsicht({ unterpunkt: \"konzept\" });\n"
        "return { ok: true };",
        antworten={"projekt/konzept.md": {"status": 200, "koerper": {"markdown": "# Konzept"}}},
    )
    assert ergebnis == {"ok": True}


# --- HTTP-Läufe gegen ein Test-Bundle unter tmp_path -----------------------


@pytest.fixture()
def test_bundle(tmp_path):
    wurzel = tmp_path / "bundle"
    (wurzel / "entscheidungen").mkdir(parents=True)
    (wurzel / "projekt" / "user-stories").mkdir(parents=True)
    (wurzel / ENTSCHEIDUNGEN_PFAD).write_text(BUNDLE_LOG, encoding="utf-8")
    for pfad, inhalt in BUNDLE_DATEIEN.items():
        (wurzel / pfad).write_text(inhalt, encoding="utf-8")
    return wurzel


@pytest.fixture()
def luecken_bundle(tmp_path):
    """Bundle ohne `entscheidungen/log.md` und ohne `projekt/phasen.md` (T5)."""
    wurzel = tmp_path / "luecke"
    (wurzel / "projekt" / "user-stories").mkdir(parents=True)
    for pfad, inhalt in BUNDLE_DATEIEN.items():
        if pfad == "projekt/phasen.md":
            continue
        (wurzel / pfad).write_text(inhalt, encoding="utf-8")
    return wurzel


def _server(wurzel: Path):
    httpd = make_server("127.0.0.1", 0, server.create_app(wurzel), threaded=True)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{httpd.server_port}"
    finally:
        httpd.shutdown()
        thread.join(timeout=5)


@pytest.fixture()
def app_server(test_bundle):
    yield from _server(test_bundle)


@pytest.fixture()
def luecken_server(luecken_bundle):
    yield from _server(luecken_bundle)


@ohne_node
def test_http_t1_entscheidungen_aus_test_bundle(app_server):
    ergebnis = ui_lauf(app_server, SZENARIO_T1)
    assert ergebnis["eintraege"] == [
        {"text": "2026-11-14: Erste Entscheidung", "href": f"{DETAIL_VORSCHLAG}entscheidungen%2Flog.md"},
        {"text": "2026-11-13: Zweite Entscheidung", "href": f"{DETAIL_VORSCHLAG}entscheidungen%2Flog.md"},
    ]
    assert ergebnis["abgerufen"] == [f"/api/file {ENTSCHEIDUNGEN_PFAD}"]


@ohne_node
def test_http_t2_eintrag_link_zur_log_datei(app_server):
    ergebnis = ui_lauf(app_server, SZENARIO_T1)
    for eintrag in ergebnis["eintraege"]:
        assert unquote(eintrag["href"][len(DETAIL_VORSCHLAG):]) == ENTSCHEIDUNGEN_PFAD


@ohne_node
def test_http_t3_projekt_unterpunkte(app_server):
    ergebnis = ui_lauf(app_server, SZENARIO_T3)
    assert [punkt["text"] for punkt in ergebnis["punkte"]] == [
        "Konzept",
        "Technische Spec",
        "User Stories",
        "Phasen",
        "Log",
    ]
    assert ergebnis["abgerufen"] == []


@ohne_node
def test_http_t4_spec_gerendert(app_server):
    ergebnis = ui_lauf(app_server, SZENARIO_T4)
    assert ergebnis["ueberschriften"] == ["Technische Spec"]
    assert ergebnis["absaetze"] == ["Spec-Absatz."]
    assert ergebnis["links"] == [{"text": "← Zurück zum Projekt", "href": "#/projekt"}]
    assert ergebnis["abgerufen"] == ["/api/file projekt/technische-spec.md"]


@ohne_node
@pytest.mark.parametrize("punkt", PROJEKT_ERWARTET)
def test_http_unterpunkt_laedt_passende_datei(app_server, punkt):
    ablauf = (
        f'await projekt.ladeProjektAnsicht({{ unterpunkt: "{punkt["unterpunkt"]}" }});\n'
        "const alle = bei(\"liste-projekt\").alleKnoten();\n"
        "return {\n"
        "  ueberschriften: alle.filter((k) => k.marke === \"h1\").map((k) => k.textContent),\n"
        "  abgerufen: aufrufe.map((a) => a.endpunkt + \" \" + a.datei),\n"
        "};"
    )
    ergebnis = ui_lauf(app_server, ablauf)
    assert ergebnis["abgerufen"] == [f"/api/file {punkt['pfad']}"]
    assert ergebnis["ueberschriften"], f"{punkt['titel']} rendert keinen Inhalt"


@ohne_node
def test_http_t5_fehlende_datei_entscheidungen_zeigt_fehlermeldung(luecken_server):
    ergebnis = ui_lauf(
        luecken_server,
        szenario_fehler("await projekt.ladeEntscheidungenAnsicht();", "liste-entscheidungen"),
    )
    assert ergebnis["text"]
    assert ergebnis["kinder"] > 0
    assert ergebnis["fehler"]["sichtbar"] is True
    assert ergebnis["fehler"]["text"]


@ohne_node
def test_http_t5_fehlende_datei_projekt_zeigt_fehlermeldung(luecken_server):
    ergebnis = ui_lauf(
        luecken_server,
        szenario_fehler('await projekt.ladeProjektAnsicht({ unterpunkt: "phasen" });', "liste-projekt"),
    )
    assert ergebnis["text"]
    assert ergebnis["kinder"] > 0
    assert ergebnis["fehler"]["sichtbar"] is True
    assert ergebnis["fehler"]["text"]

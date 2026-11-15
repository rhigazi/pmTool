"""Prüfungen für die A28-UI: Marke „neu", Kennungs-Hinweis und Freigabe (Paket 2).

Der Harness (Mini-DOM + Node-Runner) liegt in ``dom_helfer.py``; diese Datei
bringt ein eigenes Seiten-/Fetch-Gerüst mit. Geprüft werden T23–T33: Marke in
Aufgabenliste/Übersicht, Detail-Hinweis samt nächster Kennung und der
Freigabe-Knopf über den Menschen-Kanal ``POST /api/freigabe``.

Alle Läufe arbeiten gegen Fetch-Antworten aus dem Stab — nie gegen ``wissen/``.
"""

import json
from pathlib import Path

import pytest

from dom_helfer import DETAIL_JS, LISTE_JS, MINI_DOM, lies, node_ausfuehren, ohne_node

STATIC_DIR = Path(__file__).resolve().parents[1] / "static"
INDEX_HTML = STATIC_DIR / "index.html"
STYLE_CSS = STATIC_DIR / "style.css"

AUFGABE = "aufgaben/a28-neu.md"
AUFGABE_2 = "aufgaben/a1.md"
WELLE = "wellen/w1.md"
PROJEKT = "projekt/phasen.md"

MARKE = "neu"
FREIGABE = "Freigegeben"
NICHT_FREIGEGEBEN = "Nicht freigegeben"
FREIGABE_ERFOLG = "Aufgabe freigegeben."
FREIGABE_ENTZOGEN = "Freigabe entzogen."

HTML_PAYLOAD = "<img src=x onerror=alert(1)>"


def _aufgabe(pfad: str, titel: str, **felder) -> dict:
    eintrag = {
        "path": pfad,
        "titel": titel,
        "typ": "Task",
        "status": "Offen",
        "owner": "ai",
        "zuletzt_geaendert": "2026-11-15T10:00:00",
        "freigabe": False,
    }
    eintrag.update(felder)
    return eintrag


NEUE_AUFGABE = _aufgabe(AUFGABE, "Benachrichtigung bei neuer Aufgabe", neu=True)
BESTEHENDE = _aufgabe(AUFGABE_2, "A1: Mini-Aufgabe", neu=False)

# --- Listen-Gerüst -------------------------------------------------------

LISTEN_SEITE = r"""
const ANSICHTEN_DOM = [
  {
    ansicht: "ansicht-uebersicht",
    formular: "filter",
    status: "filter-status",
    owner: "filter-owner",
    zuruecksetzen: "filter-zuruecksetzen",
    tabelle: "tabelle",
    zusatz: true,
  },
  {
    ansicht: "ansicht-wellen",
    formular: "filter-wellen",
    status: "filter-wellen-status",
    owner: "filter-wellen-owner",
    zuruecksetzen: "filter-wellen-zuruecksetzen",
    tabelle: "tabelle-wellen",
  },
  {
    ansicht: "ansicht-aufgaben",
    formular: "filter-aufgaben",
    status: "filter-aufgaben-status",
    owner: "filter-aufgaben-owner",
    zuruecksetzen: "filter-aufgaben-zuruecksetzen",
    tabelle: "tabelle-aufgaben",
  },
];

for (const eintrag of ANSICHTEN_DOM) {
  const bereich = document.createElement("section");
  bereich.id = eintrag.ansicht;
  bereich._imDokument = true;
  const titel = document.createElement("h2");
  titel.textContent = eintrag.ansicht;
  const formular = document.createElement("form");
  formular.id = eintrag.formular;
  const status = document.createElement("select");
  status.id = eintrag.status;
  const owner = document.createElement("select");
  owner.id = eintrag.owner;
  const knopf = document.createElement("button");
  knopf.id = eintrag.zuruecksetzen;
  knopf.textContent = "Filter zurücksetzen";
  formular.append(status, owner, knopf);
  const tabelle = document.createElement("div");
  tabelle.id = eintrag.tabelle;
  tabelle.classList.add("tabelle-bereich");
  bereich.append(titel, formular, tabelle);
  if (eintrag.zusatz) {
    for (const id of ["uebersicht-zuletzt", "uebersicht-klarung"]) {
      const block = document.createElement("div");
      block.id = id;
      bereich.append(block);
    }
  }
}

for (const id of ["fehler", "meldung"]) {
  const bereich = document.createElement("div");
  bereich.id = id;
  bereich.hidden = true;
  bereich._imDokument = true;
}
"""

LISTEN_STAB = r"""
const ANTWORTEN = __ANTWORTEN__;
const aufrufe = [];
globalThis.fetch = async (pfad, optionen = {}) => {
  const ziel = String(pfad);
  const methode = optionen.method || "GET";
  aufrufe.push({ endpunkt: ziel, methode });
  const vorgabe = ANTWORTEN[methode + " " + ziel] ?? ANTWORTEN[ziel] ?? {
    status: 404,
    koerper: { error: "Nicht gefunden." },
  };
  return {
    ok: vorgabe.status < 400,
    status: vorgabe.status,
    headers: { get: () => "application/json" },
    text: async () => JSON.stringify(vorgabe.koerper ?? null),
  };
};

// Marken der Titel-Zelle je Zeile.
const zeilen = (id) =>
  sammle(bei(id))
    .filter((knoten) => knoten.marke === "tr" && knoten.dataset.path)
    .map((zeile) => ({
      path: zeile.dataset.path,
      titelZelle: zeile.kinder[0].textContent,
      marken: sammle(zeile.kinder[0])
        .filter((knoten) => knoten.marke === "span" && knoten.textContent === "neu")
        .map((knoten) => ({ klasse: knoten.classList.contains("status") })),
    }));
"""


def listen_lauf(ablauf: str, antworten: dict) -> dict:
    skript = (
        MINI_DOM
        + LISTEN_SEITE
        + LISTEN_STAB.replace("__ANTWORTEN__", json.dumps(antworten, ensure_ascii=False))
        + f"\nimport * as liste from {json.dumps(LISTE_JS.as_uri())};\n"
        + "const ergebnis = await (async () => {\n"
        + ablauf
        + "\n})();\n"
        + "console.log(JSON.stringify(ergebnis));\n"
    )
    return node_ausfuehren(skript)


def listen_antwort(daten, endpunkt: str = "/api/overview") -> dict:
    return {endpunkt: {"status": 200, "koerper": daten}}


# --- Detail-Gerüst mit veränderlichem Freigabe-Zustand -------------------

DETAIL_SEITE = r"""
const fehler = document.createElement("div");
fehler.id = "fehler";
fehler.hidden = true;
fehler._imDokument = true;
const meldung = document.createElement("div");
meldung.id = "meldung";
meldung.hidden = true;
meldung._imDokument = true;
const ziel = document.createElement("div");
ziel.id = "detail";
ziel._imDokument = true;

const aufrufe = [];
let freigeben = null;
const datei = { ...DATEI, frontmatter: { ...(DATEI.frontmatter || {}) } };
const antworte = (status, koerper) => ({
  ok: status < 400,
  status,
  headers: { get: () => "application/json" },
  text: async () => JSON.stringify(koerper ?? null),
});

globalThis.fetch = async (pfad, optionen = {}) => {
  const adresse = String(pfad);
  const methode = optionen.method || "GET";
  const nutzlast = typeof optionen.body === "string" ? JSON.parse(optionen.body) : null;
  aufrufe.push({
    methode,
    endpunkt: adresse.split("?")[0],
    nutzlast,
    gesperrt: knopfZustand(),
  });

  if (methode === "GET" && adresse.startsWith("/api/file")) return antworte(200, datei);
  if (methode === "GET" && adresse === "/api/wellen") return antworte(200, WELLEN);
  if (methode === "GET" && adresse === "/api/aufgaben") return antworte(200, AUFGABEN);

  if (methode === "POST" && adresse === "/api/freigabe") {
    if (GATE) await new Promise((fertig) => { freigeben = fertig; });
    if (FREIGABE_STATUS >= 400) return antworte(FREIGABE_STATUS, { error: FREIGABE_FEHLER });
    datei.freigabe = nutzlast.wert;
    datei.frontmatter.freigabe = nutzlast.wert;
    return antworte(200, {
      path: nutzlast.path,
      freigabe: nutzlast.wert,
      frontmatter: datei.frontmatter,
    });
  }

  return antworte(404, { error: "Nicht gefunden." });
};

function knopfZustand() {
  const knopf = bei("detail-freigabe");
  return knopf ? knopf.disabled : null;
}
"""


def detail_lauf(
    ablauf: str,
    datei: dict,
    *,
    wellen=None,
    aufgaben=None,
    freigabe_status: int = 200,
    freigabe_fehler: str = "Freigabe ist ein Menschen-Recht.",
    gate: bool = False,
) -> dict:
    skript = (
        MINI_DOM
        + f"const DATEI = {json.dumps(datei, ensure_ascii=False)};\n"
        + f"const WELLEN = {json.dumps(wellen or [], ensure_ascii=False)};\n"
        + f"const AUFGABEN = {json.dumps(aufgaben or [], ensure_ascii=False)};\n"
        + f"const FREIGABE_STATUS = {freigabe_status};\n"
        + f"const FREIGABE_FEHLER = {json.dumps(freigabe_fehler, ensure_ascii=False)};\n"
        + f"const GATE = {'true' if gate else 'false'};\n"
        + DETAIL_SEITE
        + f"\nimport * as detail from {json.dumps(DETAIL_JS.as_uri())};\n"
        + "const ergebnis = await (async () => {\n"
        + ablauf
        + "\n})();\n"
        + "console.log(JSON.stringify(ergebnis));\n"
    )
    return node_ausfuehren(skript)


def _datei(frontmatter: dict, markdown: str = "# Ziel\n\nFixture.\n", **felder) -> dict:
    daten = {"frontmatter": frontmatter, "markdown": markdown, "nachtraege": []}
    daten.update(felder)
    return daten


def _task_datei(freigabe=None, **felder) -> dict:
    """`/api/file`-Antwort einer Aufgabe; ``freigabe`` liegt wie in der API top-level."""
    frontmatter = {"type": "Task", "title": "A1: Mini-Aufgabe", "task_status": "offen"}
    daten = _datei(frontmatter, **felder)
    if freigabe is not None:
        daten["freigabe"] = freigabe
        frontmatter["freigabe"] = freigabe
    return daten


# --- T23: Marke in der Aufgabenliste ------------------------------------


@ohne_node
def test_t23_marke_in_der_aufgabenliste():
    ergebnis = listen_lauf(
        r"""
await liste.ladeAufgaben();
const erste = zeilen("tabelle-aufgaben");
bei("filter-status").value = "Offen";
await ausloesen(bei("filter-status"), "change");
const nachFilter = zeilen("tabelle-aufgaben");
await liste.ladeAufgaben();
return {
  erste,
  nachFilter,
  nachNeuladen: zeilen("tabelle-aufgaben"),
  aufrufe: aufrufe.map((eintrag) => eintrag.endpunkt),
};
""",
        listen_antwort([NEUE_AUFGABE, BESTEHENDE], "/api/aufgaben"),
    )

    assert [(zeile["path"], zeile["marken"]) for zeile in ergebnis["erste"]] == [
        (AUFGABE, [{"klasse": True}]),
        (AUFGABE_2, []),
    ]
    assert ergebnis["erste"][0]["titelZelle"].startswith("Benachrichtigung")
    # Idempotenz: Filterwechsel und Neuladen erzeugen keine zweite Marke.
    for stand in (ergebnis["nachFilter"], ergebnis["nachNeuladen"]):
        assert [len(zeile["marken"]) for zeile in stand] == [1, 0]
    assert ergebnis["aufrufe"] == ["/api/aufgaben", "/api/aufgaben"]


# --- T24: Marke in der Übersicht ----------------------------------------


@ohne_node
def test_t24_marke_in_der_uebersicht():
    klarung = _aufgabe("aufgaben/k1.md", "A4: Klaerung", status="Klarung", owner="mensch")
    welle = {
        "path": WELLE,
        "titel": "Welle 1",
        "typ": "Welle",
        "status": "Offen",
        "owner": "ai",
        "zuletzt_geaendert": "2026-11-14T10:00:00",
    }
    ergebnis = listen_lauf(
        r"""
await liste.ladeUebersicht();
return {
  tabelle: zeilen("tabelle"),
  top5: zeilen("uebersicht-zuletzt"),
  klarung: sammle(bei("uebersicht-klarung"))
    .filter((knoten) => knoten.marke === "li")
    .map((knoten) => ({
      text: knoten.textContent,
      marken: sammle(knoten).filter((kind) => kind.marke === "span").length,
    })),
};
""",
        listen_antwort([NEUE_AUFGABE, BESTEHENDE, klarung, welle]),
    )

    assert [(zeile["path"], len(zeile["marken"])) for zeile in ergebnis["tabelle"]] == [
        (AUFGABE, 1),
        (AUFGABE_2, 0),
        ("aufgaben/k1.md", 0),
        (WELLE, 0),
    ]
    # Top 5 sortiert nach „zuletzt geändert" (hier Gleichstand → Pfad aufsteigend).
    assert [(zeile["path"], len(zeile["marken"])) for zeile in ergebnis["top5"]] == [
        (AUFGABE_2, 0),
        (AUFGABE, 1),
        ("aufgaben/k1.md", 0),
        (WELLE, 0),
    ]
    # Die Klarung-Liste bleibt unverändert (kein span, keine Marke).
    assert [eintrag["marken"] for eintrag in ergebnis["klarung"]] == [0]
    assert ergebnis["klarung"][0]["text"] == "A4: Klaerung"


# --- T25: XSS und Robustheit -------------------------------------------


@ohne_node
def test_t25_xss_und_fehlendes_neu():
    xss = _aufgabe("aufgaben/xss.md", HTML_PAYLOAD, neu=True)
    ohne_feld = _aufgabe("aufgaben/ohne.md", "A2: Ohne Feld")
    ohne_feld.pop("neu", None)
    ergebnis = listen_lauf(
        r"""
const ausfuehrungen = [];
globalThis.alert = (wert) => ausfuehrungen.push(String(wert));
await liste.ladeAufgaben();
return {
  zeilen: zeilen("tabelle-aufgaben"),
  marken: marken(bei("tabelle-aufgaben")),
  texte: sammle(bei("tabelle-aufgaben"))
    .filter((knoten) => knoten.marke === "td")
    .map((knoten) => knoten.textContent),
  ausfuehrungen,
};
""",
        listen_antwort([xss, ohne_feld], "/api/aufgaben"),
    )

    assert ergebnis["zeilen"][0]["titelZelle"].startswith(HTML_PAYLOAD)
    assert ergebnis["zeilen"][0]["marken"] == [{"klasse": True}]
    assert ergebnis["zeilen"][1]["marken"] == []
    assert HTML_PAYLOAD in ergebnis["texte"][0]
    assert "img" not in ergebnis["marken"]
    assert "script" not in ergebnis["marken"]
    assert ergebnis["ausfuehrungen"] == []


# --- T26/T27: Detail-Hinweis -------------------------------------------


@ohne_node
def test_t26_detail_hinweis_mit_naechster_kennung():
    ergebnis = detail_lauf(
        r"""
await detail.ladeDetail({ unterpunkt: "aufgaben/a28-neu.md" });
const hinweis = bei("detail-neu-hinweis");
const kopf = sammle(bei("detail")).find((knoten) => knoten.classList.contains("detail-kopf"));
return {
  vorhanden: hinweis !== null,
  text: hinweis?.textContent ?? null,
  klasse: hinweis?.klassen() ?? [],
  knoepfeImHinweis: hinweis
    ? sammle(hinweis).filter((knoten) => knoten.marke === "button").length
    : null,
  eingaben: sammle(kopf).filter((knoten) => knoten.marke === "input").length,
  detail: bei("detail").textContent,
};
""",
        _datei(
            {"type": "Task", "title": "Benachrichtigung bei neuer Aufgabe", "task_status": "offen"},
            neu=True,
            naechste_kennung="A30",
        ),
    )

    assert ergebnis["vorhanden"] is True
    assert "Neue Aufgabe ohne Kennung" in ergebnis["text"]
    assert "Nächste freie Kennung: A30." in ergebnis["text"]
    assert "hinweis" in ergebnis["klasse"]
    # Keine Bedienung zum Setzen von Titel/Kennung.
    assert ergebnis["knoepfeImHinweis"] == 0
    assert ergebnis["eingaben"] == 0


@ohne_node
@pytest.mark.parametrize(
    "felder,erwartet",
    [
        ({"neu": False, "naechste_kennung": "A30"}, False),
        ({"neu": True}, True),
    ],
)
def test_t27_kein_hinweis_bei_kennung_und_ohne_naechste(felder, erwartet):
    ergebnis = detail_lauf(
        r"""
await detail.ladeDetail({ unterpunkt: "aufgaben/a1.md" });
const hinweis = bei("detail-neu-hinweis");
return { vorhanden: hinweis !== null, text: hinweis?.textContent ?? null };
""",
        _datei({"type": "Task", "title": "A1: Mini-Aufgabe", "task_status": "offen"}, **felder),
    )

    assert ergebnis["vorhanden"] is erwartet
    if erwartet:
        assert "Neue Aufgabe ohne Kennung" in ergebnis["text"]
        assert "Nächste freie Kennung" not in ergebnis["text"]


# --- T28: Freigabe-Anzeige ---------------------------------------------


@ohne_node
@pytest.mark.parametrize(
    "freigabe,anzeige,knopf",
    [
        (True, FREIGABE, "Freigabe entziehen"),
        (False, NICHT_FREIGEGEBEN, "Freigeben"),
        (None, NICHT_FREIGEGEBEN, "Freigeben"),
        ("ja", NICHT_FREIGEGEBEN, "Freigeben"),
    ],
)
def test_t28_freigabe_anzeige_und_knopftext(freigabe, anzeige, knopf):
    ergebnis = detail_lauf(
        r"""
await detail.ladeDetail({ unterpunkt: "aufgaben/a1.md" });
const knopf = bei("detail-freigabe");
return {
  text: bei("detail").textContent,
  knopfText: knopf?.textContent ?? null,
  knopfMarke: knopf?.marke ?? null,
  anzeige: bei("detail-freigabe-status")?.textContent ?? null,
};
""",
        _task_datei(freigabe=freigabe),
    )

    assert anzeige in ergebnis["text"]
    assert ergebnis["anzeige"] == anzeige
    assert ergebnis["knopfText"] == knopf
    assert ergebnis["knopfMarke"] == "button"


# --- T29/T30: Freigeben und Entziehen ----------------------------------


@ohne_node
def test_t29_freigeben_im_ui():
    ergebnis = detail_lauf(
        r"""
await detail.ladeDetail({ unterpunkt: "aufgaben/a1.md" });
const knopf = bei("detail-freigabe");
await ausloesen(knopf, "click");
return {
  posts: aufrufe
    .filter((eintrag) => eintrag.methode === "POST")
    .map((eintrag) => ({
      pfad: eintrag.endpunkt,
      nutzlast: eintrag.nutzlast,
      gesperrt: eintrag.gesperrt,
    })),
  meldung: { sichtbar: !bei("meldung").hidden, text: bei("meldung").textContent },
  anzeige: bei("detail-freigabe-status")?.textContent ?? null,
  knopfText: bei("detail-freigabe")?.textContent ?? null,
};
""",
        _task_datei(freigabe=False),
        gate=False,
    )

    assert ergebnis["posts"] == [
        {"pfad": "/api/freigabe", "nutzlast": {"path": AUFGABE_2, "wert": True}, "gesperrt": True}
    ]
    assert ergebnis["meldung"] == {"sichtbar": True, "text": FREIGABE_ERFOLG}
    assert ergebnis["anzeige"] == FREIGABE
    assert ergebnis["knopfText"] == "Freigabe entziehen"


@ohne_node
def test_t30_freigabe_entziehen_im_ui():
    ergebnis = detail_lauf(
        r"""
await detail.ladeDetail({ unterpunkt: "aufgaben/a1.md" });
await ausloesen(bei("detail-freigabe"), "click");
return {
  posts: aufrufe
    .filter((eintrag) => eintrag.methode === "POST")
    .map((eintrag) => eintrag.nutzlast),
  meldung: bei("meldung").textContent,
  anzeige: bei("detail-freigabe-status")?.textContent ?? null,
  knopfText: bei("detail-freigabe")?.textContent ?? null,
};
""",
        _task_datei(freigabe=True),
    )

    assert ergebnis["posts"] == [{"path": AUFGABE_2, "wert": False}]
    assert ergebnis["meldung"] == FREIGABE_ENTZOGEN
    assert ergebnis["anzeige"] == NICHT_FREIGEGEBEN
    assert ergebnis["knopfText"] == "Freigeben"


# --- T31/T32: Doppelklick und Fehlerpfad --------------------------------


@ohne_node
def test_t31_doppelklick_schreibt_nur_einmal():
    ergebnis = detail_lauf(
        r"""
await detail.ladeDetail({ unterpunkt: "aufgaben/a1.md" });
const knopf = bei("detail-freigabe");
const erstes = ausloesen(knopf, "click");
const gesperrtWaehrend = knopf.disabled;
const zweites = ausloesen(knopf, "click");
if (freigeben) freigeben();
await Promise.all([erstes, zweites]);
return {
  gesperrtWaehrend,
  posts: aufrufe.filter((eintrag) => eintrag.methode === "POST").length,
  danachBedienbar: bei("detail-freigabe")?.disabled === false,
};
""",
        _task_datei(freigabe=False),
        gate=True,
    )

    assert ergebnis["gesperrtWaehrend"] is True
    assert ergebnis["posts"] == 1
    assert ergebnis["danachBedienbar"] is True


@ohne_node
def test_t32_fehlerpfad_zeigt_meldung_und_bleibt_stehen():
    ergebnis = detail_lauf(
        r"""
await detail.ladeDetail({ unterpunkt: "aufgaben/a1.md" });
const vorher = bei("detail-freigabe-status")?.textContent ?? null;
await ausloesen(bei("detail-freigabe"), "click");
return {
  vorher,
  nachher: bei("detail-freigabe-status")?.textContent ?? null,
  posts: aufrufe.filter((eintrag) => eintrag.methode === "POST").length,
  dateiLadungen: aufrufe.filter((eintrag) => eintrag.endpunkt === "/api/file").length,
  fehler: { sichtbar: !bei("fehler").hidden, text: bei("fehler").textContent },
  meldung: { sichtbar: !bei("meldung").hidden, text: bei("meldung").textContent },
  bedienbar: bei("detail-freigabe")?.disabled === false,
};
""",
        _task_datei(freigabe=False),
        freigabe_status=403,
        freigabe_fehler="Freigabe ist ein Menschen-Recht.",
    )

    assert ergebnis["fehler"] == {"sichtbar": True, "text": "Freigabe ist ein Menschen-Recht."}
    assert ergebnis["meldung"] == {"sichtbar": False, "text": ""}
    assert ergebnis["vorher"] == ergebnis["nachher"] == NICHT_FREIGEGEBEN
    assert ergebnis["posts"] == 1
    assert ergebnis["dateiLadungen"] == 1
    assert ergebnis["bedienbar"] is True


# --- T33: Abgrenzung und Request-Budget ---------------------------------


@ohne_node
@pytest.mark.parametrize(
    "pfad,datei,endpunkte",
    [
        (
            AUFGABE_2,
            _task_datei(freigabe=False, neu=False),
            ["/api/file", "/api/wellen"],
        ),
        (
            WELLE,
            _datei({"type": "Welle", "title": "Welle 1"}),
            ["/api/file", "/api/aufgaben"],
        ),
        (
            PROJEKT,
            _datei({"type": "Projekt", "title": "Phasen"}),
            ["/api/file"],
        ),
    ],
)
def test_t33_abgrenzung_und_request_budget(pfad, datei, endpunkte):
    # Aufgaben-Detail: zwei Requests (A34 ergänzt später ``/api/aufgaben`` als dritten).
    ergebnis = detail_lauf(
        f"""
await detail.ladeDetail({{ unterpunkt: {json.dumps(pfad)} }});
return {{
  freigabe: bei("detail-freigabe") !== null,
  neuHinweis: bei("detail-neu-hinweis") !== null,
  aufrufe: aufrufe.map((eintrag) => eintrag.endpunkt),
}};
""",
        datei,
        wellen=[{"path": WELLE, "titel": "Welle 1", "typ": "Welle"}],
        aufgaben=[_aufgabe(AUFGABE_2, "A1", welle=WELLE)],
    )

    assert ergebnis["aufrufe"] == endpunkte
    if pfad == AUFGABE_2:
        assert ergebnis["freigabe"] is True
    else:
        assert ergebnis["freigabe"] is False
        assert ergebnis["neuHinweis"] is False


@ohne_node
def test_t33_listen_je_ein_request_ohne_zusatz():
    ergebnis = listen_lauf(
        r"""
await liste.ladeUebersicht();
const uebersicht = aufrufe.map((eintrag) => eintrag.endpunkt);
await liste.ladeAufgaben();
return { uebersicht, aufgaben: aufrufe.map((eintrag) => eintrag.endpunkt) };
""",
        {
            "/api/overview": {"status": 200, "koerper": [NEUE_AUFGABE]},
            "/api/aufgaben": {"status": 200, "koerper": [NEUE_AUFGABE]},
        },
    )

    assert ergebnis["uebersicht"] == ["/api/overview"]
    assert ergebnis["aufgaben"] == ["/api/overview", "/api/aufgaben"]


# --- Struktur/XSS (AK-10) ----------------------------------------------


def test_rahmen_dateien_bleiben_ohne_a28_markup():
    for datei in (INDEX_HTML, STYLE_CSS):
        quelle = lies(datei)
        assert "detail-freigabe" not in quelle
        assert "detail-neu-hinweis" not in quelle

    liste = lies(LISTE_JS)
    for senke in ("innerHTML", "insertAdjacentHTML", "document.write(", "eval("):
        assert senke not in liste
    assert '"neu"' in liste

    detail = lies(DETAIL_JS)
    for senke in ("innerHTML", "insertAdjacentHTML", "document.write(", "eval("):
        assert senke not in detail
    assert "detail-freigabe" in detail
    assert "detail-neu-hinweis" in detail
    assert "/api/freigabe" in detail

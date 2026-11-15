import { getJson } from "./api.js";

const SPALTEN = ["Titel", "Status", "owner", "zuletzt geändert"];
// Top 5 zuletzt geänderte Punkte gemäß US-1-AC4.
const ZULETZT_ANZAHL = 5;
const KEINE_ANGABE = "—";
const LEER_TABELLE = "Keine Einträge.";
const LEER_TREFFER = "Keine Treffer.";
const LEER_KLARUNG = "Keine offenen Rückfragen.";
const LADE_FEHLER = "Einträge konnten nicht geladen werden.";
const FORMAT_FEHLER = "Einträge haben ein unerwartetes Format.";

// Übersicht, Wellen und Aufgaben teilen sich dieselbe Listendarstellung.
const ANSICHTEN = {
  uebersicht: {
    pfad: "/api/overview",
    tabelle: "tabelle",
    formular: "filter",
    status: "filter-status",
    owner: "filter-owner",
    suche: "suche-uebersicht",
    zuruecksetzen: "filter-zuruecksetzen",
  },
  wellen: {
    pfad: "/api/wellen",
    tabelle: "tabelle-wellen",
    formular: "filter-wellen",
    status: "filter-wellen-status",
    owner: "filter-wellen-owner",
    suche: "suche-wellen",
    zuruecksetzen: "filter-wellen-zuruecksetzen",
  },
  aufgaben: {
    pfad: "/api/aufgaben",
    tabelle: "tabelle-aufgaben",
    formular: "filter-aufgaben",
    status: "filter-aufgaben-status",
    owner: "filter-aufgaben-owner",
    suche: "suche-aufgaben",
    zuruecksetzen: "filter-aufgaben-zuruecksetzen",
  },
};

const datenProAnsicht = new Map();
const initialisierteFilter = new Set();

// Durchsuchbare Felder aus `/api/overview`; „zuletzt geändert" gehört bewusst
// nicht dazu (Datumsrecherche ist nicht Teil der Anforderung).
const SUCHFELDER = ["titel", "path", "typ", "status", "owner", "hinweis", "welle"];

/**
 * Normalisiert Text für den Vergleich: Kleinschreibung, `ß`→`ss` und
 * NFD-Faltung, damit „prufung" auch „Prüfung" und „strasse" auch „Straße" trifft.
 */
function normalisiere(wert) {
  return String(wert ?? "")
    .toLowerCase()
    .replace(/ß/g, "ss")
    .normalize("NFD")
    .replace(/\p{M}/gu, "");
}

/** Zerlegt die Sucheingabe in getrimmte Begriffe; Leerraum trennt (UND). */
function suchbegriffe(suche) {
  return normalisiere(suche).split(/\s+/).filter(Boolean);
}

/**
 * Prüft, ob ein Eintrag alle Suchbegriffe enthält. Verglichen wird literarisch
 * über `includes` — kein `RegExp`, damit Sonderzeichen nicht crashen.
 */
function passtZurSuche(eintrag, begriffe) {
  if (begriffe.length === 0) return true;

  const text = normalisiere(SUCHFELDER.map((feld) => eintrag?.[feld]).join("\n"));
  return begriffe.every((begriff) => text.includes(begriff));
}

/**
 * Filtert Einträge nach UI-Status, owner und Suchbegriffen; leere Werte
 * bedeuten „alle". `owner: "ohne"` trifft Einträge ohne Zuständigkeit.
 */
export function filtereEintraege(eintraege, { status = "", owner = "", suche = "" } = {}) {
  if (!Array.isArray(eintraege)) return [];

  const begriffe = suchbegriffe(suche);

  return eintraege.filter((eintrag) => {
    if (!passtZurSuche(eintrag, begriffe)) return false;
    if (status && eintrag?.status !== status) return false;
    if (!owner) return true;
    if (owner === "ohne") return !eintrag?.owner;
    return eintrag?.owner === owner;
  });
}

/**
 * Entscheidet, was die Tabelle zeigt: Fehlerzustand hat Vorrang vor Filter- und
 * Leerzustand. Eine Antwort, die kein Array ist, wird als Formatfehler gemeldet
 * statt als leere Liste getarnt.
 */
export function waehleAnzeige(daten, { status = "", owner = "", suche = "" } = {}) {
  if (daten === null) return { art: "fehler", text: LADE_FEHLER, eintraege: [] };
  if (!Array.isArray(daten)) return { art: "fehler", text: FORMAT_FEHLER, eintraege: [] };

  const eintraege = filtereEintraege(daten, { status, owner, suche });
  if (eintraege.length === 0) {
    // „Keine Treffer." nur bei gesetztem Suchbegriff und vorhandenen Daten;
    // sonst bleibt es beim A11-Leerzustand „Keine Einträge.".
    const ohneTreffer = daten.length > 0 && suchbegriffe(suche).length > 0;
    return { art: "leer", text: ohneTreffer ? LEER_TREFFER : LEER_TABELLE, eintraege };
  }

  return { art: "tabelle", text: "", eintraege };
}

/** Formatiert einen ISO-Zeitstempel lokal; fehlende/ungültige Werte als „—". */
export function formatiereZeitstempel(wert) {
  if (!wert) return KEINE_ANGABE;

  const datum = new Date(wert);
  if (Number.isNaN(datum.getTime())) return KEINE_ANGABE;

  return new Intl.DateTimeFormat("de-DE", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(datum);
}

/** Sortiert absteigend nach „zuletzt geändert", Tie-Breaker `path`. */
export function sortiereNachAenderung(eintraege) {
  if (!Array.isArray(eintraege)) return [];

  return [...eintraege].sort((links, rechts) => {
    const zeitLinks = zeitwert(links);
    const zeitRechts = zeitwert(rechts);
    if (zeitLinks !== zeitRechts) return zeitRechts - zeitLinks;
    return String(links?.path ?? "").localeCompare(String(rechts?.path ?? ""));
  });
}

function zeitwert(eintrag) {
  const datum = new Date(eintrag?.zuletzt_geaendert ?? "");
  return Number.isNaN(datum.getTime()) ? 0 : datum.getTime();
}

function erstelleZelle(text, tag = "td") {
  const zelle = document.createElement(tag);
  zelle.textContent = text;
  return zelle;
}

function erstelleStatusZelle(eintrag) {
  const zelle = document.createElement("td");
  const status = eintrag?.status;
  if (!status) {
    zelle.textContent = KEINE_ANGABE;
    return zelle;
  }

  const marke = document.createElement("span");
  marke.classList.add("status");
  if (status === "Klarung") marke.classList.add("status--klarung");
  if (status === "Geschlossen") marke.classList.add("status--geschlossen");
  marke.textContent = status;
  zelle.append(marke);

  if (eintrag?.hinweis) {
    zelle.append(document.createTextNode(` (${eintrag.hinweis})`));
  }
  return zelle;
}

function erstelleOwnerZelle(eintrag) {
  const zelle = document.createElement("td");
  const owner = eintrag?.owner;
  if (!owner) {
    zelle.textContent = KEINE_ANGABE;
    return zelle;
  }

  const marke = document.createElement("span");
  marke.classList.add("owner");
  marke.textContent = owner;
  zelle.append(marke);
  return zelle;
}

function erstelleZeitZelle(eintrag) {
  const zelle = erstelleZelle(formatiereZeitstempel(eintrag?.zuletzt_geaendert));
  if (eintrag?.zuletzt_geaendert) zelle.title = eintrag.zuletzt_geaendert;
  return zelle;
}

/** Baut die Tabelle (Titel, Status, owner, zuletzt geändert) aus API-Einträgen. */
export function erstelleTabelle(eintraege) {
  const tabelle = document.createElement("table");
  tabelle.classList.add("tabelle");

  const kopf = tabelle.createTHead().insertRow();
  for (const spalte of SPALTEN) {
    const zelle = erstelleZelle(spalte, "th");
    zelle.scope = "col";
    kopf.append(zelle);
  }

  const koerper = tabelle.createTBody();
  for (const eintrag of eintraege) {
    const zeile = koerper.insertRow();
    if (eintrag?.path) zeile.dataset.path = eintrag.path;
    if (eintrag?.status === "Klarung") zeile.classList.add("klarung");
    zeile.append(
      erstelleZelle(eintrag?.titel || KEINE_ANGABE),
      erstelleStatusZelle(eintrag),
      erstelleOwnerZelle(eintrag),
      erstelleZeitZelle(eintrag),
    );
  }
  return tabelle;
}

function erstelleHinweis(text) {
  const hinweis = document.createElement("p");
  hinweis.classList.add("leer");
  hinweis.textContent = text;
  return hinweis;
}

function zeichneTabelle(bereich, eintraege) {
  if (!bereich) return;

  bereich.replaceChildren();
  if (eintraege.length === 0) {
    bereich.append(erstelleHinweis(LEER_TABELLE));
    return;
  }
  bereich.append(erstelleTabelle(eintraege));
}

function zeichneRueckfragen(bereich, eintraege) {
  if (!bereich) return;

  bereich.replaceChildren();
  if (eintraege.length === 0) {
    bereich.append(erstelleHinweis(LEER_KLARUNG));
    return;
  }

  const liste = document.createElement("ul");
  liste.classList.add("liste");
  for (const eintrag of eintraege) {
    const punkt = document.createElement("li");
    const titel = eintrag?.titel || KEINE_ANGABE;
    if (eintrag?.path) {
      const link = document.createElement("a");
      link.href = `#/detail/${encodeURIComponent(eintrag.path)}`;
      link.textContent = titel;
      punkt.append(link);
    } else {
      punkt.textContent = titel;
    }
    liste.append(punkt);
  }
  bereich.append(liste);
}

function zeichneUebersichtZusatz(daten) {
  const anzeige = waehleAnzeige(daten);
  if (anzeige.art === "fehler") {
    for (const id of ["uebersicht-zuletzt", "uebersicht-klarung"]) {
      const bereich = document.getElementById(id);
      if (bereich) bereich.replaceChildren(erstelleHinweis(anzeige.text));
    }
    return;
  }

  zeichneTabelle(
    document.getElementById("uebersicht-zuletzt"),
    sortiereNachAenderung(anzeige.eintraege).slice(0, ZULETZT_ANZAHL),
  );
  zeichneRueckfragen(
    document.getElementById("uebersicht-klarung"),
    anzeige.eintraege.filter((eintrag) => eintrag?.status === "Klarung"),
  );
}

/**
 * Hängt das Suchfeld dynamisch vor die Tabelle. Es liegt außerhalb des
 * Filterformulars (kein Submit-/Reload-Pfad) und wird nur einmal montiert.
 */
function montiereSuche(basis) {
  const konfiguration = ANSICHTEN[basis];
  const tabelle = document.getElementById(konfiguration.tabelle);
  if (!tabelle?.parentElement) return null;

  const vorhanden = document.getElementById(konfiguration.suche);
  if (vorhanden) return vorhanden;

  const bereich = document.createElement("div");
  bereich.classList.add("filter");
  const reihe = document.createElement("div");
  reihe.classList.add("filter-feld");
  const beschriftung = document.createElement("label");
  beschriftung.htmlFor = konfiguration.suche;
  beschriftung.textContent = "Suche";
  const eingabe = document.createElement("input");
  eingabe.type = "search";
  eingabe.id = konfiguration.suche;
  eingabe.value = "";

  reihe.append(beschriftung, eingabe);
  bereich.append(reihe);
  tabelle.parentElement.insertBefore(bereich, tabelle);

  eingabe.addEventListener("input", () => wendeFilterAn(basis));
  return eingabe;
}

function wendeFilterAn(basis) {
  if (!datenProAnsicht.has(basis)) return;

  const konfiguration = ANSICHTEN[basis];
  const daten = datenProAnsicht.get(basis);
  const status = document.getElementById(konfiguration.status)?.value ?? "";
  const owner = document.getElementById(konfiguration.owner)?.value ?? "";
  const suche = document.getElementById(konfiguration.suche)?.value ?? "";
  const anzeige = waehleAnzeige(daten, { status, owner, suche });

  const bereich = document.getElementById(konfiguration.tabelle);
  if (!bereich) return;

  bereich.replaceChildren();
  if (anzeige.art === "tabelle") {
    bereich.append(erstelleTabelle(anzeige.eintraege));
  } else {
    bereich.append(erstelleHinweis(anzeige.text));
  }
}

function initialisiereFilter(basis) {
  if (initialisierteFilter.has(basis)) return;

  const konfiguration = ANSICHTEN[basis];
  const formular = document.getElementById(konfiguration.formular);
  const status = document.getElementById(konfiguration.status);
  const owner = document.getElementById(konfiguration.owner);
  const zuruecksetzen = document.getElementById(konfiguration.zuruecksetzen);
  if (!formular || !status || !owner || !zuruecksetzen) return;

  const neuZeichnen = () => wendeFilterAn(basis);
  status.addEventListener("change", neuZeichnen);
  owner.addEventListener("change", neuZeichnen);
  zuruecksetzen.addEventListener("click", () => {
    status.value = "";
    owner.value = "";
    const suche = document.getElementById(konfiguration.suche);
    if (suche) suche.value = "";
    neuZeichnen();
  });

  initialisierteFilter.add(basis);
}

async function ladeListe(basis) {
  const konfiguration = ANSICHTEN[basis];
  initialisiereFilter(basis);
  montiereSuche(basis);

  const daten = await getJson(konfiguration.pfad);
  // Rohe Antwort pro Ansicht merken: Fehler-/Formatzustand bleibt so auch bei
  // Filteränderungen erhalten, bis neu geladen wird.
  datenProAnsicht.set(basis, daten ?? null);
  wendeFilterAn(basis);

  if (basis === "uebersicht") zeichneUebersichtZusatz(daten ?? null);
}

export function ladeUebersicht() {
  return ladeListe("uebersicht");
}

export function ladeWellen() {
  return ladeListe("wellen");
}

export function ladeAufgaben() {
  return ladeListe("aufgaben");
}

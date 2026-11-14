import { getJson } from "./api.js";

const SPALTEN = ["Titel", "Status", "owner", "zuletzt geändert"];
// Top 5 zuletzt geänderte Punkte gemäß US-1-AC4.
const ZULETZT_ANZAHL = 5;
const KEINE_ANGABE = "—";
const LEER_TABELLE = "Keine Einträge.";
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
    zuruecksetzen: "filter-zuruecksetzen",
  },
  wellen: {
    pfad: "/api/wellen",
    tabelle: "tabelle-wellen",
    formular: "filter-wellen",
    status: "filter-wellen-status",
    owner: "filter-wellen-owner",
    zuruecksetzen: "filter-wellen-zuruecksetzen",
  },
  aufgaben: {
    pfad: "/api/aufgaben",
    tabelle: "tabelle-aufgaben",
    formular: "filter-aufgaben",
    status: "filter-aufgaben-status",
    owner: "filter-aufgaben-owner",
    zuruecksetzen: "filter-aufgaben-zuruecksetzen",
  },
};

const datenProAnsicht = new Map();
const initialisierteFilter = new Set();

/**
 * Filtert Einträge nach UI-Status und owner; leere Werte bedeuten „alle".
 * `owner: "ohne"` trifft Einträge ohne Zuständigkeit (`null`/leer).
 */
export function filtereEintraege(eintraege, { status = "", owner = "" } = {}) {
  if (!Array.isArray(eintraege)) return [];

  return eintraege.filter((eintrag) => {
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
export function waehleAnzeige(daten, { status = "", owner = "" } = {}) {
  if (daten === null) return { art: "fehler", text: LADE_FEHLER, eintraege: [] };
  if (!Array.isArray(daten)) return { art: "fehler", text: FORMAT_FEHLER, eintraege: [] };

  const eintraege = filtereEintraege(daten, { status, owner });
  if (eintraege.length === 0) return { art: "leer", text: LEER_TABELLE, eintraege };

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
  marke.className = "status";
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
  marke.className = "owner";
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
  tabelle.className = "tabelle";

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
  hinweis.className = "leer";
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
  liste.className = "liste";
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

function wendeFilterAn(basis) {
  if (!datenProAnsicht.has(basis)) return;

  const konfiguration = ANSICHTEN[basis];
  const daten = datenProAnsicht.get(basis);
  const status = document.getElementById(konfiguration.status)?.value ?? "";
  const owner = document.getElementById(konfiguration.owner)?.value ?? "";
  const anzeige = waehleAnzeige(daten, { status, owner });

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
    neuZeichnen();
  });

  initialisierteFilter.add(basis);
}

async function ladeListe(basis) {
  const konfiguration = ANSICHTEN[basis];
  initialisiereFilter(basis);

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

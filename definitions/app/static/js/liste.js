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

// Wellen-Filter: „Alle" (leer) plus die Wellen des geladenen Bestands.
const WELLE_OHNE = "ohne";
const WELLE_ALLE_TEXT = "Alle";
const WELLE_OHNE_TEXT = "ohne Welle";
const WELLEN_ORDNER = "wellen/";

// Übersicht, Wellen und Aufgaben teilen sich dieselbe Listendarstellung.
const ANSICHTEN = {
  uebersicht: {
    pfad: "/api/overview",
    tabelle: "tabelle",
    formular: "filter",
    status: "filter-status",
    owner: "filter-owner",
    welle: "filter-welle",
    suche: "suche-uebersicht",
    zuruecksetzen: "filter-zuruecksetzen",
  },
  wellen: {
    pfad: "/api/wellen",
    tabelle: "tabelle-wellen",
    formular: "filter-wellen",
    status: "filter-wellen-status",
    owner: "filter-wellen-owner",
    welle: null,
    suche: "suche-wellen",
    zuruecksetzen: "filter-wellen-zuruecksetzen",
  },
  aufgaben: {
    pfad: "/api/aufgaben",
    tabelle: "tabelle-aufgaben",
    formular: "filter-aufgaben",
    status: "filter-aufgaben-status",
    owner: "filter-aufgaben-owner",
    welle: "filter-welle-aufgaben",
    suche: "suche-aufgaben",
    zuruecksetzen: "filter-aufgaben-zuruecksetzen",
  },
};

const datenProAnsicht = new Map();
const initialisierteFilter = new Set();

// Wellen-Metadaten aus bereits geladenen Daten (kein zusätzlicher Request):
// die Übersicht enthält alle Wellen, die Aufgabenliste referenziert sie.
let bekannteWellen = [];

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
 * Filtert Einträge nach UI-Status, owner, Suchbegriffen und Welle; leere Werte
 * bedeuten „alle". `owner: "ohne"` trifft Einträge ohne Zuständigkeit,
 * `welle: "ohne"` Einträge ohne Wellen-Zuordnung.
 */
export function filtereEintraege(
  eintraege,
  { status = "", owner = "", suche = "", welle = "" } = {},
) {
  if (!Array.isArray(eintraege)) return [];

  const begriffe = suchbegriffe(suche);

  return eintraege.filter((eintrag) => {
    if (!passtZurSuche(eintrag, begriffe)) return false;
    if (status && eintrag?.status !== status) return false;
    if (!passtZurWelle(eintrag, welle)) return false;
    if (!owner) return true;
    if (owner === "ohne") return !eintrag?.owner;
    return eintrag?.owner === owner;
  });
}

/** Wellen-Filter: exakte Pfadgleichheit; „ohne" trifft Einträge ohne ``welle``. */
function passtZurWelle(eintrag, welle) {
  if (!welle) return true;
  if (welle === WELLE_OHNE) return !eintrag?.welle;
  return eintrag?.welle === welle;
}

/**
 * Entscheidet, was die Tabelle zeigt: Fehlerzustand hat Vorrang vor Filter- und
 * Leerzustand. Eine Antwort, die kein Array ist, wird als Formatfehler gemeldet
 * statt als leere Liste getarnt.
 */
export function waehleAnzeige(
  daten,
  { status = "", owner = "", suche = "", welle = "" } = {},
) {
  if (daten === null) return { art: "fehler", text: LADE_FEHLER, eintraege: [] };
  if (!Array.isArray(daten)) return { art: "fehler", text: FORMAT_FEHLER, eintraege: [] };

  const eintraege = filtereEintraege(daten, { status, owner, suche, welle });
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

/**
 * Formatiert den abgeleiteten Arbeitsstatus als „<Label>: <Text>".
 * Fehlt eines der Teile, steht nur das andere; ohne Angabe bleibt es leer
 * (dann entsteht keine Zeile). Unbekannte Rollen kommen unverändert an.
 */
export function formatiereArbeitsstand(quelle) {
  if (quelle === null || typeof quelle !== "object" || Array.isArray(quelle)) return "";

  const label = textWert(quelle.arbeitsrolle_label) || textWert(quelle.arbeitsrolle);
  const inhalt = textWert(quelle.arbeitsstatus);
  if (label && inhalt) return `${label}: ${inhalt}`;
  return label || inhalt;
}

function textWert(wert) {
  return typeof wert === "string" ? wert.trim() : "";
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

  // Arbeitsstatus (A30): nur Aufgaben, nur bei ableitbarer Angabe.
  const arbeitsstand = eintrag?.typ === "Task" ? formatiereArbeitsstand(eintrag) : "";
  if (arbeitsstand) {
    const zeile = document.createElement("div");
    zeile.classList.add("arbeitsstand");
    zeile.textContent = arbeitsstand;
    zelle.append(zeile);
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

  // Kein eigener Leerzustand: den trägt bereits die Haupttabelle, sonst
  // erscheint „Keine Einträge." doppelt auf der Übersicht (A25-Befund 2).
  bereich.replaceChildren();
  if (eintraege.length === 0) return;
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
  // Ein verwaistes Feld (Container neu aufgebaut) wird ersetzt (A25-Befund 1).
  if (vorhanden && vorhanden.isConnected !== false) return vorhanden;

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

/** Wellen-Einträge aus dem geladenen Bestand (Präfix `wellen/`, wie `/api/wellen`). */
function wellenAusBestand(daten) {
  if (!Array.isArray(daten)) return [];
  return daten.filter(
    (eintrag) => typeof eintrag?.path === "string" && eintrag.path.startsWith(WELLEN_ORDNER),
  );
}

/** In Aufgaben referenzierte Wellen-Pfade (ohne Titel — Anzeige dann als Pfad). */
function wellenAusVerweisen(daten) {
  if (!Array.isArray(daten)) return [];
  const gefunden = [];
  for (const eintrag of daten) {
    const pfad = typeof eintrag?.welle === "string" ? eintrag.welle.trim() : "";
    if (!pfad) continue;
    if (!gefunden.some((kandidat) => kandidat.path === pfad)) gefunden.push({ path: pfad });
  }
  return gefunden;
}

function fuehreWellenZusammen(...quellen) {
  const ergebnis = [];
  for (const quelle of quellen) {
    for (const eintrag of quelle) {
      const pfad = typeof eintrag?.path === "string" ? eintrag.path.trim() : "";
      if (!pfad) continue;
      const index = ergebnis.findIndex((kandidat) => kandidat.path === pfad);
      if (index === -1) ergebnis.push({ ...eintrag, path: pfad });
      else if (!ergebnis[index].titel && eintrag?.titel) ergebnis[index] = { ...eintrag, path: pfad };
    }
  }
  return ergebnis;
}

/**
 * Wellen für eine Ansicht: die Übersicht liefert alle Wellen, die Aufgabenliste
 * ergänzt den bekannten Bestand um die in den Aufgaben referenzierten Pfade.
 */
function ermittleWellen(basis, daten) {
  const ausBestand = wellenAusBestand(daten);
  if (basis === "uebersicht") {
    bekannteWellen = ausBestand;
    return ausBestand;
  }
  return fuehreWellenZusammen(bekannteWellen, ausBestand, wellenAusVerweisen(daten));
}

function erstelleOption(wert, beschriftung) {
  const option = document.createElement("option");
  option.value = wert;
  option.textContent = beschriftung;
  return option;
}

function fuelleWellenAuswahl(auswahl, wellen) {
  const optionen = [erstelleOption("", WELLE_ALLE_TEXT), erstelleOption(WELLE_OHNE, WELLE_OHNE_TEXT)];
  for (const eintrag of wellen) {
    const titel = typeof eintrag?.titel === "string" ? eintrag.titel.trim() : "";
    // Pfad im Label, damit Titel-Duplikate unterscheidbar bleiben (A13).
    optionen.push(erstelleOption(eintrag.path, titel ? `${titel} (${eintrag.path})` : eintrag.path));
  }
  auswahl.replaceChildren(...optionen);
}

/**
 * Hängt den Wellen-Filter je Ansicht idempotent in das bestehende Filterformular
 * ein (vor „Filter zurücksetzen"); `index.html` bleibt ohne Markup. Die Optionen
 * stammen aus den bereits geladenen Listen — kein zusätzlicher Request.
 */
function montiereWellenFilter(basis, daten) {
  const konfiguration = ANSICHTEN[basis];
  const feldId = konfiguration.welle;
  if (!feldId) return null;

  const formular = document.getElementById(konfiguration.formular);
  const zuruecksetzen = document.getElementById(konfiguration.zuruecksetzen);
  if (!formular || !zuruecksetzen) return null;

  let auswahl = document.getElementById(feldId);
  if (auswahl && auswahl.isConnected === false) auswahl = null;
  if (!auswahl) {
    const reihe = document.createElement("div");
    reihe.classList.add("filter-feld");
    const beschriftung = document.createElement("label");
    beschriftung.htmlFor = feldId;
    beschriftung.textContent = "Welle";
    auswahl = document.createElement("select");
    auswahl.id = feldId;
    auswahl.setAttribute("aria-label", "Welle");
    reihe.append(beschriftung, auswahl);
    formular.insertBefore(reihe, zuruecksetzen);
    auswahl.addEventListener("change", () => wendeFilterAn(basis));
  }

  const vorher = auswahl.value;
  if (Array.isArray(daten)) {
    fuelleWellenAuswahl(auswahl, ermittleWellen(basis, daten));
    auswahl.disabled = false;
  } else {
    // Fail-loud: ohne Daten wird nicht still weggefiltert, nur „Alle" bleibt.
    auswahl.replaceChildren(erstelleOption("", WELLE_ALLE_TEXT));
    auswahl.disabled = true;
  }
  auswahl.value = optionenEnthaelt(auswahl, vorher) ? vorher : "";
  return auswahl;
}

function optionenEnthaelt(auswahl, wert) {
  if (!wert) return true;
  return Array.from(auswahl.options ?? []).some((option) => option.value === wert);
}

function wendeFilterAn(basis) {
  if (!datenProAnsicht.has(basis)) return;

  const konfiguration = ANSICHTEN[basis];
  const daten = datenProAnsicht.get(basis);
  const status = document.getElementById(konfiguration.status)?.value ?? "";
  const owner = document.getElementById(konfiguration.owner)?.value ?? "";
  const suche = document.getElementById(konfiguration.suche)?.value ?? "";
  const welle = konfiguration.welle
    ? document.getElementById(konfiguration.welle)?.value ?? ""
    : "";
  const anzeige = waehleAnzeige(daten, { status, owner, suche, welle });

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
    const welle = konfiguration.welle ? document.getElementById(konfiguration.welle) : null;
    if (welle) welle.value = "";
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
  montiereWellenFilter(basis, daten ?? null);
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

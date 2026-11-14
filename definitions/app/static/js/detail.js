import {
  getJson,
  loescheFehler,
  loescheMeldung,
  postJson,
  zeigeFehler,
  zeigeMeldung,
} from "./api.js";

const CONTAINER_ID = "detail";
const OWNER_AUSWAHL_ID = "detail-owner";
const FORMULAR_ID = "nachtrag-formular";
const TEXT_ID = "nachtrag-text";
const FEHLER_ID = "nachtrag-fehler";

const KEINE_ANGABE = "—";
const OHNE_STATUS = "ohne Status";
const LEER_KEINE_AUSWAHL = "Keine Datei ausgewählt.";
const LADE_FEHLER = "Datei konnte nicht geladen werden.";
const FORMAT_FEHLER = "Datei hat ein unerwartetes Format.";
const FELD_LEER = "Bitte einen Nachtrag eingeben.";
const NACHRAG_ERFOLG = "Nachtrag gespeichert.";
const OWNER_ERFOLG = "owner gespeichert.";
const STATUS_ERFOLG = "Status gespeichert.";
const ZURUECK_ZIEL = "#/uebersicht";

// R1: Nur diese beiden Status sind über die UI setzbar; Pipeline-Status nicht.
export const STATUS_KNOEPFE = ["Klarung", "Geschlossen"];
const OWNER_WERTE = ["mensch", "ai"];

// Spiegel von status.py (Mapping-Tabelle der Technischen Spec):
// task_status -> [UI-Status, Hinweis, owner-Default].
const TASK_STATUS_UI = {
  offen: ["Offen", null, "ai"],
  "in Klärung": ["Klarung", null, "mensch"],
  "in Planung": ["Offen", null, "ai"],
  geplant: ["Offen", null, "ai"],
  "in Umsetzung": ["In Arbeit", null, "ai"],
  "im Review": ["Testing", null, "ai"],
  "im Test": ["Testing", null, "ai"],
  "in Doku": ["Dokumentation", null, "ai"],
  "zur Abnahme": ["Klarung", null, "mensch"],
  abgeschlossen: ["Geschlossen", null, null],
  pausiert: ["Offen", "pausiert", null],
};

const UI_STATUS_WERTE = [
  "Klarung",
  "Offen",
  "In Arbeit",
  "Testing",
  "Dokumentation",
  "Geschlossen",
];

const OWNER_DEFAULTS = {
  Klarung: "mensch",
  Offen: "ai",
  "In Arbeit": "ai",
  Testing: "ai",
  Dokumentation: "ai",
  Geschlossen: null,
};

// Blockmarker des Minimal-Renderers; `ZAUN` umschließt Codeblöcke.
const ZAUN = "```";
const UEBERSCHRIFT = /^(#{1,6})\s+(.*)$/;
const ZITAT = /^>\s?(.*)$/;
const UNGEORDNET = /^[-*+]\s+(.*)$/;
const GEORDNET = /^\d+[.)]\s+(.*)$/;

function feld(frontmatter, name) {
  if (!frontmatter || typeof frontmatter !== "object") return null;

  const wert = frontmatter[name];
  if (wert === null || wert === undefined) return null;

  const text = String(wert).trim();
  return text || null;
}

/**
 * Zerlegt Markdown in Blocktokens (Überschrift, Absatz, Liste, Code, Zitat).
 * Absichtlich minimal: keine Inline-Auszeichnung, damit das Rendern ohne
 * HTML-Interpretation auskommt (R6).
 */
export function parseMarkdown(markdown) {
  if (typeof markdown !== "string" || !markdown.trim()) return [];

  const zeilen = markdown.split(/\r?\n/);
  const bloecke = [];
  let index = 0;

  while (index < zeilen.length) {
    const geprueft = zeilen[index].trim();
    if (!geprueft) {
      index += 1;
      continue;
    }

    if (geprueft.startsWith(ZAUN)) {
      const code = [];
      index += 1;
      while (index < zeilen.length && !zeilen[index].trim().startsWith(ZAUN)) {
        code.push(zeilen[index]);
        index += 1;
      }
      index += 1;
      bloecke.push({ art: "code", text: code.join("\n") });
      continue;
    }

    const ueberschrift = UEBERSCHRIFT.exec(geprueft);
    if (ueberschrift) {
      bloecke.push({
        art: "ueberschrift",
        ebene: ueberschrift[1].length,
        text: ueberschrift[2].trim(),
      });
      index += 1;
      continue;
    }

    if (ZITAT.test(geprueft)) {
      const zitat = [];
      while (index < zeilen.length) {
        const treffer = ZITAT.exec(zeilen[index].trim());
        if (!treffer) break;
        zitat.push(treffer[1]);
        index += 1;
      }
      bloecke.push({ art: "zitat", text: zitat.join("\n").trimEnd() });
      continue;
    }

    const liste = leseListe(zeilen, index);
    if (liste) {
      bloecke.push(liste.block);
      index = liste.ende;
      continue;
    }

    const absatz = [];
    while (index < zeilen.length && zeilen[index].trim() && !istBlockstart(zeilen[index])) {
      absatz.push(zeilen[index].trim());
      index += 1;
    }
    bloecke.push({ art: "absatz", text: absatz.join(" ") });
  }

  return bloecke;
}

function istBlockstart(zeile) {
  const text = zeile.trim();
  return (
    text.startsWith(ZAUN) ||
    UEBERSCHRIFT.test(text) ||
    ZITAT.test(text) ||
    UNGEORDNET.test(text) ||
    GEORDNET.test(text)
  );
}

function leseListe(zeilen, start) {
  const geprueft = zeilen[start].trim();
  const geordnet = GEORDNET.test(geprueft);
  const muster = geordnet ? GEORDNET : UNGEORDNET;
  if (!muster.test(geprueft)) return null;

  const eintraege = [];
  let index = start;
  while (index < zeilen.length) {
    const treffer = muster.exec(zeilen[index].trim());
    if (!treffer) break;
    eintraege.push(treffer[1].trim());
    index += 1;
  }

  return { block: { art: "liste", geordnet, eintraege }, ende: index };
}

/** Baut aus Markdown ein DOM-Fragment; alle Texte laufen über `textContent`. */
export function rendereMarkdown(markdown) {
  const fragment = document.createDocumentFragment();
  for (const block of parseMarkdown(markdown)) {
    fragment.append(erstelleBlock(block));
  }
  return fragment;
}

function erstelleBlock(block) {
  switch (block.art) {
    case "ueberschrift": {
      const ebene = Math.min(Math.max(block.ebene, 1), 6);
      const element = document.createElement(`h${ebene}`);
      element.textContent = block.text;
      return element;
    }
    case "liste": {
      const liste = document.createElement(block.geordnet ? "ol" : "ul");
      for (const eintrag of block.eintraege) {
        const punkt = document.createElement("li");
        punkt.textContent = eintrag;
        liste.append(punkt);
      }
      return liste;
    }
    case "code": {
      const pre = document.createElement("pre");
      const code = document.createElement("code");
      code.textContent = block.text;
      pre.append(code);
      return pre;
    }
    case "zitat": {
      const zitat = document.createElement("blockquote");
      zitat.textContent = block.text;
      return zitat;
    }
    default: {
      const absatz = document.createElement("p");
      absatz.textContent = block.text;
      return absatz;
    }
  }
}

/** UI-Status und Hinweis aus dem Frontmatter (Spiegel von `status.ui_status`). */
export function ermittleStatus(frontmatter) {
  const taskStatus = feld(frontmatter, "task_status");
  if (taskStatus) {
    const eintrag = Object.hasOwn(TASK_STATUS_UI, taskStatus) ? TASK_STATUS_UI[taskStatus] : null;
    if (eintrag) return { status: eintrag[0], hinweis: eintrag[1] };
    return { status: "Offen", hinweis: taskStatus };
  }

  const status = feld(frontmatter, "status");
  if (!status) return { status: "Offen", hinweis: OHNE_STATUS };
  if (UI_STATUS_WERTE.includes(status)) return { status, hinweis: null };
  return { status: "Offen", hinweis: status };
}

/** Anzeige-owner: explizites Feld vor Status-Default (R3). */
export function ermittleOwner(frontmatter) {
  const owner = feld(frontmatter, "owner");
  if (owner) return owner;

  const taskStatus = feld(frontmatter, "task_status");
  if (taskStatus) {
    const eintrag = Object.hasOwn(TASK_STATUS_UI, taskStatus) ? TASK_STATUS_UI[taskStatus] : null;
    return eintrag ? eintrag[2] : null;
  }

  return OWNER_DEFAULTS[feld(frontmatter, "status")] ?? null;
}

/**
 * Payload für `POST /api/meta`: Nicht gesetzte Felder werden weggelassen, weil
 * die API strikt prüft und leere Strings mit 403 abweist.
 */
export function erstelleMetaPayload(pfad, { owner, status } = {}) {
  const daten = { path: pfad };
  const ownerText = typeof owner === "string" ? owner.trim() : "";
  const statusText = typeof status === "string" ? status.trim() : "";

  if (ownerText) daten.owner = ownerText;
  if (statusText) daten.status = statusText;
  return daten;
}

/** Payload für `POST /api/nachtrag`; leerer Text ergibt `null` (kein Eintrag). */
export function erstelleNachtragPayload(pfad, text) {
  const inhalt = typeof text === "string" ? text.trim() : "";
  if (!inhalt) return null;
  return { path: pfad, text: inhalt };
}

function erstelleHinweis(text) {
  const hinweis = document.createElement("p");
  hinweis.className = "leer";
  hinweis.textContent = text;
  return hinweis;
}

function istDatei(daten) {
  return (
    daten !== null &&
    typeof daten === "object" &&
    !Array.isArray(daten) &&
    typeof daten.markdown === "string"
  );
}

function anhaengenFeld(angaben, name, inhalt) {
  const bezeichnung = document.createElement("dt");
  bezeichnung.textContent = name;
  const wert = document.createElement("dd");
  if (typeof inhalt === "string") {
    wert.textContent = inhalt;
  } else {
    wert.append(inhalt);
  }
  angaben.append(bezeichnung, wert);
}

function erstelleStatusAnzeige(status, hinweis) {
  const anzeige = document.createDocumentFragment();

  const marke = document.createElement("span");
  marke.className = "status";
  if (status === "Klarung") marke.classList.add("status--klarung");
  if (status === "Geschlossen") marke.classList.add("status--geschlossen");
  marke.textContent = status;
  anzeige.append(marke);

  if (hinweis) {
    const zusatz = document.createElement("span");
    zusatz.textContent = ` (${hinweis})`;
    anzeige.append(zusatz);
  }
  return anzeige;
}

function erstelleOwnerAuswahl(pfad, owner) {
  const auswahl = document.createElement("select");
  auswahl.id = OWNER_AUSWAHL_ID;
  auswahl.setAttribute("aria-label", "owner");

  const ohne = document.createElement("option");
  ohne.value = "";
  ohne.textContent = KEINE_ANGABE;
  auswahl.append(ohne);

  for (const wert of OWNER_WERTE) {
    const option = document.createElement("option");
    option.value = wert;
    option.textContent = wert;
    auswahl.append(option);
  }

  const aktuell = OWNER_WERTE.includes(owner) ? owner : "";
  auswahl.value = aktuell;

  auswahl.addEventListener("change", async () => {
    const wert = auswahl.value;
    if (!OWNER_WERTE.includes(wert)) {
      auswahl.value = aktuell;
      return;
    }
    if (!(await speichereMeta(pfad, { owner: wert }, OWNER_ERFOLG))) {
      auswahl.value = aktuell;
    }
  });

  return auswahl;
}

function erstelleStatusKnopf(status, aktiv) {
  const knopf = document.createElement("button");
  knopf.type = "button";
  knopf.className = "knopf";
  knopf.dataset.status = status;
  knopf.textContent = status;
  knopf.setAttribute("aria-pressed", aktiv ? "true" : "false");
  if (aktiv) knopf.classList.add("knopf--primaer");
  return knopf;
}

function erstelleAktionen(pfad, status) {
  const aktionen = document.createElement("div");
  aktionen.className = "detail-aktionen";

  for (const wert of STATUS_KNOEPFE) {
    const knopf = erstelleStatusKnopf(wert, wert === status);
    knopf.addEventListener("click", async () => {
      await speichereMeta(pfad, { status: wert }, STATUS_ERFOLG);
    });
    aktionen.append(knopf);
  }

  const zurueck = document.createElement("a");
  zurueck.className = "knopf";
  zurueck.href = ZURUECK_ZIEL;
  zurueck.textContent = "← Zurück zur Übersicht";
  aktionen.append(zurueck);

  return aktionen;
}

function erstelleKopf(pfad, daten) {
  const frontmatter =
    daten.frontmatter && typeof daten.frontmatter === "object" ? daten.frontmatter : {};
  const { status, hinweis } = ermittleStatus(frontmatter);

  const kopf = document.createElement("div");
  kopf.className = "detail-kopf";

  const titel = document.createElement("h2");
  titel.className = "ansicht-titel";
  titel.textContent = feld(frontmatter, "title") || pfad;
  kopf.append(titel);

  const angaben = document.createElement("dl");
  anhaengenFeld(angaben, "Typ", feld(frontmatter, "type") || KEINE_ANGABE);
  anhaengenFeld(angaben, "Status", erstelleStatusAnzeige(status, hinweis));
  anhaengenFeld(angaben, "owner", erstelleOwnerAuswahl(pfad, ermittleOwner(frontmatter)));
  kopf.append(angaben, erstelleAktionen(pfad, status));

  return kopf;
}

function erstelleInhalt(markdown) {
  const inhalt = document.createElement("div");
  inhalt.className = "detail-inhalt";
  inhalt.append(rendereMarkdown(markdown));
  return inhalt;
}

function erstelleNachtragFormular(pfad) {
  const formular = document.createElement("form");
  formular.id = FORMULAR_ID;
  formular.className = "formular";
  formular.setAttribute("aria-label", "Nachtrag einfügen");

  const feldBereich = document.createElement("div");
  feldBereich.className = "formular-feld";

  const beschriftung = document.createElement("label");
  beschriftung.htmlFor = TEXT_ID;
  beschriftung.textContent = "Nachtrag einfügen";

  const eingabe = document.createElement("textarea");
  eingabe.id = TEXT_ID;
  eingabe.name = "text";
  eingabe.className = "kurzkontext";
  eingabe.rows = 4;

  feldBereich.append(beschriftung, eingabe);

  const fehler = document.createElement("p");
  fehler.id = FEHLER_ID;
  fehler.className = "feldfehler";
  fehler.setAttribute("role", "alert");
  fehler.hidden = true;

  const knopf = document.createElement("button");
  knopf.type = "submit";
  knopf.className = "knopf knopf--primaer";
  knopf.textContent = "Nachtrag speichern";

  formular.append(feldBereich, fehler, knopf);

  formular.addEventListener("submit", async (ereignis) => {
    ereignis.preventDefault();

    const daten = erstelleNachtragPayload(pfad, eingabe.value);
    if (daten === null) {
      fehler.textContent = FELD_LEER;
      fehler.hidden = false;
      eingabe.focus();
      return;
    }

    fehler.textContent = "";
    fehler.hidden = true;
    loescheFehler();
    loescheMeldung();

    const ergebnis = await postJson("/api/nachtrag", daten);
    if (ergebnis === null) return;

    zeigeMeldung(NACHRAG_ERFOLG);
    await ladeDetail({ unterpunkt: pfad });
  });

  return formular;
}

/** Schreibt `owner`/`status`; Fehler zeigt bereits `api.js`, die Ansicht bleibt stehen. */
async function speichereMeta(pfad, aenderung, erfolgsmeldung) {
  loescheFehler();
  loescheMeldung();

  const ergebnis = await postJson("/api/meta", erstelleMetaPayload(pfad, aenderung));
  if (ergebnis === null) return false;

  zeigeMeldung(erfolgsmeldung);
  await ladeDetail({ unterpunkt: pfad });
  return true;
}

function zeichne(ziel, pfad, daten) {
  ziel.replaceChildren(
    erstelleKopf(pfad, daten),
    erstelleInhalt(daten.markdown),
    erstelleNachtragFormular(pfad),
  );
}

/** Lädt eine Datei aus `GET /api/file` und zeichnet die Detailansicht. */
export async function ladeDetail({ unterpunkt } = {}) {
  const ziel = document.getElementById(CONTAINER_ID);
  if (!ziel) return;

  const pfad = typeof unterpunkt === "string" ? unterpunkt.trim() : "";
  if (!pfad) {
    ziel.replaceChildren(erstelleHinweis(LEER_KEINE_AUSWAHL));
    return;
  }

  const daten = await getJson(`/api/file?path=${encodeURIComponent(pfad)}`);
  if (daten === null) {
    ziel.replaceChildren(erstelleHinweis(LADE_FEHLER));
    return;
  }

  if (!istDatei(daten)) {
    ziel.replaceChildren(erstelleHinweis(FORMAT_FEHLER));
    zeigeFehler(FORMAT_FEHLER);
    return;
  }

  zeichne(ziel, pfad, daten);
}

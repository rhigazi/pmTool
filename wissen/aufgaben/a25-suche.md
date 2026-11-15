---
type: Task
title: Suche
description: In der Übersicht Liste brauchen wir eine Möglichkeit Suchbegriffe einzugeben
  um die Aufgaben nach bestimmten Informationen zur durchsuchen
task_status: in Review
phase: 5 Review
priority: mittel
assigned_to: coder
owner: ai
---

# Ziel

In der Übersicht Liste brauchen wir eine Möglichkeit Suchbegriffe einzugeben um die Aufgaben nach bestimmten Informationen zur durchsuchen

# Akzeptanzkriterien

- Ich gebe in der Suche ein Suchbegriff und mir werden als Ergebnis nur die Aufgaben gezeigt in denen dieser Begriff vorkommt

# Testfälle (TDD)

**Zuordnung zum Akzeptanzkriterium** (ein AK-Satz + vier verbindliche PM-Vorgaben N1–N4):
**AK-1** „Suchbegriff eingeben → nur Aufgaben/Zeilen, in denen der Begriff vorkommt" → T1–T13, T16–T19.
**N2** (PM) „kombinierbar mit Status-/owner-Filter" → T11, T18.
**N3** (PM) „Leerzustand »Keine Treffer.« fail-loud-konform" → T13–T15, T19.
**N4** (PM) „XSS-sicher, Sonderzeichen crashen nicht" → T10, T21–T23.
**N1** (PM) „kein neuer Server-Endpunkt, möglichst ohne `index.html`-Änderung" → T1, T4, T16, T24.

Reihenfolge = Red-Green-Takt: erst Test schreiben, rot laufen lassen, dann das Minimum implementieren. Jede Testnummer ist ein eigener pytest-Fall (`tests/test_suche.py`), damit rot/grün einzeln nachweisbar ist.

**A. Suchfeld-Montage ohne `index.html`-Änderung (AK-1, N1)**

- **T1 Dynamische Montage:** Harness-DOM mit `#ansicht-uebersicht` → `#filter` (Formular) → `#tabelle`; nach `ladeUebersicht()` existiert genau ein `input#suche-uebersicht` mit `type="search"`, ein `label` mit `for="suche-uebersicht"` und Text „Suche", eingebettet in `div.filter` > `div.filter-feld`. Das Feld steht im DOM **vor** `#tabelle` im selben Elternknoten und **nicht** innerhalb von `#filter` (kein Submit-Pfad, Enter lädt die Seite nicht neu).
- **T2 Idempotenz:** Zweiter Aufruf von `ladeUebersicht()` (Ansichtswechsel hin/zurück) erzeugt **kein** zweites Feld (`Suchelemente == 1`); das bestehende Feld bleibt dasselbe Knotenobjekt, ein bereits eingetippter Wert bleibt erhalten.
- **T3 Alle Listenansichten:** `ANSICHTEN` führt je Ansicht eine Suchfeld-ID (`suche-uebersicht`, `suche-wellen`, `suche-aufgaben`); `ladeWellen()`/`ladeAufgaben()` montieren ihr eigenes Feld und filtern ihre eigenen Daten. Fehlt der Tabellencontainer (`tabelle` nicht im DOM), gibt es keinen Wurf, kein Feld und keinen zusätzlichen Request (`aufrufe` unverändert).
- **T4 Verträge:** `liste.js` enthält als `/api/…`-Vorkommen ausschließlich `/api/overview`, `/api/aufgaben`, `/api/wellen` (kein neuer Endpunkt), kein `innerHTML`/`outerHTML`/`insertAdjacentHTML`/`document.write(`/`eval(`, kein `addEventListener("submit"` (A11-Guard bleibt scharf), aber `textContent` und `classList`. `index.html` enthält **kein** `suche`-Markup und keinen neuen Container; `server.py` bleibt unverändert. (`style.css` ebenfalls unverändert — Wiederverwendung von `.filter`, `.filter-feld`, `.leer`.)

**B. Reine Suchlogik `filtereEintraege(eintraege, { status, owner, suche })` (AK-1, N2)**

- **T5 Einzelbegriff im Titel, case-insensitiv:** Fixture mit Titeln „A23: Feature-Liste", „A11: Listenansicht", „Suche"; Suche `"a23"` → nur die A23-Zeile; Suche `"FEATURE"` → dieselbe Zeile.
- **T6 Feldabdeckung (alle Overview-Felder):** Je ein Suchlauf gegen `path` (`"a11"`), `typ` (`"Welle"`), `status` (`"Klarung"`), `owner` (`"mensch"`), `hinweis` (`"pausiert"`), `welle` (`"w3"`) → jeweils genau die erwarteten Einträge; Suche `"aufgaben/"` trifft alle Aufgabenpfade. (`/api/overview` liefert `path`, `typ`, `titel`, `status`, `owner`, `zuletzt_geaendert`, optional `hinweis` und `welle` — **kein** `description`.)
- **T7 Mehrere Begriffe = UND:** Suche `"a23 umsetzung"` → nur Zeilen, in denen beide Begriffe vorkommen (einer im Titel, einer im Status/Pfad); Reihenfolge bleibt die Eingabereihenfolge; Suche `"a23 gibtsnicht"` → leer.
- **T8 Leerzustand der Suche = Vollbestand:** `suche: ""`, `"   "`, `"\t\n"`, `null`, `undefined` → alle Einträge in Originalreihenfolge (nur getrimmte, nicht-leere Begriffe filtern); Suchergebnis ist nie „alles weg".
- **T9 Groß/Klein, Umlaute, Faltung:** `"Prüfung"` wird von `"prüfung"`, `"PRÜFUNG"` und `"prufung"` gefunden (NFD-Normalisierung + Entfernen kombinierender Zeichen); `"strasse"` findet `"Straße"` (ß→ss); `"uber"` findet `"Über"`; `"a23"` findet `"A23"`.
- **T10 Sonderzeichen und Regex-Zeichen:** Begriffe `"("`, `")"`, `"["`, `"*"`, `"?"`, `"\\"`, `".*"`, `"a23("`, `"^$"` → kein Wurf, keine JS-Exception; Treffer nur **literal** (Vergleich über `includes`, kein `RegExp`): `".*"` findet ausschließlich Zellen, die die Zeichenfolge `.*` enthalten, nicht alle Zellen.
- **T11 Kombination mit Status-/owner-Filter:** `{status: "Klarung", owner: "mensch", suche: "a1"}` → Schnittmenge aller drei Bedingungen; Suche `""` + Filter ergibt exakt das A11-Ergebnis (Regression der Filterlogik); Eingabe-Array wird nicht mutiert (Pfade vor/nach identisch).

**C. Anzeige-/Leerzustand `waehleAnzeige(daten, { status, owner, suche })` (AK-1, N3)**

- **T12 Treffer:** `art: "tabelle"`, `eintraege` entspricht der gefilterten Menge, `text: ""`.
- **T13 Keine Treffer:** Daten vorhanden, Suchbegriff nicht leer, kein Treffer → `art: "leer"` mit Text **exakt** „Keine Treffer." (Punkt am Ende, deutsch).
- **T14 Abgrenzung „Keine Einträge.":** leeres Daten-Array → weiterhin „Keine Einträge."; Filter ohne Treffer **ohne** Suchbegriff → weiterhin „Keine Einträge." (A11-Szenario T7 bleibt wortgleich gültig).
- **T15 Fehler hat Vorrang:** `null` → „Einträge konnten nicht geladen werden."; `{}`/`42`/`"text"` → „Einträge haben ein unerwartetes Format."; in beiden Fällen **nicht** „Keine Treffer.", auch wenn ein Suchbegriff gesetzt ist (fail-loud statt leerer Tabelle).

**D. DOM-Verdrahtung: Live-Filter beim Tippen (AK-1, N2)**

- **T16 Live-Filter ohne Nachladen:** Nach `ladeUebersicht()` mit 4 Fixture-Zeilen: Wert `"a2"` ins Suchfeld setzen, `input`-Ereignis auslösen → Tabelle enthält nur die passenden Zeilen (Zeilenzahl und `data-path` geprüft), Kopfzeile unverändert; `aufrufe` bleibt bei genau einem `GET /api/overview` (kein Request pro Tastendruck, kein Debounce/Timer).
- **T17 Zurücksetzen:** Suchfeld leeren und `input` auslösen → Vollbestand wieder sichtbar; Klick auf `filter-zuruecksetzen` setzt Status, owner **und** Suchfeld-Wert auf leer und zeichnet den Vollbestand.
- **T18 Kombination im DOM:** Suchbegriff `"a1"` + Statusfilter `Klarung` → nur die Schnittmenge; anschließender Statuswechsel lässt den Suchfeld-Wert unverändert und filtert korrekt neu.
- **T19 Leerzustand im DOM:** Suchbegriff ohne Treffer → im `#tabelle`-Bereich steht „Keine Treffer.", keine leere Tabelle, kein Fehlerbereich, keine Exception (fail-loud, aber ohne Fehlalarm).
- **T20 Zusatzblöcke unberührt:** Die Übersichtsblöcke „Zuletzt geändert" (`#uebersicht-zuletzt`) und „Offene Rückfragen" (`#uebersicht-klarung`) werden durch die Suche **nicht** gefiltert (sie zeigen weiter den Gesamtbestand); ein Fehlerzustand färbt sie wie bisher.

**E. Robustheit und XSS (N4)**

- **T21 XSS-Payload als Suchbegriff:** Eingabe `<img src=x onerror=alert(1)>` → kein `img`-/`script`-Knoten im Suchbereich oder in der Tabelle, `alert` wird nicht aufgerufen, der Begriff wird nirgends als Markup ausgegeben; Ergebnis ist „Keine Treffer.".
- **T22 XSS-Payload als Daten:** Eintrag mit Titel `<img src=x onerror=alert(1)>` wird bei Suche `"img"` gefunden und als **Text** gerendert (kein `img`-Knoten, Linktext enthält das Literal) — Suchlogik arbeitet nur auf Strings, nie auf HTML.
- **T23 Fremde/fehlende Feldtypen:** Einträge mit `titel: null`, fehlendem `owner`/`hinweis`, `welle: 3`, `path` fehlend, `status: undefined` → kein Wurf; alle Werte werden für den Vergleich über `String(...)` normalisiert (`null`/`undefined` → `""`), Zahl `3` ist als `"3"` durchsuchbar; keine Zeile verschwindet ohne Suchbegriff.

**F. Regression (N1)**

- **T24 Regression:** `test_liste.py` (54 Fälle), `test_static.py`, `test_detail.py`, `test_projekt.py`, `test_formulare.py` bleiben unverändert grün; `test_features.py` (A23) bleibt grün; die Gesamtsuite wächst nur um `test_suche.py`; `bash definitions/verify.sh .` → Exit 0.

**UI-Szenarien für den `tester` (Moli-Browser, laufende App gegen Test-Bundle):**

- **S1 Suchen:** Übersicht öffnen → Suchfeld über der Tabelle; „a2" tippen → nur passende Zeilen, Zeilenzahl sichtbar reduziert, Kopfzeile unverändert, keine Konsolenfehler.
- **S2 Leeren:** Suchfeld leeren → alle Zeilen wieder da; „Filter zurücksetzen" leert Suche und beide Filter.
- **S3 Kombination:** Suchbegriff + Statusfilter + owner-Filter setzen → Schnittmenge; Filter zurücksetzen → Vollbestand.
- **S4 Kein Treffer:** „xyzgibtsnicht" eingeben → sichtbar „Keine Treffer." (nicht „Keine Einträge."), Seite bleibt bedienbar.
- **S5 Sonderzeichen/XSS:** `.*`, `(` und `<img src=x onerror=alert(1)>` eingeben → keine Exception, kein Dialog, keine kaputte Darstellung.
- **S6 Enter-Taste:** Suchbegriff eingeben und Enter drücken → kein Seiten-Reload, Filterzustand bleibt erhalten (Feld liegt außerhalb des Filterformulars).

# Kontext

- **PM-Festlegungen (2026-11-15, verbindlich):**
  - Die Suche gilt für **alle drei Listen** (Übersicht, Wellen, Aufgaben).
  - Mehrere Wörter sind **UND**-verknüpft (jeder Begriff muss vorkommen).
  - **Umlaut-/ß-Toleranz ist gewollt** (`"prufung"` findet `"Prüfung"`, `"strasse"` findet `"Straße"`).
  - **„zuletzt geändert" ist nicht durchsuchbar** (Datumsrecherche ist nicht Teil der Anforderung).
  - **„Filter zurücksetzen" leert auch die Suche** (Status, owner und Suchfeld).
  - **Phase 2 (Volltextsuche über Dateiinhalte) bleibt Vormerkung** — sie wird erst zur Aufgabe, wenn die Projektleitung sie anfordert; nicht mit der Feldsuche vermischen.
- **Anforderung/Quelle:** Anforderung der Projektleitung („In der Übersicht Liste brauchen wir eine Möglichkeit Suchbegriffe einzugeben um die Aufgaben nach bestimmten Informationen zu durchsuchen"), AK: „Ich gebe in der Suche ein Suchbegriff und mir werden als Ergebnis nur die Aufgaben gezeigt in denen dieser Begriff vorkommt".
- **Umfang Phase 1 (PM-Vorgabe N1): Feldsuche client-seitig.** Kein neuer Server-Endpunkt, keine Änderung an `server.py`/`overview.py`. Datenquelle bleibt der bereits geladene Antwortkörper von `GET /api/overview` (bzw. `/api/aufgaben`, `/api/wellen`).
- **Datenfelder (aus `overview.py` `_eintrag`/`_nicht_lesbarer_eintrag` geprüft):** `path`, `typ`, `titel`, `status` (UI-Status), `owner` (kann `null` sein), `zuletzt_geaendert` (ISO), optional `hinweis` (z. B. „pausiert", „nicht lesbar") und `welle`. **Kein** `description`-Feld im Overview-Ergebnis. Durchsucht werden alle Textfelder inkl. `welle`/`hinweis`/`typ`; „zuletzt geändert" wird **nicht** durchsucht (Datums-/Zeitrecherche liefert unerwartete Treffer und ist nicht Teil der Anforderung — PM-Festlegung 2026-11-15).
- **Umsetzungsentscheidungen (TDD-relevant, reversibel):**
  - Suche läuft in `liste.js` (geteilte Listendarstellung A11) über `filtereEintraege`/`waehleAnzeige`; die Signatur wird **abwärtskompatibel** um `suche` erweitert (Default `""`), damit alle A11-Tests unverändert grün bleiben.
  - Normalisierung: `String(wert)`, `toLowerCase()`, `normalize("NFD")` + Entfernen kombinierender Zeichen (`\p{M}`), `ß`→`ss`. Kein `RegExp` — Vergleich über `includes`, damit Sonderzeichen nicht crashen.
  - Mehrere durch Leerraum getrennte Begriffe = **UND**-Verknüpfung (jeder Begriff muss vorkommen). Getrimmte leere Eingabe = keine Einschränkung.
  - Leerzustand: „Keine Treffer." nur, wenn ein Suchbegriff gesetzt ist und Daten vorhanden sind; sonst bleibt „Keine Einträge." (A11-T7 wortgleich). Fehler-/Formatzustand hat immer Vorrang.
  - Suchfeld wird **dynamisch** vor dem Tabellencontainer eingehängt (`div.filter` > `div.filter-feld` > `label`+`input[type="search"]`, Muster A13-Formularmontage), **außerhalb** des Filterformulars → kein Submit-/Reload-Pfad, kein neues `index.html`-Markup. Montage idempotent, ein Feld je Ansicht (Übersicht, Wellen, Aufgaben — derselbe Code, keine Sonderfälle).
  - Live-Filter über `input`-Ereignis, ohne Debounce (kleine Datenmengen, keine Timer im DOM-Harness). Suche wirkt nur auf die Haupttabelle, nicht auf die Zusatzblöcke „Zuletzt geändert"/„Offene Rückfragen".
  - „Filter zurücksetzen" leert künftig auch das Suchfeld (Konsistenz).
- **Konfliktgruppe und Reihenfolge (PM-Vorgabe):** **G11 „Frontend Suche"** — `static/js/liste.js`, `tests/test_suche.py`. Mit A23 (G10: `features.js`, `app.js`, `index.html`, `style.css`, `test_features.py`) gibt es nach dieser Planung **keine Dateiüberschneidung**; **A25 läuft deshalb parallel zu A23** (PM-Festlegung 2026-11-15). Die ursprüngliche Empfehlung „Umsetzung erst nach Abschluss von A23" ist damit **aufgehoben** — Begründung des PM: die Dateimengen sind disjunkt (G11 vs. G10), eine Serialisierung würde nur Zeit kosten. Vorbehalt: Berührt A23 nachträglich `liste.js`/`test_suche.py` oder A25 `app.js`/`index.html`/`style.css`, wird der betroffene Strang hinter den anderen serialisiert. A24 (`tools/…`, `wissen/`) und A22 (`tests/test_e2e.py`) überschneiden sich nicht.
- **Frontend-Regeln wie A11–A14:** XSS-sicher (`textContent`/`createElement`, keine HTML-Senken), `classList` statt `className`, `getJson`-Wrapper aus `api.js`, fail-loud bei Nicht-Array, deutsche Meldungen ohne Pfade/OS-Details. `style.css` bleibt voraussichtlich unverändert (`.filter`, `.filter-feld`, `.leer` wiederverwendet); falls doch nötig, nur additive Regel → dann Konflikt mit A23 markieren.
- **Teststrategie:** neue Datei `tests/test_suche.py` statt Erweiterung von `test_liste.py` — Begründung: (a) `test_liste.py` ist A11s Regressionstest und bleibt als unveränderte Baseline scharf; (b) A25 braucht erstmals einen DOM-Harness in der Listenthematik (Montage/Live-Filter), `test_liste.py` ist heute rein Node-Logik; (c) `test_features.py` gehört A23 und bleibt unberührt. Der Harness wird aus `test_projekt.py` übernommen (dritte Kopie) und um `parentElement`/`insertBefore` erweitert; der Konsolidierungspunkt [A14-6] (`tests/harness_dom.py`) wird dadurch dringlicher und ist **nicht** Teil dieser Aufgabe. Alle Läufe gegen `tmp_path`-Bundles, nie gegen `wissen/`.
- **Abhängigkeiten:** A8 (`GET /api/overview`, `/api/aufgaben`, `/api/wellen`), A10 (Gerüst, `index.html`, `api.js`), A11 (`liste.js`, Filter-/Leer-/Fehlerlogik), A13 (Muster der dynamischen Formularmontage). A23 ist **keine** Voraussetzung mehr (paralleler Strang, disjunkte Dateimengen — PM-Festlegung 2026-11-15).
- **Umbenennung (ausgeführt 2026-11-15):** Die Datei wurde gemäß Nummerierungskonvention von `wissen/aufgaben/suche.md` nach **`wissen/aufgaben/a25-suche.md`** umbenannt (Inhalt unverändert) und vom `documenter` in `wissen/aufgaben/index.md` (Rubrik „Laufende Aufgaben") sowie in `wissen/features.md` verlinkt. Frontmatter jetzt `task_status: in Umsetzung`, `phase: 3 Umsetzung`.
- **Phase 2 (Vormerkung):** Volltextsuche über Datei-**Inhalte** (`# Ziel`, `# Akzeptanzkriterien`, Ergebnisse) wäre serverseitig (neuer Endpunkt oder erweitertes `/api/overview` mit `text`-Feld). Sie bleibt **Vormerkung** und wird erst zur Aufgabe, wenn die Projektleitung sie anfordert (PM-Festlegung 2026-11-15). Nicht mit der Feldsuche vermischen.
- **Risiken/Grenzen:** (a) Treffer nur in Feldern, die `/api/overview` liefert — Beschreibung/Ziel/Inhalte sind nicht durchsuchbar (Erwartungsmanagement); (b) Umlaut-Faltung ist tolerant, kann aber theoretisch zu Mehrfachtreffern führen (bewusst, dokumentiert); (c) Das DOM wird beim Ansichtswechsel nicht ersetzt (die Sektionen bleiben, nur `hidden` wechselt), trotzdem muss die Montage idempotent sein, falls der Tabellencontainer neu aufgebaut wird — Idempotenztest T2 sichert das ab; (d) ohne Debounce entsteht pro Tastendruck ein Neuzeichnen der Tabelle (unkritisch bei ≤ einigen hundert Dateien, kein Request).

# Betroffene Dateien

- `definitions/app/static/js/liste.js` — Suchlogik (`suche`-Parameter in `filtereEintraege`/`waehleAnzeige`, Normalisierung, `Keine Treffer.`), dynamische Montage des Suchfelds je Ansicht, `input`-Handler, Reset-Erweiterung, Suchfeld-IDs in `ANSICHTEN` (T1–T23).
- `definitions/app/tests/test_suche.py` (neu) — T1–T24 inkl. übernommener MINI_DOM-Harness (erweitert um `parentElement`/`insertBefore`) und Fetch-Stab; Fixtures mit Umlauten, Sonderzeichen, XSS-Payloads, fehlenden Feldern.
- **Nicht geändert:** `definitions/app/static/index.html` (kein neues Markup), `definitions/app/static/js/app.js` (keine neue Registrierung nötig), `definitions/app/server.py`, `definitions/app/overview.py`, `definitions/app/static/style.css` (angestrebt: unverändert), `definitions/app/static/js/api.js`, `features.js`, `detail.js`, `projekt.js`, `formulare.js`, `definitions/app/tests/test_liste.py`.

# Ergebnisse

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-15 — coder (Umsetzung, Stand: in Review)

- **Ergebnis:** `definitions/app/static/js/liste.js` um die Suchlogik erweitert: `filtereEintraege(eintraege, { status, owner, suche })` (Normalisierung über `String(...)`/`toLowerCase()`/NFD + Entfernen kombinierender Zeichen, `ß`→`ss`; mehrere durch Leerraum getrennte Begriffe **UND**-verknüpft; Vergleich **literal** über `includes`, kein `RegExp`; `zuletzt_geaendert` ausgenommen) und `montiereSuche` (dynamisch `div.filter` > `div.filter-feld` > `label` + `input[type="search"]`, **vor** `#tabelle` und **außerhalb** des Filterformulars, idempotent; Suchfeld-IDs `suche-uebersicht`/`suche-wellen`/`suche-aufgaben` je Ansicht). `waehleAnzeige` unterscheidet „Keine Treffer." (Suchbegriff gesetzt, Daten vorhanden) von „Keine Einträge." (leere Daten bzw. Filter ohne Treffer); Fehler-/Formatzustand hat Vorrang; „Filter zurücksetzen" leert Status, owner **und** Suche; Live-Filter über `input`-Ereignis ohne Debounce. `tests/test_suche.py` neu (72 Tests, T1–T24) mit DOM-Harness und Fetch-Stab.
- **PM-Konformität:** alle drei Listen (Übersicht, Wellen, Aufgaben); UND-Verknüpfung; ß→ss + NFD-Faltung; literal statt `RegExp`; „zuletzt geändert" nicht durchsuchbar; Reset leert die Suche; „Keine Treffer." vs. „Keine Einträge." korrekt; Fehlerzustand hat Vorrang; kein neuer Server-Endpunkt, `index.html`/`server.py`/`style.css` unverändert (A10-Vertrag).
- **Belege:** Red-Green-Takt in Blöcken: 39 Tests rot → 0 rot. `test_suche.py` **72 grün**, zusammen mit `test_liste.py` **127 grün** (72+55). Gesamtsuite **936** (Coder-Bericht; `pytest --collect-only` bestätigt 936 Testfälle). `bash definitions/verify.sh .` → Exit 0.
- **Bewusste Grenzen:** kein Volltext über Datei-**Inhalte** oder `description` (Phase 2 bleibt Vormerkung); kein Debounce (Neuzeichnen der Tabelle pro Tastendruck, aber kein Request); Treffer nur in den von `/api/overview` gelieferten Feldern.
- **Offene Punkte:** Moli-Szenarien **S1–S6** beim `tester` offen (Hinweise in der Coder-Rückmeldung). Status **A25 → in Review**; das Review läuft parallel zu A24.

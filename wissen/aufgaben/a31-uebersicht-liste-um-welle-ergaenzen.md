---
type: Task
title: "A31: Übersicht Liste um Welle ergänzen"
description: Als Mensch muss ich in der Lage sein zu sehen zu welcher Welle eine Aufgabe
  zugeordnet ist
task_status: in Doku
phase: 7 Dokumentation
priority: hoch
assigned_to: coder
welle: wellen/w2.md
owner: ai
aktuell: "PM: Review FREIGEGEBEN + S1–S4 bestanden (1156) — reif für Abschluss"
---

# Ziel

Die Projektleitung muss in der Übersichtsliste **zu jeder Aufgabe sehen, ob sie einer Welle zugeordnet ist und welcher**. A27 hat die Daten dafür bereits geschaffen (`welle` im Read-Modell, Wellen-Filter, Wellen-Sicht); es fehlt die **Anzeige in der Tabelle**.

A31 ergänzt eine eigene Spalte **„Welle"** in Übersicht und Aufgabenliste:

1. **Eigene Spalte** statt Badge in der Titel-Zelle: fünf Spalten `Titel | Welle | Status | owner | zuletzt geändert` für die beiden Aufgaben-Ansichten; Wellenliste und Wellen-Detail behalten vier Spalten (dort wäre die Spalte redundant bzw. sinnlos). Die Spalte wird rein in `liste.js` erzeugt — `index.html` bleibt unverändert.
2. **Inhalt:** Wellen-**Titel** (Kurzform), Tooltip = Pfad; ohne Zuordnung dezent „—"; nicht auflösbare/dangling Wellen zeigen den Pfad (fail-loud sichtbar, kein leeres Feld). Kein zusätzlicher Request: die Titel kommen aus den bereits geladenen Daten (Übersicht) bzw. dem A27-Cache.
3. **Keine Backend-Änderung, kein neuer Endpunkt, keine neuen Abhängigkeiten.** A30 (Arbeitsstatus in der Status-Zelle) und A25/A27 (Suche, Filter, Reset) bleiben unberührt und funktionieren kombiniert.

# Akzeptanzkriterien

- **AK-1 (Spalte und Position, PM 1):** In der **Übersichtsliste** und in der **Aufgabenliste** hat die Tabelle fünf Spalten in genau dieser Reihenfolge: `Titel`, `Welle`, `Status`, `owner`, `zuletzt geändert`. Die Spalte wird bedingt je Ansicht erzeugt (`ANSICHTEN`-Konfiguration), nicht global. Die **Wellenliste** behält vier Spalten (keine Wellen-Spalte), ebenso der Abschnitt „Aufgaben dieser Welle" im Wellen-Detail (dort wäre die Angabe für alle Zeilen identisch). Die Spaltenzahl ist über Filterwechsel, Suche, Reset, Leer- und Fehlerzustand **konstant** (kein Springen der Tabelle).
- **AK-2 (Zellinhalt, PM 1):** Zelle „Welle" je Zeile: (a) `welle` vorhanden und Wellen-Titel bekannt → **Titel** (z. B. „W2"), Zell-`title`-Attribut = Pfad (Tooltip, z. B. "wellen/w2.md"); (b) `welle` vorhanden, Titel unbekannt/nicht auflösbar (dangling, Deep-Link ohne Übersichts-Besuch, Welle fehlt im Bestand) → **Pfad** als sichtbarer Fallback (kein leeres Feld); (c) `welle` fehlt, ist leer, `null` oder kein String → **„—"** (dezent, gleiche Konvention wie leere owner-Zelle). Keine Kürzung/Truncation im Code (lange Titel umbrechen im Tabellenlayout).
- **AK-3 (Auflösung ohne Zusatz-Request, PM 1):** Die Titel werden aus den bereits geladenen Listen abgeleitet: Wellen-Einträge im `/api/overview`-Payload (Übersicht) plus der bestehende A27-Cache `bekannteWellen` (Aufgabenliste). Es entsteht **kein** zusätzlicher Request (insbesondere kein `GET /api/wellen` in `ladeUebersicht`/`ladeAufgaben`); die A25-Request-Zusicherungen bleiben unverändert.
- **AK-4 (Robustheit, PM 1):** Fehlende/falsch typisierte Felder (`welle: null`, `42`, `{}`, `[]`), ein leerer String, eine unbekannte Welle und ein fehlender `titel` der Welle führen zu keiner Exception und zu keiner falschen Zuordnung; die Zeile bleibt sichtbar, die Zelle zeigt „—" bzw. den Pfad. `null`/Nicht-Array-Antworten behalten das bestehende Fehler-/Formatverhalten (A11/A25), ohne Tabellenaufbau.
- **AK-5 (Sicherheit/XSS, PM 1):** Wellen-Titel und -Pfade werden ausschließlich über `textContent`/`createElement` gerendert (kein `innerHTML`, kein `insertAdjacentHTML`, kein `eval`); Klassen nur über `classList`. Ein Titel wie `<img src=x onerror=alert(1)>` erscheint als Text, erzeugt keinen `img`-Knoten und keinen Dialog; ein Pfad mit `<script>` ebenfalls nicht.
- **AK-6 (Kombination mit A30, A25, A27, PM 2):** Der Arbeitsstatus aus A30 bleibt in der **Status-Zelle** (zweite Zeile, z. B. „Coder: Umsetzung Paket 2"); die Welle steht ausschließlich in der neuen Spalte — keine Doppelanzeige, keine Verschiebung der A30-Anzeige. Der A27-Wellen-Filter, der A11-Status-/owner-Filter und die A25-Suche filtern weiterhin auf denselben Daten und in derselben Reihenfolge; „Filter zurücksetzen" leert alle Filter und zeichnet die Tabelle mit unveränderter Spaltenzahl. Die Wellen-Sicht (A27) und das Wellen-Dropdown (A27) bleiben unverändert.
- **AK-7 (Grenzen, alle):** Keine Änderung an `overview.py`, `meta.py`, `server.py`, `okf_bundle.py`, `status.py`, `neu_aufgabe.py`, `neu_welle.py`; kein neuer Endpunkt, keine neue Route, keine neue Abhängigkeit. `index.html` (eingefroren seit A10) und `style.css` bleiben unverändert; die Spalte entsteht dynamisch in `liste.js`. Keine neuen Filter-IDs, kein neues Markup in `index.html`, kein Schreibpfad für `welle` (Zuordnung bleibt A27).
- **AK-8 (Bewusster Vertragswechsel dokumentiert, PM 2):** Die frühere Vier-Spalten-Erwartung (A11/A25/A27) wird für Übersicht/Aufgabenliste **auf fünf Spalten** geändert. Die betroffenen Baseline-Erwartungen werden im selben Paket angepasst (nur die Kopfzeilen-Listen, keine Testlogik): `tests/test_suche.py` (T16, Übersicht), `tests/test_welle_zuordnung.py` (T31, Übersicht) und die A30-Datei `tests/test_arbeitsstand_ui.py` (T15/T17). **Unverändert vier Spalten** bleiben `tests/test_welle_zuordnung.py` T34 (Wellen-Detail) und die Wellenliste. Der Wechsel ist in der Aufgaben-Datei und im Commit begründet (Nutzerwunsch „zu welcher Welle" vor Tabellenkonvention).
- **AK-9 (Regression, PM 3):** `test_liste.py`, `test_detail.py`, `test_formulare.py`, `test_features.py`, `test_static.py`, `test_api_lesen.py`, `test_api_schreiben.py`, `test_meta.py`, `test_neu_aufgabe.py`, `test_neu_welle.py` bleiben unverändert grün; die Suite wächst nur um `tests/test_welle_spalte.py`; `bash definitions/verify.sh .` → Exit 0.

# Testfälle (TDD)

**Zuordnung AK → Testfälle:**
**AK-1** → T1–T5. **AK-2** → T6–T9, T12, T13. **AK-3** → T10, T11, T17. **AK-4** → T9, T16. **AK-5** → T14. **AK-6** → T15, T18. **AK-7** → T20. **AK-8** → T19, T22. **AK-9** → T21.

Reihenfolge = Red-Green-Takt: erst Test schreiben, rot laufen lassen, dann das Minimum implementieren, dann refaktorisieren. Jede Testnummer ist ein eigener pytest-Fall. Neue Datei `tests/test_welle_spalte.py`; sie nutzt den Harness `tests/dom_helfer.py` (in A30 angelegt) und das Seiten-/Fetch-Gerüst aus `test_arbeitsstand_ui.py` (A30) bzw. eine eigene, minimale Kopie des Gerüsts (kein Eingriff in A30s Testlogik außer den in AK-8 genannten Kopfzeilen-Erwartungen). Zusätzliche Fixtures werden im Test unter `tmp_path` erzeugt; alle API-Läufe gegen das `bundle`-Fixture.

**A. Spalte und Grundanzeige (AK-1, AK-2, AK-4)**

- **T1 Übersicht: fünf Spalten:** `ladeUebersicht()` mit zwei Aufgaben (eine mit `welle`, eine ohne) + Wellen-Eintrag → Kopfzeile exakt `["Titel", "Welle", "Status", "owner", "zuletzt geändert"]`; Reihenfolge der Zellen entspricht dem Kopf (Welle an Position 2); `data-path` unverändert.
- **T2 Aufgabenliste: fünf Spalten:** `ladeAufgaben()` → derselbe Kopf und dieselbe Zellreihenfolge; Aufgabe mit Welle zeigt den Titel, Aufgabe ohne zeigt „—".
- **T3 Wellenliste: vier Spalten:** `ladeWellen()` → Kopf exakt `["Titel", "Status", "owner", "zuletzt geändert"]`, **keine** Welle-Zelle, `data-path`/Sortierung unverändert (A27-Regression).
- **T4 Wellen-Detail: vier Spalten:** `ladeDetail({unterpunkt: "wellen/w1.md"})` → Abschnitt „Aufgaben dieser Welle" mit vier Spalten (keine redundante Wellen-Spalte), Treffer/`data-path` unverändert (A27-T34 bleibt grün).
- **T5 Konstanz:** Übersicht und Aufgabenliste behalten fünf Spalten nach Filterwechsel, Suche, „Filter zurücksetzen", leerem Ergebnis und Fehlerzustand; die Wellenliste bleibt bei vier; die Konfiguration ist je Ansicht getrennt (kein globales Umschalten).
- **T6 Anzeige mit Titel:** Welle `wellen/w2.md` mit `titel: "W2"` im Payload → Zelle zeigt `"W2"`, Zell-`title` = `"wellen/w2.md"`; kein Pfad im sichtbaren Text, kein Badge in der Titel-Zelle.
- **T7 Mehrere Zuordnungen:** drei Aufgaben mit drei verschiedenen Wellen (Titel „W1", „W2", ohne Titel → Pfad) → jede Zeile zeigt genau ihre Welle; keine Vermischung; Zeilenreihenfolge unverändert.
- **T8 Ohne Zuordnung:** `welle` fehlt/`""`/`null` → Zelle zeigt exakt „—" (kein leerer String, kein „keine Welle"); die übrigen Zellen der Zeile bleiben unverändert.
- **T9 Falsche Typen/Leerzeichen:** `welle: 42`, `{}`, `[]`, `"   "` → „—" ohne Wurf; `welle: " wellen/w2.md "` (mit Leerzeichen) → Titel „W2" (getrimmt), keine Dublette.

**B. Auflösung und Fallbacks (AK-2, AK-3)**

- **T10 Dangling-Welle:** `welle: "wellen/geloescht.md"` (nicht im Payload) → Zelle zeigt den Pfad `"wellen/geloescht.md"`, `title`-Attribut fehlt oder ist der Pfad, kein Wurf, kein leerer Platz.
- **T11 Deep-Link aufgaben:** `ladeAufgaben()` **ohne** vorherige Übersicht (Cache leer) → Zelle zeigt den Pfad der referenzierten Welle; Request-Zähler = 1 (`/api/aufgaben`), **kein** `/api/wellen`; nach einem Übersichts-Besuch und erneutem Laden zeigt dieselbe Zelle den Titel (Cache-Nutzung).
- **T12 Welle ohne Titel:** Wellen-Eintrag mit `path`, aber ohne `titel` → Zelle zeigt den Pfad; mit Titel → Titel (kein `Titel (Pfad)` im sichtbaren Text).
- **T13 Lange Titel:** Wellen-Titel mit 120 Zeichen → vollständig als `textContent` (keine Kürzung im Code), kein Wurf, keine Änderung der Spaltenzahl.

**C. Sicherheit (AK-5)**

- **T14 XSS:** Wellen-Titel `<img src=x onerror=alert(1)>` → als Text in der Zelle, kein `img`-Knoten, kein `alert`; dangling Pfad `<script>alert(1)</script>` → als Text; `liste.js` enthält weiterhin kein `innerHTML`/`insertAdjacentHTML`/`eval(`.

**D. Kombination und Regression (AK-6, AK-8, AK-9)**

- **T15 A30-Kombination:** Aufgabe mit `arbeitsrolle_label: "Coder"`, `arbeitsstatus: "Umsetzung Paket 2"` und `welle: "wellen/w2.md"` → Status-Zelle enthält „Coder: Umsetzung Paket 2", Welle-Zelle zeigt „W2"; beide Angaben genau einmal; Status-Zelle enthält **nicht** die Welle, Welle-Zelle **nicht** den Arbeitsstatus.
- **T16 Fehler-/Leerzustand:** `/api/overview` `null` → Fehlermeldung, keine Tabelle; `{}`/`42` → Formatmeldung; leeres Array → „Keine Einträge."; in keinem Fall eine halb aufgebaute Tabelle oder ein Wurf (A11/A25-Verhalten unverändert).
- **T17 Request-Budget:** `ladeUebersicht()`/`ladeAufgaben()`/`ladeWellen()` je genau ein Request; Detail-Aufgabe nur `/api/file` (+ `/api/wellen` aus A27); kein Request für die Wellen-Spalte.
- **T18 Filter/Suche/Reset:** A27-Wellen-Filter + Status + owner + Suche (A25) filtern unverändert (Schnittmenge, Reihenfolge); nach Reset Vollbestand, fünf Spalten; Wellen-Spalte zeigt weiterhin die korrekten Titel (Map bleibt gefüllt); die Suche findet weiterhin nur die bisherigen Felder (kein Treffer allein über den Wellen-Titel).
- **T19 Baseline-Anpassung (AK-8):** `test_suche.py` T16 und `test_welle_zuordnung.py` T31 erwarten `["Titel", "Welle", "Status", "owner", "zuletzt geändert"]`; `test_arbeitsstand_ui.py` T15/T17 ebenso; `test_welle_zuordnung.py` T34 bleibt bei vier Spalten. Nachweis: die Tests sind vor der Implementierung rot (neue Erwartung vs. alter Code) und danach grün.
- **T20 Grenzen:** `git diff --stat` zeigt keine Änderung an `static/index.html`, `static/style.css`, `static/js/app.js`, `static/js/api.js`, `static/js/detail.js`, `overview.py`, `server.py`, `meta.py`, `okf_bundle.py`, `status.py`; `index.html` enthält kein `Welle`-Spalten-Markup; keine neue Abhängigkeit.
- **T21 Baselines:** `test_liste.py`, `test_detail.py`, `test_formulare.py`, `test_features.py`, `test_static.py`, `test_api_lesen.py`, `test_api_schreiben.py`, `test_meta.py`, `test_neu_aufgabe.py`, `test_neu_welle.py` unverändert grün; Gesamtsuite grün; `bash definitions/verify.sh .` → Exit 0.
- **T22 Vertragswechsel (Review-Prüfschritt, kein pytest):** Die Aufgaben-Datei und der Commit begründen die vierte→fünfte Spalte (Nutzerwunsch vor A11-Konvention); `wissen/projekt/technische-spec.md`/`phasen.md` definieren keine Tabellenspalten und bleiben unverändert; `features.md`/`log.md` pflegt der PM. Nachweis im Review-Ergebnis mit Zitatstelle.

**UI-Szenarien für den `tester` (Moli-Browser, laufende App gegen Test-Bundle):**

- **S1 Übersicht:** Aufgaben mit/ohne Welle → Spalte „Welle" zeigt „W2" bzw. „—"; Hover über „W2" zeigt `wellen/w2.md`; keine Konsolenfehler.
- **S2 Aufgabenliste:** gleiche Darstellung; Wellenliste zeigt weiterhin vier Spalten; Wellen-Detail listet Aufgaben mit vier Spalten.
- **S3 Kombination:** Wellen-Filter „W2" + Suche/Status → nur passende Zeilen, Spalte zeigt weiterhin „W2"; „Filter zurücksetzen" → Vollbestand, fünf Spalten.
- **S4 Grenzfälle:** Aufgabe auf `wellen/gibtsnicht.md` setzen (per Netzwerk/Fixture) → Spalte zeigt den Pfad, kein Absturz; Welle mit HTML-Titel → nur Text; Aufgabe ohne Welle → „—"; sehr langer Wellen-Titel → Umbruch, keine Layout-Fehler.

# Kontext

- **Anforderung (Projektleitung, 2026-11-15):** „Als Mensch muss ich in der Lage sein zu sehen, zu welcher Welle eine Aufgabe zugeordnet ist." AK wörtlich: „In der Übersichtsliste sehe ich zu jeder Aufgabe, ob sie eine Welle zugeordnet ist und welche."
- **Welle:** [w2](wellen/w2.md) — A31 ist Welle 2 zugeordnet (Wellen-Freigabe A29 kommt erst nach A28).
- **Grundlage/Prüfung:** A27 (Commit `a4906d7`) liefert `welle` bereits in `/api/overview` und `/api/aufgaben` (getrimmter String, Feld fehlt ohne Zuordnung) sowie `Titel (Pfad)`-Optionen für den Filter. Damit ist A31 **rein frontend-seitig** in `liste.js` — kein neuer Endpunkt, keine Änderung an `overview.py` (geprüft: `_eintrag` unverändert nötig).
- **Entscheidung „eigene Spalte" (mit Begründung):**
  - **Lesbarkeit:** „zu welcher Welle" ist eine eigene Dimension und wird als Spalte scanbar; ein Badge in der Titel-Zelle würde diese mit dem Aufgabentitel und (ab A28) der „neu"-Marke überladen, lange Wellen-Titel würden als riesige Pille umbrechen.
  - **A30-Konflikt:** A30 legt den Arbeitsstatus als zweite Zeile in die **Status-Zelle**; eine Wellen-Marke in der Titel-Zelle wäre die dritte Information in einer Zeile. Die Spalte trennt die Belange sauber: Titel(+neu) | Welle | Status(+Rolle) | owner | Zeit.
  - **A25/A27-Vertrag:** Die Vier-Spalten-Konvention war eine Test-/Design-Vereinbarung, kein Nutzerbedürfnis; die PM-Vorgabe stellt sie ausdrücklich hinter den Nutzerwunsch. Der Wechsel wird bewusst und dokumentiert vollzogen (AK-8), betroffen sind genau drei Kopfzeilen-Erwartungen.
  - **`index.html` eingefroren:** Die Spalte entsteht in `liste.js` (Kopf + Zellen), kein neues Markup, keine `style.css`-Änderung (bestehende Tabellenklassen).
  - **Alternative (verworfen):** Badge in der Titel-Zelle (Testaufwand geringer, aber schlechter lesbar und Kollision mit A28), zusätzliche Zeile in der Status-Zelle (vermischt Welle und Arbeitsstatus), neue Detail-/Listen-Route (unnötig, `index.html`/`app.js`).
- **Anzeigeformat:** **Titel** (Kurzform) mit Pfad im Tooltip statt `Titel (Pfad)` im Zelltext. Begründung: Eine Spalte mit doppeltem Text wird breit und unruhig; der Pfad ist über Hover und im Detail erreichbar, der Titel ist die menschlich relevante Bezeichnung. Bei nicht auflösbarem Titel ist der **Pfad** der sichtbare Fallback (fail-loud, nie leer) — das deckt dangling-Verweise und den Deep-Link-Fall ab. *Offene Frage:* `Titel (Pfad)` auch im Zelltext (Standard: nein).
- **Konsistenz Aufgabenliste:** Ja, dieselbe Spalte und dieselbe Funktion, weil Übersicht und Aufgabenliste `erstelleTabelle`/`waehleAnzeige` teilen — eine unterschiedliche Darstellung wäre inkonsistent und würde zwei Codepfade erzeugen. Die **Wellenliste** bleibt bei vier Spalten (die Welle einer Welle ist bedeutungslos), der **Wellen-Detail**-Abschnitt ebenfalls (alle Zeilen gehören per Definition zu dieser Welle).
- **Ist-Stand im Code (geprüft 2026-11-15, nach A27-Commit `a4906d7`):**
  - `liste.js`: `SPALTEN = ["Titel","Status","owner","zuletzt geändert"]`, `erstelleTabelle(eintraege)` baut Kopf und Zeilen; `ANSICHTEN` konfiguriert je Ansicht `tabelle`/`formular`/`status`/`owner`/`welle`/`suche`/`zuruecksetzen`; `bekannteWellen` cached Wellen aus der Übersicht, `ermittleWellen`/`fuehreWellenZusammen`/`wellenAusVerweisen` lösen Pfade/Titel auf, `montiereWellenFilter` wird je Ansicht in `ladeListe` aufgerufen.
  - `detail.js`: nutzt `erstelleTabelle` für den Abschnitt „Aufgaben dieser Welle" (Aufruf ohne Option → vier Spalten, bleibt so).
  - `test_suche.py` T16, `test_welle_zuordnung.py` T31/T34 prüfen Kopfzeilen; `test_arbeitsstand_ui.py` (A30, geplant) prüft vier Spalten in T15/T17.
  - `overview._eintrag` liefert `welle` bereits; `overview.details` ist für A31 irrelevant.
- **Umsetzungsentscheidungen (TDD-relevant, reversibel):**
  - **Spaltenkonfiguration je Ansicht** in `ANSICHTEN` (z. B. `welleSpalte: true` für `uebersicht`/`aufgaben`, `false` für `wellen`), nicht global und nicht datenabhängig (sonst springt die Spaltenzahl bei Filtern).
  - **`erstelleTabelle(eintraege, { mitWelle = false } = {})`** als rückwärtskompatible Signaturerweiterung; `detail.js` bleibt ohne Angabe (vier Spalten). Alle Aufrufstellen in `liste.js` (`wendeFilterAn`, Top-5 in `zeichneUebersichtZusatz`) übergeben die Ansichts-Konfiguration.
  - **Wellen-Titel-Map** `wellenTitel` (Pfad → Titel) wird in `ladeListe`/`ermittleWellen` aus Payload + `bekannteWellen` gefüllt; `erstelleWelleZelle` liest nur die Map und fällt auf den Pfad zurück. Kein Modul-Zustand, der einen zusätzlichen Request braucht.
  - **Zelle „—" für leere Werte** statt „keine Welle": konsistent mit der bestehenden leeren owner-Zelle, dezent und ohne neue Vokabel.
  - **Kein Link in der Zelle:** Zeilenklick (`data-path`) bleibt der einzige Navigationsweg; ein Link in der Zelle würde die Klick-Delegation (`app.js`) überlagern und zusätzliche Tests erfordern (Follow-up, falls gewünscht).
  - **Keine Suche-Erweiterung:** `SUCHFELDER` bleibt unverändert; der Wellen-**Titel** ist nicht durchsuchbar (nur der Pfad, wie bisher). A25 bleibt unberührt.
  - **Test-Harness:** `tests/dom_helfer.py` (A30) wiederverwenden; keine neue Kopie.
- **Konfliktgruppe (neu):** **G24 „Wellen-Spalte (Liste)":** `static/js/liste.js`, `tests/test_welle_spalte.py` (neu), `tests/test_suche.py` (T16-Kopfzeile), `tests/test_welle_zuordnung.py` (T31-Kopfzeile), `tests/test_arbeitsstand_ui.py` (T15/T17-Kopfzeile, A30-Datei). **Überschneidet sich mit A30-G22 (`liste.js`) und A28-G16 (`liste.js`)** → strikt nach A30, vor A28. `detail.js` bleibt unberührt (kein A27-/A28-Konflikt dort).
- **Aufteilung in Pakete (ein Coder, eine Aufgabe):**
  - **Paket 1 — Spalte, Kopf, Grundzelle:** `ANSICHTEN.welleSpalte`, `erstelleTabelle`-Option, fünf Spalten für Übersicht/Aufgaben, „—" ohne Welle, vier Spalten für Wellenliste/Detail; die drei Baseline-Kopfzeilen-Erwartungen (T19) werden **im selben Takt** auf fünf gesetzt. Tests: T1–T5, T8, T16, T19.
  - **Paket 2 — Auflösung:** `wellenTitel`-Map, `erstelleWelleZelle` mit Titel/Tooltip/Pfad-Fallback, Anbindung an `ermittleWellen`. Tests: T6, T7, T9–T13.
  - **Paket 3 — Kombination/Regression:** A30-Kombination, Filter/Suche/Reset, Request-Budget, Grenzen. Tests: T14, T15, T17, T18, T20–T22. (Falls T14/T18 grün bleiben, ist das Paket ein reiner Nachweis; gefundene Fehler werden hier behoben.)
  - **Reihenfolge im Paket:** Test → rot → Minimum → grün. Paket 1 vor Paket 2 (ohne Titel-Map zeigt die Zelle zunächst den Pfad, dann den Titel); Paket 3 nach 2.
- **Reihenfolge-Empfehlung (inkl. A30-Koppelung):**
  1. **A30 abschließen** (Code + Tests committed; A30 ist die G22-Belegung für `liste.js`). A31 startet, sobald A30 committed ist — A30 darf parallel im Review sein, solange derselbe Coder beide Aufgaben hat (Rückläufer aus dem A30-Review werden vor A31 eingearbeitet).
  2. **Empfehlung: ein Coder, zwei Takte, getrennte Commits** — A30 zuerst vollständig, dann A31. Begründung: gleiche Datei `liste.js`, gleicher Harness, A31 ändert zwei A30-Test-Erwartungen (Kopfzeile) und baut auf den A30-Feldern auf; ein Coder vermeidet Merge-Konflikte und doppelte Einarbeitung. Zwei Reviewer-/Tester-Runden bleiben getrennt (A30-Review bewertet Arbeitsstatus, A31-Review die Wellen-Spalte).
  3. **Danach A28 → A29** (A28-G16 nutzt `liste.js` weiter; die Welle-Spalte bleibt unverändert, die „neu"-Marke sitzt in der Titel-Zelle).
  4. **Freigabe-Gate:** A31 ist laut Auftrag priorisiert (`priority: hoch`); ein `freigabe`-Feld gibt es erst mit A28. Für A31 gilt die dokumentierte PM-Freigabe als Gate; Startbedingung ist der A30-Commit. Ohne A30 darf A31 **nicht** starten (G22).
- **Abhängigkeiten:** A11 (`erstelleTabelle`, Status-/owner-Zellen), A25 (Suche, Request-Zusicherungen), A27 (Pflicht: `welle` im Read-Modell, `bekannteWellen`/`ermittleWellen`, Wellen-Filter), A30 (Pflicht: `liste.js`-Stand, `dom_helfer.py`, `test_arbeitsstand_ui.py`). A28/A29 sind keine Voraussetzungen.
- **Risiken/Grenzen:** (a) Deep-Link auf `#/aufgaben` ohne Übersichts-Besuch zeigt Pfade statt Titel (A27-Cache-Limitierung, dokumentiert; kein Extra-Request wegen A25-Request-Zusicherungen); (b) doppelte Wellen-Titel sind in der Spalte nicht unterscheidbar (Tooltip = Pfad); (c) die Spalte macht die Tabelle breiter — auf schmalen Displays umbrechen Titel/Welle (kein `style.css`-Eingriff); (d) drei Baseline-Erwartungen werden bewusst geändert — Review muss den Vertragswechsel bestätigen (T22); (e) die Suche findet den Wellen-Titel nicht (nur den Pfad) — Erwartungsmanagement.
- **Offene Fragen an den PM (Standardentscheidung in Klammern, nicht blockierend):**
  1. Zelltext `Titel (Pfad)` statt nur `Titel`? *(Standard: nur Titel, Pfad im Tooltip.)*
  2. Wellen-Zelle als Link zum Wellen-Detail? *(Standard: nein — Zeilenklick bleibt der Weg; Follow-up möglich.)*
  3. Spalte auch in der Wellenliste/Wellen-Detail? *(Standard: nein — redundant.)*
  4. Wellen-Titel durchsuchbar machen (A25)? *(Standard: nein — eigene Aufgabe.)*
  5. Spaltenreihenfolge `Titel | Welle | Status | …`? *(Standard: ja — Welle direkt neben dem Titel; alternativ ans Ende vor „zuletzt geändert".)*

# Betroffene Dateien

- `definitions/app/static/js/liste.js` — `ANSICHTEN` um `welleSpalte` ergänzen (`uebersicht`/`aufgaben: true`, `wellen: false`); `WELLE_SPALTE`/Spaltenliste je Ansicht; `erstelleTabelle(eintraege, { mitWelle = false })` mit fünf Spalten und Zellenreihenfolge `Titel, Welle, Status, owner, zuletzt geändert`; `erstelleWelleZelle` (Titel, Tooltip = Pfad, „—", Pfad-Fallback); `wellenTitel`-Map aus `ermittleWellen`/`bekannteWellen`; Aufrufstellen `wendeFilterAn` (Haupttabelle) und `zeichneTabelle`/`zeichneUebersichtZusatz` (Top 5) übergeben die Option (T1–T14, T18).
- `definitions/app/tests/test_welle_spalte.py` (**neu**) — T1–T18, T20–T22 inkl. Seiten-/Fetch-Gerüst (Harness `dom_helfer.py`).
- `definitions/app/tests/test_suche.py` — **nur** T16-Kopfzeilen-Erwartung auf fünf Spalten (T19, bewusster Vertragswechsel).
- `definitions/app/tests/test_welle_zuordnung.py` — **nur** T31-Kopfzeilen-Erwartung auf fünf Spalten; T34 (Wellen-Detail) bleibt vier (T19).
- `definitions/app/tests/test_arbeitsstand_ui.py` — **nur** die Kopfzeilen-Erwartungen in T15/T17 auf fünf Spalten (A30-Datei, T19).
- `definitions/app/tests/dom_helfer.py` — **wird genutzt, nicht geändert** (in A30 angelegt).
- **Nicht geändert:** `definitions/app/static/index.html` (eingefroren seit A10), `static/style.css`, `static/js/app.js`, `static/js/api.js`, `static/js/detail.js`, `static/js/formulare.js`, `static/js/features.js`, `static/js/projekt.js`, `definitions/app/overview.py`, `server.py`, `meta.py`, `okf_bundle.py`, `status.py`, `neu_aufgabe.py`, `neu_welle.py`, `definitions/app/tests/test_liste.py`, `test_detail.py`, `test_formulare.py`, `test_features.py`, `test_static.py`, `test_api_lesen.py`, `test_api_schreiben.py`, `test_meta.py`, `test_neu_aufgabe.py`, `test_neu_welle.py`, `wissen/projekt/phasen.md`, `wissen/projekt/technische-spec.md` (definieren keine Tabellenspalten).

# Ergebnisse

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-15 — coder (Umsetzung Paket 1 + 2 + 3)

- **Ergebnis Paket 1 (Spalte und Grundzeile):** `liste.js` — `WELLE_SPALTE = "Welle"`, `ANSICHTEN[...].welleSpalte` (`uebersicht`/`aufgaben: true`, `wellen: false`), `spaltenFuer(mitWelle)` und `erstelleTabelle(eintraege, { mitWelle = false })` mit der Reihenfolge `Titel | Welle | Status | owner | zuletzt geändert`; `erstelleWelleZelle` zeigt „—" ohne Zuordnung. Aufrufstellen übergeben die Ansichts-Konfiguration: `wendeFilterAn` (Haupttabelle) und `zeichneUebersichtZusatz`/`zeichneTabelle` (Top 5). `detail.js` ruft ohne Option → Wellen-Detail und Wellenliste bleiben bei vier Spalten. **Bewusster Vertragswechsel (AK-8):** `test_suche.py` (T16), `test_welle_zuordnung.py` (T31) und `test_arbeitsstand_ui.py` (T15) erwarten jetzt fünf Spalten; `test_welle_zuordnung.py` T34 bleibt vier. Begründung: Der Nutzerwunsch „zu welcher Welle" wiegt schwerer als die A11-Tabellenkonvention; eine Badge-Lösung in der Titel-Zelle würde mit A28 („neu"-Marke) kollidieren, eine zweite Zeile in der Status-Zelle mit A30.
- **Ergebnis Paket 2 (Auflösung):** `wellenTitel`-Map (Pfad → Titel) wird in `ermittleWellen`/`merkeWellenTitel` aus dem `/api/overview`-Payload bzw. dem A27-Cache `bekannteWellen` gefüllt (Übersicht baut neu auf, Aufgabenliste ergänzt) — **kein zusätzlicher Request**. Zelle: Titel sichtbar, `title`-Attribut = Pfad; ohne Titel (dangling, Deep-Link, Welle ohne `titel`) steht der Pfad als sichtbarer Fallback; ohne/ungültige Zuordnung (`null`, `42`, `{}`, `[]`, `"   "`) „—"; getrimmte Pfade.
- **Ergebnis Paket 3 (Kombination/Regression):** XSS-Payloads werden textuell gerendert (kein `img`/`script`, kein `alert`), A30-Arbeitsstatus bleibt allein in der Status-Zelle (keine Doppelanzeige), Request-Budget unverändert (je Ansicht ein Request, Detail-Aufgabe `/api/file` + `/api/wellen`), A27-Wellen-Filter + Status + owner + A25-Suche filtern unverändert (Schnittmenge), „Filter zurücksetzen" liefert den Vollbestand mit fünf Spalten und weiterhin aufgelösten Titeln, der Wellen-Titel ist nicht durchsuchbar (nur der Pfad).
- **Belege:** TDD-Red-Green je Paket. Paket 1: **8 rot** (T1, T2, T3, T5, T8, `test_suche` T16, A30 T15/T16) → 0. Paket 2: **6 rot** (T6, T7, T9, T11, T12, T13) → 0. Paket 3: **3 rot** (eigene Test-Autorenfehler: fehlende XSS-Konstante, Zeilenfilter über Aufgaben, Navigationslink „Wellen" in `index.html`) → 0. `test_welle_spalte.py` neu mit **24 Fällen** (T1–T21; T16 vierfach parametrisiert; T22 ist Review-Schritt). A31-relevante Dateien serialisiert (`test_welle_spalte`, `test_suche`, `test_welle_zuordnung`, `test_arbeitsstand_ui`, `test_arbeitsstand`, `test_liste`, `test_detail`, `test_features`, `test_static`, `test_formulare`, `test_api_lesen`, `test_api_schreiben`, `test_meta`, `test_neu_aufgabe`, `test_neu_welle`): **877 passed**. Gesamtsuite serialisiert (`python3 -m pytest definitions/app/tests -q -p no:randomly`): **1168 passed, 0 failed** (9:38 unter Parallel-Last).
- **Bewusste Abweichungen/Grenzen:** (1) `test_arbeitsstand_ui.py` T15/T16 mussten neben der Kopfzeile auch die **Zellindizes** um +1 verschieben (Status jetzt Index 2, owner 3) — reine Folge des Spaltenwechsels, keine Logikänderung; die Testlogik bleibt inhaltlich identisch. (2) `T21` ist als pytest-Fall umgesetzt, der prüft, dass die zehn Baseline-Dateien keine A31-Marker enthalten (die eigentliche Suite-/`verify.sh`-Ausführung steht im Lauf oben bzw. beim `tester`). (3) `T22` bleibt Review-Schritt (Begründung siehe Paket 1, `phasen.md`/`technische-spec.md` definieren keine Tabellenspalten und bleiben unverändert). (4) Deep-Link auf `#/aufgaben` ohne Übersichts-Besuch zeigt Pfade statt Titel (A27-Cache-Grenze, bewusst kein Extra-Request wegen der A25-Request-Zusicherungen).
- **Offene Punkte:** Moli-Szenarien **S1–S4** (tester); `bash definitions/verify.sh .` nicht separat gelaufen (Parallelbetrieb A26/A32); A28 **nicht** begonnen. Keine Commits.


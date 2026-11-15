---
type: Task
title: "A30: Was passiert gerade"
description: Wenn ich die Übersicht Liste Aufrufe und den Status "in Arbeit" sehe
  ich die Aufgaben die im Moment von dir bearbeitet werden, allerdings weiß ich nicht
  wo wir…
task_status: in Doku
phase: 7 Dokumentation
priority: hoch
assigned_to: coder
welle: wellen/w2.md
owner: ai
aktuell: "PM: Review FREIGEGEBEN + S1–S4 bestanden — reif für Abschluss"
---

# Ziel

Der Projektleitung fehlt in der Übersichtsliste die Information, **wo wir uns gerade befinden**: Bei Aufgaben mit dem Status „In Arbeit" ist zwar sichtbar, *dass* gearbeitet wird, aber nicht, *welche Rolle* gerade arbeitet (Planer, Coder, Tester, Review, Documenter) und *was* sie tut.

A30 macht den **Arbeitsstatus** sichtbar, ohne eine zweite Datenquelle zu schaffen:

1. **Ableitung aus `aktuell`:** Das im Frontmatter bereits gepflegte Feld `aktuell: "<Rolle>: <Was passiert gerade>"` (PM-Regel „Live-Arbeitsstand pflegen") wird serverseitig in normalisierte Rolle + Text zerlegt und im Read-Modell (`/api/overview`, `/api/aufgaben`, `/api/file`) ausgeliefert. Kein neues Frontmatter-Feld, keine Doppelpflege, keine Schreiblogik.
2. **Anzeige:** In Übersicht und Aufgabenliste erscheint der Arbeitsstatus in der **Status-Zelle** (unter „In Arbeit") als Zeile „Coder: Umsetzung Paket 2"; im Detail als `dl`-Feld „Arbeitsstatus". Fehlt/leert `aktuell`, gibt es keine Anzeige und keinen Fehler.
3. **Grenzen:** keine neue Spalte (A11/A25/A27-Vertrag), `index.html` bleibt eingefroren, `style.css` unverändert, keine neuen Abhängigkeiten, keine neuen Endpunkte.

# Akzeptanzkriterien

- **AK-1 (Ableitung und Normalisierung, PM 1):** Nur Aufgaben (`typ == "Task"`) mit nicht-leerem `aktuell` als String erhalten abgeleitete Felder. Regeln: Wert trimmen und interne Leerraumfolgen (inkl. Zeilenumbrüche) zu einem Leerzeichen zusammenfassen; am **ersten** Doppelpunkt trennen; Rolle getrimmt, **case-insensitiv** normalisiert; bekannte Rollen: `planner`/`planer` → `planner` („Planer"), `coder` → `coder` („Coder"), `tester` → `tester` („Tester"), `reviewer`/`review` → `reviewer` („Review"), `documenter`/`doku` → `documenter` („Documenter"), `pm`/`projektmanager`/`projektleitung` → `pm` („PM"). Ausgabe: `arbeitsrolle` (nur bei bekannter Rolle), `arbeitsrolle_label` (deutsche Bezeichnung; bei unbekannter Rolle der Originaltext der Rolle, unverändert in der Schreibweise), `arbeitsstatus` (Text nach dem Doppelpunkt, getrimmt; nur wenn nicht leer). Ohne Doppelpunkt: keine Rolle, `arbeitsstatus` = gesamter Text. Leere Rolle (`": Text"`) → keine Rolle, Text bleibt. Fehlt `aktuell`, ist es leer, nur Leerraum oder kein String (z. B. `42`, Liste, `null`) → **keine** Felder, kein Fehler.
- **AK-2 (Keine Anzeige nach Abschluss, PM 1):** Aufgaben mit UI-Status „Geschlossen" (`task_status: abgeschlossen`) liefern keine Arbeitsstatus-Felder, auch wenn `aktuell` noch gefüllt ist (die PM-Regel sieht Leeren bei Abschluss vor; die Anzeige zeigt nur aktive Arbeit). Alle anderen Aufgaben zeigen den Arbeitsstatus unabhängig vom abgeleiteten UI-Status (also auch „Testing"/„Dokumentation"), weil `aktuell` der Live-Stand ist.
- **AK-3 (Read-Modell, PM 1):** `GET /api/aufgaben` und `GET /api/overview` liefern die Felder `arbeitsrolle` (optional), `arbeitsrolle_label` (optional) und `arbeitsstatus` (optional) **top-level** je Task-Eintrag; `GET /api/file?path=aufgaben/<…>` liefert dieselben Felder top-level. Nicht-Tasks und Tasks ohne ableitbare Angabe haben keines der Felder. Bestehende Felder (`path`, `typ`, `titel`, `status`, `owner`, `zuletzt_geaendert`, `welle?`, `hinweis?`) und die Antwortform `{frontmatter, markdown, nachtraege}` bleiben unverändert; `frontmatter.aktuell` bleibt roh erhalten. Kein neuer Endpunkt.
- **AK-4 (Listenanzeige, PM 2):** In Übersicht und Aufgabenliste zeigt die **Status-Zelle** einer Aufgabe mit Arbeitsstatus genau eine zusätzliche Zeile mit dem Text `"<Label>: <Text>"` (bzw. nur Label oder nur Text, wenn eines fehlt), z. B. „Coder: Umsetzung Paket 2". Die Zeile ist ein `div` mit `classList.add("arbeitsstand")`, ausschließlich über `textContent` gefüllt. A30 ändert die Spaltenzahl nicht (vier Spalten zu diesem Zeitpunkt; **A31** ergänzt danach die fünfte Spalte „Welle"); Statusmarke, optionaler `hinweis`, `data-path` und Zeilenreihenfolge bleiben unverändert. Mehrere Aufgaben „In Arbeit" zeigen jeweils ihren eigenen Arbeitsstatus (keine Vermischung, keine Sammelzeile). Die Wellenliste zeigt **keinen** Arbeitsstatus. `index.html` und `style.css` bleiben unverändert.
- **AK-5 (Detailanzeige, PM 2):** Das Detail einer Aufgabe mit Arbeitsstatus zeigt im Kopf ein `dl`-Feld „Arbeitsstatus" (Wert `"<Label>: <Text>"`) zwischen „Status" und „owner". Ohne ableitbare Angabe fehlt die Zeile vollständig (kein leerer Wert, kein „—"). Die A27-Ergänzung „Welle" (nur bei Aufgaben) und der owner-Umschalter bleiben unverändert; kein zusätzlicher Request.
- **AK-6 (Sicherheit/Robustheit, PM 2):** Keine HTML-Senke: Werte werden nur über `textContent`/`createElement` gerendert (kein `innerHTML`, kein `insertAdjacentHTML`, kein `eval`). Rollen- oder Textinhalte mit HTML/JS (`<img src=x onerror=alert(1)>`, `<script>`) erscheinen als Text, lösen keinen Dialog aus und erzeugen keinen `img`/`script`-Knoten. Unbekannte Rollen, fehlende Felder, `null`-Antworten und Nicht-Arrays führen zu keiner JS-Exception; das bestehende Fehler-/Formatverhalten (A11/A25) bleibt.
- **AK-7 (Single Source of Truth, PM 1):** `aktuell` ist die einzige Quelle. Es wird **kein** paralleles Frontmatter-Feld (`arbeitsstatus`, `rolle`, `arbeitsphase` o. ä.) eingeführt, kein Endpunkt schreibt `aktuell`, und die App bietet keine Bedienung dafür (Pflege bleibt PM/`documenter`). Die Ableitung passiert ausschließlich beim Lesen (idempotent, keine Dateiänderung).
- **AK-8 (Schnittstellen/Grenzen, alle):** Keine neuen Abhängigkeiten, kein externer Dienst, kein neuer Endpunkt, keine neue Route, kein neues `index.html`-Markup, keine neuen Filter-IDs. `app.js`, `api.js`, `meta.py`, `server.py`, `okf_bundle.py`, `neu_aufgabe.py`, `neu_welle.py`, `status.py` bleiben unverändert. Deutsche Bezeichnungen exakt: Planer, Coder, Tester, Review, Documenter, PM.
- **AK-9 (Doku/Regression, PM 3):** `wissen/projekt/phasen.md` ergänzt `aktuell` im Format der Aufgaben-Datei (Live-Feld, nur Anzeige, bei Abschluss leeren); `wissen/projekt/technische-spec.md` dokumentiert die abgeleiteten Felder in der Read-Modell-Tabelle und die Regel „nur Tasks, fehlend = keine Anzeige"; `AGENTS.md` und `definitions/AGENTS.md` ergänzen in der Regel „Live-Arbeitsstand pflegen" einen Satz, dass die App `aktuell` als Arbeitsstatus anzeigt (Rolle + Text) und die Schreibweise `<Rolle>: <Text>` dafür verbindlich ist. Bestehende Tests bleiben grün (Änderungen nur additiv); `bash definitions/verify.sh .` → Exit 0.

# Testfälle (TDD)

**Zuordnung AK → Testfälle:**
**AK-1** → T1–T8. **AK-2** → T9. **AK-3** → T10–T13. **AK-4** → T14–T17. **AK-5** → T18. **AK-6** → T19, T20. **AK-7** → T13, T21. **AK-8** → T22. **AK-9** → T23, T24.

Reihenfolge = Red-Green-Takt: erst Test schreiben, rot laufen lassen, dann das Minimum implementieren, dann refaktorisieren. Jede Testnummer ist ein eigener pytest-Fall. Neue Dateien: `tests/test_arbeitsstand.py` (Modul + Read-Modell, Flask-Client), `tests/test_arbeitsstand_ui.py` (Node/DOM), `tests/dom_helfer.py` (gemeinsamer Mini-DOM-Harness, von A28/A29 wiederverwendbar). Bestehende Testdateien werden **nicht** geändert. Alle API-Läufe gegen das `bundle`-Fixture aus `conftest.py` (`tmp_path`-Kopie von `fixtures/bundle_min`); zusätzliche Dateien werden im Test unter `tmp_path` angelegt — niemals gegen `wissen/`.

**A. Modul `arbeitsstand` (`tests/test_arbeitsstand.py`, AK-1, AK-2)**

- **T1 Standardfall:** `ermittle({"type": "Task", "aktuell": "coder: Umsetzung Paket 2"})` → `{"arbeitsrolle": "coder", "arbeitsrolle_label": "Coder", "arbeitsstatus": "Umsetzung Paket 2"}`; keine weiteren Keys.
- **T2 Rollen und Aliase:** parametrisiert `"Planer: …"` → `planner`/„Planer"; `"Coder: …"` → `coder`/„Coder"; `"Tester: …"` → `tester`/„Tester"; `"Review: …"` → `reviewer`/„Review"; `"Reviewer: …"` → `reviewer`/„Review"; `"Documenter: …"` → `documenter`/„Documenter"; `"Doku: …"` → `documenter`/„Documenter"; `"PM: …"` → `pm`/„PM"; `"Projektmanager: …"` → `pm`/„PM"; `"Projektleitung: …"` → `pm`/„PM".
- **T3 Kein Doppelpunkt:** `"Umsetzung Paket 2"` → nur `{"arbeitsstatus": "Umsetzung Paket 2"}`, **kein** `arbeitsrolle`/`arbeitsrolle_label`; auch `"Coder"` ohne Doppelpunkt ist Text, keine Rolle.
- **T4 Unbekannte Rolle (fail-loud, kein Wurf):** `"Architekt: Konzept"` → `arbeitsrolle` fehlt, `arbeitsrolle_label == "Architekt"` (Originalschreibweise), `arbeitsstatus == "Konzept"`; `"  Architekt : Konzept "` → Label `"Architekt"`, Text `"Konzept"`.
- **T5 Leer/fehlend/falscher Typ:** parametrisiert `{}`, `{"aktuell": ""}`, `{"aktuell": "   "}`, `{"aktuell": None}`, `{"aktuell": 42}`, `{"aktuell": True}`, `{"aktuell": []}`, `{"aktuell": {}}` → jeweils `{}`, kein Fehler; `frontmatter=None`/`[]` → `{}`.
- **T6 Nur Rolle/leere Rolle:** `"Coder:"` → `arbeitsrolle coder`, Label „Coder", **kein** `arbeitsstatus`; `": Text"` → keine Rolle, `arbeitsstatus == "Text"`; `":"` → `{}`.
- **T7 Leerraum/Normalisierung:** `"  Coder :  Umsetzung\nPaket   2 "` → Rolle `coder`, Text `"Umsetzung Paket 2"` (Mehrfach-Leerraum/Zeilenumbruch zu einem Leerzeichen); `"coder:   "` → Label Coder, kein Text.
- **T8 Mehrere Doppelpunkte:** `"coder: Fix: Randfall"` → Rolle `coder`, `arbeitsstatus == "Fix: Randfall"` (nur am ersten Doppelpunkt trennen).
- **T9 Nach Abschluss keine Felder:** `{"type": "Task", "task_status": "abgeschlossen", "aktuell": "coder: Rest"}` → `{}`; Gegenprobe `task_status: "in Umsetzung"` → Felder vorhanden; `status: "Geschlossen"` (ohne `task_status`) → `{}`.

**B. Read-Modell (`tests/test_arbeitsstand.py`, AK-3, AK-7)**

- **T10 `/api/aufgaben`:** Task mit `aktuell` → Eintrag enthält die drei Felder; Task ohne `aktuell` → keine; Wellen-Datei mit `aktuell` → keine (typ ≠ Task); Projektdatei → keine; alle bestehenden Felder unverändert, Listenreihenfolge unverändert.
- **T11 `/api/overview`:** dito über den Gesamtbestand; genau die Tasks tragen die Felder, Nicht-Tasks nicht; Antwort bleibt ein Array.
- **T12 `/api/file`:** Task mit `aktuell` → top-level `arbeitsrolle`/`arbeitsrolle_label`/`arbeitsstatus`; `frontmatter.aktuell` unverändert roh; `markdown`/`nachtraege` unverändert; Wellen-/Projektdatei → keine der drei Felder; Antwortform unverändert.
- **T13 Keine Schreibpfade/Doppelpflege:** `POST /api/nachtrag` und `POST /api/meta` (owner/status/welle) auf einer Aufgabe mit `aktuell` → Datei enthält weiterhin genau dasselbe `aktuell` (byte-gleich), kein neues Feld; `GET` danach liefert dieselben abgeleiteten Werte wie vorher; ein `POST` mit unbekanntem Feld `arbeitsstatus` wird wie bisher ignoriert (kein 200-Schreibvorgang, Datei unverändert).

**C. Frontend (`tests/test_arbeitsstand_ui.py`, AK-4, AK-5, AK-6)**

Harness: `tests/dom_helfer.py` (neu) mit dem Mini-DOM aus `test_welle_zuordnung.py` und `node_ausfuehren`/`js_liste`/`js_detail`; `test_arbeitsstand_ui.py` definiert das Seiten-/Fetch-Gerüst (Tabellencontainer, `#detail`, `#meldung`, `#fehler`) und prüft Rendering. Kein `index.html`-Markup, keine neue Abhängigkeit (Node ist bereits Testvoraussetzung; `ohne_node`-Skip wie A11/A27).

- **T14 Formatter:** `liste.formatiereArbeitsstand({arbeitsrolle_label: "Coder", arbeitsstatus: "Umsetzung Paket 2"})` → `"Coder: Umsetzung Paket 2"`; nur Label → `"Coder"`; nur Text → `"Umsetzung Paket 2"`; `{}`, `null`, `undefined`, `42`, `[]` → `""`; unbekanntes Label `"Architekt"` → `"Architekt: Konzept"`.
- **T15 Status-Zelle:** `ladeAufgaben()` mit zwei Tasks (einer mit Feldern, einer ohne) → Status-Zelle des ersten enthält `"Coder: Umsetzung Paket 2"` genau einmal, `classList.contains("arbeitsstand")`; Zelle des zweiten unverändert; Titel-/owner-Zellen unverändert; `data-path` unverändert; Kopfzeile unverändert (vier Spalten im A30-Stand; A31 hebt sie später auf fünf).
- **T16 Mehrere „In Arbeit":** drei Tasks mit `in Umsetzung` und unterschiedlichen Rollen (Coder, Tester, Review) → jede Status-Zelle zeigt genau ihre eigene Zeile; keine Zeile enthält eine fremde Rolle; Reihenfolge der Zeilen unverändert; Übersicht (Top 5) zeigt dieselbe Zuordnung.
- **T17 Abgrenzung:** Wellen-/Projektzeilen ohne Felder → keine `arbeitsstand`-Zeile; Wellenliste (`ladeWellen`) zeigt keine `arbeitsstand`-Zeile, auch wenn ein Eintrag (fehlerhaft) Felder trägt; zweiter Aufruf/Filterwechsel erzeugt keine doppelte Zeile.
- **T18 Detail:** `/api/file`-Stub für eine Aufgabe mit Feldern → im `dl` genau eine `dt` „Arbeitsstatus" mit `dd` „Coder: Umsetzung Paket 2", zwischen „Status" und „owner"; A27-Feld „Welle" weiterhin vorhanden; Aufgabe ohne Felder → keine `dt` „Arbeitsstatus"; Wellen-/Projektdatei → keine Zeile.
- **T19 XSS:** Label `"<img src=x onerror=alert(1)>"` und Text `"<script>alert(1)</script>"` → in Liste und Detail textuell, kein `img`/`script`-Knoten, kein `alert`; `formatiereArbeitsstand` liefert die Zeichenkette unverändert (keine Interpretation).
- **T20 Quell-/Strukturprüfung:** `liste.js` erfüllt weiterhin die A11-Quellprüfungen (`textContent`, kein `innerHTML`/`insertAdjacentHTML`/`document.write(`/`eval(`, `classList` statt `className`); die neuen Stellen in `detail.js` nutzen `textContent` und `classList` und führen keine HTML-Senke ein; `index.html` enthält weder `arbeitsstand` noch ein neues Filterfeld; `fetch`-Zähler: Übersicht/Aufgabenliste je ein Request, Detail nur `/api/file` (+ `/api/wellen` bei Aufgaben), kein Zusatz-Request.

**D. Regression (`tests/test_arbeitsstand.py` bzw. Gesamtlauf, AK-8)**

- **T21 Baselines:** `test_liste.py`, `test_detail.py`, `test_suche.py`, `test_welle_zuordnung.py`, `test_api_lesen.py`, `test_static.py`, `test_formulare.py`, `test_neu_aufgabe.py`, `test_meta.py` bleiben **unverändert** grün; die Suite wächst nur um die beiden neuen Testdateien; `bash definitions/verify.sh .` → Exit 0.
- **T22 Unveränderte Dateien/A27-Verträge:** `git diff --stat` zeigt keine Änderung an `static/index.html`, `static/style.css`, `static/js/app.js`, `static/js/api.js`, `app.js`, `api.js`, `meta.py`, `server.py`, `okf_bundle.py`, `status.py`; der Wellen-Filter, das Wellen-Dropdown und der Abschnitt „Aufgaben dieser Welle" (A27) funktionieren unverändert (Baselines + A27-Tests); die Suche (A25) findet weiterhin nur die bisherigen Felder.

**E. Doku (Review-Prüfschritte, kein pytest)**

- **T23 Phasenmodell:** `wissen/projekt/phasen.md` enthält `aktuell` im Format der Aufgaben-Datei mit dem Hinweis „Live-Feld, nur Anzeige, bei Abschluss leeren"; die Rollenliste entspricht AGENTS.md.
- **T24 Technische Spec:** `wissen/projekt/technische-spec.md` nennt die abgeleiteten Felder (`arbeitsrolle`, `arbeitsrolle_label`, `arbeitsstatus`), „nur Tasks", „fehlend = keine Anzeige", „kein neuer Endpunkt"; `AGENTS.md`/`definitions/AGENTS.md` enthalten den Anzeige-Satz in der Live-Arbeitsstand-Regel. Nachweis mit Zitatstelle im Review-Ergebnis.

**UI-Szenarien für den `tester` (Moli-Browser, laufende App gegen Test-Bundle):**

- **S1 Übersicht:** Aufgabe mit `task_status: in Umsetzung` und `aktuell: "coder: Umsetzung Paket 2"` → Übersichtsliste zeigt „In Arbeit" und darunter „Coder: Umsetzung Paket 2"; Aufgabe ohne `aktuell` zeigt keine Zusatzzeile; keine Konsolenfehler.
- **S2 Mehrere Aufgaben:** zwei Aufgaben in Arbeit mit „tester: …" und „reviewer: …" → jede Zeile zeigt ihre eigene Rolle, keine Vermischung.
- **S3 Detail:** Aufgabe öffnen → Feld „Arbeitsstatus" mit Rolle + Text; A27-Feld „Welle" weiterhin vorhanden; owner-Umschalter und Statusknöpfe funktionieren.
- **S4 Grenzfälle:** `aktuell` auf `"Architekt: Konzept"` setzen → Anzeige „Architekt: Konzept" (kein Fehler); `aktuell` leeren → Zeile verschwindet nach Neuladen; Aufgabe auf `abgeschlossen` setzen → keine Arbeitsstatus-Zeile; HTML in `aktuell` → nur Text, kein Dialog.

# Kontext

- **Anforderung (Projektleitung, 2026-11-15):** „Wenn ich die Übersichtsliste aufrufe und den Status ‚In Arbeit' sehe, sehe ich die Aufgaben, die im Moment bearbeitet werden — ich weiß aber nicht, wo wir uns gerade befinden. Wichtig wäre zu sehen, was gerade passiert: Arbeitsstatus Planer, Coder, Tester, Review, Documenter."
- **Welle:** [w2](wellen/w2.md) — A30 ist der Welle 2 zugeordnet; die Wellen-Freigabe (A29) ist für A30 noch nicht relevant, weil A29 erst nach A28 kommt.
- **Datenquelle (PM-Vorgabe):** ausschließlich das Frontmatter-Feld `aktuell` (`"<Rolle>: <Was passiert gerade>"`, AGENTS.md „Live-Arbeitsstand pflegen"). Es wird **abgeleitet**, nicht neu gespeichert: normalisierte Rolle (`arbeitsrolle`), deutsche Bezeichnung (`arbeitsrolle_label`) und freier Text (`arbeitsstatus`). Kein paralleles Feld, keine Doppelpflege, kein Schreibpfad in der App — die Pflege bleibt beim PM/`documenter`.
- **Warum die Status-Zelle statt einer neuen Spalte (Begründung):** (a) Die Anforderung ist an „In Arbeit" gekoppelt — der Arbeitsstatus gehört genau dorthin, wo der Status steht; (b) `SPALTEN` ist mit vier Spalten fester Vertrag von A11/A25/A27 (Tests prüfen die Kopfzeile); für den **Arbeitsstatus** bleibt es bei der Status-Zelle (die **Welle** erhält in A31 als bewusster Vertragswechsel eine eigene Spalte); (c) `index.html` ist seit A10 eingefroren, dynamische Montage wäre möglich, aber für eine Zeile pro Datensatz unnötig; (d) `style.css` bleibt unverändert, weil die Zeile ohne neue Klasse auskommt (`div` + `classList.add("arbeitsstand")`, ungestylt). *Verworfen:* eigene Spalte für den Arbeitsstatus, Sammelbanner „3 Aufgaben in Arbeit", Badge in der Titel-Zelle (dort ist ab A28 die „neu"-Marke vorgesehen).
- **Anzeige unabhängig vom UI-Status (außer „Geschlossen"):** `aktuell` ist der Live-Stand; auch „Testing"/„Dokumentation" zeigen, wer arbeitet. Nach `abgeschlossen` wird nichts angezeigt (PM-Regel: Feld leeren), damit abgeschlossene Aufgaben nicht mit veralteten Rollen erscheinen. Der Filter `status = In Arbeit` (A11) bleibt unverändert.
- **Ist-Stand im Code (geprüft 2026-11-15, Arbeitsbaum inkl. A27-Frontend):**
  - `overview._eintrag` baut die Listeneinträge; `overview.details` liefert `{frontmatter, markdown, nachtraege}` — beide sind die einzigen Stellen für die Read-Modell-Erweiterung.
  - `liste.erstelleStatusZelle(eintrag)` rendert Statusmarke + optionalen `hinweis`; dort hängt die neue Zeile an. `SPALTEN` bleibt unverändert.
  - `detail.erstelleKopf(pfad, daten, wellen)` baut das `dl` (Typ, Status, owner, Welle bei Aufgaben) und importiert bereits `erstelleTabelle` aus `liste.js` — der Formatter kann von dort mitgenutzt werden.
  - `status.ui_status(frontmatter)` liefert den UI-Status (u. a. „Geschlossen" für `task_status: abgeschlossen`) — Grundlage für AK-2, ohne eigene Mapping-Tabelle.
  - `test_liste.py` prüft Listenlogik über Node und per Quelltext (keine `innerHTML`-Senken, `classList` statt `className`); `test_welle_zuordnung.py` enthält den vollständigen Mini-DOM-Harness (wird nach `tests/dom_helfer.py` übernommen).
  - Kein bestehendes Feld heißt `arbeitsrolle`/`arbeitsstatus`; `overview.nachtraege` nutzt `aktuell` nur als lokale Variable (keine Kollision).
- **Umsetzungsentscheidungen (TDD-relevant, reversibel):**
  - **Eigenes Modul `arbeitsstand.py`** (framework-frei, keine I/O) statt Logik in `overview.py`: testbar ohne Flask (wie `status.py`), eine Normalisierungstabelle, von `_eintrag` und `details` gemeinsam genutzt.
  - **Rollen-Aliase minimal und dokumentiert:** Groß-/Kleinschreibung und die deutschen Kurzformen (`planer`, `review`, `doku`, `pm`, `projektmanager`, `projektleitung`). Unbekannte Rollen werden **nicht** geraten, sondern mit Originaltext angezeigt (fail-loud statt stilles Verschlucken, Muster A12-3).
  - **Nur der erste Doppelpunkt trennt** — Texte wie „Fix: Randfall" bleiben vollständig.
  - **Nicht-Strings werden ignoriert** (kein `str()`-Zwang), damit `aktuell: 42` nicht als Text „42" erscheint; das Feld ist als String dokumentiert.
  - **`arbeitsstatus` ist der freie Text**, nicht der Oberbegriff — die UI-Bezeichnung ist „Arbeitsstatus"; die Feldnamen sind bewusst getrennt (`arbeitsrolle_label` + `arbeitsstatus`), damit die Rolle maschinell filterbar bleibt (auch wenn A30 keinen Rollenfilter baut).
  - **Keine Suche-Erweiterung:** `SUCHFELDER` in `liste.js` bleibt unverändert; eine Suche nach „coder" ist nicht Teil von A30 (eigene Aufgabe, falls gewünscht). Damit bleibt A25 unberührt.
  - **Kein neues JS-Modul:** `formatiereArbeitsstand` wird aus `liste.js` exportiert und von `detail.js` importiert (Präzedenz: `erstelleTabelle`).
  - **Test-Harness:** `tests/dom_helfer.py` wird aus `test_welle_zuordnung.py` extrahiert (nur der generische Teil: Mini-DOM + Node-Runner) und von A30 sowie später A28/A29 genutzt — damit wachsen die Harness-Kopien nicht weiter (Konsolidierung der Altkopien bleibt [A14-6]).
- **Konfliktgruppen (neu):**
  - **G21 „Arbeitsstatus Backend":** `arbeitsstand.py` (neu), `overview.py`, `tests/test_arbeitsstand.py` (neu). **Überschneidet sich mit A28-G15/A29-G18 (`overview.py`) und liegt in der A27-Dateimenge (dort blieb `overview.py` unverändert)** → erst nach A27, vor A28.
  - **G22 „Arbeitsstatus UI":** `static/js/liste.js`, `static/js/detail.js`, `tests/test_arbeitsstand_ui.py` (neu), `tests/dom_helfer.py` (neu). **Überschneidet sich mit A27-G14 und A28-G16/A29-G19** → nicht parallel; A30-UI strikt nach A27-Abschluss.
  - **G23 „Arbeitsstatus Doku":** `AGENTS.md`, `definitions/AGENTS.md`, `wissen/projekt/phasen.md`, `wissen/projekt/technische-spec.md` — parallel zu G22 möglich, aber vor den Doku-Paketen von A28/A29 (gleiche Dateien).
- **Aufteilung in Pakete (ein Coder, eine Aufgabe):**
  - **Paket 1 — Modul + Backend:** `arbeitsstand.py` (Rollen-/Alias-Tabelle, `ermittle`), Einbau in `overview._eintrag`/`details` (nur `typ == "Task"`). Tests: T1–T13.
  - **Paket 2 — UI:** `formatiereArbeitsstand` + Status-Zeile in `liste.js`, `dl`-Zeile in `detail.js`, Test-Harness `dom_helfer.py` + `test_arbeitsstand_ui.py`. Tests: T14–T20.
  - **Paket 3 — Doku:** AK-9, Prüfschritte T23/T24; parallel zu Paket 2 (disjunkte Dateien).
  - **Reihenfolge im Paket:** Test → rot → Minimum → grün → nächster Test. Paket 1 vor Paket 2 (UI braucht die Felder); Paket 3 parallel zu Paket 2.
- **Reihenfolge-Empfehlung (mit Gate):**
  1. **A27 abschließen** (G14: `detail.js`/`liste.js` sind belegt; der Arbeitsbaum enthält den A27-Frontend-Stand bereits, Tests/Commit stehen noch aus).
  2. **Umsetzung A30 Paket 1 → 2**, **Paket 3 parallel zu 2**; danach Review, Test (S1–S4), Doku.
  3. **A31 nach A30** (gleiche Datei `liste.js`, fünf Spalten), **A28 erst nach A31** (G16/`liste.js`/`detail.js` und G15/`overview.py` sind dann frei), **A29 nach A28**. Damit gilt die Reihenfolge A27 → A30 → A31 → A28 → A29.
  4. **Freigabe-Gate:** Die Projektleitung hat A30 laut Auftrag priorisiert und freigegeben. Die Datei enthält (Stand heute) **kein** `freigabe`-Feld — das Freigabe-Feld entsteht erst mit A28. Für A30 gilt daher die dokumentierte PM-Freigabe als Gate; sobald das A28-Fundament existiert, sollte die Projektleitung `freigabe: true` nachtragen, damit der Zustand auch maschinenlesbar ist. Ohne A27-Abschluss darf die UI-Umsetzung **nicht** starten.
- **Abhängigkeiten:** A11 (Listendarstellung `erstelleTabelle`/Status-Zelle), A12 (Detail-Kopf, `dl`-Muster), A25 (`SUCHFELDER`, Suchverhalten bleibt unverändert), A27 (Pflicht: `detail.js`/`liste.js` frei; vier-Spalten-Vertrag, Wellen-Feld). A28/A29 sind **keine** Voraussetzungen, dürfen aber erst danach starten (Dateiüberschneidung).
- **Risiken/Grenzen:** (a) `aktuell` ist Freitext — Tippfehler in der Rolle erscheinen als Originaltext (gewollt, fail-loud); (b) sehr lange Texte verlängern die Status-Zelle (kein Hard-Truncate im Code, Umbruch per Tabellenlayout; bei Bedarf eigene Aufgabe); (c) eine Zeile mehr pro Datensatz kann die Übersicht dichter machen — deshalb nur bei gesetztem `aktuell`; (d) `arbeitsstatus` als Feldname für den Freitext kann mit der UI-Bezeichnung „Arbeitsstatus" verwechselt werden — im Code/Test konsequent „Label + Text"; (e) Altbestand ohne `aktuell` zeigt nichts (kein Migrationsbedarf).
- **Offene Fragen an den PM (Standardentscheidung in Klammern, nicht blockierend):**
  1. Soll der Arbeitsstatus **nur** bei „In Arbeit" erscheinen? *(Standard: nein — bei jedem aktiven Task mit `aktuell`, unabhängig vom UI-Status; nach `abgeschlossen` ausgeblendet.)*
  2. Sollen Rolle/Text durchsuchbar sein (A25)? *(Standard: nein — eigene Aufgabe, A25 bleibt unberührt.)*
  3. Soll die Wellenliste den Arbeitsstatus zeigen? *(Standard: nein — `aktuell` ist aufgabenbezogen.)*
  4. Sollen unbekannte Rollen als Fehler gemeldet werden? *(Standard: nein — Originaltext anzeigen, kein Blocker.)*
  5. Soll der Text in der Liste gekürzt werden? *(Standard: nein — kein Hard-Truncate, Tabellenumbruch genügt.)*

# Betroffene Dateien

- `definitions/app/arbeitsstand.py` (**neu**) — framework-freie Ableitung: Rollen-/Alias-Tabelle (`planner`, `coder`, `tester`, `reviewer`, `documenter`, `pm` → „Planer"/„Coder"/„Tester"/„Review"/„Documenter"/„PM"), `ermittle(frontmatter) -> dict` mit `arbeitsrolle`/`arbeitsrolle_label`/`arbeitsstatus`, Abschluss-Guard über `status.ui_status` (T1–T9).
- `definitions/app/overview.py` — Einbau in `_eintrag` (nur `typ == "Task"`, Felder nur wenn vorhanden) und in `details` (top-level, `frontmatter` bleibt roh) (T10–T12).
- `definitions/app/static/js/liste.js` — exportierter `formatiereArbeitsstand(quelle)`, Status-Zelle erhält die `arbeitsstand`-Zeile (`div`, `textContent`), `SPALTEN` unverändert (T14–T17, T19, T20).
- `definitions/app/static/js/detail.js` — Import des Formatters, `dl`-Zeile „Arbeitsstatus" zwischen „Status" und „owner", nur wenn nicht leer (T18).
- `definitions/app/tests/test_arbeitsstand.py` (**neu**) — T1–T13.
- `definitions/app/tests/test_arbeitsstand_ui.py` (**neu**) — T14–T20 inkl. Seiten-/Fetch-Gerüst.
- `definitions/app/tests/dom_helfer.py` (**neu**) — Mini-DOM + `node_ausfuehren`/`js_liste`/`js_detail` aus `test_welle_zuordnung.py` extrahiert; wird von A28/A29 wiederverwendet.
- `AGENTS.md` **und** `definitions/AGENTS.md` — Anzeige-Satz in „Live-Arbeitsstand pflegen" (AK-9); `definitions/` ist die Single Source of Truth.
- `wissen/projekt/phasen.md` — `aktuell` im Format der Aufgaben-Datei (Live-Feld, nur Anzeige, bei Abschluss leeren) (AK-9).
- `wissen/projekt/technische-spec.md` — abgeleitete Felder in der Read-Modell-Tabelle, Regel „nur Tasks, fehlend = keine Anzeige", kein neuer Endpunkt (AK-9).
- **Nicht geändert:** `definitions/app/static/index.html` (eingefroren seit A10), `static/style.css`, `static/js/app.js`, `static/js/api.js`, `static/js/formulare.js`, `static/js/features.js`, `static/js/projekt.js`, `definitions/app/meta.py`, `server.py`, `okf_bundle.py`, `status.py`, `neu_aufgabe.py`, `neu_welle.py`, `definitions/app/tests/test_liste.py`, `test_detail.py`, `test_suche.py`, `test_welle_zuordnung.py`, `test_api_lesen.py`, `test_static.py`, `test_formulare.py`, `test_meta.py`, `test_neu_aufgabe.py`.

# Ergebnisse

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-15 — coder (Umsetzung Paket 1 + Paket 3; Paket 2 gated)

- **Ergebnis Paket 1 (Modul + Backend, G21):** `definitions/app/arbeitsstand.py` neu — framework-frei, ohne I/O: Rollen-/Alias-Tabelle (`planner`/`planer`, `coder`, `tester`, `reviewer`/`review`, `documenter`/`doku`, `pm`/`projektmanager`/`projektleitung` → „Planer"/„Coder"/„Tester"/„Review"/„Documenter"/„PM") und `ermittle(frontmatter)` → `arbeitsrolle` (nur bei bekannter Rolle), `arbeitsrolle_label` (bei unbekannter Rolle der Originaltext), `arbeitsstatus` (Text nach dem **ersten** Doppelpunkt). Normalisierung: trimmen + Leerraumfolgen (inkl. Zeilenumbruch) zu einem Leerzeichen; Rolle case-insensitiv; ohne Doppelpunkt ist alles Text; leere Rolle → keine Rolle, Text bleibt; `aktuell` fehlt/leer/Nicht-String → `{}`; Abschluss-Guard über `status.ui_status` („Geschlossen" → `{}`); Nicht-Tasks → `{}`. `overview._eintrag` und `overview.details` übernehmen die Felder **top-level** nur bei `typ == "Task"`; `frontmatter` (inkl. `aktuell`) bleibt roh, kein Schreibpfad, kein neuer Endpunkt. Deckt AK-1, AK-2, AK-3, AK-7 ab.
- **Ergebnis Paket 3 (Doku, G23):** `wissen/projekt/phasen.md` — Aufgaben-Format um `aktuell: "<Rolle>: <Was passiert gerade>"` ergänzt, mit dem Satz „Live-Feld, nur Anzeige, bei Abschluss leeren" und der vollständigen Rollen-/Aliasliste (deckungsgleich mit AGENTS.md). `wissen/projekt/technische-spec.md` — Read-Modell-Tabelle um `arbeitsrolle?`, `arbeitsrolle_label?`, `arbeitsstatus?` bei `/api/overview`, `/api/file` und den Rohlisten ergänzt, plus Regelblock „abgeleitet, nur lesend": nur `typ: Task`, fehlend = keine Anzeige, „Geschlossen" ohne Felder, `frontmatter.aktuell` roh, kein neuer Endpunkt. `AGENTS.md` und `definitions/AGENTS.md` — in „Live-Arbeitsstand pflegen" ein Satz zur Anzeige als Arbeitsstatus (Status-Zelle + Detail-Feld) und zur verbindlichen Schreibweise `<Rolle>: <Text>` inkl. Rollenliste. Deckt AK-9 (T23/T24) ab.
- **Gate eingehalten:** Paket 2 (UI: `liste.js`, `detail.js`, `tests/dom_helfer.py`, `tests/test_arbeitsstand_ui.py`) **nicht** begonnen — A27-Review/-Testphase lesen diese Dateien; Start erst auf PM-Freigabe. T14–T20 sowie T21/T22 (Baselines/Dateiinventar) bleiben offen.
- **Belege:** TDD-Red-Green. Erster Lauf: `test_arbeitsstand.py` rot (Collection-Error, Modul fehlt). Nach dem Modul: 33 grün / 4 rot (`/api/aufgaben`, `/api/overview`, `/api/file`, Schreibpfad). Nach dem Einbau in `overview.py`: **38 grün** (T1–T13 inkl. `test_t9b_nur_tasks`; T2 mit 10 Rollen-Fällen, T5 mit 10 Negativfällen). Angrenzende Suiten unverändert grün (549 Tests: `test_api_lesen`, `test_api_schreiben`, `test_welle_zuordnung`, `test_features`, `test_projekt`, `test_liste`, `test_detail`, `test_static`). Gesamtsuite serialisiert (`python3 -m pytest definitions/app/tests -q -p no:randomly`): **1107 passed, 0 failed** (6:27). Ein früherer Gesamtlauf blieb bei 78 % in `test_start_skript.py` hängen (Fremd-Ursache: `start.sh`/`test_start_skript.py` wurden parallel von einem anderen Agenten geschrieben); die Datei lief isoliert danach mit **22 passed** durch.
- **Bewusste Abweichung/Ergänzung:** Der Typ-Guard (`nur typ == "Task"`) liegt zusätzlich **im Modul** (nicht nur im Aufrufer) — dadurch kann kein künftiger Aufrufer die Felder für Wellen/Projekte erhalten; Verhalten der API unverändert. Testfall `T9b` dokumentiert das. `details`/`_eintrag` behalten den expliziten Guard zusätzlich bei.
- **Offene Punkte:** Paket 2 (UI) nach PM-Freigabe; Moli-Szenarien S1–S4 erst nach Paket 2 (tester); `bash definitions/verify.sh .` nicht separat gelaufen (parallele Umbauten an `definitions/setup.sh`/`start.sh` durch andere Agenten). Keine Commits.

## 2026-11-15 — coder (Umsetzung Paket 2: UI)

- **Ergebnis Paket 2 (UI, G22):** `liste.js` — neuer Export `formatiereArbeitsstand(quelle)` (Label aus `arbeitsrolle_label`, Fallback `arbeitsrolle`; Text aus `arbeitsstatus`; fehlende Teile werden weggelassen, ohne Angabe `""`); `erstelleStatusZelle` hängt für `typ === "Task"` genau eine `div.arbeitsstand`-Zeile mit `textContent` an (Beispiel „Coder: Umsetzung Paket 2"). Vier-Spalten-Vertrag (`SPALTEN`) unverändert. `detail.js` — importiert den Formatter und zeigt im `dl` ein Feld „Arbeitsstatus" **zwischen** „Status" und „owner", nur wenn nicht leer; A27-Feld „Welle" und owner-Umschalter unverändert; kein zusätzlicher Request. Neuer Harness `tests/dom_helfer.py` (konsolidierte Quelle: Node-Runner + Mini-DOM + `js_liste`/`js_detail`, extrahiert aus `test_welle_zuordnung.py`) und neue Testdatei `tests/test_arbeitsstand_ui.py` (T14–T20) mit eigenem Seiten-/Fetch-Gerüst. Deckt AK-4, AK-5, AK-6 ab; `index.html`, `style.css`, `app.js`, `api.js` unverändert.
- **Belege:** TDD-Red-Green: erster Lauf `test_arbeitsstand_ui.py` **13 rot / 12 grün** (Formatter-Export fehlt, Status-Zeile und `dl`-Feld fehlen), nach der Implementierung **25 grün** (T14 mit 7, T18 mit 4, T20 mit 10 Fällen). Angrenzende Suiten unverändert grün: `test_welle_zuordnung`, `test_liste`, `test_detail`, `test_suche`, `test_arbeitsstand`, `test_features`, `test_static` → **428 passed**. Gesamtsuite serialisiert (`python3 -m pytest definitions/app/tests -q -p no:randomly`): **1132 passed, 0 failed** (3:38).
- **Bewusste Abweichung:** Der Formatter fällt ohne `arbeitsrolle_label` auf `arbeitsrolle` zurück (die API liefert beides; der Fallback verhindert eine leere Anzeige bei manuell gebauten Daten). Die Zeile erscheint nur bei `typ === "Task"` — so zeigt auch die Wellenliste nichts, selbst wenn ein Eintrag fehlerhaft Felder trägt (T17).
- **Offene Punkte:** Moli-Szenarien **S1–S4** beim `tester` offen; A31 (fünfte Spalte „Welle") auf PM-Auftrag noch nicht begonnen; `bash definitions/verify.sh .` nicht separat gelaufen (Parallelbetrieb). Keine Commits.



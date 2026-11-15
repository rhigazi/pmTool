---
type: Task
title: "A34: Unter-Aufgaben erstellen"
description: Als Mensch muss ich in der Lage sein unter Aufgaben so eine Aufgabe zu
  erstellen
freigabe: true
task_status: in Umsetzung
phase: 3 Umsetzung
priority: mittel
assigned_to: coder
welle: wellen/w3.md
owner: ai
aktuell: "coder: A34 Paket 1+2 (kennung.py + parent-Anlage) — Freigabe lt. Feature-Strecken-Vorgabe"
---

# Ziel

Unter einer bestehenden Aufgabe lassen sich **Unter-Aufgaben** anlegen und in der
Detailansicht der Eltern-Aufgabe als Liste sehen. Unter-Aufgaben sind **eigenständige
OKF-Aufgaben** (`type: Task`, eigene Datei in `wissen/aufgaben/`), keine Textzeilen in
der Eltern-Datei: Sie durchlaufen dieselbe Pipeline, dieselben Filter und dasselbe
Freigabe-Gate wie jede andere Aufgabe.

A34 liefert dafür vier Bausteine:

1. **Datenmodell:** additives Frontmatter-Feld `parent` (bundle-relativer Pfad der
   Eltern-Aufgabe, genau ein Elternteil, **maximal eine Ebene**). Kein Bruch der
   OKF-Struktur, keine Sammel-Datei, keine Zweitpflege.
2. **Kennung:** `A{xxx}.{uuu}` im Titel (`A34.001: …`) und `a{xxx}.{uuu}-<slug>.md` als
   Dateiname; `uuu` = `001`–`999`. Die App vergibt die Unter-Kennung beim Anlegen
   (Elternnummer steht fest, Unter-Nummernraum ist lokal) — der Mensch tippt keine
   Nummer. A28s Kennungsprüfung (`neu`, `kennung`) wird **konsistent erweitert**.
3. **Anlegen in der Detailansicht:** Knopf „Unter-Aufgabe anlegen" (nur bei
   Aufgaben ohne `parent`, nicht bei geschlossenen Aufgaben) öffnet ein kompaktes
   Inline-Formular; `parent` wird automatisch gesetzt, `welle` von der Eltern-Aufgabe
   geerbt. Erweiterung von `POST /api/task` um `parent` — **kein neuer Endpunkt**.
4. **Anzeige:** Abschnitt „Unter-Aufgaben (n)" mit Tabelle (Titel, Status, owner,
   zuletzt geändert inkl. Arbeitsstatus aus A30); Klick öffnet die Unter-Aufgabe;
   ohne Kinder **kein** Abschnitt.

**Abgrenzung (bewusst nicht in A34):** Unter-Unter-Aufgaben (Tiefe > 1), Umhängen
einer Unter-Aufgabe an eine andere Eltern-Aufgabe, Löschen/Verschieben, Fortschritts-
Roll-up auf die Eltern-Aufgabe, verschachtelte Darstellung in der Aufgabenliste,
eigener Filter/Spalte „Unter-Aufgaben", Freigabe per Eltern-Aufgabe.

# Akzeptanzkriterien

- **AK-1 (Datenmodell `parent`, PM 1):** Aufgaben-Dateien dürfen das additive
  Frontmatter-Feld `parent` tragen: String, bundle-relativer Pfad einer vorhandenen
  Aufgabe unter `aufgaben/` (z. B. `parent: aufgaben/a34-unter-aufgaben.md`), genau
  **ein** Elternteil. Wertform wie `welle` (Pfad, nicht Kennung, nicht Titel). Fehlt
  das Feld, ist die Aufgabe Top-Level. Eine Datei mit nicht-leerem `parent` ist selbst
  **keine** Eltern-Aufgabe (Tiefe 1). Bestehende Felder, Body-Abschnitte, OKF-Struktur
  und die Anzeige von Nicht-Tasks bleiben unverändert. `parent` wird ausschließlich
  beim Anlegen geschrieben; A34 führt keinen Änderungs-/Löschweg ein.
- **AK-2 (Kennungsschema `A{xxx}.{uuu}`, PM 1):** Der Titel einer Unter-Aufgabe lautet
  exakt `A{xxx}.{uuu}: <Titel>` (Beispiel `A34.001: Erste Unter-Aufgabe`), der
  Dateiname `a{xxx}.{uuu}-<slug>.md` (Beispiel `a34.001-erste-unter-aufgabe.md`).
  `xxx` ist die Nummer der Eltern-Aufgabe nach A28 (`[1-9][0-9]*`, keine führende
  Null), `uuu` sind **genau drei Ziffern** `001`–`999`. Top-Level-Aufgaben bleiben
  unverändert (`A<N>: …`, `a<N>-<slug>.md`). Die Grammatik liegt als **einzige Quelle**
  in `kennung.py`; `overview` (A28-Felder) und `neu_aufgabe` verwenden sie. A28s
  `neu` ist genau dann `false`, wenn Titel- und Datei-Kennung **inklusive
  Unter-Nummer** übereinstimmen (beide vorhanden oder beide fehlend); jede Abweichung
  (fehlende/abweichende Unter-Nummer, `a34-001-…` statt `a34.001-…`) ergibt
  `neu: true`. `kennung` liefert `"A34.001"`. `naechste_kennung` bleibt
  **top-level-only** (`"A35"`); Unter-Kennungen beeinflussen sie nicht und es gibt
  kein neues Feld `naechste_unterkennung`. Ungültig (nicht als Unter-Kennung erkannt,
  damit `neu: true`): `A34.000`, `A34.1`, `A34.0001`, `A034.001`, `A34.001.002`.
  `a34-001-x.md` bleibt eine gültige Top-Level-Aufgabe A34 mit Slug `001-x` (bewusst:
  der Punkt trennt Nummerierungsebenen, der Bindestrich gehört zum Slug).
- **AK-3 (Anlage über `POST /api/task` mit `parent`, PM 1):** Der bestehende Endpunkt
  akzeptiert das optionale Feld `parent`; Antwort bleibt `{path}`. Der Server vergibt
  die Kennung: Ein führendes Kennungspräfix der Eingabe (`^A\d+(\.\d{3})?\s*:\s*`)
  wird entfernt, dann wird `A{Elternnummer}.{uuu}: ` vorangestellt (kein Doppelpräfix).
  Der Slug entsteht aus dem **bereinigten** Titel nach A4 (Umlaute → ASCII,
  Sonderzeichen → `-`, max. 60 Zeichen, Kollisionssuffix `-2`, `-3`, …).
  `uuu` = **kleinste freie** Nummer `001`–`999` unter dieser Eltern-Aufgabe; belegt
  ist eine Nummer, wenn eine Datei unter `aufgaben/` sie über `parent` **oder** über
  Titel-/Datei-Kennung mit derselben Elternnummer trägt (Lücken werden gefüllt, keine
  Reservierung). Neu geschriebene Datei: `type: Task`,
  `title: "A{xxx}.{uuu}: <Titel>"`, `description` aus der ersten Ziel-Zeile (≤160),
  `task_status: offen`, `phase: 2 Planung`, `priority` aus dem Formular,
  `assigned_to: coder`, `welle` **von der Eltern-Aufgabe geerbt** (nur wenn vorhanden),
  `parent`, `owner: ai`, `freigabe: false` (A28). Schlüsselreihenfolge:
  `type, title, description, task_status, phase, priority, assigned_to,
  user_story?, welle?, parent?, owner, freigabe?`. Body: die sechs A13-Abschnitte
  (`# Ziel`, `# Akzeptanzkriterien`, `# Testfälle (TDD)`, `# Kontext`,
  `# Betroffene Dateien`, `# Ergebnisse`) in gleicher Reihenfolge und Textform.
- **AK-4 (Validierung `parent`, PM 1):** `parent` ist nur gültig, wenn es (a) ein
  String ist, (b) auf eine **vorhandene, lesbare** `.md`-Datei unter `aufgaben/`
  zeigt, (c) nicht reserviert ist, (d) `type: Task` trägt, (e) selbst kein `parent`
  hat (Tiefe 1), (f) **nicht** `task_status: abgeschlossen` ist und (g) eine gültige,
  konsistente Top-Level-Kennung besitzt (Titel `A<N>: …` **und** Datei `a<N>-…`,
  keine Unter-Nummer). Jede Verletzung → **400** (`EingabeFehler`, deutsche Meldung
  ohne Pfad-/OS-Details), **keine** Datei entsteht, Bundle bleibt byte-identisch
  (kein Teilzustand). `parent` fehlt, ist `null` oder leer/Leerraum → Top-Level-Anlage
  wie A13 (kein Fehler). Nicht-String (`42`, `[]`, `{}`, `true`) → 400. `welle`
  **zusammen mit** `parent` → 400 (Vererbung statt Zweitwahrheit). Nummernraum
  `001`–`999` erschöpft → 400. `path` bleibt auf `/api/task` verboten (A9-Vertrag).
  Für ein ungültiges `parent` wird **nicht** 404 verwendet (Body-Validierung, nicht
  Ressourcen-Lookup).
- **AK-5 (Read-Modell `parent`, PM 1):** `GET /api/aufgaben` und `GET /api/overview`
  liefern für Task-Einträge mit nicht-leerem String-`parent` das Feld `parent`
  (Rohwert); Top-Level-Aufgaben und alle Nicht-Tasks tragen den Schlüssel **nicht**.
  Übrige Felder, Sortierung und `hinweis`-Verhalten bleiben unverändert. `GET
  /api/file` liefert `parent` ausschließlich roh in `frontmatter`; es gibt **kein**
  neues Top-Level-Feld und keine Änderung an A28s `neu`/`kennung`/`naechste_kennung`.
  `POST /api/meta` schreibt `parent` nicht (unbekanntes Feld wird wie bisher
  ignoriert, Datei unverändert).
- **AK-6 (Anlegen in der Detailansicht, PM 2):** Das Detail einer Aufgabe mit
  `type: Task`, ohne `parent` und ohne UI-Status „Geschlossen" zeigt in
  `.detail-aktionen` genau einen Knopf `#detail-unteraufgabe-anlegen` mit dem Text
  „Unter-Aufgabe anlegen". Klick blendet den standardmäßig versteckten Abschnitt
  `#unteraufgabe-anlegen` ein (kein Request beim Öffnen) mit den Feldern
  `#unteraufgabe-titel`, `#unteraufgabe-ziel`, `#unteraufgabe-akzeptanz`,
  `#unteraufgabe-prioritaet` (Vorauswahl `mittel`), Absenden
  `#unteraufgabe-speichern`, Abbrechen `#unteraufgabe-abbrechen`. Absenden prüft wie
  A13 (gleiche Feldmeldungen aus `formulare.js`: Titel, Ziel, mindestens ein
  Akzeptanzkriterium, gültige Priorität) und sendet bei Erfolg **genau ein**
  `POST /api/task` mit `{titel, ziel, akzeptanz[], prioritaet, parent}` — ohne
  `welle`, ohne `user_story`. Erfolgsmeldung „Unter-Aufgabe angelegt.", danach wird
  das Detail neu geladen, das neue Kind erscheint im Abschnitt, das Formular wird
  geschlossen und geleert. Während des Requests ist der Knopf `disabled`
  (`try/finally`); bei Fehler bleibt die Servermeldung sichtbar, die Eingaben bleiben
  erhalten, es wird nicht neu geladen; Doppelklick → ein Request. Kein Knopf und
  kein Formular bei Nicht-Tasks, bei Unter-Aufgaben (`frontmatter.parent`) und bei
  geschlossenen Aufgaben.
- **AK-7 (Anzeige „Unter-Aufgaben (n)", PM 2):** Hat eine Aufgabe mindestens ein Kind
  (aus `GET /api/aufgaben`, gefiltert über `parent == pfad`), zeigt das Detail nach
  dem Markdown-Inhalt und vor dem Nachtragsformular einen Abschnitt
  (`section`, Klassen `detail-abschnitt uebersicht-block`) mit
  `h3.uebersicht-titel` und dem Text exakt `Unter-Aufgaben (n)` (n = Anzahl). Die
  Tabelle entsteht über `erstelleTabelle` aus `liste.js` (Spalten Titel, Status,
  owner, zuletzt geändert; die A30-Arbeitsstatus-Zeile erscheint automatisch), jede
  Zeile trägt `data-path` des Kindes, Klick öffnet die Unter-Aufgabe über die
  bestehende Delegation in `app.js`. Sortierung: aufsteigend nach Unter-Nummer, dann
  `path` (die Nummer ist die Ordnung, nicht die mtime). Bei erfolgreich geladenen
  **null** Kindern gibt es **keinen** Abschnitt, keine Überschrift und keinen
  Leerhinweis. Bei Ladefehler oder Antwort ≠ Array erscheint der Abschnitt mit
  `Unter-Aufgaben konnten nicht geladen werden.` bzw. `Unter-Aufgaben haben ein
  unerwartetes Format.` (fail-loud). Unter-Aufgaben (Tiefe 1) zeigen auch bei
  inkonsistenten Daten **keinen** Abschnitt; die A27-Wellen-Sicht bleibt unverändert.
- **AK-8 (Freigabe-Gate bleibt intakt, PM 1):** Eine neu angelegte Unter-Aufgabe
  enthält `freigabe: false` (A28-Feld), `task_status: offen`; A34 führt **keinen**
  Schreibpfad für `freigabe` ein, ändert `POST /api/freigabe` nicht und umgeht das
  Gate nicht über `parent` (auch unter einer freigegebenen Eltern-Aufgabe bleibt das
  Kind bis zur eigenen Freigabe `offen`). Kein Auto-Dispatch, kein Statuswechsel über
  `offen` hinaus, keine Freigabe „per Eltern-Aufgabe". `POST /api/meta` liefert für
  `freigabe` weiterhin 403. Die Workflow-Regel (A28) gilt für Unter-Aufgaben
  unverändert und wird in AGENTS.md ausdrücklich genannt.
- **AK-9 (Doku/Regelwerk konsistent, PM 3):** `AGENTS.md` **und**
  `definitions/AGENTS.md` erweitern die Regel „Aufgaben-Kennung ist eindeutig und
  steht im Titel" um `A{xxx}.{uuu}: …` / `a{xxx}.{uuu}-<slug>.md`, um „Kennung
  vergibt die App beim Anlegen, die KI ändert sie nicht", um „maximal eine Ebene" und
  um „gilt für Unter-Aufgaben unverändert"; die Prüfpflicht-Merkmale nennen
  `Dateiname ohne aNN-/aNN.NNN-Präfix`. `wissen/projekt/phasen.md` ergänzt `parent`
  und das Kennungsschema im Format der Aufgaben-Datei. `wissen/projekt/technische-spec.md`
  ergänzt `parent` in der Frontmatter-Tabelle, `parent?` in der
  `POST /api/task`-Zeile, `parent` im Read-Modell sowie die Kennungsgrammatik samt
  „`naechste_kennung` bleibt top-level-only". **Zusätzlich (PM-Aufgabe, nicht
  A34-Code):** A33 schlägt „eigene Aufgabe A34 (Status-Mapping)" vor — diese Nummer
  ist durch A34 belegt; A33s Vorschlagsliste ist auf A35–A38 umzunummerieren.
- **AK-10 (Grenzen/Regression, alle):** Keine neuen Abhängigkeiten, kein externer
  Dienst, kein neuer Endpunkt, keine neue Route, kein neues `index.html`-Markup,
  keine `style.css`-Änderung. `static/index.html`, `static/style.css`, `static/js/app.js`,
  `static/js/api.js`, `static/js/liste.js`, `static/js/formulare.js`,
  `static/js/features.js`, `static/js/projekt.js`, `server.py`, `meta.py`,
  `okf_bundle.py`, `status.py`, `arbeitsstand.py`, `neu_welle.py`, `freigabe.py`
  bleiben unverändert. Nur `textContent`/`createElement`/`classList` (kein
  `innerHTML`, kein `eval`); deutsche Meldungen ohne Pfade. Bestehende Tests bleiben
  grün (Änderungen nur additiv; die Request-Zahl-Erwartung in `test_freigabe_ui.py`
  wird nachgezogen); `bash definitions/verify.sh .` → Exit 0. Tests laufen
  ausschließlich gegen `tmp_path`-Kopien, nie gegen `wissen/`.

# Testfälle (TDD)

**Zuordnung AK → Testfälle:**
**AK-1** → T1–T5, T13, T22, T28–T31. **AK-2** → T1–T12. **AK-3** → T13–T17, T26.
**AK-4** → T18–T27. **AK-5** → T28–T31. **AK-6** → T32–T36, T46.
**AK-7** → T37–T43, T45. **AK-8** → T13, T24, T26. **AK-9** → T49, T50.
**AK-10** → T44, T47, T48.

Reihenfolge = Red-Green-Takt: erst Test schreiben, rot laufen lassen, dann das Minimum
implementieren, dann refaktorisieren. Jede Testnummer ist ein eigener pytest-Fall.
Neue Dateien: `tests/test_kennung.py`, `tests/test_unteraufgabe.py`,
`tests/test_unteraufgabe_ui.py`. Bestehende Dateien nur additiv:
`tests/test_neue_aufgabe_signal.py` (A28-Konsistenz), `tests/test_freigabe_ui.py`
(Request-Zahl). Alle Läufe gegen das `bundle`-Fixture aus `conftest.py`
(`tmp_path`-Kopie von `fixtures/bundle_min`); zusätzliche Dateien werden **im Test**
unter `tmp_path` angelegt. Die UI-Tests nutzen `tests/dom_helfer.py` (in A30
angelegt) — **keine** neue Harness-Kopie.

**A. Kennungsgrammatik (`tests/test_kennung.py`, AK-1, AK-2)**

- **T1 Titel gültig:** `kennung.zerlege_titel("A34.001: Erste Unter-Aufgabe")` →
  `nummer=34`, `unter=1`, `kennung="A34.001"`; `"A34.001: X"` und `"A34.001: "`
  (nur Kennung) sind formatgültig; `"A34: X"` → `unter=None`.
- **T2 Titel ungültig:** parametrisiert `"A34.000: X"`, `"A34.1: X"`,
  `"A34.0001: X"`, `"A034.001: X"`, `"A34.001.002: X"`, `"A34.001:X"` (ohne
  Leerzeichen), `"a34.001: X"`, `"A34 .001: X"`, `"A: X"`, `""`, `None` → jeweils
  keine Kennung (kein Wurf), Folge: `neu: true`.
- **T3 Dateiname:** `a34.001-x.md` → (34, 1); `a34.001.md` → (34, 1);
  `a34.001-x-2.md` → (34, 1); `a34-001-x.md` → **keine** Unter-Kennung, sondern
  Top-Level 34 mit Slug `001-x`; `a34.0001-x.md`, `a34.1-x.md`,
  `a34.001.002-x.md`, `a034.001-x.md`, `x.md` → keine Unter-Kennung.
- **T4 Konsistenz-Matrix:** `("A34.001: X","a34.001-x.md")` → zugewiesen;
  `("A34.001: X","a34.001.md")` → zugewiesen; `("A34.001: X","a34-001-x.md")`,
  `("A34: X","a34.001-x.md")`, `("A34.001: X","a34.002-x.md")`,
  `("A34.001: X","a35.001-x.md")` → jeweils **nicht** zugewiesen.
- **T5 `kennung`-Ausgabe:** `kennung_aus_titel`/`kennung_aus_dateiname` liefern
  `"A34"` bzw. `"A34.001"`; `eltern_kennung("aufgaben/a34-x.md", {title: "A34: X"})`
  → `"A34"`; bei Unter-Aufgabe, fehlender oder inkonsistenter Kennung → `None`.
- **T6 `naechste_unterkennung`:** Bundle mit Kindern `a34.001-a.md`, `a34.002-b.md`
  und einer Datei mit Titel `A34.004` (ohne `parent`) → `"A34.003"` (kleinste freie,
  beide Signale zählen); leeres Eltern-Verzeichnis → `"A34.001"`; Kinder von A35
  (`a35.001-c.md`) beeinflussen A34 nicht; `a34-001-x.md` (Top-Level) zählt **nicht**
  als belegt; doppeltes `a34.001` (zwei Dateien) → nächste freie `002`.
- **T7 Nummernraum erschöpft:** 999 Kinder `001`–`999` belegt →
  `kennung.naechste_unterkennung` wirft `EingabeFehler` (Meldung ohne Pfad), kein
  Schreibvorgang.
- **T8 `naechste_kennung` bleibt top-level-only:** Bundle mit `a34-x.md` (Titel
  `A34: X`), `a34.001-y.md`, `a35.002-z.md` → `naechste_kennung == "A35"`; ohne
  Bestand `"A1"`; Unter-Nummern erzeugen nie `"A34.002"`.

**B. A28-Konsistenz (`tests/test_neue_aufgabe_signal.py`, additiv, AK-2)**

- **T9 `neu == false` für Unter-Aufgaben:** `aufgaben/a34.001-x.md` mit
  `title: "A34.001: X"` → `GET /api/aufgaben`, `/api/overview` und `/api/file`
  liefern `neu is False`, `kennung == "A34.001"`.
- **T10 `neu == true` bei Abweichung:** (a) Datei `a34.001-x.md`, Titel `"A34: X"`;
  (b) Datei `a34-x.md`, Titel `"A34.001: X"`; (c) Datei `a34.002-x.md`, Titel
  `"A34.001: X"`; (d) Datei `a34-001-x.md`, Titel `"A34.001: X"` → jeweils
  `neu is True`, kein Wurf.
- **T11 Detail-Felder:** Kind-Detail enthält `kennung == "A34.001"`,
  `naechste_kennung == "A35"` (kein `naechste_unterkennung`), weiterhin
  `frontmatter`, `markdown`, `nachtraege`; Wellen-/Projektdatei unverändert ohne
  diese Felder.
- **T12 Top-Level-Regression:** Die A28-Matrix (`A1: …` + `a1.md` → `neu false`;
  `A12: X` + `x.md` → `neu true`; `A12: X` + `a12-x.md` → `neu false`; `"A12: "` →
  `neu false`) bleibt unverändert grün.

**C. Anlage (`tests/test_unteraufgabe.py`, AK-1, AK-3, AK-4, AK-8)**

- **T13 Happy Path:** Eltern-Aufgabe `aufgaben/a34-unter-aufgaben.md`
  (`title: "A34: Unter-Aufgaben"`) im Bundle; `POST /api/task` mit
  `{titel: "Erste Unter-Aufgabe", ziel, akzeptanz: [...], prioritaet: "hoch",
  parent: "aufgaben/a34-unter-aufgaben.md"}` → 200 `{path:
  "aufgaben/a34.001-erste-unter-aufgabe.md"}`; Datei existiert; Frontmatter:
  `type: Task`, `title: "A34.001: Erste Unter-Aufgabe"`,
  `parent: aufgaben/a34-unter-aufgaben.md`, `owner: ai`, `task_status: offen`,
  `phase: 2 Planung`, `assigned_to: coder`, `priority: hoch`, `freigabe is False`;
  `GET /api/aufgaben` → `neu is False`, `kennung == "A34.001"`; Body enthält die
  sechs A13-Abschnitte in Reihenfolge.
- **T14 Kennung/Slug:** Titel `"Übersicht: Status & owner!"` → Datei
  `a34.001-uebersicht-status-owner.md`, Titel `"A34.001: Übersicht: Status & owner!"`;
  Titel nur aus Kennung (`"A34.001: "`) → 400, keine Datei.
- **T15 Nummerierung:** zwei Anlagen → `001`, `002`; Löschen von `001` (im Test) →
  nächste Anlage `001`; paralleles Kind von A35 → `a35.001-…` (keine Vermischung).
- **T16 Titel-Normalisierung:** Eingabe `"A34.007: Eigener Titel"` → gespeichert
  `"A34.001: Eigener Titel"`; `"A35.001: Fremd"` → `"A34.001: Fremd"`;
  `"A34.001:Fremd"` → `"A34.001: Fremd"`; **kein** doppeltes Präfix.
- **T17 `welle` geerbt:** Eltern mit `welle: wellen/w3.md` → Kind trägt
  `welle: wellen/w3.md`; Eltern ohne `welle` → kein `welle`-Schlüssel; `parent` +
  `welle` im Body → 400, keine Datei.
- **T18 `parent`-Typen:** `null`, fehlend, `""`, `"   "` → Top-Level-Anlage wie A13
  (kein Fehler, kein `parent`-Schlüssel); `42`, `[]`, `{}`, `true` → 400, keine
  Datei; `path` im Body bleibt 400.
- **T19 `parent` fehlt im Bundle:** `aufgaben/gibtsnicht.md` → 400 (nicht 404),
  Meldung ohne Pfad, Bundle byte-identisch.
- **T20 `parent` falscher Ort/reserviert/Ausbruch:** `wellen/w1.md`,
  `projekt/phasen.md`, `aufgaben/index.md`, `../aufgaben/a1.md`, `/etc/passwd`, `""`
  → jeweils 400; `_aussen`-Vergleich wie `test_api_schreiben.py` unverändert.
- **T21 `parent` kein Task:** vorhandene `aufgaben/notiz.md` ohne `type: Task` und
  eine Datei mit kaputtem YAML unter `aufgaben/` → jeweils 400.
- **T22 Tiefe > 1:** Eltern-Pfad zeigt auf `aufgaben/a34.001-x.md` (selbst mit
  `parent`) → 400 („nur eine Ebene"), keine Datei unter `aufgaben/` angelegt; auch
  eine Top-Level-Datei, die selbst `parent` trägt, wird abgewiesen.
- **T23 Eltern ohne gültige Kennung:** Eltern mit Titel `"Neue Aufgabe"` (kein `A<N>:`)
  sowie Eltern mit Titel `"A99: X"` und Datei `a34-x.md` (inkonsistent) → jeweils
  400; Eltern mit Titel `"A34.001: X"` (Unter-Aufgabe) → 400.
- **T24 Eltern abgeschlossen:** Eltern `task_status: abgeschlossen` → 400, keine
  Datei; Gegenprobe `task_status: zur Abnahme` → 200 (erlaubt).
- **T25 Erschöpfung über die API:** `kennung.naechste_unterkennung` so gepatcht, dass
  sie `EingabeFehler` wirft → HTTP 400 mit `{error}` ohne Pfad, kein Schreibvorgang
  (die 999-Datei-Variante deckt T7 ab).
- **T26 Kennungskollision im Bestand:** zwei manuell angelegte Dateien mit
  `A34.001` (verschiedene Dateinamen) → neue Anlage erhält `002`, beide bestehenden
  Dateien byte-identisch, kein Fehler; Kind erhält weiterhin `freigabe: false`.
- **T27 Atomarität/A13-Regression:** alle 400-Fälle aus T18–T24 hinterlassen das
  Bundle byte-identisch (Hash über alle Dateien) und legen keine Datei an;
  `POST /api/task` **ohne** `parent` verhält sich unverändert (Slug, Kollisionssuffix
  `-2`, sechs Abschnitte, kein `parent`-Schlüssel).

**D. Read-Modell (`tests/test_unteraufgabe.py`, AK-1, AK-5)**

- **T28 `/api/aufgaben`:** Kind-Eintrag trägt `parent` (Rohpfad); Top-Level-Aufgabe
  und Wellen-/Projekt-Eintrag tragen den Schlüssel nicht; alle übrigen Felder
  (`status`, `owner`, `welle`, `arbeitsstatus…`) unverändert.
- **T29 `/api/overview`:** dito über den Gesamtbestand; Sortierung und Feldmenge
  unverändert, Antwort bleibt ein Array.
- **T30 `/api/file`:** Kind → `frontmatter.parent` roh, **kein** Top-Level-`parent`;
  `POST /api/meta` mit `{path, parent: "aufgaben/a1.md"}` → Datei unverändert
  (Feld wird ignoriert), keine `parent`-Änderung.
- **T31 Ungültige Bestandswerte:** `parent: ""`, `parent: 42`, `parent: []` in einer
  Datei → kein `parent`-Feld im Listeneintrag, kein Fehler, Detail rendert; Eintrag
  bleibt vollständig und sortiert.

**E. Frontend (`tests/test_unteraufgabe_ui.py`, AK-6, AK-7, AK-10)**

Harness: `tests/dom_helfer.py` (A30) + Fetch-Stub; beantwortet `/api/file`,
`/api/wellen`, `/api/aufgaben` und `POST /api/task`; unerwartete Requests schlagen
fehl (`ohne_node`-Skip wie A11/A27).

- **T32 Knopf-Sichtbarkeit:** Aufgabe ohne `parent`, nicht geschlossen → genau ein
  `#detail-unteraufgabe-anlegen` in `.detail-aktionen`, Text „Unter-Aufgabe
  anlegen"; Wellen-Datei, Projektdatei, Unter-Aufgabe (`frontmatter.parent`) und
  geschlossene Aufgabe → kein Knopf; A27-Statusknöpfe/owner-Auswahl bleiben
  unverändert.
- **T33 Formular öffnen/schließen:** Klick auf den Knopf → `#unteraufgabe-anlegen`
  sichtbar mit den fünf Feldern und Vorauswahl `mittel`; **kein** Request;
  „Abbrechen" → versteckt; erneuter Klick → wieder sichtbar (genau ein Formular).
- **T34 Erfolg:** ausfüllen + absenden → genau ein `POST /api/task` mit
  `{titel, ziel, akzeptanz: [...], prioritaet, parent}` (kein `welle`, kein
  `user_story`); Meldung „Unter-Aufgabe angelegt."; `GET /api/file` erneut geladen;
  das neue Kind erscheint im Abschnitt; Formular geschlossen/geleert; Knopf während
  des Requests `disabled`.
- **T35 Validierung:** leerer Titel / leeres Ziel / keine Akzeptanz / ungültige
  Priorität → je Feldmeldung aus A13, **kein** POST, Fokus auf erstem Fehlerfeld.
- **T36 Doppelklick/Fehlerpfad:** zwei Absendungen während eines laufenden Requests
  → ein POST, Knopf danach bedienbar; 400-Antwort `{error}` → Meldung sichtbar,
  Eingaben bleiben erhalten, kein Neuladen, kein zweiter POST.
- **T37 Abschnitt mit Kindern:** `/api/aufgaben` mit zwei Kindern (`A34.002`,
  `A34.001`) und einem fremden Kind (`A35.001`) → `h3` exakt
  `Unter-Aufgaben (2)`, Tabelle mit vier Spalten, genau zwei Zeilen mit den
  `data-path` der Kinder in Reihenfolge `A34.001`, `A34.002` (mtime bewusst
  umgekehrt), Abschnitt vor dem Nachtragsformular, Klassen `detail-abschnitt`.
- **T38 Keine Kinder:** erfolgreiche Antwort ohne Treffer → kein `h3`
  „Unter-Aufgaben", kein Abschnitt, kein Leerhinweis; Knopf bleibt vorhanden.
- **T39 Fehler/Format:** `/api/aufgaben` → `null` → Abschnitt mit
  „Unter-Aufgaben konnten nicht geladen werden."; Antwort `{}` → „Unter-Aufgaben
  haben ein unerwartetes Format."; kein Wurf.
- **T40 Abgrenzung:** Wellen-Detail → weiterhin nur „Aufgaben dieser Welle (n)",
  kein Unter-Aufgaben-Abschnitt; Projektdatei → nichts; Unter-Aufgabe mit (fehlerhaft)
  gesetzten Kind-Daten → kein Abschnitt; A27-Wellen-Dropdown unverändert.
- **T41 Geschlossene Aufgabe mit Kindern:** Abschnitt sichtbar (lesend), **kein**
  Anlegen-Knopf.
- **T42 XSS:** Kind-Titel `<img src=x onerror=alert(1)>` → textuell in der Tabelle,
  kein `img`-Knoten, kein `alert`; Abschnittsüberschrift bleibt textuell.
- **T43 Request-Zähler:** Detail einer Aufgabe = genau `/api/file`, `/api/wellen`,
  `/api/aufgaben` (drei Requests, auch für Unter-Aufgaben), kein weiterer;
  Projektdatei = ein Request.
- **T44 Quell-/Strukturprüfung:** `unteraufgaben.js` nutzt ausschließlich
  `textContent`/`createElement`/`classList` (kein `innerHTML`,
  `insertAdjacentHTML`, `document.write(`, `eval(`); `detail.js` importiert den
  Aufbau statt HTML zu bauen; `index.html` enthält weder `unteraufgabe` noch neues
  Markup; `style.css`, `app.js`, `api.js`, `liste.js`, `formulare.js` unverändert.
- **T45 Idempotenz:** zweimal `ladeDetail` auf denselben Pfad → genau ein Abschnitt,
  ein Knopf, ein Formular (keine Duplikate); Filter-/Statuswechsel erzeugt keine
  zweiten Knoten.
- **T46 Payload/Sortierung (Unit):** `erstellePayload(werte, pfad)` liefert
  `parent` als letztes Feld und kein `welle`; `unteraufgabenVon(eintraege, pfad)`
  filtert fremde Eltern heraus und sortiert stabil nach Unter-Nummer, dann `path`;
  `null`/Nicht-Array → `[]` ohne Wurf.

**F. Regression und Doku (AK-9, AK-10)**

- **T47 Baselines:** `test_neu_aufgabe.py`, `test_api_schreiben.py`, `test_meta.py`,
  `test_detail.py`, `test_liste.py`, `test_suche.py`, `test_welle_zuordnung.py`,
  `test_arbeitsstand*.py`, `test_freigabe*.py`, `test_static.py`, `test_okf_bundle.py`
  bleiben unverändert grün; die Suite wächst nur um die drei neuen Dateien und die
  additiven Fälle in `test_neue_aufgabe_signal.py`/`test_freigabe_ui.py`;
  `bash definitions/verify.sh .` → Exit 0.
- **T48 Unveränderte Dateien:** `git diff --stat` zeigt keine Änderung an
  `definitions/app/static/index.html`, `static/style.css`, `static/js/app.js`,
  `static/js/api.js`, `static/js/liste.js`, `static/js/formulare.js`,
  `static/js/features.js`, `static/js/projekt.js`, `definitions/app/server.py`,
  `meta.py`, `okf_bundle.py`, `status.py`, `arbeitsstand.py`, `neu_welle.py`,
  `freigabe.py`.
- **T49 Doku AGENTS (Review-Prüfschritt, kein pytest):** `AGENTS.md` und
  `definitions/AGENTS.md` enthalten `A{xxx}.{uuu}`/`a{xxx}.{uuu}-<slug>.md`, die
  App-Vergabe, „maximal eine Ebene", die erweiterten Prüfpflicht-Merkmale und den
  Satz, dass Unter-Aufgaben unter demselben Freigabe-Gate stehen. Nachweis mit
  Zitatstelle.
- **T50 Doku Phasenmodell/Spec (Review-Prüfschritt):** `wissen/projekt/phasen.md`
  enthält `parent` im Aufgabenformat; `wissen/projekt/technische-spec.md` enthält
  `parent` (Frontmatter/Read-Modell), `POST /api/task` mit `parent?`,
  `naechste_kennung` top-level-only und die Grammatik `A{xxx}.{uuu}`. Nachweis mit
  Zitatstelle.

**UI-Szenarien für den `tester` (Moli-Browser, laufende App gegen Test-Bundle):**

- **S1 Anlegen:** Aufgabe A34 öffnen → Knopf „Unter-Aufgabe anlegen" → Formular
  ausfüllen → „Unter-Aufgabe angelegt."; Abschnitt „Unter-Aufgaben (1)" mit
  `A34.001: …`; Datei `aufgaben/a34.001-….md` enthält `parent`, `freigabe: false`,
  `welle` der Eltern-Aufgabe.
- **S2 Zweite Unter-Aufgabe:** erneut anlegen → `A34.002`; Klick auf die Zeile öffnet
  die Unter-Aufgabe; dort **kein** Anlegen-Knopf (Tiefe 1); Zurück-Navigation
  funktioniert.
- **S3 Keine Kinder:** frische Aufgabe öffnen → kein Abschnitt „Unter-Aufgaben",
  Knopf vorhanden; nach dem ersten Anlegen erscheint der Abschnitt ohne Neuladen der
  Seite.
- **S4 Grenzen:** geschlossene Aufgabe → kein Anlegen-Knopf, Abschnitt (falls Kinder)
  lesend; Wellen-/Projektdatei → nichts; Titel mit HTML → nur Text, keine
  Konsolenfehler.
- **S5 Gate:** Unter-Aufgabe anlegen, ohne freizugeben → Status „Offen", KI beginnt
  nicht (Dokumentationsprüfung; keine Freigabe-Bedienung im Unter-Aufgaben-Abschnitt).

# Kontext

- **Anforderung (Projektleitung, 2026-11-15, aus der App angelegt):** „Wenn ich eine
  Aufgabe öffne kann ich eine Unter-Aufgabe anlegen"; „Wenn ich eine Aufgabe öffne
  sehe ich eine Liste der Unter-Aufgaben"; „Eine Aufgabe hat im Titel die Nummer
  `A{xxx.uuu}`, wobei u 001–999 sein kann". Die dritte Anforderung wird in A34
  **präzisiert**: `xxx` ist die Nummer der Eltern-Aufgabe, `uuu` dreistellig
  001–999; Top-Level-Aufgaben behalten `A<N>`.
- **Ist-Stand im Code (geprüft 2026-11-15, Arbeitsbaum mit A27-Frontend und A30
  Paket 1):**
  - `neu_aufgabe.anlegen(daten)` validiert `titel/ziel/akzeptanz/prioritaet` und
    optionale Verweise (`user_story`, `welle`) und schreibt über
    `okf_bundle.schreiben`; `_freier_pfad` erzeugt `<slug>.md` mit Suffix `-2`, `-3`.
    Unbekannte Felder werden heute **stillschweigend ignoriert** — `parent` muss
    deshalb explizit aufgenommen werden (sonst entstünde eine Unter-Aufgabe ohne
    Elternbezug).
  - `server.api_task` reicht den JSON-Body unverändert an `neu_aufgabe.anlegen`
    weiter und verbietet nur `path` → **keine `server.py`-Änderung nötig**.
  - `overview._eintrag` baut Listeneinträge (`path, typ, titel, status, owner,
    zuletzt_geaendert, welle?, hinweis?`) und ergänzt A30-Felder; `details` liefert
    `{frontmatter, markdown, nachtraege}` plus A30-Felder. A28 ergänzt dort
    `neu`/`kennung`/`naechste_kennung` — A34 erweitert **dieselbe** Stelle.
  - `detail.js` hat in `erstelleAktionen` das Muster für Kopfaktionen, in
    `erstelleAufgabenSicht` das Muster „Abschnitt + `erstelleTabelle`" (A27) und in
    `erstelleNachtragFormular` das Muster „Inline-Formular mit `try/finally` und
    Reload". `zeichne()` setzt die Reihenfolge Kopf → Inhalt → Abschnitt → Nachtrag.
  - `formulare.js` exportiert `validiereAufgabe`, `teileAkzeptanz`,
    `erstelleAufgabePayload`, `leseAngelegtenPfad` — wiederverwendbar, ohne
    `formulare.js` zu ändern (kein Zyklus: `formulare.js` importiert nur `liste.js`).
  - `app.js` öffnet Detailzeilen über `click`-Delegation auf `tr[data-path]` →
    Tabellenzeilen im Unter-Aufgaben-Abschnitt sind ohne Zusatzcode klickbar.
  - `liste.js` erhält in A30 Paket 2 die Arbeitsstatus-Zeile in der Status-Zelle;
    A34 ändert `liste.js` **nicht** und bekommt die Zeile automatisch.
- **Entscheidungen (mit Begründung, reversibel):**
  1. **Feldname `parent`, Wert = bundle-relativer Pfad** (nicht `eltern`): genau ein
     Elternteil (Singular), Wertform identisch zu `welle` (Pfad einer existierenden
     Datei), für KI und Mensch ohne App lesbar, keine Kollision mit bestehenden
     Feldern. *Verworfen:* `eltern` (Plural suggeiert mehrere Eltern),
     `parent_id`/`unteraufgabe_von` (länger, keine Präzedenz), Kennung als Wert
     (`A34` — bricht bei Umbenennung und ist nicht eindeutig auflösbar).
  2. **Dateiname `a{xxx}.{uuu}-<slug>.md` mit Punkt** (nicht `a{xxx}-{uuu}-…`):
     Punkt trennt Nummerierungsebenen, Bindestrich gehört zum Slug; `A28`-Muster
     `^a(\d+)(?:-|$)` liest `a34-001-x.md` sonst als **A34 mit Slug `001-x`** und
     würde eine Unter-Aufgabe stillschweigend als Top-Level-Aufgabe behandeln. Mit
     Punkt schlägt die alte Erkennung **laut** fehl (`neu: true`), bis A34 sie
     erweitert — fail-loud statt still falsch. Titel und Dateiname sind 1:1
     abbildbar (`A34.001` ↔ `a34.001`), was A28s Konsistenzprüfung direkt vergleicht.
  3. **Nur eine Ebene (Tiefe 1):** Die geforderte Grammatik `A{xxx.uuu}` hat genau
     eine Unter-Ebene; `A34.001.002` wäre eine neue Grammatik. Eine Eltern-Aufgabe
     ohne `parent` zu sein, macht Zyklen strukturell unmöglich (kein Zyklus-Check
     nötig). Erweiterung später ohne Migration möglich (neue Grammatik + eigener
     Beschluss). Serverseitig 400, in der UI kein Knopf.
  4. **App vergibt die Unter-Kennung beim Anlegen:** Die Elternnummer steht fest, der
     Unter-Nummernraum ist lokal und erschöpfend durchsuchbar; damit erfüllt jede
     angelegte Aufgabe die Anforderung „Nummer im Titel" **ohne** manuelles Tippen
     und ohne Kollision. Ein mitgegebenes Präfix wird entfernt (idempotent, kein
     `A34.001: A34.001: …`). Die KI bleibt Herrin der **Top-Level**-Nummern
     (A28-Regel); für Unter-Nummern gilt: App vergibt, KI ändert nicht.
  5. **Kleinste freie Unter-Nummer statt max+1:** füllt Lücken, ist deterministisch
     und verhindert doppelte Kennungen auch nach manuellem Löschen. Belegt zählt
     sowohl `parent` als auch eine Titel-/Datei-Kennung mit derselben Elternnummer
     (deckt manuell umbenannte/vergessene `parent`-Felder ab). Weiterhin **keine
     Reservierung** (A28-Linie): zwei parallele Anlagen können dieselbe Nummer
     sehen; der zweite Schreibvorgang erhält durch die erneute Zählung im
     Anlagepfad die nächste freie Nummer, `_freier_pfad` bleibt als Sicherheitsnetz.
  6. **`welle` erben, `welle`+`parent` zusammen ablehnen:** Die Unter-Aufgabe gehört
     fachlich zur Welle der Eltern-Aufgabe (sonst fehlt sie in der A27-Wellen-Sicht
     und im A29-Wellen-Gate). Zwei Quellen (Formularwert und Elternwert) wären eine
     Zweitwahrheit → 400 statt stiller Priorisierung.
  7. **Inline-Formular statt Weiterleitung auf das A13-Formular:** Anforderung 1
     verlangt Anlegen **aus der geöffneten Aufgabe**; ein Sprung auf die
     Aufgaben-Ansicht würde Kontext und Elternbezug verlieren und bräuchte eine neue
     Hash-Route/`app.js`-Änderung (eingefrorener Router-Vertrag). Das Inline-Formular
     nutzt die A13-Validierung/-Payload (eine Regelquelle) und lädt nach Erfolg nur
     das Detail neu — die Liste im selben Blickfeld aktualisiert sich.
  8. **Anzeige über `GET /api/aufgaben` + Client-Filter** (analog A27-Wellen-Sicht)
     statt neuem Endpunkt oder `unteraufgaben` in `/api/file`: ein Endpunkt weniger,
     ein Muster, `parent` ist ohnehin im Read-Modell nötig (Liste/Filter). Kosten:
     ein zusätzlicher Request im Aufgaben-Detail (dokumentiert und getestet in T43;
     A28s Request-Zähler wird nachgezogen).
  9. **Sortierung nach Unter-Nummer, nicht mtime:** Die Nummer ist der
     Ordnungsvertrag der Unter-Aufgaben; mtime würde nach jedem Edit springen
     (A27 nutzt mtime, weil dort keine Ordnung existiert).
  10. **Kein Abschnitt bei null Kindern, aber fail-loud bei Ladefehler:** „keine
      Anzeige, wenn keine Kinder" ist Anforderung; ein fehlgeschlagener Request darf
      aber nicht als „keine Kinder" getarnt werden (A11/A27-Linie).
  11. **Kein `freigabe`-Schreibpfad, keine Sammelfreigabe:** A28 bleibt die einzige
      Freigabe-Instanz (Mensch, 403 für KI). Unter-Aufgaben sind eigenständige
      Aufgaben und brauchen ihre eigene Freigabe; A34 schreibt nur `freigabe: false`
      (über A28s `_inhalt`).
  12. **Ein neues Modul `kennung.py`, ein neues UI-Modul `unteraufgaben.js`:**
      Die Grammatik ist an zwei Stellen nötig (`overview` für A28-Felder,
      `neu_aufgabe` für Vergabe) — eine Implementierung verhindert Drift. Das
      UI-Modul hält `detail.js` klein und ist ohne Detail-Kontext testbar.
- **Konfliktgruppen (neu):**
  - **G24 „Kennungsgrammatik + Read-Modell":** `kennung.py` (**neu**),
    `overview.py`, `tests/test_kennung.py` (**neu**), `tests/test_neue_aufgabe_signal.py`
    (additiv). Überschneidet sich mit **A28-G15** (`overview.py`), **A29-G18**
    (`overview.py`) und A30-G21 → erst nach A28 **und** A29 Paket 1.
  - **G25 „Anlage Unter-Aufgabe":** `neu_aufgabe.py`, `tests/test_unteraufgabe.py`
    (**neu**), `tests/test_neu_aufgabe.py` (nur falls additiv nötig). Überschneidet
    sich mit **A28-G15** (`neu_aufgabe.py`) und **A33-B4/B7** (`neu_aufgabe.py`,
    `slug.py`) → nach A28, nicht parallel zu A33.
  - **G26 „Unter-Aufgaben-UI":** `static/js/detail.js`, `static/js/unteraufgaben.js`
    (**neu**), `tests/test_unteraufgabe_ui.py` (**neu**), `tests/test_freigabe_ui.py`
    (Request-Zahl, additiv). Überschneidet sich mit **A27-G14**, **A28-G16**,
    **A29-G19**, **A30-G22** und **A33-B8** (`detail.js`) → nach A29 (UI) und nach
    A33-B8 (oder A33-B8 nach A34 verschieben).
  - **G27 „Doku/Regelwerk":** `AGENTS.md`, `definitions/AGENTS.md`,
    `wissen/projekt/phasen.md`, `wissen/projekt/technische-spec.md` — überschneidet
    sich mit **A28-G17**, **A29-G20**, **A30-G23** und **A33-B9** → nach deren
    Doku-Paketen; parallel zu G26 möglich.
- **Aufteilung in Pakete (ein Coder, eine Aufgabe):**
  - **Paket 1 — Kennungsgrammatik + Read-Modell:** `kennung.py`
    (`zerlege_titel`, `zerlege_dateiname`, `kennung_aus_*`, `eltern_kennung`,
    `ist_zugewiesen`, `naechste_kennung`, `naechste_unterkennung`), Umstellung der
    A28-Muster in `overview.py` auf Importe, `parent` in `_eintrag`.
    Tests: T1–T12, T28–T31.
  - **Paket 2 — Anlage mit `parent`:** `neu_aufgabe.py` (`_eltern`-Validierung,
    Kennungsvergabe, Slug aus bereinigtem Titel, `welle`-Vererbung, `parent` in
    `_inhalt`).
    Tests: T13–T27.
  - **Paket 3 — UI:** `static/js/unteraufgaben.js`
    (`unteraufgabenVon`, `sortiereUnteraufgaben`, `erstelleUnteraufgabenSicht`,
    `erstelleAnlegeSicht` → `{bereich, knopf}`, `erstellePayload`),
    Verdrahtung in `detail.js` (Knopf in `erstelleAktionen`, Formular nach dem Kopf,
    Abschnitt nach dem Inhalt, `/api/aufgaben` für alle Tasks laden).
    Tests: T32–T46.
  - **Paket 4 — Doku:** AK-9; Prüfschritte T49/T50; parallel zu Paket 3
    (disjunkte Dateien).
  - **Reihenfolge im Paket:** Test schreiben → rot → Minimum → grün → nächster Test.
    Paket 1 → 2 (2 braucht die Grammatik), 3 nach 2 und nach A29-UI, 4 parallel zu 3.
    Paket 1 und 2 teilen keine Datei, hängen aber über `kennung.py` zusammen →
    nacheinander vom selben Coder.
- **Reihenfolge-Empfehlung und Freigabe-Gate:**
  1. **A27 abschließen** (Baseline `detail.js`/`liste.js`), **A30** (Arbeitsstatus in
     `liste.js`/`detail.js`, `overview.py`) und **A31** (Wellen-Spalte) abschließen.
  2. **A28 abschließen** — A34 erweitert A28s Regexe und setzt `freigabe: false`
     voraus; ohne A28-Paket 0/1 ist A34 nicht testbar. Danach **A29**.
  3. **A34 Paket 1+2** können starten, sobald **A29 Paket 1** (Backend `overview.py`)
     committed ist — parallel zu A29 Paket 2 (UI, `detail.js`), weil A34 Backend
     `detail.js` nicht anfasst. **A34 Paket 3** (UI) erst nach A29 Paket 2 **und**
     A33-B8. **A34 Paket 4** parallel zu Paket 3, aber nach A28/A29/A30/A33-Doku.
  4. **Freigabe-Gate für A34 selbst:** Die Datei trägt (Stand heute) kein
     `freigabe`-Feld, weil A28 noch nicht umgesetzt ist. Start nur mit dokumentierter
     Freigabe der Projektleitung; sobald A28-Paket 0 steht, `freigabe: true`
     nachtragen (Mensch-Kanal) und A34 erst danach beauftragen.
  5. Nach A34: Review, Test (S1–S5), Doku; danach sind `detail.js`/`overview.py`
     wieder frei (A35/A36 aus A33 können folgen).
- **Abhängigkeiten:** A4 (`neu_aufgabe`, Slug/Kollision), A8/A11 (`overview`-Felder,
  `erstelleTabelle`), A9 (`POST /api/task`-Validierung), A12 (`detail.js`-Kopf,
  Inline-Formular-Muster), A13 (`validiereAufgabe`/Payload/Kurzkontext), A27
  (Wellen-Sicht-Muster, `welle`), A28 (**Pflicht**: `freigabe`, Regexe, `neu`/
  `kennung`/`naechste_kennung`), A29 (Dateifreigabe `overview.py`/`detail.js`),
  A30 (`dom_helfer.py`, Arbeitsstatus-Zeile). A33 ist nur Dateikonflikt, keine
  fachliche Abhängigkeit.
- **Risiken/Grenzen:**
  (a) **Ein zusätzlicher Request** im Aufgaben-Detail (`/api/aufgaben`) — bewusst,
  dokumentiert, in T43 fixiert; Alternative (Kinder in `/api/file`) wurde verworfen
  (größere Antwort, zweite Filterlogik).
  (b) **Nur eine Ebene** ist eine bewusste Beschränkung; ein späterer Bedarf an
  Tiefe 2 erfordert eine neue Grammatik (`A34.001.001`) und eine Migration der
  Anzeige.
  (c) **Manuell falsch benannte Dateien** (`a34-001-x.md` als Unter-Aufgabe) werden
  von der Erkennung als Top-Level A34 gelesen; das ist gewollt fail-loud (`neu`
  bleibt/ wird `true`, solange Titel und Datei nicht zusammenpassen) und wird im
  Review geprüft.
  (d) **Parallele Anlagen** können kurzzeitig dieselbe Nummer berechnen; der
  Schreibpfad zählt erneut und `_freier_pfad` verhindert Überschreiben — eine echte
  Reservierung gibt es nicht (A28-Linie).
  (e) **Geschlossene Eltern-Aufgabe** blockiert neue Kinder; die Projektleitung muss
  die Aufgabe ggf. wieder öffnen (nur PM/KI kann `task_status` ändern) — bewusst
  gegen „versteckte Arbeit unter abgeschlossen".
  (f) **A28s Request-Zähler** (`test_freigabe_ui.py`) muss mit A34 von zwei auf drei
  Requests nachgezogen werden — sonst rot; als additive Änderung eingeplant.
- **Offene Fragen an den PM (Standardentscheidung in Klammern, nicht blockierend):**
  1. Sollen Unter-Aufgaben in der normalen Aufgabenliste erscheinen? *(Standard: ja,
     unverändert — sie sind Aufgaben; eine verschachtelte/einklappbare Liste wäre eine
     eigene Aufgabe.)*
  2. Tiefe > 1 erlauben? *(Standard: nein — die geforderte Grammatik hat eine
     Unter-Ebene; serverseitig 400.)*
  3. Kinder unter einer abgeschlossenen Eltern-Aufgabe? *(Standard: nein — 400; die
     Eltern-Aufgabe wird bei Bedarf wieder geöffnet.)*
  4. Wer vergibt die Unter-Kennung? *(Standard: die App beim Anlegen; Eingaben mit
     Präfix werden normalisiert.)*
  5. Welle erben oder im Formular wählen? *(Standard: erben; `welle` + `parent`
     zusammen = 400.)*
  6. Braucht jede Unter-Aufgabe eine eigene Freigabe? *(Standard: ja — A28-Regel je
     Aufgabe; keine Sammelfreigabe über die Eltern-Aufgabe.)*
  7. Sollen Unter-Aufgaben in der Übersicht/Aufgabenliste eine Marke „Unter-Aufgabe"
     tragen? *(Standard: nein — die Kennung `A34.001` ist die Marke; eigene Aufgabe,
     falls gewünscht.)*

# Betroffene Dateien

- `definitions/app/kennung.py` (**neu**) — einzige Kennungsgrammatik:
  `zerlege_titel`, `zerlege_dateiname`, `kennung_aus_titel`, `kennung_aus_dateiname`,
  `eltern_kennung`, `ist_zugewiesen`, `naechste_kennung` (top-level-only),
  `naechste_unterkennung(pfad)` (kleinste freie 001–999, `EingabeFehler` bei
  Erschöpfung); nutzt `okf_bundle.scan`/`lesen_tolerant` (T1–T8).
- `definitions/app/neu_aufgabe.py` — `_pruefe` nimmt optional `parent` auf,
  `_eltern(wert)` validiert (Existenz, `aufgaben/`, nicht reserviert, `type: Task`,
  keine Tiefe 2, nicht `abgeschlossen`, gültige Top-Level-Kennung), `welle`-Vererbung,
  `_inhalt` schreibt `parent` in fester Position (nach `welle`, vor `owner`),
  Slug aus bereinigtem Titel, `_freier_pfad` mit Kennungspräfix (T13–T27).
- `definitions/app/overview.py` — A28-Muster durch Importe aus `kennung.py` ersetzen
  (Verhalten unverändert), `parent` in `_eintrag` (nur Tasks, nur nicht-leerer String)
  (T9–T12, T28–T31).
- `definitions/app/static/js/unteraufgaben.js` (**neu**) —
  `unteraufgabenVon(eintraege, elternPfad)`, `sortiereUnteraufgaben`,
  `erstelleUnteraufgabenSicht(pfad, aufgaben)` (Abschnitt oder `null`),
  `erstelleAnlegeSicht(pfad, beiErfolg)` → `{bereich, knopf}`,
  `erstellePayload(werte, pfad)`; ausschließlich `textContent`/`createElement`/
  `classList`, wiederverwendet `erstelleTabelle` und die A13-Helfer (T32–T46).
- `definitions/app/static/js/detail.js` — Knopf „Unter-Aufgabe anlegen" in
  `erstelleAktionen` (nur Task, ohne `parent`, nicht geschlossen), Formularbereich
  nach dem Kopf, Abschnitt nach dem Inhalt (vor dem Nachtragsformular),
  `/api/aufgaben` auch für Aufgaben laden, Reload nach Erfolg (T32–T45).
- `definitions/app/tests/test_kennung.py` (**neu**) — T1–T8.
- `definitions/app/tests/test_unteraufgabe.py` (**neu**) — T13–T31 (Flask-Client,
  `bundle`-Fixture, zusätzliche Dateien unter `tmp_path`).
- `definitions/app/tests/test_unteraufgabe_ui.py` (**neu**) — T32–T46; nutzt
  `tests/dom_helfer.py` (A30), keine neue Harness-Kopie.
- `definitions/app/tests/test_neue_aufgabe_signal.py` — additiv T9–T12
  (Unter-Kennung in `neu`/`kennung`/`naechste_kennung`).
- `definitions/app/tests/test_freigabe_ui.py` — additiv: Request-Zahl im
  Aufgaben-Detail drei statt zwei (T43); keine Verhaltensänderung an A28-Signalen.
- `AGENTS.md` **und** `definitions/AGENTS.md` — Kennungsregel um `A{xxx}.{uuu}`/
  `a{xxx}.{uuu}-<slug>.md` erweitern, App-Vergabe, Tiefe 1, Prüfpflicht-Merkmale,
  Freigabe-Gate für Unter-Aufgaben (AK-9, T49).
- `wissen/projekt/phasen.md` — `parent` und Kennungsschema im Format der
  Aufgaben-Datei (AK-9, T50).
- `wissen/projekt/technische-spec.md` — `parent` in Frontmatter-/Read-Modell-Tabelle,
  `POST /api/task` mit `parent?`, Grammatik `A{xxx}.{uuu}`,
  `naechste_kennung` top-level-only (AK-9, T50).
- **Nicht geändert:** `definitions/app/static/index.html` (eingefroren seit A10),
  `static/style.css`, `static/js/app.js`, `static/js/api.js`, `static/js/liste.js`,
  `static/js/formulare.js`, `static/js/features.js`, `static/js/projekt.js`,
  `definitions/app/server.py`, `meta.py`, `okf_bundle.py`, `status.py`,
  `arbeitsstand.py`, `neu_welle.py`, `freigabe.py`,
  `tests/test_neu_aufgabe.py` (außer additiven Fällen, falls nötig),
  `tests/test_detail.py`, `test_liste.py`, `test_suche.py`,
  `test_welle_zuordnung.py`, `test_arbeitsstand*.py`, `test_api_lesen.py`,
  `test_api_schreiben.py`, `test_meta.py`, `test_static.py`, `test_okf_bundle.py`.
  `wissen/aufgaben/index.md` und Statusfelder pflegt ausschließlich PM/`documenter`.

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

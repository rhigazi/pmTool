---
type: Task
title: "A23: Feature-Liste (Menüpunkt + Feature-Status)"
description: Die Feature List erscheint nicht im Menü, es sollte möglich sein über
  die Feature List zu jedem Feature zu sehen welche Aufgaben noch offen sind welche
  umgeset…
task_status: abgeschlossen
phase: 8 Abgeschlossen
priority: hoch
assigned_to: coder
owner: ai
---

# Ziel

Die Feature List erscheint nicht im Menü, es sollte möglich sein über die Feature List zu jedem Feature zu sehen welche Aufgaben noch offen sind welche umgesetzt wurden.

# Akzeptanzkriterien

- Ich klicke auf Feature List es öffnet sich eine Liste aller Features ich sehe den Status des jeweiligen Features wenn ich ein Feature anklicke sehe ich die zuständigen Aufgaben die noch in Bearbeitung sind oder schon erledigt sind

# Testfälle (TDD)

**Zuordnung zum Akzeptanzkriterium** (das AK der Projektleitung enthält zwei Sätze, daher zwei Prüfbereiche):
**AK-1** „Menüpunkt *Feature List* öffnet eine Liste aller Features mit ihrem Status" → T1–T11 (Gerüst, Navigation, Parser), T16 (Listen-Rendering), T19 (Fehlerfälle der Liste), T20 (Zähler 0), T23 (Regression).
**AK-2** „Klick auf ein Feature zeigt die zuständigen Aufgaben mit Status (offen / in Bearbeitung / erledigt)" → T12–T15 (Gruppierung, Join, Zuordnungslücken), T17–T18 (Detail-Rendering, XSS), T21–T22 (Slug-/Container-Fehler, HTTP-Läufe).

Reihenfolge = Red-Green-Takt: erst Test schreiben, rot laufen lassen, dann das Minimum implementieren.

**A. Gerüst, Navigation, Verträge (AK-1)**

- **T1 Menüpunkt und View-Container:** `index.html` lesen → in `<nav>` genau ein Link `href="#/features"` mit Text `Feature List`; im `<main>` genau eine Sektion `id="ansicht-features"` mit `data-ansicht="features"` und darin `id="liste-features"`. Bestehende fünf Navigationspunkte, Projekt-Unterpunkte und alle vorhandenen Container bleiben wortgleich vorhanden (nur additive Ergänzung).
- **T2 Router-Verdrahtung:** `app.js` enthält `features: "ansicht-features"` in `ANSICHTEN`, importiert `./features.js` und ruft `registriereAnsicht("features", …)` auf. DOM-Lauf mit Router: Hash `#/features` → `ansicht-features` ist die einzige sichtbare Sektion (`hidden === false`), alle anderen sind `hidden`; Fehlerbereich ist leer.
- **T3 Navigation aktiv bei Detailroute:** Hash `#/features/okf-projekt-manager-spa` → der Link „Feature List" trägt `class="… aktiv"` und `aria-current="page"`, andere Links nicht. ~~(Erfordert die kleine Erweiterung der Unterpunkt-Regel in `markiereNavigation`; T3 ist rot, solange `features` dort nicht als Container-Basis geführt wird.)~~ **Falsche Planvorgabe, bewusst nicht umgesetzt (Review bestätigt 2026-11-15):** Der Feature-Link trägt kein `data-unterpunkt`; die bestehende Regel liefert bereits `true`, T3 ist ohne Änderung grün. Die vorgeschlagene Erweiterung hätte T3 rot gemacht — nicht nachholen.
- **T4 Kein neuer Server-Endpunkt, keine HTML-Senke:** Quelltext von `features.js` enthält als `/api/…`-Vorkommen ausschließlich `/api/file` und `/api/aufgaben`, kein `postJson`; `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write(` und `eval(` kommen nicht vor, `textContent` und `classList` schon. `server.py` bleibt unverändert (kein neuer `@app.get`).
- **T5 Menüpunkt ist erreichbar:** HTTP `GET /` gegen Test-Bundle → 200, HTML enthält `#/features` und `liste-features` (statischer Auslieferungsweg, kein Server-Sonderfall).

**B. Parser `parseFeatures` (reine Logik über Node, AK-1)**

- **T6 Reale Struktur:** Fixture, das `wissen/features.md` nachbildet (Frontmatter, `# Statuswerte`, `# Regeln`, `# Offene Features`, `# Umgesetzte Features`) → `parseFeatures(markdown)` liefert in Dateireihenfolge `[{titel, pfad, slug, status, hinweis, prioritaet, aufgaben}]` mit `titel: "OKF Projekt-Manager (SPA)"` (Klammern im Titel!), `pfad: "features/okf-projekt-manager-spa.md"`, `slug: "okf-projekt-manager-spa"`, `status: "umgesetzt"`, `hinweis: "MVP abnahmefähig (Abnahme durch Projektleitung ausstehend)"`, `prioritaet: "hoch"` und den Aufgaben-Pfaden aus den eingerückten Unterpunkten (`aufgaben/a1-okf-bundle.md`, `aufgaben/a2-status-mapping.md`, …) in Dateireihenfolge.
- **T7 Abschnittsgrenzen:** Bullets aus `# Regeln` (Text enthält `/features/` und `/aufgaben/`) und aus `# Offene Punkte` (z. B. `* [A22](aufgaben/a22-e2e-regression.md) …`) erzeugen **kein** Feature und keine Aufgaben-Zuordnung. Nur Bullets zwischen `# Offene Features` bzw. `# Umgesetzte Features` und der nächsten `# `-Überschrift sind Feature-Einträge.
- **T8 Status- und Prioritätsvarianten:** Feature-Zeilen mit `**offen**`, `**in Umsetzung**`, `**umgesetzt — Text**` (Halbgeviertstrich), `**pausiert**` sowie `Priorität **mittel**`/`**niedrig**` ergeben den jeweiligen Status samt Hinweis-Text; die Priorität `**hoch**` wird nicht als Status missverstanden (Status ist nur eines der vier Wörter `offen`/`in Umsetzung`/`umgesetzt`/`pausiert` am Segmentanfang).
- **T9 Fehlender und unbekannter Status:** Feature-Zeile ohne Statuswort → `status: "offen"`, `hinweis: "ohne Status"`. Unbekanntes Wort (`**in Arbeit**`) → `status: "offen"`, `hinweis: "in Arbeit"` (Spiegel von `status.ui_status`). Kein Wurf, keine stille Leeranzeige.
- **T10 Mehrere Features und Zuordnung:** Zwei Feature-Bullets; Aufgaben-Links des ersten landen nur beim ersten, ein Feature ohne Unterpunkte hat `aufgaben: []`; ein dritter Top-Level-Bullet mit `aufgaben/`-Link außerhalb eines Feature-Abschnitts wird ignoriert. Doppelt verlinkte Aufgabe wird dedupliziert (Reihenfolge des ersten Vorkommens).
- **T11 Parser-Randfälle:** `""`, `"   "`, `null`, `42` → `[]`. CRLF-Zeilen werden verarbeitet. Ziel mit Leerzeichen/`%20` im Link wird dekodiert. Bullet ohne Markdown-Link (`* **fett** …`) und Link ohne `.md`-Endung erzeugen keinen Feature-Eintrag. Abschnitte vorhanden, aber ohne Einträge → `[]` (die Ansicht zeigt dann „Keine Features."); **gar kein Feature-Abschnitt** → Parser meldet einen Formatfehler (`wirft`/`{fehler}`), damit ein umbenannter Abschnitt nicht als „keine Features" durchgeht.

**C. Gruppierung und Join (reine Logik über Node, AK-2)**

- **T12 Statusgruppen (6 UI-Status → 3 Anzeigegruppen):** `gruppeAufgaben` bildet `Klarung`→`offen`, `Offen`→`offen`, `In Arbeit`→`inBearbeitung`, `Testing`→`inBearbeitung`, `Dokumentation`→`inBearbeitung`, `Geschlossen`→`erledigt`. Jede Gruppe behält die Eingabereihenfolge, jede Aufgabe erscheint genau einmal, `{offen: n, inBearbeitung: n, erledigt: n}` passt zur Summe. Leere Eingabe → drei leere Gruppen mit Zähler 0.
  *Begründung der Zuordnung:* `Klarung` ist „noch nicht in Arbeit" (Rückfrage an den Menschen, `status.py`-owner `mensch`) → offen; `In Arbeit`/`Testing`/`Dokumentation` sind die laufenden Pipeline-Schritte (Umsetzung, Prüfung, Doku) → in Bearbeitung; nur `Geschlossen` erfüllt die DoD → erledigt. `pausiert` kommt als UI-Status `Offen` mit Hinweis und fällt damit korrekt nach „offen".
  *Unbekannter Statuswert* (nur defensiv möglich, `status.py` liefert immer einen der sechs) → Gruppe `offen` **mit sichtbarem Hinweis** statt Verwerfen; ein einzelner Ausreißer darf die Ansicht nicht in einen Fehlerzustand kippen.
- **T13 Join gegen `/api/aufgaben`:** Aufgaben-Pfade aus dem Feature gegen die API-Liste (Schlüssel `path`) → je Aufgabe `{path, titel, status, hinweis}` aus der API; Status-Anzeige ist der API-UI-Status (inkl. `hinweis` z. B. `pausiert`), nicht der rohe `task_status`.
- **T14 Link ohne API-Eintrag:** In `features.md` verlinkte, aber in `/api/aufgaben` fehlende Datei → landet **nicht** in den drei Gruppen, sondern in einer Warnliste `{pfad, grund: "nicht gefunden"}`; die Ansicht bleibt nutzbar und zeigt die Warnung sichtbar (z. B. „In features.md verlinkt, aber nicht gefunden: aufgaben/a99-xy.md").
- **T15 Aufgabe ohne Feature-Zuordnung:** `/api/aufgaben`-Einträge, deren `path` in keinem Feature vorkommt, erscheinen in keiner Feature-Detailansicht; die Liste zeigt am Ende einen Sammelhinweis „N Aufgaben ohne Feature-Zuordnung" mit der Anzahl (nur wenn > 0). Gemessen wird gegen den echten Fixture-Zustand (A23 selbst ist bis zur Verlinkung in `features.md` genau so ein Fall).

**D. Rendering im DOM-Harness (AK-1/AK-2)**

- **T16 Liste:** `ladeFeaturesAnsicht({unterpunkt: ""})` rendert je Feature einen Link `#/features/<slug>` mit Titel, Statusmarke (Wortlaut aus `features.md`, Hinweis in Klammern), Priorität und Zählern „n offen · n in Bearbeitung · n erledigt"; Reihenfolge wie in der Datei. Requests: genau `GET /api/file?path=features.md` und `GET /api/aufgaben`, nichts anderes.
- **T17 Detail:** `ladeFeaturesAnsicht({unterpunkt: "okf-projekt-manager-spa"})` rendert Feature-Titel, Status, drei Gruppenüberschriften mit Zählern, je Aufgabe einen Link `#/detail/<urlencoded pfad>` mit Titel und Statusmarke, und einen Rückweg `#/features`. Keine Gruppe ist leer dargestellt, wenn Aufgaben vorhanden sind; `#/detail/aufgaben%2Fa1-okf-bundle.md` ist dekodiert genau der API-Pfad.
- **T18 XSS:** Feature-Titel bzw. Aufgaben-Titel mit `<img src=x onerror=alert(1)>` bleibt reiner Text: keine `img`/`script`-Knoten im Container, `alert` wird nicht aufgerufen, Linktext enthält das Literal.
- **T19 Fehlerfälle fail-loud (je eigener Fall, alle rot vor der Umsetzung):**
  (a) `features.md` fehlt (404) → Meldung im Container **und** im Fehlerbereich, keine Feature-Links, kein leerer Screen;
  (b) `features.md` unlesbar (HTTP 500 mit `error`) → gleiche Erwartung, Servermeldung wird angezeigt;
  (c) Antwort ohne `markdown`-String (z. B. `{"markdown": 42}`) → „unerwartetes Format", Fehlerbereich sichtbar;
  (d) Dokument ohne Feature-Abschnitt → Formatfehler statt „Keine Features.";
  (e) `/api/aufgaben` liefert 500 → Fehlermeldung statt Teilliste mit falschen Zählern;
  (f) `/api/aufgaben` liefert ein Objekt statt Array → Formatfehler.
- **T20 Feature ohne Aufgaben:** Feature mit `aufgaben: []` → Detail zeigt Status des Features und den Hinweis „Keine Aufgaben zugeordnet." (keine drei leeren Gruppen); Liste zeigt Zähler 0/0/0.
- **T21 Unbekannter Slug / fehlender Container:** `{unterpunkt: "gibtsnicht"}` → Meldung „Unbekanntes Feature: gibtsnicht" im Container plus Fehlerbereich, keine Aufgabenliste. Fehlt `liste-features` im DOM → Meldung mit Container-ID im Fehlerbereich, **kein** Request (`aufrufe == []`). Fehlt zusätzlich der Fehlerbereich → kein Absturz (`return {ok: true}`).
- **T22 HTTP-Läufe gegen Test-Bundle:** Server via `make_server` + `server.create_app(tmp_path/bundle)`, Node-Proxy-Fetch (Muster `test_projekt.py`) → Liste und Detail liefern die erwarteten Titel/Status/Gruppen aus echten Dateien. Zusätzlich Fehlerbundles: Bundle ohne `features.md`, Bundle mit `features.md` ohne Feature-Abschnitt. **Nie gegen `wissen/`** (Testisolation, siehe Kontext).
- **T23 Regression:** `test_static.py`, `test_liste.py`, `test_detail.py`, `test_projekt.py`, `test_formulare.py` bleiben unverändert grün; die Gesamtsuite wächst nur um `test_features.py`. `verify.sh` bleibt Exit 0.

**UI-Szenarien für den `tester` (Moli-Browser, laufende App gegen Test-Bundle):**

- **S1 Menü → Liste:** Menüpunkt „Feature List" anklicken → Liste aller Features mit Statusmarke erscheint, kein Konsolenfehler.
- **S2 Feature → Aufgaben:** erstes Feature anklicken → Kopf mit Feature-Status, drei Gruppen mit den zugehörigen Aufgaben und deren Status; Zurück-Link führt zur Liste.
- **S3 Aufgabe öffnen:** Aufgabe im Feature-Detail anklicken → A12-Detail der Aufgaben-Datei (Status/owner sichtbar), Zurück zur Feature-Liste über das Menü.
- **S4 Fehlerfall:** App gegen ein Bundle ohne `features.md` starten → sichtbare deutsche Fehlermeldung, keine leere Seite, keine Konsolenfehler (fail-loud).

# Kontext

**PM-Festlegungen (2026-11-15, zu den 7 Planner-Fragen; Begründungen im Detail in den folgenden Kontext-Punkten):**

- **Menü-Label:** „Feature List" — Position direkt nach „Aufgaben".
- **Feature-Status:** wortgleich aus `features.md` (`offen` / `in Umsetzung` / `umgesetzt` / `pausiert`), kein Mapping auf die sechs UI-Status.
- **Aufgaben ohne Feature-Zuordnung:** Sammelhinweis am Listenende („N Aufgaben ohne Feature-Zuordnung"), nur bei n > 0.
- **Klick auf eine Aufgabe:** öffnet die bestehende A12-Detailansicht (`#/detail/<pfad>`), keine eigene Aufgaben-Ansicht.
- **`app.js`-Menümarkierung:** freigegeben — additiv `features` in `ANSICHTEN` und `registriereAnsicht`. **Falsche Planvorgabe, bewusst nicht umgesetzt (Review bestätigt 2026-11-15):** Die zusätzliche Unterpunkt-Regel in `markiereNavigation` war ein Denkfehler (Feature-Link ohne `data-unterpunkt`; die bestehende Regel genügt bereits) — nicht nachholen.
- **Server:** kein neuer Endpunkt — `GET /api/file?path=features.md` + `GET /api/aufgaben`, `server.py` bleibt unverändert.
- **`index.html`:** minimaler Eingriff freigegeben (ein Menüpunkt + eine View-Sektion); der A10-Vertrag wird ausschließlich für neue Ansichten gelockert, bestehendes Markup bleibt unverändert.
- **Reihenfolge:** A23 vor A22 (Feature-Liste zuerst, danach die E2E-Regression).

- **Anforderung/Quelle:** Anforderung der Projektleitung („Die Feature List fehlt"), Menüpunkt „Feature List" → Liste aller Features mit Status; Klick auf ein Feature → zuständige Aufgaben mit Status offen / in Bearbeitung / erledigt.
- **Datenquelle `wissen/` bleibt einzige Quelle (Vorgabe 1):**
  - Feature-Liste, Feature-Status und Feature→Aufgaben-Zuordnung kommen aus `GET /api/file?path=features.md` (Datei ist als `RESERVIERTE_DATEIEN` schreibgeschützt, aber lesbar — geprüft: 200 mit `{frontmatter, markdown, nachtraege}`).
  - Aufgaben-Status/-Titel kommen aus `GET /api/aufgaben` (Feld `path` = Verbindungsschlüssel, z. B. `aufgaben/a1-okf-bundle.md`; dazu `titel`, `status` (6 UI-Status aus `status.py`), `owner`, `hinweis`, `zuletzt_geaendert`).
  - **Join:** Die Zuordnung wird aus den Markdown-Links in `features.md` gelesen (Aufgaben-Links in den Unterpunkten eines Feature-Bullets). Grund: Das Phasenmodell sieht zwar ein `feature:`-Feld im Aufgaben-Frontmatter vor, im Bundle ist es derzeit bei **keiner** Aufgabe gesetzt, und `/api/aufgaben` liefert es ohnehin nicht aus. Damit ist die Linkliste in `features.md` die einzige vorhandene Quelle — genau die dokumentierte OKF-Regel „jeder Eintrag verlinkt auf … die zugehörigen Aufgaben" (`features.md#Regeln`).
  - **Kein neuer Server-Endpunkt.** Zwei bestehende GET-Endpunkte genügen; ein neuer Endpunkt würde die Datei-Semantik duplizieren und den A8-Vertrag ohne Not aufweichen.
- **Reale Struktur von `wissen/features.md` (Grundlage des Parsers, per Analyse bestätigt):** H1 `# Offene Features` mit genau einem Top-Level-Bullet `* [OKF Projekt-Manager (SPA)](features/okf-projekt-manager-spa.md) — … · **umgesetzt — MVP abnahmefähig (…)** · Priorität **hoch**`, darunter eingerückte Unterpunkte (`  * **Umgesetzt …:** [A1](aufgaben/a1-okf-bundle.md) …, [A3](…), …`) mit allen Aufgaben-Links; H1 `# Umgesetzte Features` (derzeit `*Noch keine.*`). **Fallen, die der Parser abfangen muss:** (a) `# Regeln`, `# Offene Punkte`, `## …` enthalten ebenfalls Top-Level-Bullets und `aufgaben/`-Links (z. B. A22) — nur die beiden Feature-Abschnitte zählen; (b) Titel enthalten Klammern („(SPA)"); (c) mehrere `**…**`-Segmente pro Zeile (`Status`, `Priorität`); (d) Status- und Prioritätswort müssen gegen die festen Wertelisten geprüft werden; (e) A21 ist „vorgemerkt" **ohne** Dateilink und darf keinen Aufgaben-Eintrag erzeugen.
- **Feature-Status ≠ Aufgaben-UI-Status:** `features.md` nutzt den eigenen Wertevorrat `offen` / `in Umsetzung` / `umgesetzt` / `pausiert`. Er wird **nicht** in die sechs UI-Status gemappt, sondern wortgleich angezeigt (Marke `span.status`, Zusatzklasse `status--geschlossen` bei `umgesetzt`, `status--klarung` bei `offen`; Hinweis-Text in Klammern). Nur die Aufgaben laufen über die sechs UI-Status.
- **`index.html`-Ausnahme (Vorgabe 2):** Der A10-Vertrag („keine `index.html`-Änderungen") wird ausschließlich für diese neue Ansicht gelockert: **ein** Menüeintrag (nach „Aufgaben") plus **eine** View-Sektion (`ansicht-features` mit `liste-features`). Kein bestehendes Markup umbauen, keine neuen Filter/Formulare im Markup.
- **`app.js`-Eingriff (minimal, additiv):** Eintrag `features: "ansicht-features"` in `ANSICHTEN`, Import + `registriereAnsicht("features", ladeFeaturesAnsicht)`. **Korrektur (Review bestätigt 2026-11-15):** Die hier ursprünglich vorgesehene Änderung in `markiereNavigation` (`basis === "projekt"` → `["projekt", "features"].includes(basis)`) war eine **falsche Planvorgabe** und wurde bewusst **nicht** umgesetzt: Der Feature-Link trägt kein `data-unterpunkt`, die bestehende Regel markiert ihn auf Detailrouten bereits (`true`); die Änderung hätte T3 rot gemacht. `markiereNavigation` bleibt funktional unverändert (nur Kommentar). Begründung der Route: Die Detailroute liegt in derselben Ansicht; eine eigene Route `#/detail/features/<slug>` würde die A12-Detailansicht mit Aufgaben-Gruppen überladen.
- **Frontend-Regeln wie A11–A14:** XSS-sicher (`textContent`/`createElement`, `rendereMarkdown` aus `detail.js` für optionalen Feature-Datei-Inhalt), `classList` statt `className`, fail-loud bei fehlendem/unerwartetem Format, `api.js`-Wrapper (`getJson`), Container-Vertrag mit Meldung statt Silent-Return, Meldungen deutsch und ohne Pfade/OS-Details. Wiederverwendete CSS-Klassen: `liste`, `leer`, `status`, `uebersicht-titel`, `hinweis`, `knopf` → **`style.css` bleibt voraussichtlich unverändert**; nur falls die Gruppenköpfe/Abstände nicht reichen, additive Regeln.
- **Abhängigkeiten:** A8 (`GET /api/file`, `GET /api/aufgaben`), A10 (Gerüst/Router), A11 (Listen-/Leer-/Fehlermuster), A12 (`detail.js`-Renderer, Detailroute als Klickziel), A14 (`projekt.js` als Bauplan für Liste+Unterpunkt-Detail ohne neuen Endpunkt).
- **Testisolation (Vorgabe 5):** Alle HTTP-Läufe gegen `tmp_path`-Bundles (`/tmp/opencode/…`), Fixtures mit eigener `features.md` und eigenen Aufgaben-Dateien; `wissen/` wird nie beschrieben oder als Test-Bundle verwendet. `test_features.py` übernimmt den Node-DOM-Harness (`MINI_DOM` + Fetch-Stab) aus `test_projekt.py` als **dritte Kopie** — bewusst in Kauf genommen, um bestehende Testdateien nicht anzufassen; der Konsolidierungspunkt [A14-6] (`tests/harness_dom.py`) wird damit dringlicher und ist als Folgepunkt zu erweitern, nicht Teil dieser Aufgabe.
- **Konfliktlage (Stand geprüft: 2026-11-15):** Arbeitsbaum bis auf diese Aufgaben-Datei clean; letzter Commit `c598b63` (Colab-Tab-Fix) betrifft nur `start_colab.py`, `test_start_colab.py`, `README.md`, `docs/colab-start.md` — **`app.js`, `index.html`, `static/js/*` sind unberührt, kein weiterer Worktree aktiv**. Damit ist A23 mit A22 (nur `tests/test_e2e.py`) und der Doku parallel vergebbar; gemeinsame Berührung ist nur die pytest-Gesamtsuite (Flaky-Zone → Testläufe serialisieren). **Neue Konfliktgruppe G10 („Frontend Feature List"):** `features.js`, `app.js`, `index.html`, `style.css`, `test_features.py` — allein A23. Sollte ein späterer Tab-/Router-Fix `app.js` anfassen, wird er gegen A23 serialisiert.
- **Reihenfolge & Aufwand:** (1) Testgerüst + Harness-Kopie, Parser-Tests T6–T11 → Parser; (2) Gruppierung/Join T12–T15 → reine Logik; (3) Markup + Router T1–T5 → `index.html`, `app.js`; (4) Liste T16, Detail T17–T18; (5) Fehlerfälle T19–T21, HTTP-Läufe T22; (6) Regression T23. Aufwand **mittel** (ca. 60–80 neue Tests, ein Coder-Durchlauf + Review + Testphase), geschätzt 1 Arbeitstag. UI-Szenarien S1–S4 beim `tester` (Moli).
- **Risiken/Grenzen:** (a) `features.md` ist eine KI-Datei — Formatänderungen (andere Abschnittstitel, Status außerhalb der vier Werte) brechen den Parser bewusst fail-loud, statt still leer zu bleiben; (b) Feature-Status-Badge ist ein eigener Wertevorrat (kein Mapping) — bewusst, siehe oben; (c) Aufgaben-Zuordnung hängt an den Links in `features.md`; Aufgaben ohne Link erscheinen nur im Sammelhinweis (das ist gewollt transparent, keine automatische Ableitung aus `feature:`-Frontmatter — die bräuchte einen API-Zusatz und ist Post-MVP); (d) `index.html`-Änderung lockert A10 einmalig, der Reviewer prüft die rein additive Natur (T1).
- **Umbenennung (ausgeführt 2026-11-15):** Datei von `die-feature-list-fehlt.md` nach `wissen/aufgaben/a23-feature-liste.md` umbenannt (Nummerierung wie A1–A22) und in `features.md`/`aufgaben/index.md` als A23 verlinkt; Inhalt der Planung unverändert, Frontmatter auf `in Umsetzung` / `3 Umsetzung` gesetzt. **Titel-Korrektur (2026-11-15):** `title` von „Die Feature List fehlt" auf `A23: Feature-Liste (Menüpunkt + Feature-Status)` geändert (Projektregel „Aufgaben-Kennung steht im Titel"); der ursprüngliche Nutzertitel bleibt als Ziel-Formulierung im Abschnitt „Ziel" und als Anforderungsquelle erhalten.

# Betroffene Dateien

- `definitions/app/static/js/features.js` (neu) — Parser `parseFeatures` (Abschnitts-/Status-/Prioritäts-/Link-Auswertung), `gruppeAufgaben` + Join gegen `/api/aufgaben`, Loader `ladeFeaturesAnsicht` für Liste und Feature-Detail in `#liste-features`.
- `definitions/app/static/js/app.js` — additiv: `features` in `ANSICHTEN`, Import + `registriereAnsicht("features", …)`. `markiereNavigation` **funktional unverändert** (nur Kommentar) — die im Plan vorgeschlagene Unterpunkt-Erweiterung war eine **falsche Planvorgabe** und wurde bewusst nicht umgesetzt (Review bestätigt 2026-11-15).
- `definitions/app/static/index.html` — minimal: ein Menüeintrag „Feature List" (`href="#/features"`) und eine Sektion `id="ansicht-features"` mit `div id="liste-features"`; sonst unverändert.
- `definitions/app/tests/test_features.py` (neu) — T1–T23 inkl. Harness-Kopie, Stub- und HTTP-Läufe gegen `tmp_path`-Bundles, Fehler-/Randfall-Bundles.
- `definitions/app/static/style.css` — additiv: 2 Regeln (`.feature-meta`, `.feature-gruppe`) für Statuszeile und Gruppenköpfe; alle übrigen Klassen wiederverwendet.
- **Nicht geändert:** `server.py`, `overview.py`, `status.py`, `api.js`, `liste.js`, `detail.js`, `projekt.js`, `formulare.js`.

# Ergebnisse

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-15 — coder (Umsetzung, abgeschlossen)

- **Ergebnis:** `features.js` (neu, 485 Zeilen: `parseFeatures`, `gruppeAufgaben`, `zaehleGruppen`, `verbindeAufgaben`, `ohneZuordnung`, `ladeFeaturesAnsicht`), `test_features.py` (neu, 92 Tests), `index.html` additiv (Menüeintrag „Feature List" direkt nach „Aufgaben" + Sektion `ansicht-features` mit `liste-features`), `app.js` additiv (Ansicht, Import, Registrierung), `style.css` additiv (2 Regeln). Red-Green-Takt in Blöcken: 41 rot → 48 → 63 → 90 → 92 Tests grün; T1–T23 inkl. DOM-/HTTP-Läufen gegen `tmp_path`-Bundles.
- **Belege:** App-Suite **864 grün** (769 + 3 A16 + 92 A23). `verify.sh` Exit 0; ein einmaliger Flaky-Fehlschlag in der bekannten Parallel-Zone (paralleler Testlauf), nicht reproduzierbar. Parser nur lesend gegen die reale `wissen/features.md` verifiziert: 1 Feature, Titel/Status korrekt, 22 Aufgaben-Links (A1–A22) in Dateireihenfolge, A21 („vorgemerkt", ohne Dateilink) korrekt ohne Eintrag.
- **Befunde:** Bewusste Planabweichung — `markiereNavigation` ist funktional **unverändert**; die im Plan vorgesehene Unterpunkt-Erweiterung hätte T3 rot gemacht, weil der Feature-Link kein `data-unterpunkt` trägt (die bestehende Regel wertet Unterpunkte nur für `projekt` aus und markiert den Link daher bereits auf Detailrouten). Ergänzt wurde nur ein Kommentar; die Review-Bestätigung dieser Abweichung steht aus (inzwischen bestätigt: siehe Review-Eintrag 2026-11-15). Weitere bewusste Punkte: Aufgaben-Bullets zählen nicht als Features (Abschnittsgrenzen, T7); kein Rendering der Feature-Datei im Detail (vom AK nicht verlangt); `style.css` additiv aus Layoutgründen (2 Regeln statt der angestrebten Unverändertheit).
- **Offene Punkte:** Status **A23 → in Review** (Review läuft parallel); danach reif für Doku/Abschluss. Die Planabweichung zu `markiereNavigation` ist durch den Reviewer zu bestätigen (erledigt: Review-Eintrag 2026-11-15).

## 2026-11-15 — reviewer (Review, FREIGEGEBEN)

- **Ergebnis:** **FREIGEGEBEN** — keine kritischen/wesentlichen Befunde. Sicherheit sauber (keine HTML-Senken, `textContent`/`encodeURIComponent`, kein neuer Server-Endpunkt), A10-Vertrag eingehalten (0 Deletions, rein additiv), AK 1–2 vollständig abgedeckt, Statusgruppierung deckungsgleich mit `status.py`.
- **Bestätigte Planabweichung:** `markiereNavigation` funktional **unverändert** ist die **richtige** Lösung. Die Planvorgabe war ein Denkfehler: Der Feature-Link trägt kein `data-unterpunkt`; die bestehende Regel liefert bereits `true`, die vorgeschlagene Änderung hätte T3 rot gemacht. Die betroffenen Planstellen (T3 sowie Kontext/Betroffene Dateien) sind als „falsche Planvorgabe, bewusst nicht umgesetzt (Review bestätigt 2026-11-15)" markiert — **nicht nachholen**.
- **Weitere bestätigte bewusste Punkte:** Aufgaben-Bullets erzeugen keine Features (Abschnittsgrenzen); kein Rendering der Feature-Datei im Detail (vom AK nicht verlangt); `style.css` additiv mit 2 Regeln.
- **Kleinbefunde K1–K6 — laufen als Coder-Takt (kein Review-Blocker):** K1 führender `/`-Link, K2 Singular/Plural, K3 Formatfehler bei ungewohnter Bullet-Form, K4 Klammern, K5 Router-Harness-Unterpunkte, K6 harte Zählungen.
- **Testphase-Hinweise:** **H1 GESCHLOSSEN (tester, 2026-11-15):** Planzahl war falsch — 71 `def test_`-Zeilen inkl. Fixture `test_bundle` + 22 parametrisierte Fälle ⇒ 70 echte Tests + 22 = **92** = pytest-Collect; **kein fehlender Test**. Planzahl auf **92** korrigiert; kosmetische Empfehlung (Aufräum-Takt): Fixture umbenennen (pytest sammelt sie nicht). **H2** `tests/fixtures/bundle_min/features.md` hat das ALT-Format → der `tester` nutzt für die Moli-Szenarien **S1–S3** ein eigenes Szenarien-Bundle **mit** `# Offene Features`/`# Umgesetzte Features`; **S4** bewusst eines **ohne** Datei. **H3** Harness-Konsolidierung [A14-6] bestätigt, kein Neu-Befund.
- **Offene Punkte:** Status **A23 → in Doku** (review-frei). A23-Suite **92** (H1 geschlossen, Planzahl korrigiert). Teststand-Korrektur (tester, 2026-11-15): Basis `07ad675` = App **942** + tools **69** = **1011** (die Zahl 1015 war nicht reproduzierbar; Zählumfang „Gesamtsuite" = App + tools, `definitions/tools` wird separat ausgewiesen).

## 2026-11-15 — tester (Testphase-Ergänzung / H1-Nachlauf, GESCHLOSSEN)

- **Ergebnis:** Die offene Planzahl ist geklärt — **kein fehlender Test**. Die 71 `def test_`-Zeilen enthalten die Fixture `test_bundle` (pytest sammelt sie nicht) und 22 parametrisierte Fälle: 70 echte Tests + 22 = **92** = pytest-Collect. Abdeckung T1–T23 vollständig.
- **Befunde:** Planzahl-Fehlzählung, Planvorgabe auf **92** korrigiert. Kosmetische Empfehlung (Aufräum-Takt, [A33](a33-kleinbefunde-aufräum-takt.md)): Fixture umbenennen. H2: Szenarien-Bundle für S1–S3 **mit** Feature-Abschnitten, S4 **ohne** Datei.
- **Offene Punkte:** keine — review-frei, reif für Abschluss.

## 2026-11-15 — documenter (Abschluss)

- **Ergebnis:** A23 auf `task_status: abgeschlossen` / `phase: 8 Abgeschlossen` gesetzt, im [Aufgaben-Index](index.md) nach „Abgeschlossene Aufgaben" verschoben; [features.md](/features.md) und [Projekt-Log](/log.md) nachgezogen.
- **Belege:** **92 Tests** (`test_features.py`, pytest-Collect), H1 geschlossen (Planzahl-Fehlzählung, auf 92 korrigiert), **K1–K6 erledigt**, **Review FREIGEGEBEN** (2026-11-15) inkl. Bestätigung der Planabweichung `markiereNavigation` (nicht nachholen). App-Suite **864** bleibt der A23-Zeitstand.

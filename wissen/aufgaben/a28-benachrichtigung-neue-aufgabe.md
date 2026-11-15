---
type: Task
title: "A28: Benachrichtigung bei neuer Aufgabe"
description: Wenn eine neue Aufgabe angelegt wird, muss die KI ist automatisch wahrnehmen
  können um die Planung durchzuführen. Die Aufgabe wird erst begonnen wenn der Aufga…
task_status: in Planung
phase: 2 Planung
priority: mittel
assigned_to: coder
owner: ai
aktuell: "PM: Planung fertig (10 AK, 36 Tests, 4 Pakete) — wartet auf Freigabe der Projektleitung"
---

# Ziel

Wenn über die App (`POST /api/task`) oder direkt in `wissen/aufgaben/` eine neue Aufgabe entsteht, muss die KI sie **zuverlässig wahrnehmen**, ihr im Moment der Annahme die Kennung geben (`A<N>: <Titel>`, Datei `a<N>-<slug>.md`) und **vor der Umsetzung auf die Freigabe der Projektleitung warten**.

A28 liefert dafür drei Bausteine:

1. **Wahrnehmung ohne neuen Dienst:** Die Lese-API markiert Aufgaben ohne gültige Kennung deterministisch mit `neu: true` (Dateiname ohne `a<N>-` **oder** Titel ohne `A<N>:` **oder** beide Nummern ungleich). Aufgabenliste/Übersicht zeigen eine Marke „neu", das Detail einen Hinweis samt „Nächste freie Kennung". Damit ist der Zustand „neu/unvergeben" für Mensch **und** KI maschinell eindeutig; die Prüfpflicht der KI (`git status` + `wissen/aufgaben/`, AGENTS.md) bleibt der Auslöser, die App liefert das Signal und die ID-Hilfe.
2. **Freigabe-Datenhaltung als Menschen-Recht:** Boolesches Frontmatter-Feld `freigabe` (fehlt oder ≠ `true` = **nicht freigegeben**, fail-closed). Schreiben ausschließlich über den Menschen-Kanal `POST /api/freigabe`; der KI-Weg (`meta.setzen`, `POST /api/meta`) liefert **403** und schreibt nichts.
3. **Workflow-Regel:** AGENTS.md, Phasenmodell und Technische Spec: wahrnehmen → annehmen (Kennung + Titel + Datei-Umbenennung) → sofort pushen → planen → Status `geplant` → **auf `freigabe: true` warten** → erst dann `coder` beauftragen.

# Akzeptanzkriterien

- **AK-1 (Signal „neu", PM 1):** `GET /api/aufgaben` und `GET /api/overview` liefern für jeden Eintrag mit `typ == "Task"` ein boolesches Feld `neu`. `neu == true`, wenn **mindestens eine** Bedingung zutrifft: (a) Titel matcht nicht `^A([1-9][0-9]*):(?:\s|$)`, (b) Dateiname ohne `.md` matcht nicht `^a([1-9][0-9]*)(?:-|$)` (deckt `a1.md` und `a1-slug.md` ab), (c) die Zahl aus dem Titel ist ungleich der Zahl aus dem Dateinamen. Sonst `neu == false`. Nicht-Task-Einträge haben kein `neu`-Feld. Ein nicht lesbarer Eintrag unter `aufgaben/` gilt als `neu: true` (fail-loud, bestehender `hinweis: "nicht lesbar"` bleibt).
- **AK-2 (Kennung + nächste freie Kennung, PM 1):** `GET /api/file?path=aufgaben/<…>` liefert für Tasks zusätzlich `neu` (wie AK-1), `kennung` (z. B. `"A28"`, nur wenn der Titel `^A([1-9][0-9]*):(?:\s|$)` matcht) und `naechste_kennung` (z. B. `"A30"`). `naechste_kennung` = Maximum aller Kennungszahlen aus Titel (`^A(\d+):`) **und** Dateinamen (`^a(\d+)(?:-|$)`) aller `aufgaben/*.md` + 1; ohne Bestand `"A1"`; unlesbare/fremde Dateien werden ignoriert (kein Fehler). Die Kennung ist ein **Hinweis**, keine Reservierung. Nicht-Task-Dateien erhalten keines der drei Felder.
- **AK-3 (Sichtbares Signal in Listen, PM 2):** Zeilen mit `neu == true` zeigen in der Titel-Zelle eine Marke mit dem Text „neu" (`span`, `classList.add("status")`), in Aufgabenliste **und** Übersicht. Genau eine Marke je Zeile, auch nach wiederholtem Laden/Filterwechsel. Nicht-Task-Zeilen und Zeilen mit `neu == false` bleiben unverändert. `index.html` und `style.css` bleiben unverändert (bestehende Klassen).
- **AK-4 (Detail-Hinweis neue Aufgabe, PM 2):** Das Aufgaben-Detail mit `neu == true` zeigt im Kopf einen Hinweis (`#detail-neu-hinweis`, `class="hinweis"`) mit dem Text „Neue Aufgabe ohne Kennung — die Kennung wird beim Annehmen als `A<N>: ` im Titel ergänzt." und, wenn `naechste_kennung` vorliegt, „Nächste freie Kennung: A<N>.". Bei `neu == false` fehlt der Hinweis. Es gibt **keine** Bedienung zum Setzen von Titel/Kennung (KI-Recht).
- **AK-5 (Freigabe-Feld und Default, PM 0):** Aufgaben- und Wellen-Dateien tragen ein boolesches Frontmatter-Feld `freigabe`. Fehlt es oder ist es nicht exakt `true` (z. B. `"true"`, `"ja"`, `1`, `null`), gilt die Aufgabe/die Welle als **nicht freigegeben** (fail-closed, zentral in `freigabe.ist_freigegeben`). `neu_aufgabe.anlegen` schreibt `freigabe: false` explizit; `GET`-Einträge liefern `freigabe: true|false` für `typ in ("Task", "Welle")` und bei ungültigem Rohwert zusätzlich `freigabe_hinweis` (deutsche Meldung ohne Pfad/OS-Details).
- **AK-6 (Rechteklasse Mensch, PM 0):** `freigabe` ist ein **Menschen-Recht**. `meta.setzen(..., freigabe=…)` wirft `meta.RechteFehler` (HTTP 403) und schreibt nichts — auch bei `False`. `freigabe.setzen(pfad, wert, *, herkunft)` schreibt nur bei `herkunft == freigabe.MENSCH`; `herkunft == freigabe.KI` oder fehlend → `RechteFehler`, Datei byte-identisch, kein `okf_bundle.set_meta`-Aufruf. `wert` muss echtes `bool` sein (sonst `EingabeFehler`/400). Ziel muss eine bestehende Aufgabe (`aufgaben/…` bzw. `type: Task`) oder Welle (`wellen/…` bzw. `type: Welle`) sein; reservierte Ziele → 403, fehlende Datei → 404, Pfadausbruch/leer → 400.
- **AK-7 (Endpunkt `POST /api/freigabe`, PM 0):** Body `{path, wert}` → 200 `{path, freigabe: <bool>, frontmatter}`. Fehlender `wert`, Nicht-Bool, fehlender/leerer `path` → 400; unbekanntes Ziel → 400; fehlende Datei → 404; reserviert → 403; `GET` → 405. Genau ein atomarer Schreibvorgang, Body byte-identisch, genau ein `freigabe`-Schlüssel, idempotent (unveränderter Wert = kein Schreibvorgang, weiterhin 200). `/api/meta` mit `freigabe` → **403**, auch in Kombination mit gültigem `owner`/`status` (kein Teil-Schreibvorgang). Endpunktliste wächst um genau `/api/freigabe`.
- **AK-8 (Freigabe-Bedienung im Aufgaben-Detail, PM 2):** Das Aufgaben-Detail zeigt den Freigabe-Zustand („Freigegeben" / „Nicht freigegeben") und genau einen Knopf (`#detail-freigabe`) mit wechselndem Text „Freigeben" bzw. „Freigabe entziehen". Klick → genau ein `POST /api/freigabe` mit `{path, wert}`; Erfolgsmeldungen „Aufgabe freigegeben." / „Freigabe entzogen."; danach wird das Detail neu geladen und zeigt den neuen Zustand. Während des Requests ist der Knopf `disabled`; bei Fehler bleibt der angezeigte Zustand erhalten, die Servermeldung ist sichtbar, der Knopf wird wieder bedienbar (`try/finally`). Nur für Tasks; Welle/Projektdateien zeigen keinen Aufgaben-Freigabe-Knopf.
- **AK-9 (Workflow-Regel dokumentiert, PM 3):** `AGENTS.md` **und** `definitions/AGENTS.md` enthalten die verbindliche Reihenfolge „wahrnehmen (Signal `neu` + `git status`/`wissen/aufgaben/`) → annehmen (Kennung + Titel `A<N>: …` + Datei `a<N>-<slug>.md`) → sofort pushen → planen → `geplant` → auf `freigabe: true` warten → umsetzen" sowie „Freigabe setzt ausschließlich die Projektleitung; die KI setzt `freigabe` nie (API 403)". `wissen/projekt/phasen.md` ersetzt den Satz „Es gibt keine fachliche Freigabe-Phase vor der Umsetzung" durch die Phase **„3b. Freigabe (Projektleitung, human)"** und dokumentiert `geplant` als Wartestatus sowie `freigabe` im Aufgaben-Format. `wissen/projekt/technische-spec.md` ergänzt `freigabe` in der Schreibrechte-Matrix (Mensch ✅ / KI ❌ 403), das Feld in der Datenmodell-Tabelle und `POST /api/freigabe` in der Schnittstellen-Tabelle.
- **AK-10 (Grenzen/Regression, alle):** Keine neuen Abhängigkeiten, kein externer Dienst, kein Push/Watcher. `index.html` (eingefroren seit A10), `style.css`, `app.js`, `api.js`, `formulare.js`, `features.js`, `projekt.js`, `okf_bundle.py` bleiben unverändert. XSS-sicher (`textContent`/`createElement`, nur `classList`), fail-loud bei `null`/Nicht-Array-Antworten, deutsche Meldungen ohne Pfade. Bestehende Testfälle bleiben grün (Änderungen nur additiv); `bash definitions/verify.sh .` → Exit 0.

# Testfälle (TDD)

**Zuordnung AK → Testfälle:**
**AK-1** → T1–T4, T7. **AK-2** → T5, T6. **AK-3** → T23–T25. **AK-4** → T26, T27. **AK-5** → T8, T13, T14, T16, T17, T22. **AK-6** → T9–T12, T15. **AK-7** → T16–T21. **AK-8** → T28–T33. **AK-9** → T36 (Review-Prüfschritt, kein pytest). **AK-10** → T34, T35.

Reihenfolge = Red-Green-Takt: erst Test schreiben, rot laufen lassen, dann das Minimum implementieren, dann refaktorisieren. Jede Testnummer ist ein eigener pytest-Fall. Neue Dateien: `tests/test_freigabe.py`, `tests/test_neue_aufgabe_signal.py`, `tests/test_freigabe_ui.py`. Bestehende Dateien nur additiv: `tests/test_meta.py`, `tests/test_api_schreiben.py`, `tests/test_neu_aufgabe.py`. Alle Läufe gegen das `bundle`-Fixture aus `conftest.py` (`tmp_path`-Kopie von `fixtures/bundle_min`); zusätzliche Dateien werden **im Test** unter `tmp_path` angelegt — niemals gegen `wissen/` oder `/content/pmTool/wissen`.

**A. Read-Modell „neu"/Kennung (`tests/test_neue_aufgabe_signal.py`, AK-1, AK-2)**

- **T1 `neu` ohne Kennung:** Fixture-Aufgabe `aufgaben/benachrichtigung-neue-aufgabe.md` (Dateiname ohne `a<N>-`, Titel ohne `A<N>:`) → `GET /api/aufgaben`: genau ein Eintrag mit `path`, `typ == "Task"`, `neu is True`; `GET /api/overview` derselbe Wert; der Wellen-Eintrag `wellen/w1.md` hat **kein** `neu`-Feld.
- **T2 `neu` false bei konsistenter Kennung:** `aufgaben/a1.md` mit `title: "A1: Mini-Aufgabe"` → `neu is False`; Eintrag ansonsten unverändert (`status`, `owner`, `welle`).
- **T3 `neu` bei halber/inkonsistenter Kennung:** parametrisiert (a) Titel `"A12: X"` + Datei `aufgaben/x.md`, (b) Datei `aufgaben/a12-x.md` + Titel `"X"`, (c) Titel `"A12: X"` + Datei `aufgaben/a13-x.md` → jeweils `neu is True`; Gegenprobe `"A12: X"` + `a12-x.md` → `neu is False` und `"A12: X"` + `a12.md` (Altbestand ohne Slug) → `neu is False`.
- **T4 Formatstrenge:** Titel `"A: X"`, `"A12:X"` (ohne Leerzeichen), `"a12: X"`, `"A12 - X"`, `"A0: X"`, fehlender Titel, Titel `42` → jeweils `neu is True`, kein Wurf; `"A12: "` (nur Kennung) → `neu is False` (Format erfüllt).
- **T5 `naechste_kennung`:** Bundle mit `aufgaben/a1.md` (`A1`), `aufgaben/a27-x.md` (`A27`), `aufgaben/a3-y.md` (Titel `A7`) und einer Datei mit kaputtem YAML unter `aufgaben/` → `GET /api/file?path=aufgaben/a1.md` liefert `naechste_kennung == "A28"`; leeres `aufgaben/` → `"A1"`; `GET /api/file?path=wellen/w1.md` und `projekt/phasen.md` → Feld fehlt.
- **T6 Detail-Felder:** `GET /api/file?path=aufgaben/a1.md` → `neu is False`, `kennung == "A1"`; Aufgabe ohne Kennung → `neu is True`, `kennung` fehlt; Antwort enthält weiterhin `frontmatter`, `markdown`, `nachtraege` (A8-Vertrag unverändert).
- **T7 Nicht lesbare Aufgabe:** `aufgaben/kaputt.md` mit ungültigem YAML → Eintrag in `/api/aufgaben` mit `neu is True` und bestehendem `hinweis == "nicht lesbar"`; die übrigen Einträge bleiben vollständig und sortiert (kein stilles Weglassen, kein 500).

**B. Freigabe-Modul und Rechte (`tests/test_freigabe.py`, AK-5, AK-6, AK-7)**

- **T8 `ist_freigegeben` fail-closed:** parametrisiert `{}` → `False`; `{"freigabe": True}` → `True`; `{"freigabe": False}`, `{"freigabe": "true"}`, `{"freigabe": "ja"}`, `{"freigabe": 1}`, `{"freigabe": 0}`, `{"freigabe": None}`, `{"freigabe": ""}` → jeweils `False`.
- **T9 Setzen (Menschen-Kanal):** `freigabe.setzen("aufgaben/a1.md", True, herkunft=freigabe.MENSCH)` → Rückgabe-Frontmatter mit `freigabe is True`, Datei enthält genau eine Zeile `freigabe: true`, Body-SHA256 vor/nach identisch, `okf_bundle.set_meta` genau einmal (Spy), übrige Frontmatter-Keys unverändert.
- **T10 KI-Kanal verweigert:** `setzen(..., herkunft=freigabe.KI)` und `setzen(..., herkunft=None)` → `meta.RechteFehler`, Datei-SHA256 unverändert, `set_meta`-Spy leer.
- **T11 Nur echtes Bool:** `wert` = `"true"`, `"ja"`, `1`, `0`, `None`, `[]`, `{}` → jeweils `okf_bundle.EingabeFehler`, Datei unverändert, kein Schreibvorgang.
- **T12 Zielprüfung:** `aufgaben/a1.md` und `wellen/w1.md` → erlaubt; `index.md`, `log.md`, `features.md`, `wellen/index.md` → `RechteFehler`; `projekt/phasen.md` → `EingabeFehler`; `aufgaben/gibtsnicht.md` → `FileNotFoundError`; `../wellen/w1.md`, `/etc/passwd`, `""` → `okf_bundle.BundlePfadFehler` bzw. `EingabeFehler`; in allen Fehlerfällen bleibt das Bundle byte-identisch (`_aussen`-Vergleich wie `test_api_schreiben.py`).
- **T13 Idempotenz:** Aufgabe mit `freigabe: true` + erneut `wert=True` → 200/Rückgabe, `set_meta` nicht aufgerufen, Datei-SHA und mtime unverändert; dasselbe für `false` + `False`.
- **T14 Entziehen:** `true` → `wert=False` → `freigabe is False`, genau ein `freigabe`-Schlüssel (`text.count("\nfreigabe:") == 1`), Body byte-identisch.
- **T15 `meta`-Guard (auch Modul-Ebene):** `meta.setzen("aufgaben/a1.md", freigabe=True)` und `…, freigabe=False` → `meta.RechteFehler`, kein Schreibvorgang; `POST /api/meta {"path": …, "freigabe": true}` → **403**, `{"path": …, "owner": "mensch", "freigabe": true}` → **403** und `owner` in der Datei unverändert (fail-closed vor jedem Schreiben); `{"path": …, "freigabe": false}` → **403**.
- **T16 Endpunkt setzt:** `POST /api/freigabe {"path": "aufgaben/a1.md", "wert": true}` → 200, `mimetype application/json`, Antwort `{path, freigabe: true, frontmatter}`, Datei `freigabe: true`, Body-SHA identisch; `GET /api/aufgaben` spiegelt `freigabe is True` für denselben Pfad.
- **T17 Endpunkt entzieht:** danach `{"path": …, "wert": false}` → 200, `freigabe is False`, genau ein Schlüssel, Body identisch.
- **T18 Endpunkt-Validierung:** `{path}` ohne `wert` → 400; `wert` = `"true"`, `1`, `null`, `[]` → 400; `path` fehlt/`""`/`42` → 400; `{}` → 400; Ziel `projekt/phasen.md` → 400; `aufgaben/gibtsnicht.md` → 404; `features.md` → 403; `GET /api/freigabe` → 405; in allen Fällen Datei bzw. Bundle unverändert, `error` nicht leer und ohne Pfad-/OS-Details.
- **T19 Atomarität:** zwei Requests hintereinander (`true`, dann `false`) → genau ein `freigabe`-Schlüssel, Body unverändert, `set_meta` genau einmal je Request (Spy); kein Zwischenzustand mit doppeltem Schlüssel.
- **T20 Endpunkt-Inventar:** `ENDPUNKTE` in `test_api_schreiben.py` lautet `("/api/nachtrag", "/api/task", "/api/welle", "/api/meta", "/api/freigabe")`; kein weiterer neuer Endpunkt; die bestehenden `ENDPUNKTE`-Parametertests laufen für den neuen Eintrag mit (405/400-Verhalten).
- **T21 Signale ohne neuen Endpunkt:** `neu`, `kennung`, `naechste_kennung`, `freigabe` kommen ausschließlich aus `/api/overview`, `/api/aufgaben`, `/api/wellen`, `/api/file`; die UI-Tests (T23–T33) prüfen per Request-Zähler, dass dafür kein zusätzlicher Request entsteht.

**C. Neuanlage (`tests/test_neue_aufgabe_signal.py`, AK-5)**

- **T22 Neue Aufgabe ist nicht freigegeben:** `POST /api/task` mit gültigen Formulardaten → Datei enthält `freigabe: false`; `GET /api/aufgaben` liefert für den neuen Pfad `neu is True`, `freigabe is False`; die A13-Abschnitte (`# Ziel`, `# Akzeptanzkriterien`, `# Testfälle (TDD)`, `# Kontext`, `# Betroffene Dateien`, `# Ergebnisse`) bleiben vollständig und in der Reihenfolge.

**D. Frontend (`tests/test_freigabe_ui.py`, AK-3, AK-4, AK-8, AK-10)**

Harness: `tests/dom_helfer.py` nutzen (wird in **A30** angelegt: Mini-DOM + Node-Runner, aus `test_welle_zuordnung.py` extrahiert) und darauf den Fetch-Stub mit Request-Zähler aufsetzen. `fetch` beantwortet `/api/file` und `/api/wellen` aus Fixtures; unerwartete Requests schlagen fehl. Keine weitere Harness-Kopie (A30 läuft vor A28).

- **T23 Marke in der Aufgabenliste:** `ladeAufgaben()` mit zwei Einträgen (`neu: true` / `neu: false`) → genau eine Marke mit `textContent == "neu"` in der Titel-Zelle der neuen Aufgabe, `classList.contains("status")`; `data-path` beider Zeilen unverändert; zweiter Aufruf und Filterwechsel erzeugen keine zweite Marke (Idempotenz).
- **T24 Marke in der Übersicht:** `ladeUebersicht()` → Marke „neu" in der Top-5-Tabelle für den neuen Eintrag; die Klarung-Liste bleibt unverändert (nur Links/Text, keine Marke); Nicht-Task-Zeilen ohne Marke.
- **T25 XSS/robust:** Titel `<img src=x onerror=alert(1)>` mit `neu: true` → Titel textuell, Marke textuell, kein `img`-Knoten, kein `alert`; Eintrag ohne `neu`-Feld wird wie `false` behandelt (kein Wurf).
- **T26 Detail-Hinweis:** `/api/file`-Stub `{frontmatter: {type: "Task", title: "Benachrichtigung"}, neu: true, naechste_kennung: "A30"}` → `#detail-neu-hinweis` sichtbar, Text enthält „Neue Aufgabe ohne Kennung" und „Nächste freie Kennung: A30"; kein Knopf zum Setzen des Titels.
- **T27 Kein Hinweis bei Kennung:** `neu: false` → `#detail-neu-hinweis` fehlt; `naechste_kennung` fehlt → Hinweis ohne den Zusatz, kein Wurf.
- **T28 Freigabe-Anzeige:** Aufgaben-Detail `freigabe: true` → „Freigegeben" sichtbar und Knopftext „Freigabe entziehen"; `freigabe: false`, fehlendes Feld und `"ja"` → „Nicht freigegeben" und Knopftext „Freigeben" (fail-closed).
- **T29 Freigeben im UI:** Klick auf `#detail-freigabe` (Zustand nicht freigegeben) → genau ein `POST /api/freigabe` mit Body `{path, wert: true}`; Meldung „Aufgabe freigegeben."; nach dem Neuladen zeigt das Detail „Freigegeben"; Knopf während des Requests `disabled`.
- **T30 Entziehen im UI:** Zustand freigegeben → Klick → genau ein `POST /api/freigabe` mit `{path, wert: false}`; Meldung „Freigabe entzogen.".
- **T31 Doppelklick:** zwei Klicks während eines laufenden Requests → genau ein POST; Knopf danach wieder bedienbar.
- **T32 Fehlerpfad:** Stub antwortet 403 `{error: "…"}` → Fehlerbereich zeigt die Servermeldung, Anzeige bleibt beim alten Zustand (kein Neuladen), Knopf wieder bedienbar, kein zweiter POST.
- **T33 Abgrenzung/Requests:** Wellen-Detail (`wellen/w1.md`) und Projektdatei (`projekt/phasen.md`) → kein `#detail-freigabe`, kein `#detail-neu-hinweis`; Aufgaben-Detail = `GET /api/file` (+ `/api/wellen` aus A27), Übersicht/Aufgabenliste = je ein Listen-Request, **kein** zusätzlicher Request für Marke/Hinweis/Freigabe.

**E. Regression und Doku (AK-9, AK-10)**

- **T34 Baselines:** `test_detail.py`, `test_liste.py`, `test_suche.py`, `test_welle_zuordnung.py`, `test_formulare.py`, `test_features.py`, `test_static.py`, `test_api_lesen.py`, `test_neu_welle.py`, `test_okf_bundle.py` bleiben **unverändert** grün; die Suite wächst nur um die neuen Dateien und die additiven Fälle in `test_meta.py`/`test_api_schreiben.py`/`test_neu_aufgabe.py`; `bash definitions/verify.sh .` → Exit 0.
- **T35 Unveränderte Dateien:** `git diff --stat` zeigt keine Änderung an `definitions/app/static/index.html`, `static/style.css`, `static/js/app.js`, `static/js/api.js`, `static/js/formulare.js`, `static/js/features.js`, `static/js/projekt.js`, `definitions/app/okf_bundle.py`; `test_static.py` grün.
- **T36 Doku-Regelwerk (Review-Prüfschritt, kein pytest):** `AGENTS.md` und `definitions/AGENTS.md` enthalten die Reihenfolge aus AK-9 und den Satz „Freigabe setzt ausschließlich die Projektleitung"; `wissen/projekt/phasen.md` enthält „3b. Freigabe", den Wartestatus `geplant` und `freigabe` im Aufgaben-Format; `wissen/projekt/technische-spec.md` enthält die Rechtezeile `freigabe` (Mensch ✅ / KI ❌), `POST /api/freigabe` und die Felder `neu`, `kennung`, `naechste_kennung`. Nachweis im Review-Ergebnis mit Zitatstelle.

**UI-Szenarien für den `tester` (Moli-Browser, laufende App gegen Test-Bundle):**

- **S1 Neue Aufgabe wahrnehmen:** Aufgabe über das Formular anlegen → Aufgabenliste zeigt die Zeile mit Marke „neu", Detail zeigt den Kennungs-Hinweis samt nächster freier Kennung, keine Konsolenfehler.
- **S2 Annehmen (KI/Datei):** Titel auf `A<N>: …` ändern und Datei auf `a<N>-….md` umbenennen → Marke verschwindet nach Neuladen, Hinweis weg.
- **S3 Freigeben:** Detail öffnen → Knopf „Freigeben" → Meldung „Aufgabe freigegeben.", Anzeige „Freigegeben", Knopf „Freigabe entziehen"; Datei enthält `freigabe: true`, Body unverändert.
- **S4 Entziehen/Fehler:** „Freigabe entziehen" → `freigabe: false`; danach per Netzwerk einen 403 provozieren → sichtbare Meldung, Anzeige unverändert, Knopf wieder bedienbar.
- **S5 Grenzen:** Welle und Projektdatei öffnen → kein Freigabe-Knopf, kein Kennungs-Hinweis; Aufgabenliste mit Filter/Suche → Marke bleibt korrekt, kein Flackern/Doppelmarke.

# Kontext

- **Anforderung (Projektleitung, 2026-11-15):** „Wenn eine neue Aufgabe angelegt wird, muss die KI sie automatisch wahrnehmen können, um die Planung durchzuführen. Die Aufgabe wird erst begonnen, wenn ihr eine Aufgabennummer im Titel zugeteilt wurde (z. B. `A{xxx}:Titel`) und die Aufgabe geklärt und freigegeben wurde."
- **Antwort auf „Wahrnehmungsmechanismus" (a):** Ein Push-Kanal zur KI existiert nicht und wird **nicht** eingeführt (kein externer Dienst, keine neue Abhängigkeit, keine Watcher/Webhooks). Die KI nimmt Aufgaben weiterhin über ihre Prüfpflicht wahr (`git status`, `wissen/aufgaben/`: Dateiname ohne `aNN-`, `task_status: offen`, `owner: ai`, `freigabe` ≠ `true`); die App macht den Zustand **deterministisch sichtbar und maschinenlesbar**: abgeleitetes `neu`-Flag in der Lese-API, Marke „neu" in den Listen, Kennungs-Hinweis samt nächster freier Nummer im Detail. Damit kann weder eine über die App noch eine direkt angelegte Aufgabe „übersehen" werden, ohne dass ein sichtbarer Zustand dagegen spricht. *Verworfen:* Telegram-Versand aus der App (Seiteneffekt im Request, Config-Abhängigkeit, nicht testbar ohne Mock), Datei-Watcher/Webhook (neuer Dienst), `inotify` (Plattformabhängigkeit).
- **Antwort auf „Datenhaltung der Freigabe" (b):** **Frontmatter-Feld `freigabe` (bool)** in der Aufgaben-Datei; Default fehlt = nicht freigegeben. Begründung: OKF-konform, für KI und Mensch ohne App lesbar, ein Feld je Datei (keine Zweitpflege), `okf_bundle.set_meta` schreibt es ohne Erweiterung. Bewusst **kein** neues Statuswert im `task_status`-Vokabular: `geplant` bleibt der Wartestatus, `in Umsetzung` setzt weiterhin nur die KI.
- **Antwort auf „Auswirkung auf den Workflow" (c):** Regel in AGENTS.md/Phasenmodell (AK-9): annehmen → Kennung/Titel/Datei → pushen → planen → `geplant` → **warten auf `freigabe: true`** → umsetzen. Die KI prüft die Freigabe **vor jeder Beauftragung** eines `coder`; fehlt sie, bleibt die Aufgabe `geplant` und wird nicht vergeben. Der Mensch kann freigeben/entziehen; ein Entzug stoppt **keine** bereits laufende Umsetzung (kein Zwangsabbruch), sondern sperrt weitere Beauftragungen — der PM entscheidet über den Rücklauf.
- **Rechte-Modell (neu, Erweiterung von `meta.py`):** Rechteklasse **Mensch** für `freigabe`. Der bestehende KI-Weg (`meta.setzen`, `POST /api/meta`) ist der Standard-/KI-Kanal und liefert für `freigabe` **403**; der Menschen-Kanal ist `POST /api/freigabe`, das intern `freigabe.setzen(..., herkunft=freigabe.MENSCH)` aufruft. **Ehrliche Grenze:** Die App hat keine Authentifizierung (lokale Single-User-App); die Rechteklasse ist eine Modul-/API-Konvention plus Projektregel in AGENTS.md, keine kryptografische Absicherung. Sie ist dennoch wirksam, weil der dokumentierte KI-Schreibweg (Datei-/Modul-Ebene, `meta.setzen`, `/api/meta`) technisch 403 liefert und der Menschen-Kanal nur von der UI benutzt wird. Ein Modultest (T10) sichert, dass ohne explizite Menschen-Herkunft kein Schreibvorgang stattfindet.
- **Ist-Stand im Code (geprüft 2026-11-15):**
  - `okf_bundle.set_meta` schreibt boolesche Werte bereits korrekt (`yaml.safe_dump` → `freigabe: true`) und erhält den Body byte-identisch — **keine Kernänderung** nötig.
  - `meta.setzen` prüft `owner`/`status`-Whitelists, `welle` und die Zieldatei; `server.api_meta` reicht nur `owner`/`status`/`welle` weiter und ignoriert unbekannte Felder (ein `freigabe` im Body würde heute still verworfen → deshalb expliziter 403-Guard).
  - `overview._eintrag` baut die Listeneinträge (`path`, `typ`, `titel`, `status`, `owner`, `zuletzt_geaendert`, `welle?`, `hinweis?`); `overview.details` liefert `{frontmatter, markdown, nachtraege}`.
  - `neu_aufgabe._inhalt` schreibt das Frontmatter in fester Reihenfolge (`type`, `title`, `description`, `task_status`, `phase`, `priority`, `assigned_to`, `user_story?`, `welle?`, `owner`).
  - `detail.js` hat mit dem owner-Umschalter und `speichereMeta` bereits das Muster für „Feld ändern → POST → Meldung → neu laden → Rückfall bei Fehler"; `erstelleMetaPayload` wird für die Freigabe **nicht** wiederverwendet (anderer Endpunkt).
  - `liste.js` baut die Titel-Zelle in `erstelleTabelle` (`erstelleZelle(eintrag?.titel)`) — dort hängt die Marke an, A29 erweitert dieselbe Stelle für Wellen.
- **Umsetzungsentscheidungen (TDD-relevant, reversibel):**
  - **Ein gemeinsames Freigabe-Fundament (Paket 0) für A28 und A29:** Feldname, Rechteklasse, Endpunkt und Read-Modell-Feld werden **einmal** gebaut (`freigabe.py`, `meta.py`, `server.py`, `overview.py`), damit A29 keine zweite Rechteklasse oder einen zweiten Endpunkt braucht. A29 hängt damit hart an A28 Paket 0.
  - **`freigabe`-Werte:** geschrieben wird ausschließlich `true`/`false`; gelesen wird ausschließlich `is True` als freigegeben (`ist_freigegeben`). Kein Löschen des Schlüssels (sichtbarer Zustand statt fehlender Information); Default für Altbestand bleibt „nicht freigegeben".
  - **`neu` wird abgeleitet, nicht gespeichert:** kein zusätzliches Frontmatter-Feld „erkannt/angenommen" (würde eine zweite Wahrheit schaffen und bei Umbenennung veralten). Die Ableitung ist idempotent und für App- und Direktanlagen identisch.
  - **`naechste_kennung` ist ein Hinweis, keine Reservierung:** Sie wird bei jedem Detailaufruf neu berechnet; zwei gleichzeitig angelegte Aufgaben können dieselbe Nummer sehen — die KI vergibt die Kennung weiterhin selbst und prüft Kollisionen (bestehende Regel).
  - **Marke statt neuer Spalte/Filter:** `erstelleTabelle` bleibt bei vier Spalten (A11/A27-Vertrag, inkl. A27-Tests zur Kopfzeile); die Marke sitzt in der Titel-Zelle und ist damit auch in der Übersicht sichtbar. Ein `neu`-Filter ist **nicht** Teil von A28 (kein Eingriff in die A25/A27-Filterlogik; bei Bedarf eigene Aufgabe).
  - **UI nur im Detail schreibend:** Freigeben/Entziehen ausschließlich im Aufgaben-Detail (nicht in der Liste), damit kein versehentlicher Klick in einer Tabelle schreibt und das A12-Muster (ein `speichereMeta`-analoger Aufruf) erhalten bleibt. Für die Welle kommt dieselbe Bedienung in A29 ins Wellen-Detail.
  - **Kein `style.css`-Eingriff:** Marke nutzt `classList.add("status")` (bestehende Pille), Hinweis `class="hinweis"` — dadurch bleibt `index.html`/`style.css` unverändert (A10-Linie, kein Konflikt mit A23).
- **Konfliktgruppen (neu):**
  - **G15 „Freigabe-Fundament (Backend)":** `freigabe.py` (neu), `meta.py`, `server.py`, `overview.py`, `neu_aufgabe.py`, `tests/test_freigabe.py` (neu), `tests/test_neue_aufgabe_signal.py` (neu), `tests/test_meta.py`, `tests/test_api_schreiben.py`, `tests/test_neu_aufgabe.py`. **Überschneidet sich mit A27 (G13: `meta.py`, `server.py`, `okf_bundle.py`)** → erst nach Abschluss von A27.
  - **G16 „Freigabe-UI (Aufgaben)":** `static/js/liste.js`, `static/js/detail.js`, `tests/test_freigabe_ui.py` (neu). **Überschneidet sich mit A27-G14 (`detail.js`, `liste.js`) und mit A29** → nicht parallel zu A27/A29.
  - **G17 „Doku/Regelwerk":** `AGENTS.md`, `definitions/AGENTS.md`, `wissen/projekt/phasen.md`, `wissen/projekt/technische-spec.md` — disjunkt zu G15/G16, kann parallel zum UI-Paket laufen. `wissen/`-Statusfelder (`task_status`, `phase`, `aktuell`) ändert ausschließlich der PM/`documenter`.
- **Aufteilung in Pakete (ein Coder, eine Aufgabe):**
  - **Paket 0 — Freigabe-Fundament (gemeinsam A28/A29):** `freigabe.py` (`ist_freigegeben`, `setzen(pfad, wert, *, herkunft)`, `pruefe_ziel`, `MENSCH`/`KI`), 403-Guard in `meta.setzen`/`server.api_meta`, `POST /api/freigabe`, `freigabe: false` in `neu_aufgabe._inhalt`, generisches `freigabe`/`freigabe_hinweis` in `overview._eintrag`. Tests: T8–T21, T22 (Modul-/API-Teil), T15.
  - **Paket 1 — Wahrnehmungssignale:** `neu`, `kennung`, `naechste_kennung` in `overview` (Liste und Detail). Tests: T1–T7.
  - **Paket 2 — UI:** Marke in `liste.js`, Hinweis/Anzeige/Knopf in `detail.js`. Tests: T23–T33.
  - **Paket 3 — Doku/Regelwerk:** AK-9. Parallel zu Paket 2 möglich (disjunkte Dateien), Prüfschritt T36.
  - **Reihenfolge im Paket:** Test schreiben → rot → Minimum → grün → nächster Test. Paket 0 und 1 teilen `overview.py` → **nacheinander** vom selben Coder; Paket 2 nach Paket 1; Paket 3 parallel zu Paket 2.
- **Reihenfolge-Empfehlung und Freigabe-Gate:**
  1. **A27 abschließen** (Frontend `liste.js`/`detail.js` in Umsetzung, G13/G14 belegt) und **A30 abschließen** (Arbeitsstatus nutzt `liste.js`/`detail.js` und `overview.py`) — vorher **kein** Start von A28 Paket 0/2.
  2. **Freigabe von A28 durch die Projektleitung** (`freigabe: true` in dieser Datei) — **Start-Gate**. Aktuell fehlt das Feld; die Aufgabe ist damit nicht freigegeben und die Umsetzung darf **nicht** beginnen (Selbstanwendung der neuen Regel).
  3. Danach **Paket 0 → 1 → 2**, **Paket 3 parallel zu 2**; anschließend Review, Test (S1–S5), Doku.
  4. **A29 startet erst nach A28** (Paket 0 und 2 müssen grün und committed sein) **und** nach eigener Freigabe.
- **Abhängigkeiten:** A8 (`overview`-Felder), A9 (`POST /api/meta`-Semantik), A11/A12 (`liste.js`/`detail.js`-Muster), A13 (`neu_aufgabe`), A25/A27 (geteilte Dateien `liste.js`/`detail.js`, Filter-/Wellen-Verträge). A23 (`features.js`, `index.html`, `style.css`) ist **keine** Voraussetzung, solange diese Dateien unberührt bleiben.
- **Risiken/Grenzen:** (a) `neu` ist eine Heuristik — eine bewusst abweichende Dateibenennung (z. B. `a12-x.md` mit Titel `A13:`) gilt als „neu"; das ist gewollt (die KI soll die Inkonsistenz sehen). (b) `naechste_kennung` zählt nur `aufgaben/*.md`; Kennungen in anderen Dateien (z. B. Fließtext) zählen nicht. (c) Rechteklasse ohne Authentifizierung (siehe oben) — dokumentierte Grenze, kein Sicherheitsversprechen gegen einen böswilligen Aufruf. (d) `freigabe`-Feld in Wellen-Dateien wird von A27 nicht geschrieben; die Wellen-Datei bleibt bis zur ersten Freigabe unverändert (keine Migration). (e) `POST /api/freigabe` ist ein neuer Endpunkt → `ENDPUNKTE`-Inventar und `test_static.py` (falls Routen geprüft werden) müssen nachgezogen werden.
- **Offene Fragen an den PM (Standardentscheidung in Klammern, nicht blockierend):**
  1. Soll die Freigabe auch **in der Aufgabenliste** sichtbar sein (eigene Spalte/Marke), nicht nur im Detail? *(Standard: nein — Liste bleibt beim A11/A27-Vertrag, Detail genügt; sonst eigene Aufgabe.)*
  2. Soll es einen Filter „neu/unvergeben" geben? *(Standard: nein — Marke genügt, kein Eingriff in A25/A27-Filter.)*
  3. Soll `freigabe` beim Entziehen gelöscht oder auf `false` gesetzt werden? *(Standard: `false` schreiben — sichtbarer Zustand, ein Schlüssel, idempotent.)*
  4. Soll die App die Projektleitung aktiv benachrichtigen (Telegram)? *(Standard: nein — kein Seiteneffekt im Request, keine Config-Abhängigkeit; Prüfpflicht + Signal genügen.)*

# Betroffene Dateien

- `definitions/app/freigabe.py` (**neu**) — `MENSCH`/`KI`, `ist_freigegeben`, `setzen(pfad, wert, *, herkunft)`, `pruefe_ziel`; nutzt `meta.RechteFehler` (eine 403-Klasse) und `okf_bundle.set_meta` (ein atomarer Schreibvorgang) (T8–T14).
- `definitions/app/meta.py` — `freigabe`-Guard in `setzen` (immer `RechteFehler`) und Rechte-Matrix-Konstante; keine Änderung an `owner`/`status`/`welle`-Semantik (T15).
- `definitions/app/server.py` — `POST /api/freigabe` (`{path, wert}`) und 403-Guard in `api_meta`; keine weitere Route (T16–T20).
- `definitions/app/overview.py` — `neu`, `kennung`, `naechste_kennung` in `details`; `freigabe`/`freigabe_hinweis` in `_eintrag`; nicht lesbare Aufgaben `neu: true` (T1–T7).
- `definitions/app/neu_aufgabe.py` — `freigabe: false` im Frontmatter neuer Aufgaben (T22).
- `definitions/app/static/js/liste.js` — Marke „neu" in der Titel-Zelle der Tabellen (T23–T25).
- `definitions/app/static/js/detail.js` — `#detail-neu-hinweis`, Freigabe-Anzeige, `#detail-freigabe` mit POST/Erfolg/Fehler/Reload, `istAufgabe`-Erkennung, Payload-Helfer (T26–T33).
- `definitions/app/tests/test_freigabe.py` (**neu**) — T8–T21.
- `definitions/app/tests/test_neue_aufgabe_signal.py` (**neu**) — T1–T7, T22.
- `definitions/app/tests/test_freigabe_ui.py` (**neu**) — T23–T33; nutzt den Harness aus `tests/dom_helfer.py` (A30) und ergänzt den Fetch-Stub.
- `definitions/app/tests/test_meta.py` — additiver Modul-Test für den `freigabe`-Guard (T15).
- `definitions/app/tests/test_api_schreiben.py` — `ENDPUNKTE` + `/api/freigabe`-Fälle (T16–T20).
- `definitions/app/tests/test_neu_aufgabe.py` — additiv `freigabe is False` (T22).
- `AGENTS.md` **und** `definitions/AGENTS.md` — Workflow-Regel (AK-9); `definitions/` ist die Single Source of Truth, die Root-Datei wird mitgezogen.
- `wissen/projekt/phasen.md` — Phase „3b. Freigabe", Wartestatus `geplant`, `freigabe` im Aufgaben-Format (AK-9).
- `wissen/projekt/technische-spec.md` — Rechte-Matrix-Zeile `freigabe`, Feld-Doku, `POST /api/freigabe`, Read-Modell-Felder (AK-9).
- **Nicht geändert:** `definitions/app/static/index.html` (eingefroren seit A10), `static/style.css`, `static/js/app.js`, `static/js/api.js`, `static/js/formulare.js`, `static/js/features.js`, `static/js/projekt.js`, `definitions/app/okf_bundle.py`, `definitions/app/neu_welle.py`, `definitions/app/status.py`, `tests/test_detail.py`, `test_liste.py`, `test_suche.py`, `test_welle_zuordnung.py`, `test_formulare.py`, `test_features.py`, `test_static.py`, `test_api_lesen.py`, `test_neu_welle.py`, `test_okf_bundle.py`.

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

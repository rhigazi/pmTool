---
type: Task
title: "A29: Wellen abarbeiten"
description: Wellen die eine Aufgabe zugeordnet wurden werden erst ab gearbeitet wenn
  die gesamte Welle freigegeben wurde
freigabe: true
task_status: in Planung
phase: 2 Planung
priority: mittel
assigned_to: coder
owner: ai
aktuell: "PM: FREIGEGEBEN + Feld nachgetragen (Projektleitung 2026-11-15) — Umsetzung nach A28"
---

# Ziel

Aufgaben werden einer Welle zugeordnet (Feld `welle`, A27). Eine Welle ist **standardmäßig nicht freigegeben**. Erst die Freigabe der Welle durch die Projektleitung startet die Umsetzung der Aufgaben dieser Welle.

A29 baut auf dem Freigabe-Fundament aus A28 (Feld `freigabe`, Rechteklasse Mensch, `POST /api/freigabe`) auf und ergänzt drei Bausteine:

1. **Datenhaltung:** Boolesches Frontmatter-Feld `freigabe` in `wellen/<x>.md`; fehlt es oder ist es ≠ `true`, gilt die Welle als **nicht freigegeben** (fail-closed). Schreiben ausschließlich über den Menschen-Kanal; der KI-Weg liefert **403**.
2. **Wirksame Freigabe je Aufgabe:** Server-seitig berechnetes `welle_freigabe` und `wirksam_freigegeben` im Aufgaben-Detail (UND aus Aufgaben-Freigabe und Wellen-Freigabe; ohne Welle gilt nur die Aufgaben-Freigabe; fehlende/unbekannte Welle → gesperrt). Damit ist die Sperre an einer Stelle entschieden und testbar, nicht in mehreren UI-Stellen.
3. **Sichtbarkeit:** Wellenliste und Wellen-Detail zeigen den Freigabe-Status, das Wellen-Detail bietet „Welle freigeben"/„Freigabe entziehen" (Menschen-Kanal), das Aufgaben-Detail zeigt bei Sperre einen klaren Hinweis. Die Umsetzung startet wellenweit erst nach der Freigabe.

# Akzeptanzkriterien

- **AK-1 (Feld und Default, PM 1):** Wellen-Dateien tragen ein boolesches Frontmatter-Feld `freigabe`. Fehlt es, ist es `false` oder kein echtes `true` (z. B. `"ja"`, `"true"`, `1`, `null`), gilt die Welle als **nicht freigegeben** (zentral: `freigabe.ist_freigegeben`). Bestehende Wellen werden **nicht** migriert (kein Schreibvorgang), `neu_welle.anlegen` schreibt `freigabe: false` explizit.
- **AK-2 (Read-Modell, PM 1):** `GET /api/wellen` und `GET /api/overview` liefern für Einträge mit `typ == "Welle"` `freigabe: true|false` (immer vorhanden) und bei ungültigem Rohwert zusätzlich `freigabe_hinweis` (deutsch, ohne Pfad/OS-Details). Aufgaben-Einträge bleiben wie in A28; andere Typen erhalten kein `freigabe`-Feld.
- **AK-3 (Wirksame Freigabe im Aufgaben-Detail, PM 1):** `GET /api/file?path=aufgaben/<…>` liefert für Tasks zusätzlich `welle_freigabe` (JSON `true`, `false` oder `null`; Feld immer vorhanden) und `wirksam_freigegeben` (`bool`, immer vorhanden). Regeln: keine `welle` → `welle_freigabe is null`, `wirksam_freigegeben == freigabe`; Welle vorhanden und freigegeben → `welle_freigabe true`; Welle vorhanden und nicht freigegeben → `false`; `welle` zeigt auf eine fehlende/unbekannte/nicht-Wellen-Datei → `welle_freigabe is null` und `wirksam_freigegeben false` (fail-closed). `wirksam_freigegeben = freigabe AND (keine Welle OR welle_freigabe is True)`. Nicht-Task-Dateien erhalten keines der Felder.
- **AK-4 (Wellenliste sichtbar, PM 2):** Die Wellenliste zeigt je Zeile in der Titel-Zelle eine Marke mit dem Text „freigegeben" bzw. „nicht freigegeben" (`span`, `classList.add("status")`). Die Tabelle behält **vier Spalten** (A11/A27-Vertrag), `data-path` und Sortierung bleiben unverändert; Nicht-Wellen-Zeilen erhalten keine solche Marke. `index.html`/`style.css` bleiben unverändert.
- **AK-5 (Wellen-Detail: Anzeige und Bedienung, PM 2):** Das Wellen-Detail zeigt „Freigabe: freigegeben" bzw. „Freigabe: nicht freigegeben (Standard)" und genau einen Knopf (`#detail-welle-freigabe`) mit „Welle freigeben"/„Freigabe entziehen". Klick → genau ein `POST /api/freigabe` mit `{path, wert}`; Erfolgsmeldungen „Welle freigegeben." / „Freigabe entzogen."; danach Neuladen mit neuem Zustand. Während des Requests `disabled`, bei Fehler bleibt der Zustand, die Servermeldung ist sichtbar, der Knopf wird wieder bedienbar (`try/finally`). Aufgaben-Details zeigen diesen Knopf nicht.
- **AK-6 (Sperrhinweis im Aufgaben-Detail, PM 2):** Ist `wirksam_freigegeben == false`, zeigt das Aufgaben-Detail einen Hinweis (`#detail-sperre-hinweis`, `class="hinweis"`, `role="status"`): bei nicht freigegebener Welle „Umsetzung gesperrt: Welle nicht freigegeben.", bei nicht freigegebener Aufgabe „Umsetzung gesperrt: Aufgabe nicht freigegeben.", bei beidem „Umsetzung gesperrt: Aufgabe und Welle nicht freigegeben.". Bei `wirksam_freigegeben == true` oder bei Nicht-Tasks fehlt der Hinweis. Der Aufgaben-Freigabe-Knopf aus A28 bleibt unabhängig davon bedienbar.
- **AK-7 (Konsistenz mit A27, PM 1/2):** Zuordnung, Filter, Sortierung und die Wellen-Sicht aus A27 bleiben unverändert (Join über `GET /api/aufgaben`, `welle`-Feld als Single Source of Truth). A29 schreibt in die Wellen-Datei **ausschließlich** `freigabe`; `# Aufgaben` und alle anderen Frontmatter-Keys bleiben byte-identisch (Präzisierung von A27-AK-11: kein Schreiben der Wellen-Datei außer dem Freigabe-Feld). `welle`-Änderungen, Filter und das Wellen-Detail funktionieren unverändert; `overview.liste("wellen")` bleibt in Reihenfolge und Feldern gleich (nur `freigabe`/`freigabe_hinweis` kommen hinzu).
- **AK-8 (Rechte, PM 1):** `freigabe` ist Menschen-Recht (A28-Fundament): `POST /api/meta` mit `freigabe` → **403**; `meta.setzen(..., freigabe=…)` → `RechteFehler`; `freigabe.setzen(..., herkunft="ki")` → `RechteFehler`; in allen Fällen Datei byte-identisch und kein Schreibvorgang. `wellen/index.md` ist reserviert → 403; `wellen/<unbekannt>.md` → 404; Pfadausbruch/leer → 400.
- **AK-9 (Workflow-Regel dokumentiert, PM 3):** `AGENTS.md` und `definitions/AGENTS.md`: Eine Welle ist standardmäßig nicht freigegeben; freigeben/entziehen darf nur die Projektleitung über die App; die KI setzt `freigabe` nie (403). Vor jeder Beauftragung eines `coder` prüft der PM **beide** Gates (Aufgabe `freigabe: true` **und** – falls zugeordnet – Welle `freigabe: true`); erst die Wellen-Freigabe startet die Umsetzung aller zugeordneten, bereits freigegebenen Aufgaben. Ein Entzug stoppt keine laufende Umsetzung, sperrt aber weitere Beauftragungen (PM entscheidet über Rücklauf). `wissen/projekt/phasen.md` ergänzt die Wellen-Freigabe als zweite Stufe der Phase „3b. Freigabe" und dokumentiert die UND-Regel; `wissen/projekt/technische-spec.md` ergänzt `freigabe` bei Wellen, `welle_freigabe`/`wirksam_freigegeben` und die Gate-Regel.
- **AK-10 (Grenzen/Regression, alle):** Kein neuer Endpunkt über A28 hinaus (`POST /api/freigabe` wird wiederverwendet), keine neuen Abhängigkeiten, kein externer Dienst, keine Migration bestehender Wellen. `index.html`, `style.css`, `app.js`, `api.js`, `formulare.js`, `features.js`, `projekt.js`, `meta.py`, `server.py`, `okf_bundle.py` bleiben unverändert. XSS-sicher (`textContent`/`createElement`, nur `classList`), fail-loud bei `null`/Nicht-Array, deutsche Meldungen ohne Pfade. Bestehende Tests bleiben grün (Änderungen nur additiv); `bash definitions/verify.sh .` → Exit 0.

# Testfälle (TDD)

**Zuordnung AK → Testfälle:**
**AK-1** → T1–T3, T12. **AK-2** → T1–T3. **AK-3** → T8–T10. **AK-4** → T13, T14. **AK-5** → T15–T19. **AK-6** → T20. **AK-7** → T4, T5, T11, T22. **AK-8** → T6, T7. **AK-9** → T23, T24 (Review-Prüfschritte, kein pytest). **AK-10** → T21, T22.

Reihenfolge = Red-Green-Takt: erst Test schreiben, rot laufen lassen, dann das Minimum implementieren, dann refaktorisieren. Jede Testnummer ist ein eigener pytest-Fall. Neue Datei `tests/test_wellen_freigabe.py` (Backend); **Frontend-Tests werden in `tests/test_freigabe_ui.py` ergänzt** (von A28 angelegt; Harness aus `tests/dom_helfer.py`, in A30 angelegt — keine weitere Kopie). Neue Fixtures (Wellen mit/ohne `freigabe`, Aufgaben mit `welle`) werden im Test unter `tmp_path` angelegt; `bundle_min` hat nur `wellen/w1.md` ohne `freigabe`.

**A. Read-Modell (AK-1, AK-2)**

- **T1 Default = nicht freigegeben:** `wellen/w1.md` ohne `freigabe` → `GET /api/wellen`: Eintrag mit `path`, `typ == "Welle"`, `freigabe is False`, **kein** `freigabe_hinweis`; `GET /api/overview` derselbe Wert; Aufgabe `aufgaben/a1.md` (ohne `freigabe`) ebenfalls `freigabe is False` (A28-Feld).
- **T2 Freigegeben:** Welle mit `freigabe: true` → `GET /api/wellen` und `/api/overview` liefern `freigabe is True`; explizites `freigabe: false` → `False` ohne Hinweis.
- **T3 Ungültiger Wert fail-closed:** parametrisiert `"ja"`, `"true"`, `1`, `0`, `null`/leer → `freigabe is False` **und** `freigabe_hinweis` nicht leer, ohne Pfad-/OS-Details; die Welle bleibt in der Liste sichtbar (kein stilles Weglassen); `typ`, `titel`, `status`, `owner` unverändert.

**B. Endpunkt/Rechte für Wellen (AK-7, AK-8)**

- **T4 Wellen-Freigabe setzen:** `POST /api/freigabe {"path": "wellen/w1.md", "wert": true}` → 200 `{path, freigabe: true, frontmatter}`; Datei enthält genau eine Zeile `freigabe: true`, Body-SHA256 vor/nach identisch, genau ein `set_meta`-Aufruf (Spy); `GET /api/wellen` spiegelt `freigabe is True` sofort (Join-Beleg, kein Neustart).
- **T5 Entziehen und Konsistenz:** danach `wert: false` → 200, `freigabe is False`, genau ein `freigabe`-Schlüssel (`text.count("\nfreigabe:") == 1`), Body identisch, `# Aufgaben` byte-identisch, `owner`/`status`/`title`/`type` unverändert; A27-Daten (`GET /api/aufgaben`-Join, `welle`-Feld) unverändert.
- **T6 KI-Kanal verweigert:** `POST /api/meta {"path": "wellen/w1.md", "freigabe": true}` → **403**; `meta.setzen("wellen/w1.md", freigabe=True)` → `RechteFehler`; `freigabe.setzen("wellen/w1.md", True, herkunft=freigabe.KI)` → `RechteFehler`; Datei-SHA256 in allen Fällen unverändert, kein `set_meta`-Aufruf.
- **T7 Ziel-/Eingabefehler:** `wellen/index.md` → 403; `wellen/gibtsnicht.md` → 404; `wellen/../aufgaben/a1.md`, `/etc/passwd`, `""` → 400; `wert` fehlt/`"true"`/`1`/`null` → 400; `projekt/phasen.md` als Ziel (keine Welle/Aufgabe) → 400; Bundle unverändert (`_aussen`-Vergleich), Meldungen ohne Pfade.

**C. Wirksame Freigabe im Detail (AK-3)**

- **T8 `welle_freigabe`:** Aufgabe `aufgaben/a1.md` mit `welle: "wellen/w1.md"`; w1 `freigabe: true` → `GET /api/file` liefert `welle_freigabe is True`; w1 ohne Feld/`false` → `False`; Aufgabe ohne `welle` → `welle_freigabe is None` (Feld vorhanden, JSON `null`), `wirksam_freigegeben == freigabe`.
- **T9 `wirksam_freigegeben` (UND-Matrix):** parametrisiert (Aufgabe, Welle) = (true,true) → `True`; (true,false) → `False`; (false,true) → `False`; (false,false) → `False`; (true, keine Welle) → `True`; (false, keine Welle) → `False`; (true, `welle` zeigt auf `wellen/geloescht.md`) → `False` und `welle_freigabe is None` (fail-closed, kein Wurf).
- **T10 Abgrenzung:** `GET /api/file?path=wellen/w1.md` und `projekt/phasen.md` → weder `welle_freigabe` noch `wirksam_freigegeben` noch `neu`/`kennung`/`naechste_kennung`; Antwortform `{frontmatter, markdown, nachtraege}` unverändert; `welle` zeigt auf `aufgaben/a1.md` (kein Wellen-Typ) → `welle_freigabe is None`, `wirksam_freigegeben is False`, kein 500.
- **T11 A27-Konsistenz:** Wellen-Datei-SHA256 vor/nach `POST /api/freigabe` identisch **außer** der `freigabe`-Zeile (Body byte-identisch); die Aufgaben dieser Welle aus `GET /api/aufgaben` (Join) sind vor/nach identisch; Wellenliste-Sortierung und Felder unverändert; `test_welle_zuordnung.py` unverändert grün.
- **T12 Keine Migration:** `neu_welle.anlegen` schreibt `freigabe: false` im Frontmatter (additiver Test in `test_neu_welle.py`); bestehende Dateien unter `wissen/wellen/` werden durch die Umsetzung nicht verändert (`git diff` leer).

**D. Frontend (`tests/test_freigabe_ui.py`, AK-4, AK-5, AK-6, AK-10)**

- **T13 Marke in der Wellenliste:** `ladeWellen()` mit zwei Einträgen (eine `freigabe: true`, eine `false`) → je Zeile genau eine Marke „freigegeben"/„nicht freigegeben" in der Titel-Zelle (`classList.contains("status")`), `data-path` unverändert, **vier** Kopfspalten (Titel, Status, owner, zuletzt geändert), Sortierung unverändert; zweiter Aufruf erzeugt keine zweite Marke.
- **T14 Abgrenzung/XSS:** Aufgabenliste/Übersicht erhalten **keine** Wellen-Freigabe-Marke (nur die A28-„neu"-Marke); Wellentitel `<img src=x onerror=alert(1)>` erscheint textuell, kein `img`-Knoten, kein `alert`; fehlendes `freigabe`-Feld → „nicht freigegeben".
- **T15 Wellen-Detail Anzeige:** `ladeDetail({unterpunkt: "wellen/w1.md"})` mit `freigabe: false` → Text „Freigabe: nicht freigegeben (Standard)" und Knopf `#detail-welle-freigabe` mit „Welle freigeben"; mit `freigabe: true` → „Freigabe: freigegeben" und „Freigabe entziehen"; Aufgaben-Detail zeigt den Knopf nicht.
- **T16 Freigeben im Wellen-Detail:** Klick (Zustand nicht freigegeben) → genau ein `POST /api/freigabe` mit `{path: "wellen/w1.md", wert: true}`; Meldung „Welle freigegeben."; nach Neuladen „Freigegeben"; Knopf während des Requests `disabled`.
- **T17 Entziehen im Wellen-Detail:** Zustand freigegeben → Klick → genau ein `POST` mit `{path, wert: false}`; Meldung „Freigabe entzogen.".
- **T18 Fehlerpfad:** Stub antwortet 403 `{error: "…"}` → Fehlerbereich zeigt die Servermeldung, Anzeige bleibt beim alten Zustand (kein Neuladen), Knopf wieder bedienbar; Doppelklick während des Requests → genau ein POST.
- **T19 Requests:** Wellen-Detail = genau `GET /api/file` (kein zusätzlicher Request, insbesondere kein `/api/wellen`); Aufgaben-Detail = `GET /api/file` (+ `/api/wellen` aus A27) — kein neuer Request für die Sperre (Felder kommen aus `/api/file`).
- **T20 Sperrhinweis Aufgaben-Detail:** `wirksam_freigegeben: false`, `freigabe: true`, `welle_freigabe: false` → `#detail-sperre-hinweis` mit „Umsetzung gesperrt: Welle nicht freigegeben."; `freigabe: false`, `welle_freigabe: true` → „… Aufgabe nicht freigegeben."; beide `false` → „… Aufgabe und Welle nicht freigegeben."; `wirksam_freigegeben: true` → kein Hinweis; Aufgabe ohne Welle und `freigabe: true` → kein Hinweis; Welle/Projektdatei → kein Hinweis. Der A28-Freigabe-Knopf bleibt in allen Fällen sichtbar und bedienbar.
- **T21 XSS/Fail-loud:** `freigabe_hinweis` mit HTML-Payload wird als Text gerendert; `/api/wellen` liefert `null` → Wellenliste zeigt die A11-Meldung (kein stilles Leer-Ergebnis), die Aufgabenliste bleibt unberührt; Nicht-Array → Formatmeldung.
- **T22 A27-Regression:** `test_welle_zuordnung.py` unverändert grün (Dropdown, Filter, Wellen-Sicht, XSS); `test_liste.py`/`test_detail.py`/`test_suche.py` unverändert grün; `index.html`/`style.css` unverändert (`git diff --stat`).

**E. Doku (Review-Prüfschritte, kein pytest)**

- **T23 Regelwerk:** `AGENTS.md` und `definitions/AGENTS.md` enthalten: Welle standardmäßig nicht freigegeben, Freigabe nur Projektleitung, KI setzt nie `freigabe` (403), UND-Gate vor jeder Coder-Beauftragung, Wellen-Freigabe als letzter Auslöser, Entzug stoppt keine laufende Umsetzung. Nachweis mit Zitatstelle im Review-Ergebnis.
- **T24 Phasenmodell/Spec:** `wissen/projekt/phasen.md` nennt die zweite Freigabe-Stufe (Welle) und die UND-Regel; `wissen/projekt/technische-spec.md` enthält `freigabe` bei Wellen, `welle_freigabe`/`wirksam_freigegeben` und die Gate-Regel.

**UI-Szenarien für den `tester` (Moli-Browser, laufende App gegen Test-Bundle):**

- **S1 Wellen-Status:** Wellenliste öffnen → jede Welle zeigt „nicht freigegeben"; Wellen-Detail zeigt „Freigabe: nicht freigegeben (Standard)" und „Welle freigeben", keine Konsolenfehler.
- **S2 Freigeben:** „Welle freigeben" → Meldung „Welle freigegeben.", Anzeige „Freigegeben", Liste zeigt „freigegeben"; Wellen-Datei enthält `freigabe: true`, `# Aufgaben` unverändert.
- **S3 Gate:** Aufgabe mit dieser Welle und eigener Freigabe → Aufgaben-Detail ohne Sperrhinweis; Welle wieder entziehen → Aufgaben-Detail zeigt „Umsetzung gesperrt: Welle nicht freigegeben."; Aufgabe ohne Freigabe → „… Aufgabe nicht freigegeben.".
- **S4 Entziehen/Fehler:** „Freigabe entziehen" → `freigabe: false`; per Netzwerk 403 provozieren → sichtbare Meldung, Anzeige unverändert, Knopf bedienbar.
- **S5 A27-Kombination:** Aufgabe über das Wellen-Dropdown einer freigegebenen Welle zuordnen → Wellen-Sicht listet sie, Aufgaben-Detail sofort ohne Sperre; Zuordnung entfernen → nur Aufgaben-Freigabe gilt.

# Kontext

- **Anforderung (Projektleitung, 2026-11-15):** „Wellen, denen eine Aufgabe zugeordnet wurde, werden erst abgearbeitet, wenn die gesamte Welle freigegeben wurde. Standardmäßig ist eine Welle nicht freigegeben; erst durch die Freigabe der Welle beginnt die Umsetzung aller Aufgaben in einer Welle."
- **Datenhaltung der Wellen-Freigabe:** **Frontmatter-Feld `freigabe` (bool) in `wellen/<x>.md`**, Default fehlt = nicht freigegeben (fail-closed). Begründung: dieselbe Semantik wie bei Aufgaben (A28), OKF-lesbar ohne App, keine Zweitpflege in `wissen/wellen/index.md` (reserviert), ein atomarer Schreibvorgang über das vorhandene `okf_bundle.set_meta`. **Bewusste Präzisierung von A27-AK-11:** Die App schreibt die Wellen-Datei ab A29 **ausschließlich** für `freigabe`; `# Aufgaben` und alle anderen Keys bleiben unangetastet (Test T5/T11). Damit entfällt kein A27-Verhalten, die Aussage „Wellen-Datei wird nie geschrieben" wird zu „wird nur für `freigabe` geschrieben".
- **Gate-Semantik (UND, Empfehlung mit Begründung):** `wirksam_freigegeben = Aufgabe freigegeben AND (keine Welle zugeordnet OR Welle freigegeben)`. Begründung: A28 verlangt die Freigabe **je Aufgabe** (Planabnahme), A29 verlangt die Freigabe **je Welle** (MVP-Terminierung). Kein Zwang zur Wellen-Zuordnung: eine Ad-hoc-Aufgabe ohne Welle (z. B. ein Hotfix) wäre sonst nie umsetzbar. Die Wellen-Freigabe ist der **letzte Auslöser** („startet alle Aufgaben der Welle"), weil die Einzelfreigabe typischerweise vorher erfolgt. *Alternative (verworfen):* Wellen-Freigabe ersetzt die Einzelfreigabe (ODER) — dann wäre A28 für Wellen-Aufgaben wirkungslos und eine ungeplante Aufgabe würde mit der Welle mitlaufen.
- **Sichtbarkeit (PM-Vorgabe):** Freigabe-Status in Wellen-Liste **und** -Detail. In der Liste als Marke in der Titel-Zelle statt als neue Spalte, weil A27 die Vier-Spalten-Tabelle und ihre Tests festgeschrieben hat (kein Bruch des A11/A27-Vertrags); im Detail als `dl`-Feld plus Knopf. Keine `index.html`-/`style.css`-Änderung (A10-Linie, Konfliktfreiheit zu A23).
- **Ist-Stand im Code (geprüft 2026-11-15):**
  - A27 (in Umsetzung) liefert `welle` im Read-Modell und das Detail-Dropdown; `detail.js` lädt im Aufgaben-Detail bereits `/api/wellen` (A27-AK-1) — A29 braucht dort **keinen** zusätzlichen Request, nutzt aber die server-seitigen Felder aus `/api/file`.
  - `freigabe.py`, `POST /api/freigabe` und das generische `freigabe`-Feld in `overview._eintrag` entstehen in **A28 Paket 0** (gemeinsames Fundament). A29 implementiert **keine** zweite Rechteklasse und **keinen** zweiten Endpunkt.
  - `overview.details` liest heute nur die Zieldatei; für `welle_freigabe` kommt **ein** zusätzlicher toleranter Lesezugriff auf die Wellen-Datei (fehlend/kaputt → `null`/gesperrt, kein Fehler).
  - `detail.js` hat für das owner-Feld und die Statusknöpfe das Muster „POST → Meldung → `ladeDetail` → Rückfall bei Fehler"; die Wellen-Freigabe nutzt dasselbe Muster mit eigenem Endpunkt.
  - `liste.js` erhält die Marke in derselben Titel-Zelle wie A28s „neu" (gemeinsame Hilfsfunktion, damit beide Marken kombinierbar sind).
- **Umsetzungsentscheidungen (TDD-relevant, reversibel):**
  - **Wirksame Freigabe server-seitig**, nicht im UI: eine Wahrheit, testbar ohne DOM, und die KI kann sie über `GET /api/file` prüfen. `welle_freigabe` ist `null` (nicht `false`), wenn keine Welle zugeordnet ist oder die Wellen-Datei fehlt — `false` bleibt der echte „nicht freigegeben"-Zustand; die Sperre ist in beiden Fällen `wirksam_freigegeben: false`.
  - **Kein Schreiben in `wissen/wellen/index.md`** (reserviert) und keine Wellen-Migration: „nicht freigegeben" ist der sichere Default für den Altbestand.
  - **`freigabe: false` explizit bei Neuanlage** (`neu_welle.anlegen`) — symmetrisch zu A28, sichtbarer Zustand; das Feld ist ein Default, kein Recht (die Rechteklasse schützt das *Setzen* auf `true`/`false` durch die KI).
  - **Entzug sperrt nur künftige Beauftragungen:** laufende Umsetzungen werden nicht abgebrochen (kein Zwangslöschen, kein Statusrücksprung durch die App); der PM entscheidet über den Rücklauf. Dokumentiert in AK-9.
  - **A29 erweitert `tests/test_freigabe_ui.py`** (von A28 angelegt) statt eine sechste Mini-DOM-Kopie zu erzeugen; die Konsolidierung der Harness-Kopien bleibt [A14-6]. Deshalb ist A29 strikt nach A28 zu starten.
- **Konfliktgruppen (neu):**
  - **G18 „Wellen-Freigabe (Backend)":** `overview.py`, `freigabe.py` (nur falls eine Wellen-Lesehilfe nötig ist), `neu_welle.py`, `tests/test_wellen_freigabe.py` (neu), `tests/test_neu_welle.py`. **Überschneidet sich mit A27 (G13: `overview.py`) und A28 (G15/G16)** → nach beiden.
  - **G19 „Wellen-Freigabe (UI)":** `static/js/detail.js`, `static/js/liste.js`, `tests/test_freigabe_ui.py`. **Überschneidet sich mit A27-G14 und A28-G16** → nicht parallel.
  - **G20 „Doku/Regelwerk (Welle)":** `AGENTS.md`, `definitions/AGENTS.md`, `wissen/projekt/phasen.md`, `wissen/projekt/technische-spec.md` — parallel zum UI-Paket möglich; Statusfelder der Aufgaben ändert nur PM/`documenter`.
- **Aufteilung in Pakete (ein Coder, eine Aufgabe):**
  - **Paket 1 — Backend:** `welle_freigabe`/`wirksam_freigegeben` in `overview.details`, `freigabe: false` in `neu_welle`, ggf. Lesehilfe in `freigabe.py`. Tests: T1–T12.
  - **Paket 2 — UI:** Marke in `liste.js` (Wellenzeilen), Anzeige/Knopf im Wellen-Detail, Sperrhinweis im Aufgaben-Detail. Tests: T13–T22 (in `test_freigabe_ui.py` ergänzt).
  - **Paket 3 — Doku:** AK-9, Prüfschritte T23/T24; parallel zu Paket 2.
  - **Reihenfolge im Paket:** Test → rot → Minimum → grün. Paket 1 vor Paket 2 (UI braucht die Felder); Paket 3 parallel zu Paket 2.
- **Reihenfolge-Empfehlung und Freigabe-Gate:**
  1. **A27 abgeschlossen** (Wellen-Zuordnung, Filter, Wellen-Sicht, `detail.js`/`liste.js` committed), **A30 abgeschlossen** (Arbeitsstatus nutzt `liste.js`/`detail.js`) und **A31 abgeschlossen** (Wellen-Spalte in `liste.js`).
  2. **A28 Paket 0 (Freigabe-Fundament) und Paket 2 (Aufgaben-UI) abgeschlossen** — A29 nutzt `freigabe.py`, `POST /api/freigabe`, `freigabe` im Read-Modell und die gemeinsame Titel-Zellen-Hilfe.
  3. **Freigabe von A29 ist erteilt** (Projektleitung 2026-11-15, dokumentiert im Feld `aktuell`) — **Start-Gate erfüllt**; das Feld `freigabe` wird nach A28 Paket 0 maschinenlesbar nachgetragen. Die **Umsetzung** wartet dennoch auf Schritt 1 und 2.
  4. Danach **Paket 1 → 2**, **Paket 3 parallel zu 2**; anschließend Review, Test (S1–S5), Doku.
- **Abhängigkeiten:** A27 (Pflicht: Wellen-Zuordnung, `detail.js`/`liste.js`, `welle`-Read-Modell), A28 (Pflicht: Freigabe-Feld, Rechteklasse, Endpunkt, `overview`-Freigabefeld), A8/A11/A12 (Listen-/Detail-Muster), A25 (Filter, nur Regression). A23 ist keine Voraussetzung.
- **Risiken/Grenzen:** (a) UND-Gate kann überraschen („Welle frei, Aufgabe noch nicht") — deshalb der explizite Sperrhinweis mit Grund (AK-6) und die Doku-Regel. (b) `welle`-Feld zeigt auf gelöschte Welle → fail-closed gesperrt und im Detail als „Welle nicht freigegeben" angezeigt; keine automatische Bereinigung (A27-Verhalten). (c) `overview.details` macht einen zusätzlichen Lesezugriff je Aufgaben-Detail — unkritisch bei kleinen Bundles, Fehler werden zu `null` (kein 500). (d) Entzug während laufender Umsetzung stoppt nichts (dokumentiert, PM-Entscheidung). (e) Rechteklasse ohne Authentifizierung — dokumentierte Grenze wie A28.
- **Offene Fragen an den PM (Standardentscheidung in Klammern, nicht blockierend):**
  1. UND oder ODER aus Aufgaben- und Wellen-Freigabe? *(Standard: UND; Wellen-Freigabe ist der letzte Auslöser.)*
  2. Müssen Aufgaben zwingend einer Welle zugeordnet sein? *(Standard: nein — ohne Welle gilt nur die Aufgaben-Freigabe.)*
  3. Soll eine Wellen-Freigabe die Aufgaben-Freigabe automatisch mitziehen (Feld auf Aufgaben schreiben)? *(Standard: nein — je Aufgabe ein Feld, keine Sammelschreibung, kein Teilzustand.)*
  4. Soll der Entzug laufende Aufgaben zurücksetzen? *(Standard: nein — nur künftige Beauftragungen sperren, PM entscheidet.)*
  5. Freigabe-Status zusätzlich in `wissen/wellen/index.md`? *(Standard: nein — reservierte Datei, keine Doppelpflege.)*

# Betroffene Dateien

- `definitions/app/overview.py` — `welle_freigabe` (`true|false|null`) und `wirksam_freigegeben` in `details` für Tasks; toleranter Lesezugriff auf die Wellen-Datei (T8–T10).
- `definitions/app/freigabe.py` — nur falls eine Lesehilfe (`wellen_freigabe(pfad)`) nötig ist; **keine** zweite Rechteklasse, kein zweiter Endpunkt (T6).
- `definitions/app/neu_welle.py` — `freigabe: false` im Frontmatter neuer Wellen (T12).
- `definitions/app/static/js/liste.js` — Marke „freigegeben"/„nicht freigegeben" in der Titel-Zelle von Wellenzeilen, kombinierbar mit der A28-„neu"-Marke (T13, T14).
- `definitions/app/static/js/detail.js` — Freigabe-Feld im `dl` und `#detail-welle-freigabe` im Wellen-Detail; `#detail-sperre-hinweis` im Aufgaben-Detail; POST/Erfolg/Fehler/Reload, `try/finally`, Doppelklickschutz (T15–T20).
- `definitions/app/tests/test_wellen_freigabe.py` (**neu**) — T1–T12.
- `definitions/app/tests/test_freigabe_ui.py` — **von A28 angelegt**, hier um T13–T22 erweitert (gleicher Harness, bewusst keine sechste Kopie).
- `definitions/app/tests/test_neu_welle.py` — additiv `freigabe is False` (T12).
- `AGENTS.md` **und** `definitions/AGENTS.md` — Wellen-Gate, Rechte, UND-Regel (AK-9); `definitions/` ist die Single Source of Truth.
- `wissen/projekt/phasen.md` — zweite Freigabe-Stufe (Welle), UND-Regel (AK-9).
- `wissen/projekt/technische-spec.md` — `freigabe` bei Wellen, `welle_freigabe`/`wirksam_freigegeben`, Gate-Regel (AK-9).
- **Nicht geändert:** `definitions/app/static/index.html` (eingefroren seit A10), `static/style.css`, `static/js/app.js`, `static/js/api.js`, `static/js/formulare.js`, `static/js/features.js`, `static/js/projekt.js`, `definitions/app/meta.py`, `definitions/app/server.py`, `definitions/app/okf_bundle.py`, `definitions/app/status.py`, `definitions/app/tests/test_welle_zuordnung.py`, `test_liste.py`, `test_detail.py`, `test_suche.py`, `test_formulare.py`, `test_features.py`, `test_static.py`, `test_api_lesen.py`, `test_api_schreiben.py`, `test_meta.py`, `test_neu_aufgabe.py`, `test_freigabe.py`, `test_neue_aufgabe_signal.py`.

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

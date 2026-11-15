---
type: Document
title: Übergabeprotokoll — OKF Projekt-Manager (SPA)
description: Gesamtstand zum Sitzungswechsel 2026-11-15 (Pause): Aufgabenstatus, laufende/abgebrochene Arbeiten mit Rest-Umfang je Aufgabe, WIP-Hinweis, Weiterführung und Startprompt.
tags: [uebergabe, status, protokoll]
generated: { by: opencode/mimo-v2.6-pro, at: 2026-11-15T06:30:00Z }
status: aktuell
---

# Zweck dieses Protokolls

**Geplante Pause 2026-11-15 (Anweisung der Projektleitung):** Die Feature-Strecke ist weitgehend umgesetzt; die Projektleitung beginnt jetzt **eigene Testläufe** (Beginn von **A39** — gemeinsame Test-/Abstimmungsrunde). Danach werden **gemeinsam weitere Aufgaben festgelegt**. Dieses Protokoll sichert den gesamten Stand inkl. der **abgebrochenen Subagenten-Arbeit** (WIP-Commit `f00e81a`).

**Lesereihenfolge für eine neue Session (Projektmanager):** erst dieses Protokoll, dann `wissen/index.md`, dann `wissen/entscheidungen/log.md`. Den Startprompt aus `docs/startprompt.md` als erste Nachricht schicken.

# Projekt in Kürze

**OKF Projekt-Manager (SPA)** — browserbasierte Ein-Personen-Oberfläche zur Verwaltung eines OKF-Projekts in Mensch-KI-Zusammenarbeit. Tracker über dem OKF-Bundle `wissen/` (keine Zweitdatenbank); die eigentliche Arbeit läuft über den OpenCode-CLI-Chat (PM + Subagenten). Regeln: `AGENTS.md` (+ `definitions/AGENTS.md` = Single Source of Truth). Workflow: PM + `planner`/`coder`/`reviewer`/`tester`/`documenter`, TDD, Commits je Takt, Sofort-Push bei angenommenen Aufgaben.

# Aktueller Stand (2026-11-15, Pause)

- **Abgeschlossen:** A1–A20 (MVP), A23, A24, A25.
- **Review-frei + testbestanden, reif für Abschluss (nur Doku-Runde):** A27, A30, A31, A32.
- **In Arbeit (WIP, siehe unten):** A26, A28, A29, A34, A33-Batches.
- **Vormerkungen:** A35–A38 (nach A29/A33), A22/A21 (Post-MVP).
- **A39 (Testpause + README) läuft ab jetzt:** Projektleitung testet selbst; PM sammelt Befunde → Lückenliste → neue Aufgaben (ID+Titel+Sofort-Push) → README-Abschluss.

**Teststände (Zählumfang „Gesamtsuite" = Root-Suite = App-Suite + `definitions/tools/tests`; Spiegel `tools/tests` zählt nicht):**
- App-Suite zuletzt attestiert: **1338 passed** (Snapshot A29, Commit `7748dee`).
- Root-Suite zuletzt attestiert: **1118** (A26) + seitheriger Zuwachs (A28/A29/A34/WIP — nicht mehr nachgezogen).
- `bash definitions/verify.sh .` → zuletzt Exit 0 (Snapshot-Stände).
- **WIP-Commit `f00e81a` ist NICHT als grün attestiert** — die Suite kann dort rot sein (halbfertige Pakete).

# Aufgabenstatus (Stand: 2026-11-15, Pause)

| # | Aufgabe | Status | Was noch zu tun ist |
|---|---|---|---|
| A1–A20 | MVP-Strecke | abgeschlossen | — |
| A23/A24/A25 | Feature-Liste / Neues Projekt / Suche | abgeschlossen | — (Doku-Nachträge siehe A33-B9) |
| A27 | Wellen-Zuordnung | in Doku (reif) | Doku-Runde → `abgeschlossen` |
| A30 | Was passiert gerade | in Doku (reif) | Doku-Runde → `abgeschlossen` (Testlücke T5 → A33/A30-R1) |
| A31 | Welle in der Liste | in Doku (reif) | Doku-Runde → `abgeschlossen` (K1–K3/H1–H6 → A33) |
| A32 | Neues-Projekt-Flow | in Doku (reif) | Doku-Runde → `abgeschlossen` (H1/H2/H3/H6 → A33-Polish) |
| A26 | Verteilung + Root-Suite | in Nachbesserung | **Rücklauf W1/W2 abgebrochen** — WIP vervollständigen (siehe unten), dann Bestätigungs-Review; K1/K2/K5 → Doku |
| A28 | Freigabe + Wahrnehmung | in Nachbesserung | **Welle A abgebrochen** (W2/K7/W3/K5 vervollständigen); **Welle B offen** (W1/K1/K2); dann Bestätigungs-Review |
| A29 | Wellen abarbeiten | in Review | **Review + Testphase abgebrochen** — Zwischenurteil/-bericht einholen, ggf. Nachbesserung, dann Doku/Abschluss |
| A34 | Unter-Aufgaben | in Umsetzung | **Paket 1+2 abgebrochen** (WIP prüfen/fertigstellen); danach Paket 3 (UI, erst nach A33-B8), Paket 4 (Doku), Review/Test |
| A33 | Kleinbefunde-/Aufräum-Takt | in Umsetzung | **B5+B6+B8 abgebrochen** (vervollständigen); offen: B1 (nach A26!), B4, B7, B9 + Nachträge (siehe A33-Abschnitt) |
| A35–A38 | Status-Mapping serverseitig / schreibgeschuetzt-Signal / DOM-Harness / Log-Anker | offen (vorgemerkt) | Umsetzung nach A29/A33 (Reihenfolge A35 → A36; A37/A37 nach A29) |
| A22 | E2E-Regressionstest | offen (Post-MVP) | T1/T2/T7-Kette aus A17 überführen |
| A21 | Desktop-Modus/Lokal-Betrieb | vorgemerkt | Nummer reserviert, keine Datei |
| **A39** | **Gemeinsame Test-/Abstimmungsrunde + README-Abschluss** | **läuft (owner: mensch)** | Projektleitung testet; PM sammelt Befunde → Lückenliste → Folgeaufgaben → README final |

# Laufende/abgebrochene Arbeiten — Rest-Umfang im Detail (WIP-Commit `f00e81a`)

Die sechs laufenden Subagenten wurden um ~06:30 per STOPP angehalten; ihre unvollständige Arbeit steckt im WIP-Commit. **Nächste Session: zuerst `git status` + die WIP-Dateien sichten, Pakete sauber zu Ende bringen oder gezielt zurückrollen.**

1. **A26-Rücklauf (W1/W2 + K3/K4): FAKTISCH FERTIG** (Bericht nach STOPP): W1 Selbstkopie-Guard (Inode-Vergleich in `install_file` **und** `copy_tree`, kanonische Pfade), W2 Dev-Layout (`DEV_REPO=1`, 4b/5/10 werden übersprungen — real belegt: `setup.sh . --force` → Exit 0, kein `app/`), K3a–c (Tests t9/t10/t11), K4 Namensregel, README präzisiert. Tools-Suite 82 passed, Root-Suite **1373 passed** (ruhiger Baum), `verify.sh` Exit 0. **Offen:** (a) finaler Root-/Verify-Lauf auf ruhigem Baum (letzter Lauf kippte durch Fremd-Rot der Parallelarbeit — kein A26-Befund; t4/t10 spiegeln die App-Suite und sind last-sensibel), (b) **Bestätigungs-Review**. K1/K2/K5 → Doku-Runde.
2. **A28-Welle A: FERTIG** (Bericht nach STOPP): W2+K7 (T10 über `herkunft × wert` parametrisiert, Gegenwert + `set_meta`-Spy + Byte-Gleichheit je Fall; PM-Mutante getötet, 5 rot), W3 (Spec-Tabelle `freigabe`-Zeile), K5 (echter Leerfall-Modultest + Testname korrigiert; Kopie-Mutante würde fehlschlagen). `test_freigabe.py` 72 passed, `test_neue_aufgabe_signal.py` 33 passed, berührte Suiten 354 passed. **Offen:** (a) **Welle B** (W1 `overview.py` `NUMMER_DATEI` `$` + T5-Fall `a<N>.md`, K1 `neu`-Fixture-Default in `test_welle_spalte.py` entfernen, K2 `test_arbeitsstand.py` T12 exakte Menge), (b) Gesamt-App-Suite über den vereinigten Stand, (c) **Bestätigungs-Review**. Hinweis: K5-Test nutzt `kennung.naechste_kennung()` — bei A34-Abschluss ggf. Bezeichner anpassen.
3. **A29 (Review + Testphase): Testphase S1–S5 BESTANDEN** (Zwischenbericht nach STOPP, Snapshot `7748dee`, Moli): S1 Marken/Detail, S2 Freigeben (1 Request, nur `freigabe`-Zeile, `# Aufgaben` byte-identisch), S3 Sperrhinweise korrekt + Gate, S4 Live-Gate + 403-Rollback, S5 Robustheit/XSS. **HTTP-Matrix bestanden** (KI-Kanal 403 auch bei `false`, byte-identisch). Suite **1338 passed**. **Review-Zwischenurteil: NACHBESSERUNG (klein)** — **Muss:** falscher Sperrgrund bei `welle_freigabe: null` (= A29-T1, vom Review bestätigt, T20-Null-Fall fehlt); **Soll:** Wellen-Marke auf Wellen-Ansicht begrenzen (PM-Entscheidung), Label `"Freigabe:"` → `"Freigabe"`; Doku-Präzisierungen (Spec-Satz eingrenzen, T19-Aufgabentext veraltet). Gate-Logik/Rechte/Schreibpfad/Doku wurden als tragfähig belegt (Mutantenproben alle rot, byte-identische Schutzdateien). **Offen:** Rücklauf (Muss + Soll 1/2 + Doku-Präzisierungen), `verify.sh`-Lauf, Verteilungs-Probe, knappe Regressionsteilmenge, Vollständigkeits-Gegenlesung. Danach **Bestätigungs-Review** → Doku/Abschluss.
4. **A34-Paket 1+2: FERTIG** (Bericht nach STOPP): **Paket 1** `definitions/app/kennung.py` (neu: Grammatik `A{xxx}`/`A{xxx.uuu}`, `naechste_kennung` top-level-only, `naechste_unterkennung` kleinste freie 001–999 mit Lückenfüllung, 000/`A34.1`/`A034.001`-Regeln), `overview.py` nutzt nur noch `kennung.py`, `parent`/`kennung` in Listeneinträgen. **Paket 2** `neu_aufgabe.py` `parent`-Validierung (Tiefe 1 → 400, nicht `abgeschlossen`, `welle` ererbt, `welle`+`parent` → 400, Präfix-Normalisierung, Dateiname `a34.001-<slug>.md`). Tests: `test_kennung.py` T1–T8, `test_unteraufgabe.py` T13–T31, `test_neue_aufgabe_signal.py` T9–T12. **Gesamt-App-Suite: 1444 passed** (inkl. Parallelstände). **Bewusste Abweichung fürs Review prüfen:** die A28-Erwartung „Familienzählung" wurde für **verwaiste** `a34.001` (ohne Eltern-Datei) von `A35` auf `A2` korrigiert (AK-2/T8 strikt top-level-only) — konsistent? **Offen:** Paket 3 (UI `unteraufgaben.js` + `detail.js`, **wartet auf A33-B8**; danach `test_freigabe_ui.py` T33 → 3 Requests), Paket 4 (Doku; A33-Liste A34→A35–A38 umnummerieren = PM-Aufgabe), Review + Tester (S1–S5).
5. **A33-B5+B6+B8: FERTIG** (Bericht nach STOPP): **B5** Startfehler ohne Pfad (T12 rot→grün, T13 Bestandsschutz), **B6** T2 Body-Hash geschärft (Mutationsbeleg), **B8** `istDateiAntwort` zentral in `api.js` (drei Altkopien inkl. `projekt.js` entfernt) + alle Nachträge: A27-K2 (`bekannteWellen` für `wellen`), A31-H1 (Titel-Cache in `ladeListe`), **A27-F1 als „lazy nachladen"** (erste Filter-Interaktion → `GET /api/wellen`, kein Zusatzrequest beim Anzeigen, 3 neue Tests), A31-H3/H4 (Testschärfung; Mutationslauf: Status-Assertions bleiben grün). `test_static` 71, `test_welle_spalte` 27, `test_server` 28, `test_meta` 46; **Gesamt-App-Suite 1444 passed**. **Außerhalb des Auftrags weiter offen:** A27-K1 (`meta.py`-unquote), A30-R1 (T5 Nicht-String), A31-K3 (skipif im verteilten Projekt), plus Rest-Index-Assertion in `test_arbeitsstand_ui` T15 (`zellen[3]`) — Härtungs-Kandidat. Nichts unter `tools/` angefasst (A26-Regel). **Weiterhin offene A33-Batches:** B1 (Werkzeug-Härtung — **jetzt möglich**, A26-Rücklauf ist fertig), B4 (Wellen-Linktext, A13-3), B7 (Slug-Konsolidierung, A5-B4), B9 (Doku-Sammel: A4-2/A6-1/A9-K3/A9-K4/A16-1/A24-H2 + A5-B2-Asymmetrie).
6. **A33-Nachträge (gesammelt, nicht im obigen WIP):** A30-R1 (T5 Nicht-String-Fälle), A31-K3 (T19–T21 im verteilten Projekt per `skipif`), A32-H1/H2/H3/H6 (`start.sh`-Polish), A27-K1 (`meta.py` `_wellen_pfad` unquote — mit B6), A28-Testvermerk (A31-Fixture-Text präzisieren: Feld wird weggelassen, nicht `false` gesetzt).

# Offene Punkte (klein, in A33 verankert)

Siehe A33-Befund-Katalog in `wissen/aufgaben/a33-kleinbefunde-aufräum-takt.md` (18 Befunde in 9 Batches + Nachträge). Größere Punkte sind als eigene Aufgaben A35–A38 ausgegliedert. Betriebs-Hinweise (kein Code): A20-Pin-Pflege (Moli-URL+SHA256 gemeinsam), N8 (Suite wächst mit neuen Testdateien), Verteilungs-Prüfungen künftig aus committeten Snapshots (A31-K3-Ursache).

# Wichtige Regelungen (Auswahl, Details im Entscheidungslog)

- **Freigabe-Gate:** Umsetzung beginnt erst nach Freigabe der Projektleitung (Menschen-Recht; KI-Weg → 403; fail-closed `freigabe: true`). Phase „3b. Freigabe" in `phasen.md`. Freigaben A28/A29 als `freigabe: true` nachgetragen (stellvertretender Menschen-Kanal per Datei-Edit — künftig via `POST /api/freigabe`).
- **Neue Aufgaben:** wahrnehmen → ID + Titel (`A<N>: <Titel>`) + Dateiname → **sofort pushen** → planen → auf Freigabe warten → umsetzen.
- **Zählumfang:** „Gesamtsuite" = Root-Suite = App-Suite + `definitions/tools/tests`.
- **Testisolation:** nur tmp-Bundles, nie `wissen/`; Verteilungs-/Setup-Tests nur auf tmp-Ziele.
- **Freigabe-Interpretation:** „alle ausstehenden Features fertig machen" der Projektleitung gilt als Freigabe der Feature-Strecke (A31/A34 darunter); revidierbar.

# Weiterführung — nächste Schritte (in dieser Reihenfolge)

1. **A39 läuft:** Projektleitung testet. PM: Test-Befunde sammeln und als Lückenliste „was fehlt für sauberes Zusammenarbeiten" dokumentieren; daraus Folgeaufgaben ableiten (ID+Titel+Sofort-Push). Danach README final aktualisieren und bewusste Pause ohne neue Feature-Takte.
2. **WIP-Arbeit sauber abschließen** (Reihenfolge wegen Datei-Konflikte): A26-Rücklauf → A28-Welle A + B → A29-Review/-Test nachholen → A33-B5/B6/B8 vervollständigen → A34-P1+2 fertigstellen → A33-B8 → A34-P3 (UI) → A33-B1/B4/B7/B9 → A34-P4. Jeweils: Review + Testphase, Commits je Takt.
3. **Doku-Runde (`documenter`):** A27/A30/A31/A32 abschließen; A28-K4-Plan-Korrektur; A28-Testvermerk; Standzahlen nachziehen; Ergebnisprotokolle vervollständigen (A26-Datei fehlt!).
4. **Bestätigungs-Reviews** für A26- und A28-Rückläufe; A29-Review/-Test abschließen.
5. **Danach (Post-MVP):** A35–A38, A22, A21.

# Umgebungs-Wiederherstellung (neue Colab-Sitzung)

1. `git clone https://github.com/rhigazi/pmTool && cd pmTool`
2. `bash start.sh --colab` (lokal: `bash start.sh`) — erkennt bei Repo-Pull vorbefüllte Projektdaten und schlägt interaktiv den Reset vor (A32); `--neu` setzt gezielt zurück (Backup + saubere Vorlage).
3. Telegram-Secrets (`config.json` ist gitignored!): Colab-Secrets `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID`, Zelle aus `docs/colab-start.md`.
4. OpenCode-CLI im Projektverzeichnis starten; Session-Start-Regel: `wissen/index.md` zuerst.
5. Kontrolle: `bash definitions/verify.sh .` → Exit 0. `moli` liegt unter `/root/.local/bin/moli` (nicht im PATH — explizit aufrufen).

# Historie (Kurz)

1.–5.: siehe frühere Protokollstände (Projektstart, MVP A1–A20, Abnahmelauf A17 bestanden).
6. Post-MVP-Strecke 2026-11-15: A23/A24/A25 (abgeschlossen), A26/A27, Kleinbefunde-Takte.
7. Groß-Takt 2026-11-15 (diese Session): A27/A30/A31/A32 komplett (review-frei + testbestanden), A28 (Paket 0–3 umgesetzt, Review → Nachbesserung W1–W3), A29 komplett umgesetzt (Review/Test offen), A28/A29-Freigaben nachgetragen, A33 (B2/B3 erledigt, Nachträge gesammelt), A34 gestartet, A35–A38 angelegt, A39 als Abschluss-Meilenstein definiert. **STOPP + WIP-Commit `f00e81a`** auf Anweisung der Projektleitung (Beginn der Testphase A39).

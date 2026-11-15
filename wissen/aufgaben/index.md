# Aufgaben

Alle Aufgaben liegen als eigene Dateien in diesem Verzeichnis. Das Format ist in [/projekt/phasen.md](/projekt/phasen.md) definiert. **Stand 2026-11-15: MVP abnahmefähig** — die Aufgaben A1–A20 sind abgeschlossen, A23 ist in Review, A25 ist in Umsetzung (parallel, disjunkte Dateimengen), A24 ist in Doku (Review/Testphase gebündelt offen), A26 ist offen (Umsetzung nach A23/A25); offen sind außerdem die Post-MVP-Vormerkungen A21/A22.

# Laufende Aufgaben

* [A23: Feature-Liste](a23-feature-liste.md) - Menüpunkt „Feature List": Liste aller Features mit Status, Klick auf ein Feature zeigt die zugehörigen Aufgaben (offen / in Bearbeitung / erledigt) — **in Review** (Phase 5; Code fertig, 92 Tests grün, App-Suite 864)
* [A25: Suche in der Listenansicht](a25-suche.md) - Suchfeld über der Tabelle in allen drei Listen (Übersicht, Wellen, Aufgaben), mehrere Wörter = UND, Umlaut-/ß-tolerant, kombiniert mit Status-/owner-Filter, Leerzustand „Keine Treffer.", „Filter zurücksetzen" leert auch die Suche — **in Umsetzung** (Phase 3, läuft parallel zu A23)
* [A24: Neues Projekt beginnen (wissen/ zurücksetzen)](a24-neues-projekt.md) - `python3 tools/neues_projekt.py` ersetzt `wissen/` nach Plan-Vorschau (`--ja`) und Backup durch die OKF-Vorlage `definitions/wissen-vorlage/` — **in Doku** (Phase 7; Code fertig, 24 Tests grün, Review/Testphase gebündelt offen)
* [A26: Werkzeug-Verteilung und Root-Suite-Konflikt](a26-verteilung-und-suite-konflikt.md) - `neues_projekt.py` nach `definitions/tools/` spiegeln (Verteilung durch `setup.sh`) und den Collection-Konflikt der Root-Suite (doppelte Testdateinamen in `tools/` und `definitions/tools/`) lösen — **offen** (Phase 2, Umsetzung nach A23/A25)

# Abgeschlossene Aufgaben

* [A1: Fundament okf_bundle.py (Pfadschutz, Frontmatter-I/O, Scan)](a1-okf-bundle.md) - Zentrale Zugriffsschicht mit Pfadschutz, Frontmatter-I/O, atomarem Schreiben und Bundle-Scan — **abgeschlossen** (45 Tests; Sicherheits-Nachbesserung + Kleinbefunde)
* [A2: Status-Mapping status.py](a2-status-mapping.md) - `task_status`/`status` auf die 6 UI-Status abbilden, owner-Defaults, ohne Dateizugriff — **abgeschlossen** (44 Tests, Test bestanden, Doku)
* [A3: Nachtrag anfügen nachtrag.py](a3-nachtrag.md) - `# Nachträge` mit Marker `> **Nachtrag (Mensch, YYYY-MM-DD):**` rein anfügend ergänzen — **abgeschlossen** (21 Tests; A3-1/A3-2 erledigt)
* [A4: Aufgabe anlegen neu_aufgabe.py](a4-neu-aufgabe.md) - `aufgaben/<slug>.md` im Phasen-Format inkl. `owner: ai`, Slug-Normalisierung, Kollisionssuffix — **abgeschlossen** (32 Tests; Grenzfall-Fix)
* [A5: Welle anlegen neu_welle.md](a5-neu-welle.md) - `wellen/<kuerzel>.md` mit `type: Welle`, validiertem Status/owner, Aufgaben-Linkliste — **abgeschlossen** (55 Tests; Bestätigungs-Review review-frei)
* [A6: Meta-Update meta.py (owner/Status mit Rechteprüfung)](a6-meta.md) - Serverseitig nur `mensch`/`ai` und `Klarung`/`Geschlossen`, sonst 403; ein atomarer Schreibvorgang — **abgeschlossen** (30 Tests)
* [A7: Server-Gerüst und Start server.py](a7-server.md) - App-Factory, statische Auslieferung, JSON-Fehlerformat, Start über `BUNDLE_ROOT`/`PORT` — **abgeschlossen** (23 Tests; Pfad-Leak dreifach abgesichert)
* [A8: Lese-API overview / file / aufgaben / wellen](a8-api-lesen.md) - GET-Endpunkte für Liste, Detail mit Nachträgen und gefilterte Ansichten — **abgeschlossen** (33 Tests + Live-HTTP-Smoke)
* [A9: Schreib-API nachtrag / task / welle / meta](a9-api-schreiben.md) - POST-Endpunkte, Validierung vor dem Schreiben, korrekte 4xx-Codes — **abgeschlossen** (78 Tests + Live-Smoke; K1/W1/K2 erledigt)
* [A10: Frontend-Gerüst Navigation, Layout, Router, API-Client](a10-frontend-geruest.md) - `index.html`, `style.css`, `api.js`, Hash-Router in `app.js`; danach keine `index.html`-Änderungen — **abgeschlossen** (66 Tests, Testphase bestanden)
* [A11: Listenansicht mit Filtern und Klarung-Hervorhebung](a11-liste.md) - Tabelle aus der Overview-API, Status-/owner-Filter, Leer- und Fehlerzustand — **abgeschlossen** (54 Tests; A11-1 erledigt)
* [A12: Detailansicht Markdown, Nachtrag, owner/Status-Bedienung](a12-detail.md) - Detail mit XSS-sicherem Rendering, Nachtragsformular, nur Status `Klarung`/`Geschlossen` — **abgeschlossen** (52 Tests; T10/A12-3 erledigt)
* [A13: Formulare Aufgabe und Welle anlegen](a13-formulare.md) - Inline-Validierung, Erfolgsanzeige mit Pfad und kopierbarem Kurzkontext, Doppelklickschutz — **abgeschlossen** (81 Tests + Moli-Smoke; Kleinbefunde 1–2 erledigt, 3 Post-MVP)
* [A14: Entscheidungen- und Projekt-Ansicht](a14-projekt-ansicht.md) - Log-Einträge und die fünf Projekt-Unterpunkte über `GET /api/file`, kein neuer Endpunkt — **abgeschlossen** (55 Tests + Moli-Smoke; Review freigegeben)
* [A15: setup.sh/verify.sh um App-Verteilung erweitern](a15-setup-verify.md) - `app/` nach Zielprojekt verteilen, Verify-Prüfungen und App-Tests ergänzen — **abgeschlossen** (13/13 grün; R12/tools-Cache erledigt)
* [A16: Colab-Startzelle start_colab.py](a16-start-colab.md) - Pakete prüfen, Server als Subprozess starten, Port über Colab freigeben, Fallback-URL — **abgeschlossen** (8 Tests; A16-2/3 erledigt)
* [A17: End-to-End-Absicherung und Abnahmelauf](a17-e2e.md) - Gesamtsuite, API-E2E und Moli-Kernszenario auf Test-Bundle; `/content/pmTool/wissen` bleibt unberührt — **abgeschlossen** (Abnahmelauf bestanden: 23/23 API-E2E, 761 passed, verify.sh Exit 0, Moli 0 Konsolenfehler, Hash-Nachweis; MVP abnahmefähig)
* [A18: Startskript start.sh und docs/colab-start.md](a18-start-skript.md) - Umgebungs-Wiederherstellung: lokal, `--colab`, `--dry-run`, sauberes Ctrl+C; Anleitung inkl. Telegram-Secrets-Zelle — **abgeschlossen** (7 Tests; A18-1–3 erledigt)
* [A19: verify.sh akzeptiert definitions/app als Fallback](a19-verify-app-fallback.md) - Verify-Abschnitt 7 prüft `app/` oder `definitions/app/` (Fallback analog zu `start.sh`), passende Tests — **abgeschlossen** (5 Tests; verify.sh Exit 0 im Dev-Repo)
* [A20: setup.sh-Härtung (Moli/Skill-Installation)](a20-setup-haertung.md) - `--global`-Sektion absichern: Pin + SHA256, `command -v moli`-Guard, npx-Quelle, verify-Hinweistext — **abgeschlossen** (Teil 1 + Teil 2, Commits `c1a1a23`/`4d1f335`/`f0a37c8`/`cd91b78`)

# Offene Aufgaben (Post-MVP)

* [A22: E2E-Regressionstest (test_e2e.py)](a22-e2e-regression.md) - T1/T2/T7-Kette aus dem A17-Abnahmelauf als dauerhaften E2E-Test überführen — **offen** (Post-MVP)
* **A21 „Desktop-Modus/Lokal-Betrieb"** — **vorgemerkt** (Nummer reserviert, noch keine Aufgaben-Datei); pywebview-Desktop-Modus nach MVP (Entscheidung der Projektleitung 2026-11-14, siehe [features.md](/features.md))

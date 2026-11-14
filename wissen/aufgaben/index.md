# Aufgaben

Alle Aufgaben liegen als eigene Dateien in diesem Verzeichnis. Das Format ist in [/projekt/phasen.md](/projekt/phasen.md) definiert; jede Aufgabe ist so dokumentiert, dass ein `coder` sie eigenständig abarbeiten kann. Die Statusangaben entsprechen `task_status`/`phase` der Aufgaben-Dateien (Stand: Zwischenstände zum Halt, 2026-11-14).

# Offene Aufgaben

* [A13: Formulare Aufgabe und Welle anlegen](a13-formulare.md) - Inline-Validierung, Erfolgsanzeige mit Pfad und kopierbarem Kurzkontext, Doppelklickschutz — **offen**
* [A14: Entscheidungen- und Projekt-Ansicht](a14-projekt-ansicht.md) - Log-Einträge und die fünf Projekt-Unterpunkte über `GET /api/file`, kein neuer Endpunkt — **offen**
* [A17: End-to-End-Absicherung und Abnahmelauf](a17-e2e.md) - Gesamtsuite, API-E2E und Moli-Kernszenario auf Test-Bundle; `/content/pmTool/wissen` bleibt unberührt — **offen**
* [A19: verify.sh akzeptiert definitions/app als Fallback](a19-verify-app-fallback.md) - Verify-Abschnitt 7 prüft `app/` oder `definitions/app/` (Fallback analog zu `start.sh`), passende Tests — **offen**

# Laufende Aufgaben

* [A1: Fundament okf_bundle.py (Pfadschutz, Frontmatter-I/O, Scan)](a1-okf-bundle.md) - Zentrale Zugriffsschicht mit Pfadschutz, Frontmatter-I/O, atomarem Schreiben und Bundle-Scan — **im Test** (Umsetzung + Review fertig; offen: formale Testphase/Doku)
* [A3: Nachtrag anfügen nachtrag.py](a3-nachtrag.md) - `# Nachträge` mit Marker `> **Nachtrag (Mensch, YYYY-MM-DD):**` rein anfügend ergänzen — **im Review** (Umsetzung fertig; offen: Review/Test/Doku)
* [A4: Aufgabe anlegen neu_aufgabe.py](a4-neu-aufgabe.md) - `aufgaben/<slug>.md` im Phasen-Format inkl. `owner: ai`, Slug-Normalisierung, Kollisionssuffix — **im Review** (Umsetzung fertig; offen: Review/Test/Doku)
* [A5: Welle anlegen neu_welle.md](a5-neu-welle.md) - `wellen/<kuerzel>.md` mit `type: Welle`, validiertem Status/owner, Aufgaben-Linkliste — **im Review** (Umsetzung fertig; offen: Review/Test/Doku)
* [A6: Meta-Update meta.py (owner/Status mit Rechteprüfung)](a6-meta.md) - Serverseitig nur `mensch`/`ai` und `Klarung`/`Geschlossen`, sonst 403; ein atomarer Schreibvorgang — **im Test** (Umsetzung + Review fertig; offen: formale Testphase/Doku)
* [A7: Server-Gerüst und Start server.py](a7-server.md) - App-Factory, statische Auslieferung, JSON-Fehlerformat, Start über `BUNDLE_ROOT`/`PORT` — **im Test** (Umsetzung + Review fertig; offen: formale Testphase/Doku)
* [A8: Lese-API overview / file / aufgaben / wellen](a8-api-lesen.md) - GET-Endpunkte für Liste, Detail mit Nachträgen und gefilterte Ansichten — **im Review** (Umsetzung + Kleinnachtrag fertig; offen: Review/Testphase/Doku)
* [A9: Schreib-API nachtrag / task / welle / meta](a9-api-schreiben.md) - POST-Endpunkte, Validierung vor dem Schreiben, korrekte 4xx-Codes — **im Review** (Umsetzung fertig; offen: Review/Testphase/Doku)
* [A10: Frontend-Gerüst Navigation, Layout, Router, API-Client](a10-frontend-geruest.md) - `index.html`, `style.css`, `api.js`, Hash-Router in `app.js`; danach keine `index.html`-Änderungen — **in Doku** (Umsetzung + Review + Testphase bestanden; offen: Doku, Abschluss)
* [A11: Listenansicht mit Filtern und Klarung-Hervorhebung](a11-liste.md) - Tabelle aus der Overview-API, Status-/owner-Filter, Leer- und Fehlerzustand — **im Test** (Umsetzung + Review + Nachbesserung fertig; offen: Testphase/Doku)
* [A12: Detailansicht Markdown, Nachtrag, owner/Status-Bedienung](a12-detail.md) - Detail mit XSS-sicherem Rendering, Nachtragsformular, nur Status `Klarung`/`Geschlossen` — **im Review** (Umsetzung fertig; offen: Review/Testphase/Doku)
* [A15: setup.sh/verify.sh um App-Verteilung erweitern](a15-setup-verify.md) - `app/` nach Zielprojekt verteilen, Verify-Prüfungen und App-Tests ergänzen — **im Review** (Umsetzung fertig; offen: Review/Testphase/Doku)
* [A16: Colab-Startzelle start_colab.py](a16-start-colab.md) - Pakete prüfen, Server als Subprozess starten, Port über Colab freigeben, Fallback-URL — **im Review** (Umsetzung fertig; offen: Review/Testphase/Doku)
* [A18: Startskript start.sh und docs/colab-start.md](a18-start-skript.md) - Umgebungs-Wiederherstellung: lokal, `--colab`, `--dry-run`, sauberes Ctrl+C; Anleitung inkl. Telegram-Secrets-Zelle — **im Review** (Umsetzung + Testphase bestanden; offen: Review/Doku)

# Abgeschlossene Aufgaben

* [A2: Status-Mapping status.py](a2-status-mapping.md) - `task_status`/`status` auf die 6 UI-Status abbilden, owner-Defaults, ohne Dateizugriff — **abgeschlossen** (44 Tests, Test bestanden, Doku)

# Aufgaben

Alle Aufgaben liegen als eigene Dateien in diesem Verzeichnis. Das Format ist in [/projekt/phasen.md](/projekt/phasen.md) definiert; jede Aufgabe ist so dokumentiert, dass ein `coder` sie eigenständig abarbeiten kann. Die Statusangaben entsprechen `task_status`/`phase` der Aufgaben-Dateien (Stand: 2026-11-14, nach gebündelter Testphase und Review-Runden).

# Offene Aufgaben

* [A17: End-to-End-Absicherung und Abnahmelauf](a17-e2e.md) - Gesamtsuite, API-E2E und Moli-Kernszenario auf Test-Bundle; `/content/pmTool/wissen` bleibt unberührt — **offen**

# Laufende Aufgaben

## In Umsetzung (Nachbesserung/Korrektur läuft)

* [A20: setup.sh-Härtung (Moli/Skill-Installation)](a20-setup-haertung.md) - `--global`-Sektion absichern: Pin + SHA256, `command -v moli`-Guard, npx-Quelle, verify-Hinweistext — **in Umsetzung** (Teil 1 + Teil 2 umgesetzt; Semantik-Korrektur läuft)

## Im Review

* [A1: Fundament okf_bundle.py (Pfadschutz, Frontmatter-I/O, Scan)](a1-okf-bundle.md) - Zentrale Zugriffsschicht mit Pfadschutz, Frontmatter-I/O, atomarem Schreiben und Bundle-Scan — **im Review** (Sicherheits-Nachbesserung [B1]/[B2] umgesetzt; Bestätigungs-Review läuft)
* [A5: Welle anlegen neu_welle.md](a5-neu-welle.md) - `wellen/<kuerzel>.md` mit `type: Welle`, validiertem Status/owner, Aufgaben-Linkliste — **im Review** ([B1] behoben, Commit `d651ec6`; Bestätigung ausstehend; B2–B4 klein offen)
* [A7: Server-Gerüst und Start server.py](a7-server.md) - App-Factory, statische Auslieferung, JSON-Fehlerformat, Start über `BUNDLE_ROOT`/`PORT` — **im Review** (Sicherheits-Nachbesserung [A7-1] umgesetzt; Bestätigung läuft)
* [A9: Schreib-API nachtrag / task / welle / meta](a9-api-schreiben.md) - POST-Endpunkte, Validierung vor dem Schreiben, korrekte 4xx-Codes — **im Review** (Sicherheits-Nachbesserung K1/W1/K2/A8-1 umgesetzt; Bestätigung läuft; K3/K4 dokumentiert)
* [A13: Formulare Aufgabe und Welle anlegen](a13-formulare.md) - Inline-Validierung, Erfolgsanzeige mit Pfad und kopierbarem Kurzkontext, Doppelklickschutz — **im Review** (Umsetzung abgeschlossen, 81 Tests; Review + Testphase laufen parallel)
* [A14: Entscheidungen- und Projekt-Ansicht](a14-projekt-ansicht.md) - Log-Einträge und die fünf Projekt-Unterpunkte über `GET /api/file`, kein neuer Endpunkt — **im Review** (Umsetzung abgeschlossen, 55 Tests; Review + Testphase laufen parallel)
* [A19: verify.sh akzeptiert definitions/app als Fallback](a19-verify-app-fallback.md) - Verify-Abschnitt 7 prüft `app/` oder `definitions/app/` (Fallback analog zu `start.sh`), passende Tests — **im Review** (umgesetzt, verify.sh Exit 0, 5 neue Tests)

## In Doku

* [A3: Nachtrag anfügen nachtrag.py](a3-nachtrag.md) - `# Nachträge` mit Marker `> **Nachtrag (Mensch, YYYY-MM-DD):**` rein anfügend ergänzen — **in Doku** (Review freigegeben, Testphase bestanden; A3-1/A3-2 klein offen)
* [A4: Aufgabe anlegen neu_aufgabe.py](a4-neu-aufgabe.md) - `aufgaben/<slug>.md` im Phasen-Format inkl. `owner: ai`, Slug-Normalisierung, Kollisionssuffix — **in Doku** (Review freigegeben, Testphase bestanden; A4-1/A4-2 klein offen)
* [A6: Meta-Update meta.py (owner/Status mit Rechteprüfung)](a6-meta.md) - Serverseitig nur `mensch`/`ai` und `Klarung`/`Geschlossen`, sonst 403; ein atomarer Schreibvorgang — **in Doku** (Review freigegeben, Testphase bestanden; A6-2 optional offen)
* [A8: Lese-API overview / file / aufgaben / wellen](a8-api-lesen.md) - GET-Endpunkte für Liste, Detail mit Nachträgen und gefilterte Ansichten — **in Doku** (Review freigegeben, Testphase bestanden; A8-1 mit erledigt)
* [A10: Frontend-Gerüst Navigation, Layout, Router, API-Client](a10-frontend-geruest.md) - `index.html`, `style.css`, `api.js`, Hash-Router in `app.js`; danach keine `index.html`-Änderungen — **in Doku** (Testphase bestanden)
* [A11: Listenansicht mit Filtern und Klarung-Hervorhebung](a11-liste.md) - Tabelle aus der Overview-API, Status-/owner-Filter, Leer- und Fehlerzustand — **in Doku** (Review freigegeben, Testphase bestanden; A11-1 klein offen)
* [A12: Detailansicht Markdown, Nachtrag, owner/Status-Bedienung](a12-detail.md) - Detail mit XSS-sicherem Rendering, Nachtragsformular, nur Status `Klarung`/`Geschlossen` — **in Doku** (Review freigegeben, Testphase bestanden inkl. T10; A12-1/A12-3 klein offen)
* [A15: setup.sh/verify.sh um App-Verteilung erweitern](a15-setup-verify.md) - `app/` nach Zielprojekt verteilen, Verify-Prüfungen und App-Tests ergänzen — **in Doku** (Review-Nachbesserung erledigt, 13/13 grün; tools/-`__pycache__` offen)
* [A16: Colab-Startzelle start_colab.py](a16-start-colab.md) - Pakete prüfen, Server als Subprozess starten, Port über Colab freigeben, Fallback-URL — **in Doku** (Review freigegeben, Testphase bestanden; A16-1–4 klein offen)
* [A18: Startskript start.sh und docs/colab-start.md](a18-start-skript.md) - Umgebungs-Wiederherstellung: lokal, `--colab`, `--dry-run`, sauberes Ctrl+C; Anleitung inkl. Telegram-Secrets-Zelle — **in Doku** (Review freigegeben, Testphase bestanden; A18-1–3 klein offen)

# Abgeschlossene Aufgaben

* [A2: Status-Mapping status.py](a2-status-mapping.md) - `task_status`/`status` auf die 6 UI-Status abbilden, owner-Defaults, ohne Dateizugriff — **abgeschlossen** (44 Tests, Test bestanden, Doku)

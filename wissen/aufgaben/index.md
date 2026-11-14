# Aufgaben

Alle Aufgaben liegen als eigene Dateien in diesem Verzeichnis. Das Format ist in [/projekt/phasen.md](/projekt/phasen.md) definiert; jede Aufgabe ist so dokumentiert, dass ein `coder` sie eigenständig abarbeiten kann. Die Statusangaben entsprechen `task_status`/`phase` der Aufgaben-Dateien (Stand: 2026-11-14, nach gebündelter Testphase und Review-Runden).

# Offene Aufgaben

* [A17: End-to-End-Absicherung und Abnahmelauf](a17-e2e.md) - Gesamtsuite, API-E2E und Moli-Kernszenario auf Test-Bundle; `/content/pmTool/wissen` bleibt unberührt — **offen**

# Laufende Aufgaben

## In Umsetzung (Nachbesserung/Korrektur läuft)

*Noch keine.*

## Im Review

*Noch keine.*

## In Doku

* [A20: setup.sh-Härtung (Moli/Skill-Installation)](a20-setup-haertung.md) - `--global`-Sektion absichern: Pin + SHA256, `command -v moli`-Guard, npx-Quelle, verify-Hinweistext — **in Doku** (umgesetzt und gepusht, Commits `c1a1a23`/`4d1f335`/`f0a37c8`/`cd91b78`; Pin-Pflege offen)
* [A13: Formulare Aufgabe und Welle anlegen](a13-formulare.md) - Inline-Validierung, Erfolgsanzeige mit Pfad und kopierbarem Kurzkontext, Doppelklickschutz — **in Doku** (Review freigegeben, Testphase 2 bestanden inkl. Moli-Smoke; 81 Tests; Kleinbefunde 1–2 erledigt, 3 Post-MVP)
* [A14: Entscheidungen- und Projekt-Ansicht](a14-projekt-ansicht.md) - Log-Einträge und die fünf Projekt-Unterpunkte über `GET /api/file`, kein neuer Endpunkt — **in Doku** (Review freigegeben, Testphase bestanden, 55 Tests + Moli-Smoke; Kleinbefunde 2/3/4/8 erledigt, 5–9 offen)

* [A1: Fundament okf_bundle.py (Pfadschutz, Frontmatter-I/O, Scan)](a1-okf-bundle.md) - Zentrale Zugriffsschicht mit Pfadschutz, Frontmatter-I/O, atomarem Schreiben und Bundle-Scan — **in Doku** (Bestätigungs-Review review-frei; Doku/Abschluss)
* [A3: Nachtrag anfügen nachtrag.py](a3-nachtrag.md) - `# Nachträge` mit Marker `> **Nachtrag (Mensch, YYYY-MM-DD):**` rein anfügend ergänzen — **in Doku** (review-frei; A3-1/A3-2 erledigt)
* [A4: Aufgabe anlegen neu_aufgabe.py](a4-neu-aufgabe.md) - `aufgaben/<slug>.md` im Phasen-Format inkl. `owner: ai`, Slug-Normalisierung, Kollisionssuffix — **in Doku** (Review freigegeben, Testphase bestanden; A4-1/A4-2 klein offen)
* [A5: Welle anlegen neu_welle.md](a5-neu-welle.md) - `wellen/<kuerzel>.md` mit `type: Welle`, validiertem Status/owner, Aufgaben-Linkliste — **in Doku** (Bestätigungs-Review review-frei; A5-2 per PM-Entscheidung geschlossen)
* [A6: Meta-Update meta.py (owner/Status mit Rechteprüfung)](a6-meta.md) - Serverseitig nur `mensch`/`ai` und `Klarung`/`Geschlossen`, sonst 403; ein atomarer Schreibvorgang — **in Doku** (Review freigegeben, Testphase bestanden; A6-2 optional offen)
* [A7: Server-Gerüst und Start server.py](a7-server.md) - App-Factory, statische Auslieferung, JSON-Fehlerformat, Start über `BUNDLE_ROOT`/`PORT` — **in Doku** (Bestätigungs-Review review-frei; Doku/Abschluss)
* [A8: Lese-API overview / file / aufgaben / wellen](a8-api-lesen.md) - GET-Endpunkte für Liste, Detail mit Nachträgen und gefilterte Ansichten — **in Doku** (Review freigegeben, Testphase bestanden; A8-1 mit erledigt)
* [A9: Schreib-API nachtrag / task / welle / meta](a9-api-schreiben.md) - POST-Endpunkte, Validierung vor dem Schreiben, korrekte 4xx-Codes — **in Doku** (Bestätigungs-Review review-frei; K3/K4 dokumentiert)
* [A10: Frontend-Gerüst Navigation, Layout, Router, API-Client](a10-frontend-geruest.md) - `index.html`, `style.css`, `api.js`, Hash-Router in `app.js`; danach keine `index.html`-Änderungen — **in Doku** (Testphase bestanden)
* [A11: Listenansicht mit Filtern und Klarung-Hervorhebung](a11-liste.md) - Tabelle aus der Overview-API, Status-/owner-Filter, Leer- und Fehlerzustand — **in Doku** (Review freigegeben, Testphase bestanden; A11-1 erledigt)
* [A12: Detailansicht Markdown, Nachtrag, owner/Status-Bedienung](a12-detail.md) - Detail mit XSS-sicherem Rendering, Nachtragsformular, nur Status `Klarung`/`Geschlossen` — **in Doku** (Review freigegeben, Testphase 2 bestanden inkl. T10 + Moli-Smoke; A12-3/T4 erledigt; A12-1 und Schreib-UI-Grenze Post-MVP)
* [A15: setup.sh/verify.sh um App-Verteilung erweitern](a15-setup-verify.md) - `app/` nach Zielprojekt verteilen, Verify-Prüfungen und App-Tests ergänzen — **in Doku** (Bestätigungs-Review review-frei, 13/13 grün; R12/tools-Cache erledigt)
* [A16: Colab-Startzelle start_colab.py](a16-start-colab.md) - Pakete prüfen, Server als Subprozess starten, Port über Colab freigeben, Fallback-URL — **in Doku** (Review freigegeben, Testphase bestanden; A16-2/3 erledigt, 1/4 offen)
* [A18: Startskript start.sh und docs/colab-start.md](a18-start-skript.md) - Umgebungs-Wiederherstellung: lokal, `--colab`, `--dry-run`, sauberes Ctrl+C; Anleitung inkl. Telegram-Secrets-Zelle — **in Doku** (Review freigegeben, Testphase bestanden; A18-1–3 erledigt)
* [A19: verify.sh akzeptiert definitions/app als Fallback](a19-verify-app-fallback.md) - Verify-Abschnitt 7 prüft `app/` oder `definitions/app/` (Fallback analog zu `start.sh`), passende Tests — **in Doku** (Bestätigungs-Review review-frei; Doku/Abschluss)

# Abgeschlossene Aufgaben

* [A2: Status-Mapping status.py](a2-status-mapping.md) - `task_status`/`status` auf die 6 UI-Status abbilden, owner-Defaults, ohne Dateizugriff — **abgeschlossen** (44 Tests, Test bestanden, Doku)

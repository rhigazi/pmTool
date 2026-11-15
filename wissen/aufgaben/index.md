# Aufgaben

Alle Aufgaben liegen als eigene Dateien in diesem Verzeichnis. Das Format ist in [/projekt/phasen.md](/projekt/phasen.md) definiert. **Stand 2026-11-15: MVP abnahmefähig** — die Aufgaben A1–A20 sowie A23, A24 und A25 sind abgeschlossen; A26 (Werkzeug-Verteilung/Root-Suite-Konflikt) und A27 (Wellen-Zuordnung) sind in Review, A28–A33 sind in Planung/laufend. Offen sind außerdem die Post-MVP-Vormerkungen A21/A22.

# Laufende Aufgaben

* [A34: Unter-Aufgaben erstellen](a34-unter-aufgaben.md) - Unter einer Aufgabe Unter-Aufgaben anlegen und als Liste in der Detailansicht sehen; Nummernschema `A{xxx.uuu}` (u = 001–999) — **in Planung** (2026-11-15 aus der App angelegt, angenommen als A34; Konsistenz zu A28-Kennungsprüfung beachten)
* [A35: Status-Mapping server-seitig](a35-status-mapping-serverseitig.md) - `overview.details` liefert `ui_status`/`hinweis`/`owner_default` aus `status.py`, JS-Spiegel in `detail.js` entfällt (A12-1) — **offen** (vorgemerkt, Umsetzung nach A29)
* [A36: schreibgeschuetzt-Signal](a36-schreibgeschuetzt-signal.md) - API markiert reservierte Dateien, UI blendet Schreibaktionen aus; Server-403 bleibt zweite Barriere — **offen** (vorgemerkt, Umsetzung nach A35)
* [A37: DOM-Harness-Konsolidierung](a37-dom-harness-konsolidierung.md) - `tests/dom_helfer.py` als einzige Harness-Quelle, Altkopien umstellen (A14-6) — **offen** (vorgemerkt, Umsetzung nach A29)
* [A38: Log-Anker](a38-log-anker.md) - Anker je Log-Eintrag, Verweise öffnen den konkreten Eintrag (A14-9) — **offen** (vorgemerkt, Umsetzung nach A29)

* [A33: Kleinbefunde-/Aufräum-Takt](a33-kleinbefunde-aufräum-takt.md) - Gebündelte Behebung der offenen Kleinbefunde aus Reviews/Post-MVP (A24-K1–K3, A23-Fixture, A12-1, A14-5/6/7/9, N5/N8 u. a.) in Batches mit je eigenem Commit — **in Planung** (2026-11-15 vom PM angelegt; Umsetzung nach A30/A31/A32)

* [A32: Neues-Projekt-Flow — start.sh --neu + Erststart-Hinweis](a32-neues-projekt-flow.md) - Nach Repo-Pull erkennt `start.sh` pmTool-Projektdaten in `wissen/` und schlägt interaktiv den Reset vor (mit Backup); zusätzlich Flag `--neu` — **in Planung** (2026-11-15, Entscheidung der Projektleitung; Reset-Logik nur über A24-Werkzeug, keine zweite Lösch-Implementierung)

* [A31: Übersicht Liste um Welle ergänzen](a31-uebersicht-liste-um-welle-ergaenzen.md) - Die Übersichtsliste zeigt zu jeder Aufgabe die zugeordnete Welle (oder „keine") — **in Planung** (2026-11-15 aus der App angelegt, angenommen als A31; Priorität hoch; Umsetzung nach A30 wg. `liste.js`)

* [A30: Was passiert gerade](a30-was-passiert-gerade.md) - In-Arbeit-Aufgaben zeigen den Arbeitsstatus der Subagenten (Planer, Coder, Tester, Review, Documenter) — **in Planung** (2026-11-15 aus der App angelegt, angenommen als A30; von der Projektleitung als nächste Aufgabe priorisiert und freigegeben; Umsetzung nach A27 wg. `liste.js`)

* [A28: Benachrichtigung bei neuer Aufgabe](a28-benachrichtigung-neue-aufgabe.md) - Bei neuer Aufgabe wird die KI benachrichtigt; sie vergibt die Kennung in den Titel (`A<N>: Titel`) und wartet auf die Freigabe — erst danach beginnt die Umsetzung — **in Planung** (2026-11-15 aus der App angelegt und angenommen; Umsetzung erst nach Freigabe der Projektleitung)
* [A29: Wellen abarbeiten](a29-wellen-abarbeiten.md) - Aufgaben werden einer Welle zugeordnet; eine Welle ist standardmäßig nicht freigegeben — erst die Freigabe der Welle startet die Umsetzung aller Aufgaben der Welle — **in Planung** (2026-11-15 aus der App angelegt und angenommen; Umsetzung nach A27 wg. Datei-Überschneidung und nach Freigabe)

* [A27: Wellen-Zuordnung](a27-wellen-zuordnung.md) - Aufgaben nachträglich einer Welle zuordnen/entfernen (Detail-Dropdown), Listen nach Welle filtern, Aufgaben einer Welle im Wellen-Detail — **in Review** (Phase 5; Umsetzung 2026-11-15: 98 neue Tests, App-Suite **1039** grün; Review + UI-Szenarien S1–S7 laufen; die 2 A25-Klein-Befunde sind im Paket 2 mitbehoben)

* [A26: Werkzeug-Verteilung und Root-Suite-Konflikt](a26-verteilung-und-suite-konflikt.md) - `neues_projekt.py` nach `definitions/tools/` spiegeln (Verteilung durch `setup.sh`) und den Collection-Konflikt der Root-Suite (doppelte Testdateinamen in `tools/` und `definitions/tools/`) lösen — **in Review** (Phase 5; umgesetzt 2026-11-15: `definitions/tools/` ist Quelle, `conftest`-Lösung für die Root-Suite, `setup.sh` 4b) verteilt; Root-Suite **1118** grün; Review + Verteilungs-E2E laufen)

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
* [A23: Feature-Liste](a23-feature-liste.md) - Menüpunkt „Feature List": Liste aller Features mit Status, Klick auf ein Feature zeigt die zugehörigen Aufgaben (offen / in Bearbeitung / erledigt) — **abgeschlossen** (**92 Tests** (`test_features.py`), H1 geschlossen (Planzahl-Fehlzählung, auf 92 korrigiert), Kleinbefunde K1–K6 erledigt, Review freigegeben; App-Suite 864 — Zeitstand A23)
* [A24: Neues Projekt beginnen (wissen/ zurücksetzen)](a24-neues-projekt.md) - `python3 tools/neues_projekt.py` ersetzt `wissen/` nach Plan-Vorschau (`--ja`) und Backup durch die OKF-Vorlage `definitions/wissen-vorlage/` — **abgeschlossen** (**32 Tests**, Bestätigungs-Review FREIGEGEBEN 2026-11-15: beide wesentlichen Sicherheits-Befunde behoben, `tools/tests` 69 grün; Quelle jetzt `definitions/tools/` (A26), `tools/` ist Spiegel)
* [A25: Suche in der Listenansicht](a25-suche.md) - Suchfeld über der Tabelle in allen drei Listen (Übersicht, Wellen, Aufgaben), mehrere Wörter = UND, Umlaut-/ß-tolerant, kombiniert mit Status-/owner-Filter, Leerzustand „Keine Treffer.", „Filter zurücksetzen" leert auch die Suche — **abgeschlossen** (**72 Tests** (`test_suche.py`), Testphase S1–S6 bestanden 44/44 (tester, 2026-11-15), Review freigegeben; die 2 Klein-Befunde sind in A27 behoben und werden dort abgeschlossen)

# Offene Aufgaben (Post-MVP)

* [A22: E2E-Regressionstest (test_e2e.py)](a22-e2e-regression.md) - T1/T2/T7-Kette aus dem A17-Abnahmelauf als dauerhaften E2E-Test überführen — **offen** (Post-MVP)
* **A21 „Desktop-Modus/Lokal-Betrieb"** — **vorgemerkt** (Nummer reserviert, noch keine Aufgaben-Datei); pywebview-Desktop-Modus nach MVP (Entscheidung der Projektleitung 2026-11-14, siehe [features.md](/features.md))

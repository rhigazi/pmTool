---
type: Document
title: Übergabeprotokoll — OKF Projekt-Manager (SPA)
description: Gesamtstand zum Sitzungswechsel: Aufgabenstatus, offene Punkte, Weiterführung und Anleitung zur Umgebungs-Wiederherstellung in einer neuen Colab-Sitzung.
tags: [uebergabe, status, protokoll]
generated: { by: opencode/mimo-v2.6-pro, at: 2026-11-14T00:00:00Z }
status: aktuell
---

# Zweck dieses Protokolls

Dieses Dokument sichert den **gesamten Projektstand zum Sitzungswechsel**. Es wurde erstellt, weil die Arbeitsumgebung (Colab-Container) neu aufgesetzt wird. Mit diesem Protokoll, dem Repository (`github.com/rhigazi/pmTool`) und dem Startskript (`start.sh`) kann das Projekt in einer neuen Sitzung ohne Informationsverlust fortgesetzt werden.

**Start in der neuen Sitzung:** Den Startprompt aus `docs/startprompt.md` als erste Nachricht an den Projektmanager schicken — er bringt den PM auf Stand (inkl. Session-Start-Regel und Weiterführung).

**Lesereihenfolge für eine neue Session (Projektmanager):** erst dieses Protokoll, dann `wissen/index.md` (Session-Start-Regel), dann `wissen/entscheidungen/log.md`.

# Projekt in Kürze

**OKF Projekt-Manager (SPA)** — browserbasierte Ein-Personen-Oberfläche zur Verwaltung eines OKF-Projekts in Mensch-KI-Zusammenarbeit. Die App ist ein **Tracker** (Status/Zuständigkeit/Nachträge/Wellen), die eigentliche Arbeit läuft autonome über den OpenCode-CLI-Chat (Projektmanager + Subagenten). Datenquelle ist stets das OKF-Bundle `wissen/` — keine Zweitdatenbank.

Grundlagen: `docs/prd.md` (PRD + Entscheidungen), `wissen/projekt/technische-spec.md`, `wissen/projekt/user-stories/` (US-1…US-7), `wissen/projekt/planung.md` (TDD-Aufgabenplan A1–A17), `wissen/projekt/phasen.md` (Workflow/Format).

# Projektstruktur (Repository)

```
pmTool/
├── start.sh                 # Startskript Umgebungs-Wiederherstellung (A18)
├── docs/
│   ├── prd.md               # PRD + Produktentscheidungen
│   ├── colab-start.md       # Anleitung: neue Colab-Sitzung
│   └── uebergabeprotokoll.md  # dieses Dokument
├── definitions/             # Single Source of Truth (OpenCode-Definitionen)
│   ├── AGENTS.md, setup.sh, verify.sh, README.md
│   ├── agents/ (planner, coder, reviewer, tester, documenter)
│   ├── app/                 # App-Quelle: server.py, okf_bundle.py, status.py,
│   │                        #   overview.py, nachtrag.py, neu_aufgabe.py,
│   │                        #   neu_welle.py, meta.py, start_colab.py,
│   │                        #   static/ (index.html, style.css, js/*), tests/
│   └── wissen-vorlage/      # OKF-Gerüst für neue Projekte
├── wissen/                  # OKF-Bundle des Projekts (Datenbasis der App)
├── AGENTS.md, opencode.jsonc, .opencode/agents/, tools/   # installierte Projekt-Wurzel
└── .gitignore               # u. a. config.json (Telegram-Secret!), __pycache__
```

# Aufgabenstatus (Stand zum Halt)

Statuswerte laut Phasenmodell. „Review/Test/Doku offen" heißt: Umsetzung liegt vor, die Pipeline-Phasen 5–7 sind noch zu durchlaufen.

| # | Aufgabe | Status | Was liegt vor / Was fehlt |
|---|---|---|---|
| A1 | `okf_bundle.py` (Fundament) | Umsetzung + Review fertig (45 Tests) | Guard reservierter Dateien, zentrale Exceptions, Review-Nachbesserung erledigt. **Offen:** formale Testphase/Doku |
| A2 | `status.py` (Mapping) | Komplett (44 Tests, Test bestanden, Doku) | **Offen:** Abschluss (`abgeschlossen`) + Index-Verschiebung + Commit |
| A3 | `nachtrag.py` | Umsetzung fertig (19 Tests) | Sammel-Nachbesserung lief: T9-Test (reservierte Ziele abgewiesen), zentraler `EingabeFehler`. **Offen:** Review/Test/Doku |
| A4 | `neu_aufgabe.py` | Umsetzung fertig (32 Tests) | `EingabeFehler`-Import-Umstellung lief. **Offen:** Review/Test/Doku |
| A5 | `neu_welle.py` | Umsetzung fertig (48 Tests) | `ziel` ist Pflicht (PM-Entscheidung); Import-Umstellung lief. **Offen:** Review/Test/Doku |
| A6 | `meta.py` (Rechte) | Umsetzung + Review fertig (30 Tests, Testhärtung H1/H5/H7) | **Offen:** formale Testphase/Doku |
| A7 | `server.py` (Gerüst) | Umsetzung + Review fertig (12 Tests + Smoke) | **Offen:** formale Testphase/Doku |
| A8 | Lese-API (`overview.py`, 4 GET-Routen) | **Umsetzung + Review fertig (33 Tests)** — Kleinnachtrag sauber abgeschlossen | Pfadfreie Fehlermeldungen, Per-Datei-Guard (Overview bricht nicht), `.md`-Allowlist, Nachtrag-Parser mit Absatzumbruch. **Offen:** Review/Testphase/Doku; Detail-Endpunkt: unlesbare Datei → noch 500 statt neutraler Meldung (kleiner Punkt für A9-Review/A17) |
| A9 | Schreib-API (4 POST-Routen) | **Umsetzung fertig (78 Tests, Suite 541 grün)** — beim Halt sauber abgeschlossen | 4 POST-Routen + Helfer (`_json_nutzdaten`, `_pflicht_pfad`, `_ohne_pfadfeld`), Fail-Closed-Regeln bestätigt (PM-Entscheidung 2026-11-14). **Offen:** Review/Testphase/Doku |
| A10 | Frontend-Gerüst | Umsetzung + Review + **Testphase BESTANDEN** (66 Tests, UI-Szenarien T5–T8 via HTTP + Node-Harness) | **Offen:** Doku, Abschluss |
| A11 | Listenansicht | Umsetzung + Review fertig (40 Tests) | Nachbesserung (Fehlerzustand, fail-loud, `classList`) angehalten — Stand siehe Session-Rückmeldung. **Offen:** Testphase/Doku |
| A12 | Detailansicht | **Umsetzung fertig (49 Tests, Suite 539+ grün)** — beim Halt sauber abgeschlossen | Minimal-Renderer (XSS-sicher, E2E-Smoke bewiesen), Nachtrag-Formular, owner-Umschalter, nur `Klarung`/`Geschlossen`-Buttons, strikte Payload ohne leere Felder. **Offen:** Testphase (Moli/Harness), Review/Doku |
| A13 | Formulare (Aufgabe/Welle) | Offen | — |
| A14 | Entscheidungen-/Projekt-Ansicht | Offen | — |
| A15 | `setup.sh`/`verify.sh`/README | **Umsetzung fertig (Suite 549 grün, Exit 0)** — beim Halt sauber abgeschlossen | Abschnitt „10) App (`app/`)" mit `copy_tree` (ohne `__pycache__`), verify-Abschnitt „7) App", README mit Colab-Start-Zellen, `test_setup_verteilung.py` (9+1 Tests). **Offen:** Review/Testphase/Doku; Nebenbefund: `tools/`-Abschnitt kopiert weiterhin `__pycache__` (R12: bestehende Abschnitte unverändert) — eigene kleine Aufgabe |
| A16 | Colab-Startzelle `start_colab.py` | Umsetzung fertig (8 Tests gemockt) | **Offen:** Review/Testphase/Doku |
| A17 | E2E-Absicherung | Offen | — |
| A18 | Startskript `start.sh` + `docs/colab-start.md` | **In Arbeit (Vorrang, Übergabe)** | Teil dieser Übergabe |

**Teststand (letzter bekannter Gesamtlauf):** `python3 -m pytest definitions/app/tests -q` → **546 Tests grün, 2 fehlgeschlagen, 9 übersprungen**. Die 2 Fehlschläge stammen aus dem A18-Konflikt (`test_start_skript.py` erwartete `app/start.sh` im verteilten Ziel — Korrektur läuft; Ursprungskonflikt ist geklärt: `start.sh` bleibt Repo-Root-Werkzeug). Weitere Hinweise: `test_setup_verteilung.py::test_t1b_keine_cache_artefakte`/`test_t2_idempotenz` sind unter Parallelbetrieb flaky (in ruhiger Lage grün).

# Offene Punkte & anhängige Entscheidungen

1. **Moli-Browser fehlt** in der Umgebung — UI-Szenarien laufen per HTTP + Node-DOM-Harness (keine neue Abhängigkeit). **Offene Frage an die Projektleitung** (per Telegram gestellt): Moli installieren oder Harness-Weg beibehalten? Standardentscheidung: Harness.
2. **A9/A12/A15/Zwischenstände** — siehe Session-Rückmeldungen im Abschnitt unten (werden zum Zeitpunkt des Push ergänzt).
3. `feature:`-Feld in Aufgaben bleibt optional (Entscheidung R10); Feature-Dateien werden erst bei Feature-Beginn angelegt.
4. Gleicheitsschreibzugriffe (KI + App): kein Locking im MVP (R8), atomares Schreiben + Re-Read — bekanntes Risiko.

# Weiterführung — nächste Schritte

1. **Zwischenstände von A9/A12/A15 einarbeiten** (Stand aus den Session-Rückmeldungen unten) — A9/A12 fertigstellen oder verwerfen/Neuplanung entscheiden.
2. **A18 (Startskript)** abschließen und in `docs/colab-start.md` verifizieren.
3. **Offene Aufgaben:** A13 (Formulare), A14 (Entscheidungen/Projekt), A17 (E2E).
4. **Gebündelte Testphase** für A1, A3–A8, A11, A16 (DoD-Beleg wie bei A2/A10) — spart Einzelrunden.
5. **Doku-Runde** (`documenter`): Ergebnis-Protokolle in `wissen/aufgaben/*`, `features.md`, `log.md`.
6. **Commits** je Takt (Sicherungs-Commits laufend, wie seit 2026-11-14 praktiziert).
7. **MVP-Abnahme** durch die Projektleitung (siehe `wissen/projekt/phasen.md`).

# Umgebungs-Wiederherstellung (neue Colab-Sitzung)

1. **Repository klonen** (im Zielverzeichnis, z. B. `/content`):
   ```bash
   git clone https://github.com/rhigazi/pmTool
   cd pmTool
   ```
2. **Umgebung starten:**
   ```bash
   bash start.sh --colab   # in Colab: startet Server + öffnet Browser-Fenster
   # alternativ lokal: bash start.sh   (Server auf http://localhost:5000)
   ```
   Das Skript installiert fehlende Pakete (`flask`, `pyyaml`, `pytest`), prüft die Projektstruktur und startet die App mit `BUNDLE_ROOT=$PROJEKT/wissen` (absolut gesetzt, `PROJEKT` = Projektroot).
3. **Telegram-Konfiguration neu erzeugen** (`config.json` ist gitignored und wird **nicht** mitgeklont!): Colab-Secrets `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` setzen und die Zelle aus `docs/colab-start.md` ausführen.
4. **OpenCode-CLI im Projektverzeichnis starten** — Projektregeln (`AGENTS.md`) und Subagenten (`.opencode/agents/`) werden automatisch gefunden. Session-Start-Regel: zuerst `wissen/index.md` lesen.
5. **Kontrolle:** `bash definitions/verify.sh .` → Exit 0 = Umgebung vollständig.

# Session-Rückmeldungen zum Halt (Zwischenstände)

Alle laufenden Sessions wurden auf einen sicheren Stand gesetzt und haben gemeldet. Zusammenfassung (Details in den jeweiligen Aufgaben-Dateien, sobald die Doku-Runde erfolgt):

| Session | Ergebnis zum Halt |
|---|---|
| **A9 Schreib-API** | Sauber abgeschlossen: 4 POST-Routen (`/api/nachtrag`, `/api/task`, `/api/welle`, `/api/meta`) + Helfer, 78 Tests. Auslegungsfragen (path-Verbot in Anlege-Endpunkten, `null` = nicht gesetzt, Anlegen-Welle mit allen 6 UI-Status) vom PM bestätigt. Offen: Review/Testphase/Doku |
| **A12 Detailansicht** | Sauber abgeschlossen: `detail.js` mit XSS-sicherem Minimal-Renderer, Nachtrag-Formular, owner-Umschalter, nur `Klarung`/`Geschlossen`-Buttons, 49 Tests + E2E-Smoke. Offen: Testphase (Harness), Review/Doku |
| **A15 setup/verify/README** | Sauber abgeschlossen: setup.sh-Abschnitt „10) App" (copy_tree ohne `__pycache__`), verify-Abschnitt „7) App", README mit Colab-Start-Zellen, `test_setup_verteilung.py` (9+1 Tests). Nebenbefund: `tools/`-Abschnitt kopiert weiterhin `__pycache__` (offener Kleinpunkt) |
| **A8-Kleinnachtrag** | Sauber abgeschlossen: pfadfreie Fehlermeldungen, Per-Datei-Guard (Overview bricht nicht mehr), `.md`-Allowlist, Nachtrag-Parser mit Absatzumbruch, 33 Tests. Offener Kleinpunkt: unlesbare Datei im Detail → noch 500 statt neutraler Meldung |
| **A11-Nachbesserung** | Sauber abgeschlossen: Fehlerzustand bleibt sichtbar (auch bei Filterwechsel), fail-loud bei Nicht-Array, `classList` statt `className` (A13-tauglich), toter Code entfernt, XSS-Verbot erweitert, 54 Tests |
| **Sammel (zentrale Exceptions)** | Sauber abgeschlossen: `EingabeFehler` zentral aus `okf_bundle` (lokale Definitionen entfernt, Geschwister-Import in `neu_welle.py` aufgelöst), T9-Test parametrisiert über alle reservierten Dateien, 102 Tests |
| **A18 Startskript** | Sauber abgeschlossen: `start.sh` (lokal + `--colab`, `--dry-run`, sauberes Ctrl+C), `docs/colab-start.md` (inkl. Telegram-Secrets-Zelle), `test_start_skript.py` (7 Tests, skipif im verteilten Ziel). PM-Klarstellung umgesetzt: `start.sh` bleibt Repo-Root-Werkzeug, wird nicht von `setup.sh` verteilt |

**Endstand Gesamtsuite:** `python3 -m pytest definitions/app/tests -q` → **549 passed, Exit 0**. Separate Läufe: `tools/` → 37 passed.

**A18-Doku-Kosmetik (2026-11-14, erledigt):** Die drei Kosmetikpunkte aus der A18-Testverifikation sind behoben — (1) `--dry-run`-Hinweis („`verify.sh` wird dabei still übersprungen") in `docs/colab-start.md` und im `start.sh`-Kommentar; (2) `BUNDLE_ROOT`-Wortlaut an den tatsächlichen `start.sh`-Wert angeglichen (`$PROJEKT/wissen`, absolut); (3) Reihenfolge der Telegram-Secrets-Zelle vereinheitlicht: einheitlich **nach** `bash start.sh --colab` (Schritt 3) — Kurzfassung in `docs/colab-start.md` angeglichen.

# Offene Punkte (für die Weiterführung)

1. **Moli-Frage** an die Projektleitung offen (Telegram): Moli installieren oder Node-DOM-Harness beibehalten? Standardentscheidung: Harness.
2. **Root-Suite `pytest -q` bricht** (vorbestehend): doppelter Testdateiname `test_telegram_send.py` in `tools/tests/` und `definitions/tools/tests/` → Collection-Konflikt. Kleine Aufgabe: eine Datei umbenennen oder pytest-Konfiguration/`ignore` setzen.
3. **`tools/`-Abschnitt in `setup.sh`** kopiert weiterhin `__pycache__` mit (R12: bestehende Abschnitte unverändert gelassen) — kleine eigene Aufgabe.
4. **Detail-Endpunkt:** unlesbare Datei → 500 statt neutraler Meldung (Pfad-Leak-frei, aber nicht die gewünschte Fehlerart) — für A9-Review/A17 vormerken.
5. **Pipeline offen:** Für A1, A3–A8, A11, A16 fehlen die formalen Phasen 5–7 (Review/Test/Doku) — gebündelte Testphase vorgesehen. A9, A12, A15 stehen vor Review/Test/Doku. A13, A14, A17 sind offen.

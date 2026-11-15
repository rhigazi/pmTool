---
type: Document
title: Übergabeprotokoll — OKF Projekt-Manager (SPA)
description: Gesamtstand zum Sitzungswechsel: Aufgabenstatus, offene Punkte, Weiterführung und Anleitung zur Umgebungs-Wiederherstellung in einer neuen Colab-Sitzung.
tags: [uebergabe, status, protokoll]
generated: { by: opencode/mimo-v2.6-pro, at: 2026-11-14T00:00:00Z }
status: aktuell
---

# Zweck dieses Protokolls

Dieses Dokument sichert den **gesamten Projektstand** nach Abschluss der MVP-Umsetzung. Stand: **MVP abnahmefähig** — alle Aufgaben A1–A20 sind abgeschlossen. Zusätzlich sind A23 (Feature-Liste) und A25 (Suche) im Review, A24 (Neues Projekt) ist in Doku; offen sind die **MVP-Abnahme durch die Projektleitung**, A26 (Werkzeug-Verteilung/Root-Suite-Konflikt) und die Post-MVP-Vormerkungen A21/A22.

**Start in der neuen Sitzung:** Den Startprompt aus `docs/startprompt.md` als erste Nachricht an den Projektmanager schicken — er bringt den PM auf Stand (inkl. Session-Start-Regel und Weiterführung).

**Lesereihenfolge für eine neue Session (Projektmanager):** erst dieses Protokoll, dann `wissen/index.md` (Session-Start-Regel), dann `wissen/entscheidungen/log.md`.

# Projekt in Kürze

**OKF Projekt-Manager (SPA)** — browserbasierte Ein-Personen-Oberfläche zur Verwaltung eines OKF-Projekts in Mensch-KI-Zusammenarbeit. Die App ist ein **Tracker** (Status/Zuständigkeit/Nachträge/Wellen), die eigentliche Arbeit läuft autonom über den OpenCode-CLI-Chat (Projektmanager + Subagenten). Datenquelle ist stets das OKF-Bundle `wissen/` — keine Zweitdatenbank.

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
│   │                        #   static/ (index.html, style.css, js/*: app.js,
│   │                        #   api.js, liste.js, detail.js, formulare.js, projekt.js, features.js), tests/
│   └── wissen-vorlage/      # OKF-Gerüst für neue Projekte
├── wissen/                  # OKF-Bundle des Projekts (Datenbasis der App)
├── AGENTS.md, opencode.jsonc, .opencode/agents/, tools/   # installierte Projekt-Wurzel
└── .gitignore               # u. a. config.json (Telegram-Secret!), __pycache__
```

# Aufgabenstatus (Stand: 2026-11-15)

Statuswerte laut Phasenmodell. Alle Aufgaben A1–A20 sind **abgeschlossen** (Umsetzung, Review, Testphase, Doku/Ergebnisprotokoll); A23 und A25 sind **in Review**, A24 ist **in Doku**, A26 ist **offen**.

| # | Aufgabe | Status | Kurzstand / Beleg |
|---|---|---|---|
| A1 | `okf_bundle.py` (Fundament) | abgeschlossen | 45 Tests; Sicherheits-/Kleinbefunde erledigt |
| A2 | `status.py` (Mapping) | abgeschlossen | 44 Tests, Test bestanden, Doku |
| A3 | `nachtrag.py` | abgeschlossen | 21 Tests; A3-1/A3-2 erledigt |
| A4 | `neu_aufgabe.py` | abgeschlossen | 32 Tests; Grenzfall-Fix |
| A5 | `neu_welle.py` | abgeschlossen | 55 Tests; Bestätigungs-Review review-frei |
| A6 | `meta.py` (Rechte) | abgeschlossen | 30 Tests |
| A7 | `server.py` (Gerüst) | abgeschlossen | 23 Tests; Pfad-Leak dreifach abgesichert |
| A8 | Lese-API (4 GET-Routen) | abgeschlossen | 33 Tests + Live-HTTP-Smoke |
| A9 | Schreib-API (4 POST-Routen) | abgeschlossen | 78 Tests + Live-Smoke; K1/W1/K2 erledigt |
| A10 | Frontend-Gerüst | abgeschlossen | 66 Tests, Testphase bestanden |
| A11 | Listenansicht | abgeschlossen | 54 Tests; A11-1 erledigt |
| A12 | Detailansicht | abgeschlossen | 52 Tests (T10/A12-3 geschlossen) |
| A13 | Formulare (Aufgabe/Welle) | abgeschlossen | 81 Tests + Moli-Smoke |
| A14 | Entscheidungen-/Projekt-Ansicht | abgeschlossen | 55 Tests + Moli-Smoke; Review freigegeben |
| A15 | `setup.sh`/`verify.sh`/README | abgeschlossen | 13/13 Tests; R12/tools-Cache erledigt |
| A16 | Colab-Startzelle `start_colab.py` | abgeschlossen | 19 Tests; A16-2/3 + Port-Freigabe-Iterationen (final: neuer Browser-Tab via `proxyPort`, 2026-11-15) |
| A17 | E2E-Absicherung/Abnahmelauf | abgeschlossen | Abnahmelauf bestanden (23/23 API-E2E, Moli 0 Konsolenfehler, Hash-Nachweis) — **MVP abnahmefähig** |
| A18 | Startskript `start.sh` + `docs/colab-start.md` | abgeschlossen | 7 Tests; A18-1–3 erledigt |
| A19 | `verify.sh`-Fallback `definitions/app` | abgeschlossen | 5 Tests; `verify.sh` Exit 0 im Dev-Repo |
| A20 | `setup.sh`-Härtung (Moli/Skill-Installation) | abgeschlossen | Pin v1.1.24 + SHA256, `command -v moli`-Guard; Commits `c1a1a23`/`4d1f335`/`f0a37c8`/`cd91b78` |
| A23 | Feature-Liste (`features.js`) | in Review | 92 Tests; App-Suite **864** (Zeitstand A23); `markiereNavigation` funktional unverändert |
| A24 | Neues Projekt/Reset (`tools/neues_projekt.py`) | in Doku | 24 Tests; App-Suite **862** (Zeitstand A24); Verteilung/Root-Suite → A26 |
| A25 | Suche in der Listenansicht (`liste.js`) | in Review | 72 Tests (`test_suche.py`); **127 grün** (72+55); Gesamtsuite **936**; Moli-Szenarien S1–S6 offen |
| A26 | Werkzeug-Verteilung + Root-Suite-Konflikt | offen | `neues_projekt.py` nach `definitions/tools/`; doppelte Testdateinamen auflösen — nach A23/A25 |
| A21 | Desktop-Modus/Lokal-Betrieb | vorgemerkt (Post-MVP) | Nummer reserviert, noch keine Aufgaben-Datei |
| A22 | E2E-Regressionstest (`test_e2e.py`) | offen (Post-MVP) | Datei angelegt; überführt die T1/T2/T7-Kette aus A17 |

**Teststand (Stand A25, 2026-11-15):** `python3 -m pytest definitions/app/tests -q` → **936 passed, Exit 0** (Coder-Beleg; A23-Zeitstand 864; serialisiert — Parallelbetrieb ist eine bekannte Flaky-Zone). `bash definitions/verify.sh .` → **Exit 0**.

# Offene Punkte (Post-MVP)

* **A23/A25 im Review, A24 in Doku** — Review-Bestätigung und Testphase stehen aus; bei A25 sind die Moli-Szenarien S1–S6 offen, bei A23 S1–S4. Danach Abschluss/Doku und Sicherungs-Commit.
* **A26** Werkzeug-Verteilung + Root-Suite-Konflikt: `neues_projekt.py` nach `definitions/tools/` spiegeln (Verteilung durch `setup.sh`) und die doppelten Testdateinamen (`test_telegram_send.py`, künftig auch `test_neues_projekt.py`) auflösen — Umsetzung nach A23/A25.
* **A22** E2E-Regressionstest (`test_e2e.py`) — T1/T2/T7-Kette aus A17 dauerhaft überführen (offen).
* **A21** Desktop-Modus/Lokal-Betrieb (vorgemerkt, pywebview nach MVP).
* A12-1 Status-Mapping-Spiegel (Mapping-Drift langfristig lösen); A12-Grenze: Schreib-UI auf reservierten Dateien bleibt sichtbar (fail-loud 403) — Ausblendung erst mit `schreibgeschuetzt`-Signal der API.
* A13-3 Linktext-Kosmetik (bräuchte Wellen-Titel-Lookup).
* A4-1 `#`-Maskierung in `ziel`-Zeilen; A4-2 `welle`-Feld in Spec/phasen.md ergänzen.
* A5-B3 `description`-Feld bei Wellen; A5-B4 Slug-Logik-Duplikat.
* A6-1 H1/H5/H7-Belege je H-Punkt (H-Definitionen fehlen im Bundle); A6-2 T2 Body-Hash optional.
* A7-2 Startfehler-Meldung nennt absoluten Pfad.
* A9-K3 403-Notiz/Spec-Abgleich; A9-K4 TOCTOU als R8-Einschränkung (bekanntes Risiko).
* A14-5 `istDatei`/Meldungen nach `api.js`; A14-6 DOM-Harness-Fork `MINI_DOM` konsolidieren; A14-7 Request-Sequenz-Guard gegen Races; A14-9 Anker je Log-Eintrag.
* A16-1 R11-Zitat korrigieren oder Ausweichport vormerken; A16-4 Env-Weitergabe.
* N5 Cache-Fixture schreibt ins Definitions-Repo (kosmetisch); N8 T7 verschärft sich mit neuen Testdateien (Betriebshinweis).
* A20 Pin-Pflege: URL + SHA256 bei Moli-Updates zusammen ändern.
* Optional: Fett-Rendering des Nachtrag-Markers; owner-Signal-Testnotiz (A17-T1); Root-Suite-Konflikt → A26.

# Weiterführung — nächste Schritte

1. **Laufende Aufgaben abschließen:** Review von A23 (Feature-Liste) und A25 (Suche) bestätigen, A24-Review/Testphase gebündelt nachholen; Testphase mit Moli (A23 S1–S4, A25 S1–S6), danach Doku/Abschluss und Sicherungs-Commit.
2. **MVP-Abnahme durch die Projektleitung** (Kurzbericht: A17-Belege — 23/23 API-E2E, 761 passed, `verify.sh` Exit 0, Moli 0 Konsolenfehler, Hash-Nachweis; Aufgaben A1–A20 abgeschlossen; aktueller Teststand 936).
3. **Nach der Abnahme (Post-MVP):** A26 (Werkzeug-Verteilung/Root-Suite), A22 (E2E-Regression), A21 (Desktop-Modus) sowie die Post-MVP-/Aufräum-Punkte — ggf. als eigener Takt.
4. **Sicherungs-Commits** je Takt und nach jedem grünen Tester-Stand weiterführen (Regel „Sicherungs-Push nach grünen Tests").

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
3. **Telegram-Konfiguration neu erzeugen** (`config.json` ist gitignored und wird **nicht** mitgeklont!) — **nach** `bash start.sh --colab`: Colab-Secrets `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` setzen und die Zelle aus `docs/colab-start.md` ausführen.
4. **OpenCode-CLI im Projektverzeichnis starten** — Projektregeln (`AGENTS.md`) und Subagenten (`.opencode/agents/`) werden automatisch gefunden. Session-Start-Regel: zuerst `wissen/index.md` lesen.
5. **Kontrolle:** `bash definitions/verify.sh .` → Exit 0. Hinweis: Abschnitt 7 akzeptiert `app/` **oder** `definitions/app/` (Fallback) — `verify.sh` ist damit auch im Dev-Repo ohne verteiltes `app/` Exit 0. `moli` wird über `setup.sh --global` installiert (bzw. ist per Symlink im PATH).

# Historie (Kurz)

1. Sitzungsübergabe: Projekt angehalten, Übergabeprotokoll, Startskript (A18).
2. Weiterführung Takt 1: Zwischenstände A1–A19 eingearbeitet, A2 abgeschlossen, A19 angelegt.
3. Review-Runden 1+2, Bestätigungs-Review (A1/A5/A7/A9/A15/A19 review-frei), gebündelte Testphase, Testphase 2 (A12/A13/A14), Moli-Smoke erfolgreich.
4. Kleinbefunde-Takt (4 Batches, je eigener Commit) — 761 grün.
5. A17-Abnahmelauf bestanden → **MVP abnahmefähig** (alle A1–A20 abgeschlossen).
6. Post-MVP-Strecke 2026-11-15: A23 (Feature-Liste, 864) und A24 (Neues Projekt, 862) umgesetzt; A25 (Suche, `test_suche.py` 72 Tests) umgesetzt → Gesamtsuite **936**; A23/A25 im Review, A24 in Doku; A26 (Verteilung/Root-Suite) angelegt.

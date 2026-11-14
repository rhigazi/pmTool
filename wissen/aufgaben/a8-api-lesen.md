---
type: Task
title: "A8: Lese-API overview / file / aufgaben / wellen"
description: GET-Endpunkte für Übersichtsliste, Dateidetail inklusive Nachträgen sowie getrennte Aufgaben- und Wellenlisten.
task_status: offen
phase: 2 Planung
priority: hoch
assigned_to: coder
user_story: /projekt/user-stories/us-1.md
owner: ai
---

# Ziel

Lese-Endpunkte gemäß Spec: `GET /api/overview` (Liste mit `path, typ, titel, status, owner, zuletzt_geaendert, hinweis?, welle?`), `GET /api/file?path=` (`{frontmatter, markdown, nachtraege[]}`), `GET /api/aufgaben` und `GET /api/wellen`. Sortierung nach `zuletzt_geaendert` absteigend, Tie-Breaker `path`.

# Akzeptanzkriterien

- Alle nicht-reservierten `.md`-Dateien erscheinen mit korrektem Status-/owner-Mapping.
- Zeitstempel sind ISO-8601.
- Pfad-Traversal → 400 ohne Inhalte; fehlende Datei → 404.
- Eine Datei ohne Frontmatter bricht die Liste nicht.
- `nachtraege[]` parst die Markerzeilen aus dem Dateiinhalt.

# Testfälle (TDD)

- **T1 Overview-Liste:** `GET /api/overview` → 200, 3 Einträge (Fixture).
- **T2 Feldschema:** Keys ⊇ `path, typ, titel, status, owner, zuletzt_geaendert`.
- **T3 Status-Mapping (`in Umsetzung`):** `status == "In Arbeit"`.
- **T4 Sortierung:** absteigend nach `zuletzt_geaendert`, Tie-Breaker `path`.
- **T5 Reserve ausgeschlossen:** `index.md`/`log.md` nicht gelistet.
- **T6 Detaildatei:** `frontmatter.type == "Task"`, `markdown` ohne Frontmatter, `nachtraege` ist eine Liste.
- **T7 Traversal:** `?path=../../etc/passwd` → 400 `{error}`, Body ohne `root:`.
- **T8 Fehlende Datei:** → 404 `{error}`.
- **T9 Nur Aufgaben:** `GET /api/aufgaben` → nur `aufgaben/*`.
- **T10 Nur Wellen:** `GET /api/wellen` → nur `wellen/*`; leeres Verzeichnis → `[]`.
- **T11 Datei ohne Frontmatter:** → `typ == "unbekannt"`, 200.
- **T12 Nachtrag-Parsing:** Marker werden korrekt ausgelesen.

# Kontext

- **Abhängigkeiten:** A7 (App-Factory), A1 (`okf_bundle`), A2 (`status`).
- **Konfliktgruppe G7b+G7a:** `server.py` und `overview.py` — **nicht parallel zu A7/A9**.
- **Nachfolger:** A9 baut die Schreib-Endpunkte auf derselben App; A11/A12/A14 konsumieren die Lese-Endpunkte.
- **Entscheidungen:** R4 (Overview-Umfang: alle nicht-reservierten `.md`, `type` als `typ`, `index.md`/`log.md` ausgeschlossen), R7 (mtime als ISO-Zeitstempel), R3 (`owner` fehlt → `null`/„—", kein Migrationsschreiben).
- **Verweise:** Schnittstellen-Tabelle in [Technischer Spec](/projekt/technische-spec.md#schnittstellen-json-api-des-servers).

# Betroffene Dateien

- `definitions/app/overview.py`
- `definitions/app/server.py` (Routen)
- `definitions/app/tests/test_api_lesen.py`

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

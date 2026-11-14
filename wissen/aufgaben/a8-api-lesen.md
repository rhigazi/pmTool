---
type: Task
title: "A8: Lese-API overview / file / aufgaben / wellen"
description: GET-Endpunkte für Übersichtsliste, Dateidetail inklusive Nachträgen sowie getrennte Aufgaben- und Wellenlisten.
task_status: in Doku
phase: 7 Dokumentation
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
- **T5 Reserve ausgeschlossen:** `index.md`/`log.md`/`features.md` nicht gelistet.
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
- **Entscheidungen:** R4 (Overview-Umfang: alle nicht-reservierten `.md`, `type` als `typ`, `index.md`/`log.md`/`features.md` ausgeschlossen), R7 (mtime als ISO-Zeitstempel), R3 (`owner` fehlt → `null`/„—", kein Migrationsschreiben).
- **Verweise:** Schnittstellen-Tabelle in [Technischer Spec](/projekt/technische-spec.md#schnittstellen-json-api-des-servers).

# Betroffene Dateien

- `definitions/app/overview.py`
- `definitions/app/server.py` (Routen)
- `definitions/app/tests/test_api_lesen.py`

# Ergebnisse

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-14 — coder (Kleinnachtrag, Stand zum Halt)

- **Ergebnis:** Kleinnachtrag sauber abgeschlossen: pfadfreie Fehlermeldungen, Per-Datei-Guard (Overview bricht bei unlesbaren Dateien nicht mehr ab), `.md`-Allowlist, Nachtrag-Parser mit Absatzumbruch. (Quelle: Session-Rückmeldung „A8-Kleinnachtrag" im Übergabeprotokoll.)
- **Belege:** 33 Tests.
- **Befunde:** (a) Offener Kleinpunkt: Detail-Endpunkt liefert bei unlesbarer Datei noch 500 statt einer neutralen Meldung (pfad-leak-frei) — für A9-Review/A17 vormerken. (b) Widerspruch im Übergabeprotokoll: Statusspalte nennt „Umsetzung + Review fertig", die Fehlt-Spalte „Offen: Review/Testphase/Doku". Hier als **Review offen** geführt, da der Kleinnachtrag nach dem Review lief.
- **Offene Punkte:** Review, Testphase, Doku.

## 2026-11-14 — tester (Gebündelte Testphase)

- **Ergebnis:** **Testphase BESTANDEN** (DoD-Beleg): 33 Tests grün + Live-HTTP-Smoke, keine offenen Testbefunde. Gesamtlauf: 549 passed (Start = Ende, kein Zuwachs), 0 rot, 0 geskippt.
- **Offene Punkte:** Review ausstehend.

## 2026-11-14 — reviewer (Review-Runde 1, Kleinnachtrag)

- **Ergebnis:** **Freigegeben** — keine kritischen Befunde. 1 Kleinbefund.
- **Befunde:** [A8-1] klein: `_zeitstempel`-Guard in `overview._eintrag` (in der Sicherheits-Nachbesserung mit erledigt, siehe Eintrag coder 2026-11-14).
- **Offene Punkte:** Doku/Abschluss.

## 2026-11-14 — coder (Kleinbefunde-Takt, Batch A)

- **Ergebnis:** [N3] Regressionssicherung: Ungültiges YAML → 200 mit `frontmatter: {}` ist jetzt durch Tests belegt und damit dokumentiert.
- **Belege:** Kleinbefunde-Takt Batch A (+12 Tests); Gesamtsuite 761 grün.
- **Offene Punkte:** Doku/Abschluss.

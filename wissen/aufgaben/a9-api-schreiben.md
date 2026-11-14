---
type: Task
title: "A9: Schreib-API nachtrag / task / welle / meta"
description: POST-Endpunkte mit vollständiger Validierung vor dem Schreiben, korrekten 4xx-Codes und Pfadschutz.
task_status: im Review
phase: 5 Review
priority: hoch
assigned_to: coder
user_story: /projekt/user-stories/us-2.md
owner: ai
---

# Ziel

POST-Endpunkte gemäß Spec: `/api/nachtrag`, `/api/task`, `/api/welle`, `/api/meta`. Validierung vollständig **vor** dem Schreiben (kein Teilzustand), Fehler als 4xx `{error}` mit korrektem Code (403 für Rechteverstöße), alle Pfade gegen `BUNDLE_ROOT` geprüft.

# Akzeptanzkriterien

- Alle vier POST-Endpunkte sind implementiert und nutzen A3–A6.
- Ungültige Eingaben führen zu 4xx mit `{error}` und ohne Datei-/Verzeichnisrest.
- Rechteverstöße liefern 403, Pfadverstöße 400.
- Erfolgsantworten enthalten den Pfad (`{path}`) bzw. die aktualisierten Daten.
- Es entsteht nie ein Teilzustand (weder Datei noch Verzeichnis).

# Testfälle (TDD)

- **T1 Nachtrag ok:** POST gültig → 200, Antwort enthält Marker; Datei enthält Marker.
- **T2 Nachtrag leer:** POST mit leerem Text → 400, Datei-Hash unverändert.
- **T3 Aufgabe ok:** POST gültig → 200 `{path}`; in `/api/overview` mit `Offen`/`ai`.
- **T4 Aufgabe unvollständig:** Pflichtfeld fehlt → 400, keine neue Datei.
- **T5 Welle ok:** POST gültig → 200 `{path}`; in `/api/wellen`.
- **T6 Welle ungültiger Status:** → 400 `{error}`.
- **T7 Meta owner:** POST `{owner: "ai"}` → 200, `owner: ai` in der Datei.
- **T8 Meta Status verboten (`Testing`):** → 403 `{error}`, Datei unverändert.
- **T9 Meta reserviert (`index.md`):** → 400/403 `{error}`.
- **T10 Traversal (alle 4 Endpunkte):** `path` mit `../` → 400 `{error}`.
- **T11 JSON-Fehlerformat:** `application/json`, `error` nicht leer.
- **T12 Kein Teilzustand:** bei Fehlschlag weder Datei noch Verzeichnis angelegt.

# Kontext

- **Abhängigkeiten:** A8 (App-Gerüst und Lese-Routen), A3, A4, A5, A6.
- **Konfliktgruppe G7c:** **nach A8** — `server.py` nicht parallel bearbeiten.
- **Nachfolger:** A12 (Nachtrag/Meta-UI) und A13 (Formulare) nutzen diese Endpunkte.
- **Entscheidungen:** R1 (nur `Klarung`/`Geschlossen` sind über die API setzbar; Pipeline-Status 403), R8 (atomares Schreiben, kein Locking im MVP), R13 (Datum im Marker als Parameter, Serverzeit UTC).
- **Design-Notizen aus Reviews A6/A7:** (a) Exception-Mapping der Domänenfehler ist in `server.py` bereits ergänzt (`BundlePfadFehler`/`FrontmatterFehler`/`EingabeFehler` → 400, `ReservierteDateiFehler`/`meta.RechteFehler` → 403, `FileNotFoundError` → 404) — nutzend übernehmen; (b) `meta.setzen` prüft die Whitelist strikt ohne Trimming: Das Frontend (A12) darf leere/Whitespace-Felder nicht senden — nicht gesetzte Felder weglassen; (c) unbekannte Werte (`status="in Klärung"`) liefern 403 statt 400 — bekannter, aber verbotener Pipeline-Status; 400 bleibt ungültigen/unbekannten Werten vorbehalten; (d) Whitelist greift vor dem Lesen: ungültiger Wert + nicht existierende Datei → 403 (bewusst fail-closed).
- **Verweise:** Schnittstellen-Tabelle und Schreibrechte in [Technischer Spec](/projekt/technische-spec.md#schnittstellen-json-api-des-servers).

# Betroffene Dateien

- `definitions/app/server.py` (POST-Routen)
- `definitions/app/tests/test_api_schreiben.py`

# Ergebnisse

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-14 — coder (Umsetzung, Stand zum Halt)

- **Ergebnis:** 4 POST-Routen (`/api/nachtrag`, `/api/task`, `/api/welle`, `/api/meta`) inkl. Helfer (`_json_nutzdaten`, `_pflicht_pfad`, `_ohne_pfadfeld`); Fail-Closed-Regeln bestätigt (PM-Entscheidung 2026-11-14: `path`-Verbot in Anlege-Endpunkten, `null` = nicht gesetzt, Anlegen-Welle mit allen 6 UI-Status — siehe [Entscheidungslog](/entscheidungen/log.md)). (Quelle: Session-Rückmeldung „A9 Schreib-API" im Übergabeprotokoll.)
- **Belege:** 78 Tests; Gesamtsuite 549 grün (Endstand zum Halt).
- **Offene Punkte:** Review, Testphase, Doku.

## 2026-11-14 — tester (Gebündelte Testphase)

- **Ergebnis:** **Testphase BESTANDEN** (DoD-Beleg): 78 Tests grün + Live-Smoke (`/api/nachtrag`, `/api/task`, `/api/welle` ok; 400/403 korrekt), keine offenen Testbefunde. Gesamtlauf: 549 passed (Start = Ende, kein Zuwachs), 0 rot, 0 geskippt.
- **Offene Punkte:** Review ausstehend.

## 2026-11-14 — reviewer (Review-Runde 1)

- **Ergebnis:** **Nachbesserung läuft** (gemeinsamer Rücklauf A7+A9 an `coder`).
- **Befunde:** [K1] kritisch: Pfad-Leak in 404-Meldungen (gleiche Ursache wie A7-1). [W1] wesentlich: Schreibziel-Validierung vor dem Schreiben. [K2] klein: 400 statt 200-No-Op bei leerer Payload (PM-Entscheidung). [A8-1] klein: `_zeitstempel`-Guard. [K3] PM-Entscheidung: Das 403-Verhalten bleibt AK-konform (A6-AK „sonst 403") — Design-Notiz (c) entsprechend präzisiert (kein Code-Change). [K4] TOCTOU: bekannte Einschränkung laut R8 (atomares Schreiben, kein Locking im MVP).
- **Offene Punkte:** K1/W1/K2/A8-1 in Umsetzung; K3 im Ergebnisprotokoll präzisiert; K4 als bekannte Einschränkung dokumentiert.

## 2026-11-14 — documenter (Präzisierung K3 + bekannte Einschränkung K4)

- **K3 (403-Verhalten, PM-Entscheidung):** Design-Notiz (c) wird präzisiert: Unbekannte/verbotene Workflow-Werte (z. B. `status="in Klärung"`) liefern bewusst **403**, nicht 400 — das ist AK-konform (A6-AK: „sonst 403"), weil der Wert bekannt, aber für die App nicht setzbar ist. 400 bleibt ungültigen/unbekannten Werten und Payload-Fehlern vorbehalten. Kein Code-Change.
- **K4 (TOCTOU):** Bekannte Einschränkung laut Entscheidung R8 — atomares Schreiben + Re-Read, kein Locking im MVP; gleichzeitige Schreibzugriffe (KI + App) können sich überschreiben. Bekanntes Risiko, nicht im MVP-Scope.
- **Offene Punkte:** K1/W1/K2/A8-1 (siehe coder-Eintrag); K4 bleibt bewusst offen.

## 2026-11-14 — coder (Sicherheits-Nachbesserung, abgeschlossen)

- **Ergebnis:** [K1]/[A7-1] Pfad-Leak geschlossen (neutrale Meldungskonstanten in `okf_bundle`, zentraler `_sichere_meldung`-Schutz in `server._domaenen_handler`). [W1] Schreibziel-Validierung vor dem Schreiben (`okf_bundle.pruefe_zieldatei()`/`_pruefe_schreibziel`: `.md` + Datei-Existenz), angewandt in `nachtrag.anfuegen` und `meta.setzen` (Fail-Closed-Reihenfolge: Whitelist vor Pfad-Check). [K2] `POST /api/meta` ohne setzbare Felder → 400 „Keine setzbaren Felder" (PM-Entscheidung). [A8-1] `_zeitstempel` im Guard-try von `overview._eintrag`.
- **Belege:** 29 neue Tests (alle rot→grün belegt), Gesamtsuite 676 grün; Commit des Sicherheits-Blocks.
- **Offene Punkte:** Bestätigungs-Review läuft parallel.

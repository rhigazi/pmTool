---
type: Task
title: "A9: Schreib-API nachtrag / task / welle / meta"
description: POST-Endpunkte mit vollständiger Validierung vor dem Schreiben, korrekten 4xx-Codes und Pfadschutz.
task_status: in Umsetzung
phase: 4 Umsetzung
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

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

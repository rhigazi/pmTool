---
type: Feature
title: OKF Projekt-Manager (SPA)
description: Browserbasierter Tracker auf das OKF-Bundle — Status/Zuständigkeit anzeigen, Nachträge einfügen, Aufgaben und Wellen anlegen; aus Colab gestartet, Daten bleiben die .md-Dateien des Bundles.
status: in Umsetzung
priority: hoch
---

# Ziel

Eine Ein-Personen-Oberfläche (SPA) zur Verwaltung von OKF-Projekten in Mensch-KI-Zusammenarbeit: Der Mensch sieht jederzeit Status, Zuständigkeit und offene Rückfragen, kann Nachträge anfügen und Aufgaben/Wellen anlegen — die inhaltliche Bearbeitung bleibt bei der KI. Kommunikationskanal bleiben Dateien und Status im Bundle, kein Zweitdatenbestand.

# Umfang (MVP)

- **Tracker-Funktion:** Listenansicht über die fünf Navigationspunkte mit Titel, Status (6 UI-Werte), `owner` und letzter Änderung; Filter nach Status/owner; offene Rückfragen (`Klarung`) hervorgehoben.
- **Status & owner:** `owner` umschaltbar (`mensch`/`ai`); der Mensch darf Status `Klarung`/`Geschlossen` setzen, Pipeline-Status bleibt KI-Sache (serverseitig geprüft).
- **Nachträge:** rein anfügendes Einfügen als `> **Nachtrag (Mensch, YYYY-MM-DD):** …` in beliebige OKF-Dateien, ohne bestehende Inhalte zu überschreiben.
- **Aufgaben & Wellen:** Anlegen im Phasen-Format (`aufgaben/<slug>.md`, `wellen/<kuerzel>.md`) inkl. Slug-Normalisierung und Aufgaben-Verknüpfung.
- **Colab-Start:** eine Zelle startet den Flask-Server und gibt den Port über die eingebaute Colab-Port-Freigabe frei (kein externer Tunnel); Daten unter `/content/pmTool/wissen/`.
- **Schutz:** Pfadschutz gegen Ausbrüche, reservierte Dateien (`index.md`/`log.md`) unangetastet, OKF-Konformität bleibt gewahrt.

# Grundlagen

- [User Stories](/projekt/user-stories/index.md) — US-1 bis US-7
- [Technische Spec](/projekt/technische-spec.md) — Architektur, Mapping, Schreibrechte, JSON-API, Testbefehle
- [Planung](/projekt/planung.md) — TDD-Aufgabenplan mit Reihenfolge und Parallelisierung

# Aufgaben

- [A1: Fundament okf_bundle.py](/aufgaben/a1-okf-bundle.md)
- [A2: Status-Mapping status.py](/aufgaben/a2-status-mapping.md) — umgesetzt, Review und Test bestanden
- [A3: Nachtrag anfügen nachtrag.py](/aufgaben/a3-nachtrag.md)
- [A4: Aufgabe anlegen neu_aufgabe.py](/aufgaben/a4-neu-aufgabe.md)
- [A5: Welle anlegen neu_welle.py](/aufgaben/a5-neu-welle.md)
- [A6: Meta-Update meta.py](/aufgaben/a6-meta.md)
- [A7: Server-Gerüst und Start server.py](/aufgaben/a7-server.md)
- [A8: Lese-API](/aufgaben/a8-api-lesen.md)
- [A9: Schreib-API](/aufgaben/a9-api-schreiben.md)
- [A10: Frontend-Gerüst](/aufgaben/a10-frontend-geruest.md)
- [A11: Listenansicht](/aufgaben/a11-liste.md)
- [A12: Detailansicht](/aufgaben/a12-detail.md)
- [A13: Formulare Aufgabe und Welle](/aufgaben/a13-formulare.md)
- [A14: Entscheidungen- und Projekt-Ansicht](/aufgaben/a14-projekt-ansicht.md)
- [A15: setup.sh/verify.sh erweitern](/aufgaben/a15-setup-verify.md)
- [A16: Colab-Startzelle start_colab.py](/aufgaben/a16-start-colab.md)
- [A17: End-to-End-Absicherung](/aufgaben/a17-e2e.md)

# Stand

Teil-Umsetzung A2 (`status.py`) abgeschlossen: Review ohne kritische Befunde, 44 Tests grün, Gesamtsuite 99 passed. Übrige Aufgaben offen.

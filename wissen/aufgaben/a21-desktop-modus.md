---
type: Task
title: "A21: Desktop-Modus/Lokal-Betrieb"
description: Die App läuft als Desktop-Fenster (pywebview, Option B) mit direktem Zugriff auf die lokalen Domänen-Module — als eigener Startweg neben dem Browser-Betrieb.
freigabe: true
task_status: offen
phase: 2 Planung
priority: niedrig
assigned_to: coder
owner: ai
aktuell: ""
---

# Ziel

Desktop-Modus für lokale Nutzung ohne Browser-Fenster: **Option B** (pywebview-Desktop-Fenster mit direktem Aufruf der Domänen-Module — Entscheidung der Projektleitung 2026-11-14, Umsetzung mit Freigabe 2026-11-16). Der bestehende Server-/Browser-Betrieb (MVP/Colab) bleibt unverändert; der Desktop-Modus ist ein zusätzlicher Startweg.

# Akzeptanzkriterien

- **AK-1:** Eigener Startweg (z. B. `bash start.sh --desktop` bzw. `python3 definitions/app/desktop.py`) öffnet die Oberfläche als Desktop-Fenster; `BUNDLE_ROOT`-Semantik unverändert (Default `<Projekt>/wissen`).
- **AK-2:** `pywebview` ist eine **optionale** Abhängigkeit: fehlt sie, gibt der Start eine klare, deutsche Meldung (Installation/Hinweis) und endet sauber — der Server-/Browser-Betrieb funktioniert ohne pywebview unverändert.
- **AK-3:** Bestehende Features (Listen, Detail, Formulare, Freigabe-Gate, Unter-Aufgaben) sind im Desktop-Fenster nutzbar — die Oberfläche bleibt dieselbe (kein zweites Frontend).
- **AK-4:** Tests: Startlogik/Import-Guard/Argumente headless testbar (kein Fenster im Test); bestehende Suites bleiben grün; `verify.sh` Exit 0.
- **AK-5:** Doku: README (Desktop-Abschnitt), `docs/colab-start.md`-Vermerk (Desktop-Modus ist **nicht** der Colab-Weg), `definitions/README.md` bei Bedarf.
- **AK-6:** Abhängigkeits-Regel: pywebview wird in `requirements`/Doku ausdrücklich als optional geführt; kein `curl | sh`, keine weiteren neuen Abhängigkeiten.

# Testfälle (TDD)

- T1 Start ohne pywebview → klare Meldung, Exit ≠ 0, kein Traceback.
- T2 Startargument `--desktop` wird erkannt (Dispatch-Test, Fenster-Start gestubbt).
- T3 Bestandsschutz: `start.sh` ohne `--desktop` unverändert; Server-Start-Tests bleiben grün.

# Kontext

- Entscheidungslog 2026-11-14 „Lokal-Betrieb/Desktop-Modus — MVP/Colab zuerst": Option B als eigenes Feature vorgemerkt; Option A (Ein-Klick unsichtbar) ggf. klein vorab, Option C (File System Access API) verworfen.
- Freigabe der Projektleitung 2026-11-16 („alles frei") umfasst A21.
- **Reihenfolge:** nach A35–A38/A22 (größtes Stück zuletzt); Planung (planner) vor Umsetzung.

# Betroffene Dateien

- `definitions/app/desktop.py` (**neu**) — Fenster-/Startlogik, Import-Guard
- `start.sh` (Dispatch `--desktop`)
- `definitions/app/tests/test_desktop.py` (**neu**)
- `README.md`, `docs/colab-start.md`, `definitions/README.md` (Doku)

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle, Ergebnis, Befunde und Belege.

---
type: Task
title: "A7: Server-Gerüst und Start server.py"
description: Flask-App-Factory mit statischer Auslieferung, einheitlichem JSON-Fehlerformat und CLI-Start über BUNDLE_ROOT/PORT.
task_status: offen
phase: 2 Planung
priority: hoch
assigned_to: coder
user_story: /projekt/user-stories/us-6.md
owner: ai
---

# Ziel

`definitions/app/server.py` stellt `create_app(bundle_root)` als App-Factory bereit, liefert die statischen Dateien aus und installiert einen einheitlichen JSON-Fehlerhandler (`{error}` mit 4xx/5xx, nie HTML-Traceback). `main()` liest `BUNDLE_ROOT` und `PORT` aus der Umgebung, bindet an `0.0.0.0` und beendet sich mit Exit ≠ 0 bei belegtem Port oder ungültigem `BUNDLE_ROOT`. Der Start funktioniert lokal auch ohne `google.colab`.

# Akzeptanzkriterien

- `create_app(bundle_root)` ist als App-Factory nutzbar (Testclient ohne laufenden Server).
- Statische Dateien (Index, CSS) werden ausgeliefert.
- Fehlerantworten sind JSON mit dem Feld `error`, auch bei 404 und 500; kein Traceback im Body.
- `main()` liest `BUNDLE_ROOT`/`PORT` aus der Umgebung und bindet an `0.0.0.0`.
- Belegter Port oder fehlendes/ungültiges `BUNDLE_ROOT` → Exit ≠ 0 mit verständlicher stderr-Meldung.
- Der Start ist lokal ohne `google.colab` möglich.

# Testfälle (TDD)

- **T1 Index erreichbar:** `GET /` → 200, Body enthält `<html`.
- **T2 Statik:** `GET /static/style.css` → 200, `text/css`.
- **T3 404-Format:** unbekannte Route → 404 JSON mit `error`.
- **T4 500-Format:** provozierter Fehler → 500 JSON `{error}`, kein `Traceback` im Body.
- **T5 Port belegt:** belegten Port belegen, `main()` starten → Exit ≠ 0, stderr nennt „belegt".
- **T6 BUNDLE_ROOT fehlt:** Start ohne `BUNDLE_ROOT` → Exit ≠ 0, stderr nennt `BUNDLE_ROOT`.
- **T7 Bind-Adresse:** Startparameter prüfen → `host == "0.0.0.0"`.
- **T8 Port aus env:** `PORT=8123` → `port=8123`.

# Kontext

- **Abhängigkeiten:** A1; **zwingend seriell** vor A8 und A9.
- **Konfliktgruppe G7a:** `server.py` wird von A7/A8/A9 nacheinander bearbeitet — nicht parallelisieren.
- **Nachfolger:** A8 hängt die Lese-Routen, A9 die Schreib-Routen in dieselbe App; A16 startet `server.py` als Subprozess.
- **Entscheidungen:** R11 (Default-Port 5000, Ausweichport mit klarer Meldung bei Belegung wird in A16 umgesetzt), R7 („zuletzt geändert" als mtime, Auslieferung in A8).
- **Verweise:** Architektur und Startbefehle in [Technischer Spec](/projekt/technische-spec.md#build--start--test-befehle).

# Betroffene Dateien

- `definitions/app/server.py`
- `definitions/app/tests/test_server.py`

Die statischen Inhalte (`static/index.html`, `static/style.css`) werden von A7 nur ausgeliefert; angelegt und gepflegt werden sie in A10 (Konfliktmatrix: `index.html`/`style.css` → A10).

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

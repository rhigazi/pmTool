---
type: Task
title: "A16: Colab-Startzelle start_colab.py"
description: Ausführbare Startzelle, die Abhängigkeiten prüft, server.py als Subprozess startet und den Port über die eingebaute Colab-Funktion freigibt.
task_status: offen
phase: 2 Planung
priority: hoch
assigned_to: coder
user_story: /projekt/user-stories/us-6.md
owner: ai
---

# Ziel

`definitions/app/start_colab.py` ist ausführbar und importierbar: prüft/installiert `flask` und `pyyaml`, startet `server.py` als Subprozess mit `BUNDLE_ROOT=/content/pmTool/wissen` und `PORT` (Default 5000), erkennt einen belegten Port („läuft bereits" statt Doppelstart) und ruft `google.colab.output.serve_kernel_port_as_window(port)` auf. Ohne Colab wird die URL `http://localhost:<port>` ausgegeben. Kein Schreibzugriff aufs Bundle.

# Akzeptanzkriterien

- `serve_kernel_port_as_window` wird in Colab genau einmal mit dem Port aufgerufen.
- Der Subprozess erhält `BUNDLE_ROOT=/content/pmTool/wissen` und `PORT`.
- Ohne `google.colab` endet das Skript mit Exit 0 und gibt die lokale URL aus.
- Bei belegtem Port wird „läuft bereits" gemeldet und kein zweiter Prozess gestartet.
- Fehlende Pakete lösen einen `pip install`-Aufruf aus.
- Das Bundle wird nicht beschrieben.

# Testfälle (TDD)

Alle Testfälle laufen mit gemockten Abhängigkeiten (Colab-Output, `Popen`, `pip`).

- **T1 Port-Freigabe:** Start mit gemocktem Colab → `serve_kernel_port_as_window(5000)` genau einmal.
- **T2 Subprozess-Env:** `Popen`-Aufruf prüfen → `BUNDLE_ROOT == /content/pmTool/wissen`, `PORT` gesetzt.
- **T3 Ohne Colab:** Import/Start ohne Colab → Exit 0, Ausgabe `http://localhost:5000`.
- **T4 Port belegt:** Port vorab belegen → Ausgabe „läuft bereits", kein `Popen`.
- **T5 Fehlende Pakete:** Import von `flask`/`yaml` fehlschlagen lassen → `pip install`-Aufruf (gemockt).
- **T6 Kein Bundle-Schreibzugriff:** Tree-Hash des Bundles vor/nach identisch.

# Kontext

- **Abhängigkeiten:** A7 (`server.py`).
- **Konfliktgruppe G11:** `README.md` nur in Abstimmung mit A15 — **A15 zuerst**.
- **Entscheidungen:** R11 (Default-Port 5000, Ausweichport + klare Meldung bei Belegung), R14 (`start_colab.py` installiert `flask`/`pyyaml` bei Bedarf; keine neuen Abhängigkeiten zur Spec).
- **Verweise:** Startbefehle in [Technischer Spec](/projekt/technische-spec.md#build--start--test-befehle), [US-6](/projekt/user-stories/us-6.md).

# Betroffene Dateien

- `definitions/app/start_colab.py`
- `definitions/app/tests/test_start_colab.py`
- `definitions/README.md` (nur nach A15)

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

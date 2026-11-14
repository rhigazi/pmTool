---
type: Task
title: "A15: setup.sh/verify.sh um App-Verteilung erweitern"
description: Setup verteilt app/ nach bestehendem Muster in Zielprojekte, verify.sh prüft zusätzlich App-Dateien und App-Tests; README-Tabelle ergänzt.
task_status: im Review
phase: 5 Review
priority: mittel
assigned_to: coder
user_story: /projekt/user-stories/us-6.md
owner: ai
---

# Ziel

`definitions/setup.sh` erhält einen neuen Abschnitt „App (`app/`)" nach bestehendem Muster (`install_file`, Verzeichnisse wie `tools/` mit `cp -r` und Skip-Logik): verteilt `*.py`, `static/` und `tests/` nach `<ziel>/app/`. Ohne `--force` wird nie überschrieben; bestehende Abschnitte und Nummern bleiben funktional unverändert. `definitions/verify.sh` prüft zusätzlich `app/server.py`, `app/static/index.html` und `python3 -m pytest app/tests -q`. Die `README.md`-Tabelle wird um `app/` ergänzt.

# Akzeptanzkriterien

- Neuinstallation legt `<ziel>/app/` mit Python-Modulen, `static/` und `tests/` an.
- Bestehende Dateien werden ohne `--force` übersprungen und gemeldet; mit `--force` werden sie ersetzt.
- Bestehende Projektdateien (z. B. `AGENTS.md`) bleiben erhalten.
- `verify.sh` schlägt bei fehlenden App-Dateien fehl und nennt sie; bei vollständiger Installation ist es grün.
- Die mitverteilten Tests laufen im Zielprojekt durch.
- Die vorhandenen Setup-Abschnitte bleiben funktional unverändert.

# Testfälle (TDD)

pytest-Tests, die `setup.sh`/`verify.sh` per `subprocess` gegen `tmp_path` ausführen.

- **T1 Erstinstallation:** `setup.sh <tmp>` → Exit 0; `app/server.py` u. a. vorhanden.
- **T2 Idempotenz:** erneut ausführen → Datei unverändert, Ausgabe enthält „übersprungen".
- **T3 `--force`:** veränderte Datei wird auf das Original zurückgesetzt.
- **T4 Bestandsschutz:** Marker in `AGENTS.md` bleibt nach dem Lauf erhalten.
- **T5 Verify grün:** vollständige Installation → `verify.sh` Exit 0.
- **T6 Verify rot:** `app/server.py` entfernen → Exit 1, Ausgabe nennt `app/server.py`.
- **T7 Tests mitverteilt:** `python3 -m pytest tmp/app/tests -q` → Exit 0.
- **T8 Keine Regression:** Setup-Abschnitte 1–8 weiterhin vorhanden.

# Kontext

- **Abhängigkeiten:** A1, A7, A10 (App-Struktur muss stehen).
- **Konfliktgruppe G10:** `setup.sh`/`verify.sh` exklusiv; parallel zur App-Entwicklung möglich, sobald die Struktur existiert.
- **Reihenfolge:** **A15 zuerst, dann A16** — die `README.md` wird von beiden berührt.
- **Entscheidungen:** R12 (`verify.sh`-Erweiterung als neuer Abschnitt, bestehende Blöcke unverändert).
- **Verweise:** [Technische Spec](/projekt/technische-spec.md#build--start--test-befehle), bestehende Muster in `definitions/setup.sh` und `definitions/verify.sh`.

# Betroffene Dateien

- `definitions/setup.sh`
- `definitions/verify.sh`
- `definitions/README.md`
- `definitions/tools/tests/test_setup_app.py`

# Ergebnisse

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-14 — coder (Umsetzung, Stand zum Halt)

- **Ergebnis:** `setup.sh`-Abschnitt „9) App" (`copy_tree` ohne `__pycache__`), `verify.sh`-Abschnitt „7) App", README mit Colab-Start-Zellen, `definitions/app/tests/test_setup_verteilung.py` (9+1 Tests). (Quelle: Session-Rückmeldung „A15 setup/verify/README" im Übergabeprotokoll.)
- **Belege:** Gesamtsuite 549 grün, Exit 0.
- **Befunde:** (a) `tools/`-Abschnitt in `setup.sh` kopiert weiterhin `__pycache__` (Abschnitt 4 ohne `copy_tree`-Filter; R12: bestehende Abschnitte unverändert gelassen) — vom `tester` bestätigt, kleine eigene Aufgabe. (b) `verify.sh` Abschnitt 7 akzeptiert nur `app/` und schlägt im Dev-Repo (`definitions/app/`) fehl — als [A19](a19-verify-app-fallback.md) vorgemerkt (Entscheidung 2026-11-14).
- **Offene Punkte:** Review, Testphase, Doku.

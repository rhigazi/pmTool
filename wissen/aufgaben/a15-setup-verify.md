---
type: Task
title: "A15: setup.sh/verify.sh um App-Verteilung erweitern"
description: Setup verteilt app/ nach bestehendem Muster in Zielprojekte, verify.sh prüft zusätzlich App-Dateien und App-Tests; README-Tabelle ergänzt.
task_status: in Doku
phase: 7 Dokumentation
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
- `definitions/app/tests/test_setup_verteilung.py`

# Ergebnisse

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-14 — coder (Umsetzung, Stand zum Halt)

- **Ergebnis:** `setup.sh`-Abschnitt „10) App (app/)" (`copy_tree` ohne `__pycache__`), `verify.sh`-Abschnitt „7) App", README mit Colab-Start-Zellen, `definitions/app/tests/test_setup_verteilung.py` (9+1 Tests). (Quelle: Session-Rückmeldung „A15 setup/verify/README" im Übergabeprotokoll.)
- **Belege:** Gesamtsuite 549 grün, Exit 0.
- **Befunde:** (a) `tools/`-Abschnitt in `setup.sh` kopiert weiterhin `__pycache__` (Abschnitt 4 ohne `copy_tree`-Filter; R12: bestehende Abschnitte unverändert gelassen) — vom `tester` bestätigt, kleine eigene Aufgabe. (b) `verify.sh` Abschnitt 7 akzeptiert nur `app/` und schlägt im Dev-Repo (`definitions/app/`) fehl — als [A19](a19-verify-app-fallback.md) vorgemerkt (Entscheidung 2026-11-14).
- **Offene Punkte:** Review, Testphase, Doku.

## 2026-11-14 — tester (Gebündelte Testphase)

- **Ergebnis:** **Testphase BESTANDEN** (DoD-Beleg): 10 Tests grün, 2× serialisiert stabil. `test_setup_verteilung.py` ist von der Projektleitungs-Änderung in `setup.sh --global` unberührt (die Tests rufen `setup.sh` nie mit `--global` auf). Der `tester` hat `setup.sh --global` bewusst nie ausgeführt (hätte den Installer getriggert).
- **Offene Punkte:** Review ausstehend.

## 2026-11-14 — reviewer (Review-Runde 1)

- **Ergebnis:** **Nachbesserung läuft** (Rücklauf an `coder`).
- **Befunde:** [A15-1] wesentlich: T7 prüft nur einen Teil — auf ganzes `app/tests` erweitern, T5b-Skip streichen (AK „verify grün" erzwingen). [A15-2] klein: `.pytest_cache`-Filter in `copy_tree`.
- **Offene Punkte:** A15-1/A15-2 in Umsetzung.

## 2026-11-14 — coder (Nachbesserung, abgeschlossen)

- **Ergebnis:** [A15-1] behoben: T7 prüft jetzt ganz `app/tests` (mit `-p no:cacheprovider`), T5b-Skip gestrichen (AK „verify grün" wird erzwungen). [A15-2] behoben: `copy_tree` filtert `.pytest_cache` (Dateien + Verzeichnisse) mit Fixture-Ergänzung. [A15-3] Nummerierung behoben. [A15-4] Doku-Mismatch behoben (Verweise in diesem Blatt korrigiert: Testdatei `definitions/app/tests/test_setup_verteilung.py`, Sektion „10) App (app/)").
- **Belege:** `test_setup_verteilung.py` 13/13 serialisiert grün.
- **Offene Punkte:** Nebenbefund `tools/`-Abschnitt kopiert `__pycache__` bleibt offen (R12); Doku/Abschluss.

## 2026-11-14 — reviewer (Bestätigungs-Review, Runde 2)

- **Ergebnis:** **Review-frei** — [A15-1], [A15-2] und [A15-3] sind behoben und durch echte, nicht abgeschwächte Tests belegt; die Testphase liegt als Beleg vor (13/13 serialisiert grün).
- **Befunde:** keine kritischen/wesentlichen Befunde offen.
- **Offene Punkte:** `tools/`-Abschnitt `__pycache__` (Batch C); Doku/Abschluss.

## 2026-11-14 — coder (Kleinbefunde-Takt, Batch C, R12)

- **Ergebnis:** [R12] Der `tools/`-Abschnitt in `setup.sh` nutzt jetzt `copy_tree` mit Cache-Filter (`test_t1c_keine_cache_artefakte_in_tools`) — der letzte offene Nebenbefund aus A15 ist geschlossen.
- **Belege:** Kleinbefunde-Takt Batch C (+2 Tests); Gesamtsuite 761 grün.
- **Offene Punkte:** Doku/Abschluss.

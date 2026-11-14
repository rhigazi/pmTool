---
type: Task
title: "A18: Startskript start.sh und docs/colab-start.md"
description: Startskript zur Umgebungs-Wiederherstellung (lokal + Colab) mit Anleitung für neue Colab-Sitzungen und Telegram-Secrets-Zelle.
task_status: im Review
phase: 5 Review
priority: hoch
assigned_to: coder
user_story: /projekt/user-stories/us-6.md
owner: ai
---

# Ziel

`start.sh` in der Repo-Wurzel stellt die Arbeitsumgebung wieder her und startet die App: lokal (`bash start.sh`) und in Colab (`bash start.sh --colab`), dazu `--dry-run` und sauberes Ctrl+C. `docs/colab-start.md` beschreibt den Start einer neuen Colab-Sitzung inklusive Telegram-Secrets-Zelle. `start.sh` bleibt Repo-Root-Werkzeug und wird **nicht** von `setup.sh` verteilt (PM-Klarstellung).

# Akzeptanzkriterien

- `bash start.sh` startet den Server lokal (http://localhost:5000).
- `bash start.sh --colab` startet `definitions/app/start_colab.py` (Port-Freigabe im Browser).
- `--dry-run` zeigt das Vorhaben ohne Ausführung; Ctrl+C beendet sauber.
- Der Startpfad zeigt auf `app/server.py` mit Fallback `definitions/app/server.py`.
- `docs/colab-start.md` ist inhaltlich konsistent zu `start.sh` (inkl. Telegram-Secrets-Zelle).
- `start.sh` liegt in der Repo-Wurzel und wird nicht von `setup.sh` verteilt.

# Testfälle (TDD)

- **T1–T7 `test_start_skript.py`:** Aufrufe und Optionen von `start.sh` (lokal, `--colab`, `--dry-run`) — 7 Tests; im verteilten Ziel per `skipif` übersprungen.
- **Verifikation (tester):** Dry-Runs `bash start.sh --dry-run` und `bash start.sh --colab --dry-run` → Exit 0; Startpfad/Fallback, Ctrl+C-Handling, Konsistenz `docs/colab-start.md` — siehe Ergebnis-Eintrag des `tester`.

# Kontext

- **Entstehung:** Während der Umsetzungsphase als Übergabe-Aufgabe mit Vorrang angelegt (nicht Teil des ursprünglichen Plans A1–A17); Quelle: [Übergabeprotokoll](/../docs/uebergabeprotokoll.md).
- **PM-Klarstellung:** `start.sh` bleibt Repo-Root-Werkzeug, wird nicht von `setup.sh` verteilt (Ursprungskonflikt mit `test_start_skript.py` ist damit geklärt).
- **Konfliktgruppe:** `start.sh` und `docs/colab-start.md` exklusiv.
- **Verweise:** Umgebungs-Wiederherstellung im [Übergabeprotokoll](/../docs/uebergabeprotokoll.md); Startbefehle in [Technischer Spec](/projekt/technische-spec.md#build--start--test-befehle).

# Betroffene Dateien

- `start.sh`
- `docs/colab-start.md`
- `definitions/app/tests/test_start_skript.py`

# Ergebnisse

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-14 — coder (Umsetzung, Stand zum Halt)

- **Ergebnis:** `start.sh` (lokal + `--colab`, `--dry-run`, sauberes Ctrl+C), `docs/colab-start.md` (inkl. Telegram-Secrets-Zelle), `definitions/app/tests/test_start_skript.py` (7 Tests, `skipif` im verteilten Ziel). PM-Klarstellung umgesetzt: `start.sh` bleibt Repo-Root-Werkzeug, wird nicht von `setup.sh` verteilt. (Quelle: Session-Rückmeldung „A18 Startskript" im Übergabeprotokoll.)
- **Belege:** Gesamtsuite 549 passed, Exit 0 (Endstand zum Halt).
- **Offene Punkte:** Review, Testphase, Doku (Testphase inzwischen bestanden — siehe tester-Eintrag).

## 2026-11-14 — tester (Testphase)

- **Ergebnis:** **Testphase BESTANDEN** (DoD-Beleg): 7/7 Tests in `test_start_skript.py` grün, Gesamtsuite 549 passed (Soll erreicht), Dry-Runs `bash start.sh --dry-run` und `bash start.sh --colab --dry-run` jeweils Exit 0, Startpfad zeigt korrekt auf `app/server.py` mit Fallback `definitions/app/server.py`, Ctrl+C-Handling im Code vorhanden, `docs/colab-start.md` inhaltlich konsistent zu `start.sh` und Übergabeprotokoll.
- **Befunde:** Drei unkritische Doku-Kosmetikpunkte, für die Doku-Runde vorgemerkt (siehe [Projekt-Log](/log.md)): (1) `--dry-run`-Doku erwähnt nicht, dass `verify.sh` dort still übersprungen wird; (2) `BUNDLE_ROOT`-Wortlaut uneinheitlich (Protokoll `./wissen`, `start.sh` setzt absolut `$PROJEKT/wissen`); (3) Reihenfolge Telegram-Secrets-Zelle uneinheitlich (Protokoll „nach `start.sh --colab`", colab-start-Kurzfassung „davor").
- **Offene Punkte:** Review (Phase 5) und Doku (Phase 7) — Testphase ist vorzeitig/nebenläufig bereits bestanden.

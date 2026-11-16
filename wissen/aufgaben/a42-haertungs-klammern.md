---
type: Task
title: "A42: Härtungs-Klammern (B1-K2, T15-Index, O_EXCL-Backup)"
description: Drei gesammelte Härtungs-Punkte umsetzen (B1-K2 Negativ-Check Pflichtdateien, robuste Rest-Index-Assertion test_arbeitsstand_ui T15, O_EXCL-Öffnen im Backup-Werkzeug R8-Rest-TOCTOU).
freigabe: true
task_status: offen
phase: 2 Planung
priority: mittel
assigned_to: coder
owner: ai
aktuell: ""
---

# Ziel

Drei aus Reviews gesammelte Härtungs-Klammern werden umgesetzt (Lückenliste `docs/lueckenliste-a39.md`, Abschnitt 3; Freigabe der Projektleitung 2026-11-16 „alles frei"):

1. **B1-K2 — Negativ-Check „Pflichtdateien vollständig":** der entfallene Negativ-Check (fehlende Pflichtdatei → Fehler) wird als Test nachgezogen und, wo nötig, das Verhalten gesichert.
2. **T15 — Rest-Index-Assertion `test_arbeitsstand_ui` (`zellen[3]`):** die harte Index-Assertion wird robust (Zelle über Kopf/Text zuordnen statt `zellen[3]`), ohne die Aussage zu schwächen.
3. **R8 — `O_EXCL`-Öffnen im Backup-Werkzeug:** Rest-TOCTOU zwischen `lexists`-Prüfung und `tarfile.open` in `definitions/tools/neues_projekt.py` schließen (exklusives Öffnen); `O_EXCL` war post-MVP vorgemerkt und ist jetzt freigegeben.

# Akzeptanzkriterien

- **AK-1:** Für jeden der drei Punkte mindestens ein neuer Testfall (TDD: rot → grün).
- **AK-2:** Punkt 2 erst nach A37 (Datei-Konflikt `test_arbeitsstand_ui.py` — A37 migriert die Harness dort); Punkte 1 und 3 jederzeit.
- **AK-3:** Spiegel-Regel (A26): `tools/neues_projekt.py` bleibt byte-identisch zu `definitions/tools/neues_projekt.py` (Drift-Test `test_verteilung` grün).
- **AK-4:** Alle betroffenen Testdateien grün, keine Verhaltensänderung außer der Härtungen; Backup-Sicherheitsinvariante („kein Löschen ohne erhaltenes Backup") bleibt bestehen.
- **AK-5:** R8-Vermerk im Docstring wird auf den neuen Stand gebracht (TOCTOU-Rest ist dann dokumentiert geschlossen oder bleibt nur für `tarfile`-Interne bestehen — ehrlich benennen).

# Testfälle (TDD)

- T1 (B1-K2): Fehlende Pflichtdatei → Verhalten/Prüfung greift (Negativ-Test).
- T2 (T15): `test_arbeitsstand_ui` T15 ordnet die Zelle textbasiert zu — schlägt bei einer Spaltenverschiebung genau dann fehl, wenn die Aussage bricht (Mutantenprobe dokumentieren).
- T3 (O_EXCL): Konkurrenz-/Symlink-Fall wird beim Öffnen abgelehnt (`FileExistsError`/`BackupFehler`), kein Schreiben außerhalb des Ziels; bestehende T2/T3 (lexists) bleiben grün.

# Kontext

- Herkunft: A33-Review-K B1-K2, A31-Rest-K T15, A24-R8 (`O_EXCL` Post-MVP — jetzt freigegeben).
- A24-Werkzeug: `definitions/tools/neues_projekt.py` (Quelle), `tools/` (Spiegel); Sicherheitsfunktionen `_backup_name`, `_pruefe_backup_ziel`, `backup_erstellen` (lexists seit A33-B1).

# Betroffene Dateien

- `definitions/tools/neues_projekt.py` (+ Spiegel `tools/neues_projekt.py`)
- `definitions/tools/tests/test_neues_projekt.py`
- `definitions/app/tests/test_arbeitsstand_ui.py` (T15 — **nach A37**)
- `definitions/app/tests/test_setup_verteilung.py` (ggf. B1-K2-Test)

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle, Ergebnis, Befunde und Belege.

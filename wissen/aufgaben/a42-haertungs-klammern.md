---
type: Task
title: "A42: Härtungs-Klammern (B1-K2, T15-Index, O_EXCL-Backup)"
description: Drei gesammelte Härtungs-Punkte umsetzen (B1-K2 Negativ-Check Pflichtdateien, robuste Rest-Index-Assertion test_arbeitsstand_ui T15, O_EXCL-Öffnen im Backup-Werkzeug R8-Rest-TOCTOU).
freigabe: true
task_status: im Review
phase: 5 Review
priority: mittel
assigned_to: coder
owner: ai
aktuell: "reviewer: A42 Review (Mutanten + Urteil)"
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
## 2026-11-16 — reviewer: FREIGEGEBEN — Rücklauf K1/K2/K4 läuft

- **Urteil:** FREIGEGEBEN (keine W-Befunde). Mutanten: 6/8 getötet (O_EXCL-Weg, Pflichtdatei-Check, Post-Copy-Block, FileExistsError-Schlucken, fremdes Ziel löschen, Reihenfolge-vor-Tausch); Mutante d (T15 zurück auf `zellen[3]`) überlebt nur, weil die Grenzprobe nicht in der Suite liegt → **K2**; Mutante g (lexists-Vorprüfung) benign (Redundanz zu O_EXCL). Spiegel byte-identisch, Sicherheitslogik geprüft (Altstand/Backup erhalten auf allen Fehlerpfaden).
- **K-Punkte:** K1 Docstring `_pruefe_backup_ziel` widerspricht der Umsetzung („O_EXCL Post-MVP" → nachziehen, Quelle+Spiegel); K2 Grenzproben-Test ergänzen; K3 Berichtszahl korrigiert („13 neue Tests" = +11 Fälle; hiermit berichtigt); K4 Aufräum-`unlink` pfadbasiert — Rest-Risiko-Wortlaut eingrenzen. Rücklauf K1/K2/K4 läuft. Bewertung der Abweichungen: Post-Copy-Prüfung und O_EXCL-Abbruch statt `-2`-Ausweich beide **akzeptabel**.

## 2026-11-16 — coder (Welle B): Härtungs-Klammern — 13 neue Tests grün

- **B1-K2 (13 neue Testfälle = +11 Funktionen/Fälle in der Suite: 38 → 49):** `_fehlende_pflichtdateien(basis)` als einzige Quelle; **neu** prüft `tausche_gegen_vorlage` die Pflichtdateien am **aufgebauten Baum** vor dem Tausch (belegt die Erfolgsmeldung „8/8 übernommen"); Fehlendes → `NeuesProjektFehler` („Es wurde nichts gelöscht."), Altstand byte-gleich, Backup erhalten. Tests +11 (parametrisiert über alle 8 Pflichtdateien + Post-Copy-Abbruch); Mutante `return []` → 9 failed. Bundle-seitiger Negativ-Check bleibt in `verify.sh` (A40, gesperrt für A42).
- **T15:** `test_arbeitsstand_ui.py` ordnet Zellen **über die Kopfzeile** zu (`spalten(id, zeile)`), keine Index-Assertion mehr; Aussage unverändert. Grenzproben: legitime neue Spalte „Priorität" → neue Assertion grün/alt rot; Zelle ohne Kopf → rot. 25 grün.
- **R8/O_EXCL:** `backup_erstellen` öffnet das Archiv `os.open(ziel, O_WRONLY|O_CREAT|O_EXCL)` (Tarfile schreibt in den Deskriptor); `FileExistsError` → `BackupFehler`, Ziel unangetastet, Symlink nicht verfolgt. **Vorher-Nachweis (HEAD):** fremdes Backup wurde truncatet, durch untergeschobenen Symlink wurde **nach außen geschrieben** — beides jetzt abgewiesen (2 neue Tests, gegen HEAD rot). Sicherheitsinvariante „kein Löschen ohne erhaltenes Backup" unverändert; Docstrings auf neuen Stand (Rest-Risiko: nur tarfile-Interna).
- **Drift (A26-Regel):** Quelle↔Spiegel byte-identisch (`sha256sum`), `diff -rq` leer, T7 grün. Läufe: `test_neues_projekt.py` **49** (vorher 38), `test_arbeitsstand_ui.py` 25, Kombi 67–84 grün (t10 unter Parallel-Last abgebrochen — Sammellauf klärt).
- **Bewusst:** Post-Copy-Prüfung ist eine Verhaltensergänzung (begründet); bei verlorenem Namens-Wettlauf bricht der Reset ab statt auf `-2` auszuweichen (sichere Variante, im Docstring benannt); ein angepasster Bestandstest (Fake schreibt in `kwargs["fileobj"]`), Assertion unverändert.
- **Offen:** Review läuft.


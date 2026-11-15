---
type: Task
title: "A24: Neues Projekt beginnen (wissen/ zurücksetzen)"
description: "`python3 tools/neues_projekt.py` löscht `wissen/` und ersetzt es durch die saubere OKF-Vorlage `definitions/wissen-vorlage/` — mit Plan-Vorschau, Backup und Verify-Nachweis."
task_status: offen
phase: 2 Planung
priority: hoch
assigned_to: coder
feature: /features/okf-projekt-manager-spa.md
owner: ai
---

# Ziel

`python3 tools/neues_projekt.py` löscht `wissen/` und ersetzt es durch die saubere OKF-Vorlage `definitions/wissen-vorlage/` — damit eine frisch gezogene Instanz mit einem eigenen, leeren Projekt beginnen kann.

Nutzer-Anforderung 2026-11-15: „Möglichkeit, alles zu löschen, um ein neues sauberes Projekt zu beginnen".

# Akzeptanzkriterien

1. **Plan-Vorschau ohne `--ja`:** Ohne `--ja` zeigt das Skript nur den Plan (was würde gelöscht, wo läge das Backup, welche Vorlage würde kopiert) und ändert nichts (Exit 0, Dateisystem unverändert).
2. **Backup vor dem Löschen:** Mit `--ja` wird vor dem Löschen ein Backup `wissen-backup-YYYYMMDD-HHMMSS.tar.gz` im Repo-Root erzeugt (Pfad per `--backup` überschreibbar). Schlägt das Backup fehl, wird **nicht** gelöscht (Exit ≠ 0, `wissen/` unverändert).
3. **Exakte Vorlage danach:** Nach dem Reset enthält `wissen/` exakt die Vorlage — keine alten Projektdateien, kein `__pycache__`, keine `.pyc`.
4. **Verify + Start:** Nach dem Reset liefert `bash definitions/verify.sh .` Exit 0 und die App startet mit leerem Projekt.
5. **Klare Ausgabe:** Das Skript meldet, was gelöscht wurde, wo das Backup liegt und wie es weitergeht (nächste Schritte).
6. **Sicherheit:** Schreibzugriffe nur innerhalb des Repo-Roots, sauberer Abbruch ohne Halbzustand (kein Zwischenstand aus halb gelöschtem/teilweise kopiertem `wissen/`), Pfad-Checks wie in `okf_bundle` (kein `..`, keine absoluten Fremdpfade, Symlink-Ausbruch verhindern).

# Testfälle (TDD)

Reihenfolge = Red-Green-Takt: erst Test schreiben, rot laufen lassen, dann das Minimum implementieren.

- **T1 Ohne `--ja` nichts geändert:** Aufruf ohne `--ja` gegen ein Test-Bundle → Plan-Ausgabe enthält Löschziel, Backup-Pfad und Vorlagenquelle; Hash bzw. Dateiliste von `wissen/` vor/nach identisch; kein Backup-Archiv entstanden.
- **T2 Mit `--ja` Backup + Vorlage:** Test-Bundle mit alter Projektdatei → Aufruf mit `--ja`; ein `wissen-backup-*.tar.gz` im Repo-Root existiert und enthält die alte Datei; `wissen/` entspricht exakt der Vorlage (Dateiliste und Inhalte).
- **T3 Backup-Fehler ⇒ kein Löschen:** Backup-Ziel nicht beschreibbar (z. B. `--backup` auf ein Verzeichnis oder in ein nicht existierendes, nicht anlegbares Ziel) → Exit ≠ 0, `wissen/` unverändert (alter Inhalt vollständig vorhanden).
- **T4 Vorlage fehlt ⇒ Abbruch ohne Löschung:** `definitions/wissen-vorlage/` fehlt oder ist leer → Exit ≠ 0 mit klarer Meldung, `wissen/` unverändert; kein Backup-Zwangslauf nötig, aber auch keine Löschung.
- **T5 Keine Cache-Artefakte:** Vorlage mit `__pycache__/` und `.pyc`-Dateien → nach dem Reset ist nichts davon in `wissen/` (Filter wie bei `setup.sh`/`copy_tree`).
- **T6 E2E Reset + Verify:** Auf einem Test-Ziel: Reset mit `--ja`, danach `bash definitions/verify.sh .` → Exit 0; App startet mit leerem Projekt (Smoke: Overview-API liefert leere Aufgaben-/Wellen-Listen).
- **T7 Idempotenz:** Zweiter Aufruf mit `--ja` direkt nach einem Reset → erneut erfolgreich, `wissen/` entspricht weiterhin exakt der Vorlage, neues Backup entsteht, Exit 0.

**Isolation:** Alle Tests laufen ausschließlich gegen Test-Bundles unter `/tmp/opencode/…`; `/content/pmTool/wissen` wird nie beschrieben (Hash-Nachweis wie bei A17/A22).

# Kontext

- **Ursprung:** Nutzer-Anforderung 2026-11-15 („Möglichkeit, alles zu löschen, um ein neues sauberes Projekt zu beginnen"). Typisches Szenario: frisch gezogene Test-Instanz (frischer GitHub-Klon in eigener Colab-Runtime) soll ohne Altprojekt-Wissen neu starten.
- **Quelle der Wahrheit:** `definitions/wissen-vorlage/` ist die saubere OKF-Vorlage (`index.md`, `features.md`, `log.md`, `aufgaben/`, `entscheidungen/`, `projekt/` inkl. `phasen.md`, `technische-spec.md`, `user-stories/`).
- **Abgrenzung:** A23 (Feature-Liste) läuft parallel und berührt andere Dateien (`definitions/app/…`); keine gemeinsamen betroffenen Dateien mit A24. Die Doku der Test-Instanz steht in README und `docs/colab-start.md`.
- **Doku-Anteil:** README + `docs/colab-start.md`, Abschnitt „Neues Projekt beginnen" — läuft nach und wird vom `documenter` ergänzt (nicht Teil der Code-Umsetzung).
- **Sicherheitsmuster:** Pfadschutz und atomare Schreibweise aus `definitions/tools/okf_bundle.py` übernehmen (Repo-Root-Check, `resolve()`, Symlink-Prüfung).
- **Verweise:** [Phasenmodell](/projekt/phasen.md), [Technische Spec](/projekt/technische-spec.md), [Feature](/features/okf-projekt-manager-spa.md), [A22](a22-e2e-regression.md) (Test-Isolation), [A23](a23-feature-liste.md) (paralleler Strang).

# Betroffene Dateien

- `tools/neues_projekt.py` (neu)
- `tools/tests/test_neues_projekt.py` (neu)
- Doku: `README.md` + `docs/colab-start.md`, Abschnitt „Neues Projekt beginnen" (nachgelagert, `documenter`)

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

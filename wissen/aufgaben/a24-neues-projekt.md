---
type: Task
title: "A24: Neues Projekt beginnen (wissen/ zurücksetzen)"
description: "`python3 tools/neues_projekt.py` löscht `wissen/` und ersetzt es durch die saubere OKF-Vorlage `definitions/wissen-vorlage/` — mit Plan-Vorschau, Backup und Verify-Nachweis."
task_status: in Doku
phase: 7 Dokumentation
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
- Doku: `README.md` + `docs/colab-start.md`, Abschnitt „Neues Projekt beginnen" — 2026-11-15 vom `documenter` ergänzt

# Ergebnisse

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-15 — coder (Umsetzung, Stand: in Doku)

- **Ergebnis:** `tools/neues_projekt.py` (358 Zeilen) und `tools/tests/test_neues_projekt.py` (24 Tests) umgesetzt. TDD-Verlauf: **4 Tests rot → 24 grün**. Umgesetztes Verhalten:
  - **Plan ohne `--ja`:** Ausgabe mit Projektpfad, Umfang von `wissen/` und Vorlage, Backup-Ziel, Löschhinweis; Exit 0 und **nichts verändert** (Datei-Baum-Hash vor/nach identisch).
  - **Backup Pflicht:** `wissen-backup-YYYYMMDD-HHMMSS.tar.gz` im Repo-Root (per `--backup` überschreibbar); Namenskollision → Suffix `-2`, `-3`, … (kein Überschreiben). Backup-Fehler ⇒ **kein Löschen**; ein halb fertiges Archiv wird entfernt.
  - **Vorlage-Vorabprüfung:** fehlende/unvollständige/leere Vorlage → Exit ≠ 0, die fehlende Datei wird benannt, keine Löschung.
  - **Reset:** Inhalt von `wissen/` inkl. versteckter Dateien wird ersetzt; `__pycache__`/`.pytest_cache`/`*.pyc` werden aus der Vorlage gefiltert, keine temporären Verzeichnisse bleiben zurück.
  - **Atomarer Tausch:** neuer Baum `.wissen-neu-*` neben `wissen/`, Tausch per `os.replace`, Rollback bei Fehler (kein Halbzustand).
  - **Pfad-Checks analog `okf_bundle`:** realpath-Containment im Repo-Root, keine Symlinks als Ziel, kein Schreiben in Vorlage oder `wissen/`.
- **Belege:** `python3 -m pytest tools/tests/test_neues_projekt.py -q` → **24 passed**. E2E: Reset + `bash definitions/verify.sh .` → Exit 0 (Test mit App-Stub wegen Rekursionsschutz; der Vollnachweis — Reset, Verify, App-Start mit leerem Projekt — wurde manuell auf einer echten Repo-Kopie gefahren). Idempotenz belegt: zweiter `--ja`-Lauf erneut Exit 0, `wissen/` entspricht weiterhin exakt der Vorlage. App-Suite zum A24-Zeitpunkt: **862** (inkl. der parallel laufenden A23-Tests).
- **PM-Entscheidungen (2026-11-15):**
  - **(a)** Die Backup-Restriktion „nur innerhalb Repo-Root" bleibt (Spec-konform); sie ist als bewusste Grenze dokumentiert (Backup landet immer im Projekt, nie auf einem Fremdpfad).
  - **(b)** `main(argv=None, root=None)` bleibt als Testinjektion erhalten (Tests laufen gegen `/tmp/opencode/…`, ohne CLI-Parsing zu duplizieren).
  - **(c)** **Verteilungslücke** (Skript fehlt in `definitions/tools/`, `setup.sh` verteilt es nicht) wird nicht in A24 nachgezogen, sondern zusammen mit dem alten Root-Suite-Konflikt (doppelte `test_telegram_send.py`) als [A26](a26-verteilung-und-suite-konflikt.md) bereinigt.
- **Befunde:** Ein `pytest -q` im Repo-Root ist derzeit generell nicht lauffähig (Collection-Konflikt `test_telegram_send.py`, belegt: 924 collected, 1 error) — unabhängig von A24, aber durch das künftige Spiegeln von `test_neues_projekt.py` verschärft → A26.
- **Offene Punkte:** Review und Testphase laufen gebündelt nach (Status deshalb `in Doku`, nicht `zur Abnahme`); A26 (Verteilung + Root-Suite).

## 2026-11-15 — reviewer (Review, NACHBESSERUNG NÖTIG)

- **Ergebnis:** **NACHBESSERUNG NÖTIG** — Rücklauf an den `coder` läuft. Die AK-Punkte 1–7 sind bis auf die folgenden Lücken erfüllt (Abgleich im Review-Text). Bei einem **Löschwerkzeug** zwei **wesentliche** Sicherheits-Befunde:
  1. **Explizites `--backup`-Ziel wird still überschrieben** — könnte beliebige Repo-Dateien zerstören und überschreibt ggf. das einzige Backup. Erwartung: ein vorhandenes Ziel verweigern oder ausweichen (nie überschreiben).
  2. **Fehlgeschlagener Rollback + `finally` vernichtet den Altbestand** — AK 6 („kein Halbzustand") ist damit nicht garantiert; genau dieser Zweig war ungetestet.
- **Kleinbefunde:** Modus `0700`; Symlink-Folgen in der Vorlage; unpräzise Erfolgsmeldung.
- **Testlücken (a–e):** fünf Lücken gemäß Reviewer-Rückmeldung; im Rücklauf an den `coder` mitzubeheben (Details dort).
- **Offene Punkte:** Rücklauf an den `coder` läuft (inkl. Testlücken a–e). Status **A24 → in Nachbesserung** (Phase 4). Danach erneutes Review und Testphase; A26 (Verteilung + Root-Suite) bleibt separat.

## 2026-11-15 — coder (Nachbesserung, Stand: in Doku)

- **Ergebnis:** Beide **wesentlichen** Review-Befunde behoben; Kleinbefunde 3–5 und die Testlücken a–e mit erledigt. Commit `a959d75`.
  - **Befund 1 — Backup-Ziel wird nie überschrieben/trunciert:** Ein vorhandenes Ziel ist jetzt ein `PfadFehler` („bestehende Sicherungen werden nie überschrieben", mit Hinweis auf einen freien Pfad); ein Verzeichnis oder Symlink als Ziel wird ebenfalls abgelehnt. **Doppel-Barriere:** geprüft wird einmal bei der Pfadauflösung des Arguments (`--backup`) **und** noch einmal unmittelbar in `backup_erstellen` vor dem Öffnen des Archivs — die zweite Prüfung deckt den Fall ab, dass das Ziel zwischen Vorschau und Lauf entsteht (`tarfile` würde es sonst truncaten und damit die einzige Sicherung vernichten). Der automatische Name weicht bei Kollision weiter auf `-2`, `-3`, … aus; ein **explizit** genanntes Ziel wird nie ausgewichen und nie überschrieben.
  - **Befund 2 — fehlgeschlagener Rollback erhält den Altbaum:** Der `os.replace`-Aufruf liegt jetzt in einem eigenen Seam (`_ersetze`) und ist im Test gezielt zum Scheitern zu bringen. Scheitert der Rücktausch, bleibt der Altbestand unter `.wissen-alt-*` **liegen** und wird in der Meldung benannt — er wird nie gelöscht, solange er nicht zurückgetauscht ist (im `finally` wird der Altbaum bei `alt_erhalten` nicht entfernt, sondern nur auf `stderr` gemeldet). Gegen die **alte Git-Version** nachgewiesen: der neue Test schlägt dort fehl (Altbaum wäre verloren), auf dem neuen Stand ist er grün.
  - **Kleinbefunde 3–5:** Modus der neuen `wissen/`-Struktur **0755** (vorher 0700, für andere lesbar); **Symlinks in der Vorlage werden vor jedem Backup abgelehnt** (kein Dereferenzieren, Vorlage muss ein reiner Dateibaum sein); Erfolgsmeldung **ohne unbelegten verify-Nachweis** (das Skript behauptet keinen Verify-Lauf mehr, den es nicht selbst gefahren hat).
  - **Testlücken a–e geschlossen:** 8 neue Tests, `test_neues_projekt.py` **24 → 32**; u. a. vorhandenes Backup-Ziel, Symlink-Ziel, Backup-Ziel als Verzeichnis, Symlink in der Vorlage, fehlgeschlagener Rollback, Lesbarkeit der neuen Struktur, keine verify-Behauptung.
- **Sicherheitsinvariante bestätigt:** **„kein Löschen ohne erhaltenes Backup"** — jeder Fehlerpfad (Ziel belegt, Backup-Fehler, Vorlage unvollständig/Symlink, Rollback-Fehler) lässt den Altbestand unangetastet; ein halb fertiges Archiv wird entfernt.
- **PM-Entscheidung (2026-11-15):** Der **Plan-Lauf** (ohne `--ja`) bricht bei belegtem Backup-Ziel ebenfalls ab — bleibt so, weil es konsistent ist: Die Vorschau kündigt keinen Lauf an, der mit Sicherheit scheitern würde. Alternative „Vorschau warnt, Lauf weicht aus" wurde verworfen (würde die Regel „nie überschreiben" im Lauf wieder aufweichen).
- **Belege:** `python3 -m pytest tools/tests -q` → **69 passed** (davon `test_neues_projekt.py` **32**), geprüft 2026-11-15 durch den `documenter`. Der Rollback-Test ist gegen den Elternstand von `a959d75` (alte Git-Version) nachweislich rot und auf dem neuen Stand grün.
- **Offene Punkte:** Status **A24 → in Doku** (Phase 7). Die Review-Bestätigung des Rücklaufs folgt im gebündelten Lauf bzw. als kurzes Bestätigungs-Review; danach Testphase. **A26** (Verteilung `definitions/tools/` + Root-Suite-Konflikt) bleibt separat und unverändert offen.

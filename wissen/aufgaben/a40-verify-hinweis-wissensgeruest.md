---
type: Task
title: "A40: Verify-Hinweis bei fehlendem Wissens-Gerüst"
description: verify.sh meldet bei einem verteilten Ziel ohne OKF-Wissensgerüst gezielt, dass setup.sh --wissen fehlt — statt generisch mit Exit 1 zu enden.
freigabe: true
task_status: abgeschlossen
phase: 8 Abgeschlossen
priority: mittel
assigned_to: coder
owner: ai
aktuell: ""
---

# Ziel

Sammellauf-Befund V1 der A39-Testrunde (2026-11-16): Ein per `setup.sh` (ohne `--wissen`) verteiltes Zielprojekt endet in `verify.sh` mit Exit 1, weil das OKF-Wissensgerüst (`wissen/index.md`, `features.md`, `log.md`, `entscheidungen/log.md`, `aufgaben/index.md`, `projekt/phasen.md`, `projekt/konzept.md`, `projekt/technische-spec.md`) fehlt. Die Fehlermeldung soll **gezielt** sagen, woran es liegt und wie man es behebt (`setup.sh --wissen`), statt nur „fehlt: <Datei>".

# Akzeptanzkriterien

- **AK-1:** Fehlt das Wissensgerüst (eine oder mehrere der 8 Pflichtdateien), gibt `verify.sh` eine eigene, deutliche Meldung aus, die `setup.sh --wissen` als Lösung nennt (deutsch, ohne Umwege); Exit-Code bleibt ≠ 0 (fail-loud).
- **AK-2:** Mit vollständigem Gerüst ändert sich nichts (Exit 0, bestehende Abschnitte und Meldungen unverändert — R12); im Dev-Repo (Fallback `definitions/app/`) unverändert Exit 0.
- **AK-3:** Tests in `definitions/app/tests/test_setup_verteilung.py` (oder passendem Ort): verteiltes Ziel ohne `--wissen` → Exit ≠ 0 **und** Meldungsnachweis `setup.sh --wissen`; mit `--wissen` → Exit 0. Mindestens 2 neue Testfälle, TDD (rot → grün).
- **AK-4:** Keine neuen Abhängigkeiten; `bash definitions/verify.sh .` im Dev-Repo weiterhin Exit 0; Root-Suite grün.

# Testfälle (TDD)

- T1 Ziel ohne `--wissen` verteilen → `verify.sh` Exit ≠ 0, stderr/stdout enthält den `--wissen`-Hinweis.
- T2 Ziel mit `--wissen` → Exit 0, kein `--wissen`-Hinweis.
- T3 Bestandsschutz: alle bisherigen verify-Abschnitte unverändert (bestehende Tests bleiben grün).

# Kontext

- Herkunft: Lückenliste `docs/lueckenliste-a39.md` (V1), Freigabe der Projektleitung 2026-11-16 („alles frei").
- `setup.sh`-Abschnitt 5 legt das Gerüst nur mit `--wissen` an (Verhalten bleibt so — A40 ändert nur die verify-Meldung).
- A26-Regel: Quelle `definitions/`, Spiegel `tools/` — nach Änderungen `test_verteilung` (Drift) grün halten.

# Betroffene Dateien

- `definitions/verify.sh` (Meldung/Prüfung Wissens-Gerüst)
- `definitions/app/tests/test_setup_verteilung.py` (Tests T1–T2)
- `definitions/README.md` (ggf. ein Satz zur Verify-Erwartung)

# Ergebnisse
## 2026-11-16 — coder (Rücklauf) + PM: W1/K2/K3 behoben → **abgeschlossen**

- **W1 (echte Remediation bei Teilgerüst):** setup.sh-Verhältnisse in Temp-Zielen **real geprüft** (bei vorhandenem `wissen/index.md`: Abschnitt 5 übersprungen, fehlende Datei bleibt fehlend; bei fehlendem `index.md`: `cp -r` überschreibt vorhandene Wissensdateien). `verify.sh` unterscheidet jetzt: **kein Gerüst** → unveränderte Meldung + `setup.sh --wissen`; **Teilgerüst** → eigene ehrliche Meldung („vorhandene Wissensdateien bleiben erhalten — ergänze fehlende Dateien einzeln aus `definitions/wissen-vorlage/`") inkl. ausdrücklichem Hinweis, warum `setup.sh --wissen` allein hier **nicht** hilft. Exit 1 bleibt.
- **K2:** T14 (1 fehlende Datei, präzise Meldung + kein falscher Lösungshinweis) + neu **T14b** (parametrisiert 2/3/3 fehlende Dateien inkl. `index.md`, **exakte** Liste + Anzahl). Probe „listet nur die erste fehlende Datei" → 3/3 rot. **K3:** Leerzeile am Dateiende entfernt (`git diff --check` sauber).
- Läufe: T12–T14 **6 passed** (460 s), `bash -n` sauber, Dev-Repo-Lauf Abschnitt 1 ohne OKF-Hinweis (Gesamtlauf = kombinierter Testlauf). **A40 abgeschlossen** (PM, 2026-11-16). Rest-Klammern: K1 (`-e` statt `-f`, geerbt), K4 (`WISSEN_DATEIEN` doppelt — Drift-Risiko).

## 2026-11-16 — reviewer (kombiniert mit A38): NACHBESSERUNG (W1) — Rücklauf läuft

- **Urteil:** NACHBESSERUNG — Kernmeldung/Testlage grün, 3/3 eigene Mutanten getötet. **W1 (echter Befund):** Die Remediation „`setup.sh --wissen`" stimmt bei **Teilgerüst** nicht — (a) bei vorhandenem `wissen/index.md` überspringt `setup.sh --wissen` Abschnitt 5 (fehlende Datei bleibt fehlend), (b) bei fehlendem `index.md` überschreibt `cp -r` vorhandene Wissensdateien (widerspricht der Meldung „vorhandene Dateien bleiben unangetastet") — beides mit Temp-Zielen belegt. Fix: Meldung nach Voll-/Teilgerüst unterscheiden, T14 um echten Remediation-Lauf erweitern. **K-Klammern:** K1 `-e` statt `-f` (geerbt), K2 Testlücke (nur erste fehlende Datei genügt beiden Tests → parametrisieren, im Rücklauf), K3 Leerzeile am Dateiende, K4 `WISSEN_DATEIEN` doppelt gepflegt (Drift-Risiko), K5 kein fester Skriptpfad (bewusst, akzeptiert).

## 2026-11-16 — coder (Welle A): Verify-Hinweis — 3 neue Tests grün

- **Ergebnis:** `definitions/verify.sh` Abschnitt 1 geteilt (allgemeine Dateien / 8 OKF-Pflichtdateien); fehlt mindestens eine, erscheint **eine** gebündelte Meldung: „✗ OKF-Wissensgerüst fehlt (N von 8 Pflichtdateien): … → Lösung: setup.sh --wissen ausführen — legt das Gerüst unter <ziel>/wissen/ an (vorhandene Dateien bleiben unangetastet)". Zählung/Liste dynamisch („1 von 8 …" im Einzelfall); FAIL bleibt gesetzt (Exit 1); vorhandene Dateien weiterhin einzeln ✓, Reihenfolge unverändert.
- **Tests:** `test_setup_verteilung.py` T12 (Ziel ohne `--wissen`: Exit 1 + Meldungsnachweis), T13 (mit `--wissen`: Exit 0, kein Hinweis — R12/Bestandsschutz), T14 (Einzelfall: eine Datei gelöscht → „1 von 8", exakte Liste). TDD: 2 failed/1 passed → 6 passed (Auswahl); Vollauf der Datei **17 passed** (925 s).
- **Zusatzbelege:** `bash -n` sauber; Alt-/Neu-Skript gegen dasselbe Ziel mit vollständigem Gerüst → stdout **byte-identisch**; Dev-Repo `bash definitions/verify.sh .` → Exit 0 ohne neuen Hinweis; `definitions/README.md` um einen Satz ergänzt.
- **Bewusst:** Meldung nennt keinen festen Skriptpfad (im verteilten Ziel existiert kein `setup.sh` im Root); parallele Fremd-Änderungen verursachten zwischenzeitlich 3 flüchtige Fehlschläge (kopierendes Setup-Fixture) — nach stabilem Baum 17/17 grün, kein A40-Befund.
- **Offen:** Review (kombiniert mit A38) läuft.

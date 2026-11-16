---
type: Task
title: "A40: Verify-Hinweis bei fehlendem Wissens-Gerüst"
description: verify.sh meldet bei einem verteilten Ziel ohne OKF-Wissensgerüst gezielt, dass setup.sh --wissen fehlt — statt generisch mit Exit 1 zu enden.
freigabe: true
task_status: offen
phase: 2 Planung
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

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle, Ergebnis, Befunde und Belege.

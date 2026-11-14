---
type: Feature Overview
title: Features-Überblick
description: Zeigt für jedes Feature, ob es umgesetzt ist oder noch offen, mit Verweis auf die zugehörigen Aufgaben.
tags: [features, steuerung]
---

# Statuswerte

`offen` · `in Umsetzung` · `umgesetzt` · `pausiert`

# Regeln

* Jeder Eintrag verlinkt auf seine Feature-Datei unter `/features/` und auf die zugehörigen Aufgaben unter `/aufgaben/`.
* Jeder Feature-Eintrag trägt eine Priorität (`hoch`/`mittel`/`niedrig`); die Planung leitet daraus Reihenfolge und Meilensteine ab.
* Zu jedem offenen Punkt müssen die Aufgaben so dokumentiert sein, dass ein `coder` sie eigenständig abarbeiten kann (siehe [Phasenmodell](/projekt/phasen.md)).
* Jede Umsetzung wird hier eingetragen und ins [Projekt-Log](/log.md) protokolliert.

# Offene Features

* [OKF Projekt-Manager (SPA)](features/okf-projekt-manager-spa.md) — Tracker auf das OKF-Bundle: Status/owner anzeigen, Nachträge, Aufgaben und Wellen anlegen, Colab-Start · **in Umsetzung** · Priorität **hoch**
  * **Umgesetzt (Pipeline offen):** [A1](aufgaben/a1-okf-bundle.md) `okf_bundle.py` (Fundament, Pfadschutz, zentrale Exceptions), [A3](aufgaben/a3-nachtrag.md) `nachtrag.py`, [A4](aufgaben/a4-neu-aufgabe.md) `neu_aufgabe.py`, [A5](aufgaben/a5-neu-welle.md) `neu_welle.py`, [A6](aufgaben/a6-meta.md) `meta.py`, [A7](aufgaben/a7-server.md) `server.py`, [A8](aufgaben/a8-api-lesen.md) Lese-API (4 GET-Routen, inkl. Kleinnachtrag), [A9](aufgaben/a9-api-schreiben.md) Schreib-API (4 POST-Routen), [A10](aufgaben/a10-frontend-geruest.md) Frontend-Gerüst (Testphase bestanden), [A11](aufgaben/a11-liste.md) Listenansicht, [A12](aufgaben/a12-detail.md) Detailansicht, [A15](aufgaben/a15-setup-verify.md) `setup.sh`/`verify.sh`/README (App-Verteilung), [A16](aufgaben/a16-start-colab.md) `start_colab.py`, [A18](aufgaben/a18-start-skript.md) `start.sh` + `docs/colab-start.md` (Testphase bestanden) — Gesamtsuite 549 grün
  * **Abgeschlossen:** [A2](aufgaben/a2-status-mapping.md) `status.py` (44 Tests, Test bestanden, Doku)
  * **Offen:** [A13](aufgaben/a13-formulare.md) Formulare, [A14](aufgaben/a14-projekt-ansicht.md) Entscheidungen-/Projekt-Ansicht, [A17](aufgaben/a17-e2e.md) E2E-Absicherung, [A19](aufgaben/a19-verify-app-fallback.md) verify.sh-Fallback; dazu Review/Test/Doku für die umgesetzten Aufgaben (gebündelte Testphase vorgesehen)

# Offene Punkte (ohne eigene Aufgaben-Datei)

* Root-Suite `pytest -q` bricht am doppelten Testdateinamen `test_telegram_send.py` (`tools/tests/` vs. `definitions/tools/tests/`) — vom `tester` bestätigt; kleine eigene Aufgabe (umbenennen oder pytest-`ignore`).
* `tools/`-Abschnitt in `setup.sh` (Abschnitt 4) kopiert weiterhin `__pycache__` ohne `copy_tree`-Filter — vom `tester` bestätigt; kleine eigene Aufgabe (R12 ließ bestehende Abschnitte unverändert).
* Doku-Kosmetik für die Doku-Runde (Details im [Projekt-Log](/log.md)): `--dry-run`-Hinweis zu `verify.sh`, `BUNDLE_ROOT`-Wortlaut, Reihenfolge Telegram-Secrets-Zelle.
* Detail-Endpunkt: unlesbare Datei → 500 statt neutraler Meldung (für A9-Review/A17 vormerken).

# Umgesetzte Features

*Noch keine.*

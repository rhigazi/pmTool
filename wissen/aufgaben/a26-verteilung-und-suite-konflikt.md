---
type: Task
title: "A26: Werkzeug-Verteilung und Root-Suite-Konflikt"
description: "`tools/neues_projekt.py` in die Definitions-Quelle spiegeln und den Collection-Konflikt der Repo-Root-Suite (doppelte Testdateinamen in `tools/` und `definitions/tools/`) dauerhaft lösen."
task_status: abgeschlossen
phase: 8 Abgeschlossen
priority: mittel
assigned_to: coder
aktuell: ""
feature: /features/okf-projekt-manager-spa.md
owner: ai
---

# Ziel

Zwei offene Punkte aus A15/A24 gemeinsam bereinigen, weil beide dieselbe Ursache haben — zwei parallel gepflegte `tools/`-Bäume:

1. **Verteilungslücke schließen:** `tools/neues_projekt.py` und `tools/tests/test_neues_projekt.py` liegen nur im Entwicklungs-Repo, nicht in der Quelle `definitions/tools/`. Damit fehlt das Werkzeug in jedem per `setup.sh` installierten Zielprojekt. Die Definitions bleiben Single Source of Truth; `setup.sh` verteilt das Skript wie die übrigen Werkzeuge.
2. **Root-Suite-Konflikt lösen:** `python3 -m pytest -q` im Repo-Root bricht bei der Collection, weil `test_telegram_send.py` in `tools/tests/` **und** `definitions/tools/tests/` liegt (pytest importiert Testmodule über den Basisnamen). Nach dem Spiegeln von `test_neues_projekt.py` entstünde derselbe Konflikt ein zweites Mal.

# Akzeptanzkriterien

- `python3 -m pytest -q` im Repo-Root läuft durch (kein Collection-Fehler) und ist grün.
- `definitions/setup.sh` verteilt `neues_projekt.py` (und den zugehörigen Test) in Zielprojekte; ein frisch installiertes Zielprojekt enthält `tools/neues_projekt.py` und `tools/tests/test_neues_projekt.py`.
- `bash definitions/verify.sh .` bleibt kompatibel (Exit 0 im Dev-Repo und im vollständig installierten Zielprojekt).
- **Keine doppelte Code-Pflege:** Der Lösungstyp ist entweder eine pytest-Konfiguration/`ignore`-Regel am Repo-Root **oder** eine Deduplizierung (ein Baum ist Quelle, der andere wird nicht mehr als Testbaum kollektiert) — die Wahl wird im Ergebnis begründet.
- Bestehende Testzahlen bleiben erhalten: Die Root-Suite führt jede Testdatei genau einmal aus; es verschwinden keine Tests still.
- Idempotenz: erneuter `setup.sh`-Lauf ohne `--force` überschreibt nichts und meldet „übersprungen".

# Testfälle (TDD)

Reihenfolge = Red-Green-Takt: erst Test schreiben, rot laufen lassen, dann das Minimum implementieren.

- **T1 Root-Collection:** `python3 -m pytest -q --collect-only` im Repo-Root → Exit 0, keine `import file mismatch`-/`ERROR collecting`-Zeile. (Aktuell rot: „module 'test_telegram_send' … not the same as the test file we want to collect".)
- **T2 Root-Suite grün:** `python3 -m pytest -q` im Repo-Root → Exit 0; die Anzahl gesammelter Tests entspricht der Summe der eindeutigen Testdateien (keine Doppelzählung, kein stilles Überspringen ganzer Bäume ohne Begründung).
- **T3 Verteilung:** `setup.sh <tmp>` → `tools/neues_projekt.py` und `tools/tests/test_neues_projekt.py` vorhanden; Aufruf `python3 tools/neues_projekt.py` im Zielprojekt liefert den Plan (Exit 0, nichts verändert).
- **T4 Verteilte Tests laufen:** `python3 -m pytest <tmp>/tools/tests -q` → Exit 0 (kein Importfehler durch den neuen Testbaum).
- **T5 Verify kompatibel:** vollständige Installation → `bash definitions/verify.sh <tmp>` Exit 0; im Dev-Repo `bash definitions/verify.sh .` Exit 0.
- **T6 Single Source / Drift:** `definitions/tools/neues_projekt.py` und `tools/neues_projekt.py` sind inhaltsgleich (bzw. der verbleibende Baum ist als Quelle dokumentiert); Test oder Prüfschritt benennt die Quelle, damit künftige Änderungen nicht wieder auseinanderlaufen.
- **T7 Idempotenz/Bestandsschutz:** zweiter `setup.sh`-Lauf ohne `--force` → „übersprungen", Dateien unverändert; mit `--force` → ersetzt.
- **T8 Keine Cache-Artefakte:** verteilter `tools/`-Baum enthält kein `__pycache__`/`.pytest_cache` (bestehender `copy_tree`-Filter, Regression).

# Kontext

- **Ursprung A24 (2026-11-15):** `tools/neues_projekt.py` (~360 Zeilen) und `tools/tests/test_neues_projekt.py` (24 Tests) wurden im Entwicklungs-Repo umgesetzt, aber nicht in `definitions/tools/` gespiegelt. `setup.sh` kopiert ausschließlich aus `definitions/tools/` (`SRC/tools/*`) — im Zielprojekt fehlt das Werkzeug daher komplett. PM-Entscheidung: nicht in A24 nachziehen, sondern als eigene Aufgabe A26 bündeln.
- **Ursprung A15:** Der Root-Suite-Konflikt ist als offener Punkt notiert („doppelte `test_telegram_send.py` in `tools/tests/` vs. `definitions/tools/tests/` — umbenennen oder pytest-`ignore`"). `tools/telegram_send.py` und `definitions/tools/telegram_send.py` sind derzeit **byte-identisch**, ebenso die Testdateien (`diff -q` bestätigt).
- **Belegter Ist-Zustand (2026-11-15, Repo-Root):** `python3 -m pytest -q --collect-only` → „924 tests collected, 1 error"; Fehler: `imported module 'test_telegram_send' has this __file__ attribute: /content/pmTool/definitions/tools/tests/test_telegram_send.py which is not the same as the test file we want to collect: /content/pmTool/tools/tests/test_telegram_send.py`. Ohne `--collect-only` bricht der Lauf mit „Interrupted: 1 error during collection" ab — es läuft **kein** Test.
- **Warum jetzt zwei Konflikte:** Nach dem Spiegeln von `test_neues_projekt.py` nach `definitions/tools/tests/` tritt derselbe Basisnamen-Konflikt für das zweite Paar auf. Ein Fix nur für `test_telegram_send.py` (Umbenennen) wäre also unvollständig.
- **Lösungsoptionen (Auswahl im Ergebnis begründen):**
  (a) **Root-pytest-Konfiguration** (`pytest.ini`/`pyproject.toml`/`conftest.py`) mit `testpaths` + `--import-mode=importlib` oder gezielten `--ignore`-Pfaden: minimalinvasiv, aber die Root-Suite muss weiterhin alle Tests genau einmal ausführen (T2) — `--ignore` auf `definitions/**` würde die App-Suite aus dem Root-Lauf nehmen, das ist zu prüfen und zu begründen.
  (b) **Deduplizierung:** Nur ein Baum bleibt Test-Baum (z. B. `definitions/tools/tests` als Quelle, Root-`tools/tests` wird nicht separat kollektiert) — beseitigt die Doppelpflege strukturell, berührt aber die Verteilung und ggf. `verify.sh`-Pfade.
  (c) **Eindeutige Dateinamen** in einem Baum: einfachste Variante, behebt aber nur das Symptom und erzeugt bei jeder neuen Testdatei erneut Pflegeaufwand.
- **Abgrenzung:** A26 fasst **keine** App-Quellen an (`definitions/app/**`) und ändert keine Testinhalte. Die App-Suite bleibt funktional unverändert; gearbeitet wird an Root-Konfiguration, `definitions/setup.sh`, ggf. `definitions/verify.sh` und der Ablage der beiden `tools/`-Bäume.
- **Reihenfolge:** Umsetzung **erst nach A23 und A25**. Eine Root-`pytest`-Konfiguration bzw. Umbenennung berührt **alle** Testläufe und damit auch die parallel laufenden Aufgaben; A23/A25 laufen derzeit in getrennten Sessions.
- **Verweise:** [A15](a15-setup-verify.md) (Verteilung/verify, offener `tools/`-Punkt), [A24](a24-neues-projekt.md) (Werkzeug und Verteilungslücke), [Phasenmodell](/projekt/phasen.md), [Technische Spec](/projekt/technische-spec.md), [features.md](/features.md).

# Betroffene Dateien

- `definitions/tools/neues_projekt.py` (neu, Spiegel der Quelle)
- `definitions/tools/tests/test_neues_projekt.py` (neu, Spiegel)
- `definitions/setup.sh` (Verteilung `tools/` — ggf. nur Dokumentation/Reihenfolge, wenn die Kopierschleife bereits greift)
- `definitions/verify.sh` (nur falls die neuen Werkzeuge geprüft werden sollen)
- Repo-Root: `pytest.ini` **oder** `pyproject.toml` **oder** `conftest.py` (je nach gewählter Lösung), alternativ Anpassung der Testablage
- `tools/tests/test_neues_projekt.py` / `tools/tests/test_telegram_send.py` (nur bei Deduplizierung/Umbenennung)

# Ergebnisse

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-15 — coder (Umsetzung + Rücklauf W1/W2 + K3/K4)

- **Ergebnis:** `definitions/tools/` ist Quelle des A24-Werkzeugs (`neues_projekt.py`), `tools/` der per `setup.sh` (Abschnitt 4b) verteilte Spiegel; der Root-Suite-Collections-Konflikt (doppelte Testdatei-Basisnamen) ist über `conftest.py` mit `collect_ignore` für den Spiegel gelöst (Namensregel im Docstring = K4). Rücklauf auf das Review NACHBESSERUNG: **W1** Dev-Selbstlauf — `bash definitions/setup.sh . --force` erkennt Selbstkopien („übersprungen (Quelle = Ziel)"), Exit 0, Hash-identisch; **W2** dokumentierte Auffrischung erzeugt kein zweites `app/` (Abschnitte 4b/5/10 werden im Dev-Repo übersprungen); **K3** Testlücken T9/T10/T11/T5b gehärtet. Zeitstand Rücklauf: **1373 grün** (Commit `f504da9`).
- **Belege:** `wissen/log.md` 2026-11-15 (A26-Einträge), [Entscheidungslog](/entscheidungen/log.md) 2026-11-15 (A26-Review). **Protokolllücke:** detaillierte Rot→Grün-Belege des Rücklaufs nicht überliefert.

## 2026-11-15 — tester (Testphase)

- **Ergebnis:** FREIGEGEBEN (1118 ×2, Verteilungs-E2E + Drift grün) — belegt über den damaligen Live-Arbeitsstand. **Protokolllücke:** Einzelprotokoll der Testphase nicht überliefert.

## 2026-11-16 — reviewer (Bestätigungs-Review, Modell Beam): FREIGEGEBEN — Aufgabe abgeschlossen

- **Urteil:** FREIGEGEBEN — alle sechs Prüfpunkte erfüllt, keine W-Befunde.
- **W1:** `setup.sh . --force` im Dev-Repo Exit 0; Hash-Vorher/Nachher identisch (0 Zeilen Differenz), `git status` sauber; Regressionsfälle `test_verteilung.py` T9/T11 (+ T10).
- **W2:** README-Auffrischung konsistent zum Code (`DEV_REPO=1` bei `TARGET == SRC/..`, Skip 4b/10); kein zweites `app/`, Root-Suite bleibt 1632 collected. K-Nuance: Abschnitt 5 (`wissen/`) läuft nur mit `--wissen` — README-Wortlaut in der Abschluss-Runde nachgezogen.
- **K3:** 102 passed (`test_setup_verteilung.py` + `definitions/tools/tests/`). **K4:** Namensregel im `conftest.py`-Docstring zitiert. **Drift:** T7 grün, `diff -rq` nur Cache-Artefakte. **Zählumfang:** 1632 collected (App 1544 + Tools 88, Spiegel 0), Volllauf **1632 passed** (776 s). `bash definitions/verify.sh .` → Exit 0.
- **Rest-K-Punkte (Abschluss-Runde erledigt):** veralteter `docs/colab-start.md`-Vermerk „Werkzeug derzeit nicht" bereinigt; README-Wortlaut Abschnitt 5 präzisiert. Vermerk: die Selbstkopie-Erkennung nutzt `-ef` (Inode-Vergleich), nicht `realpath` — funktional gleichwertig.

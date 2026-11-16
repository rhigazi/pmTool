---
type: Task
title: "A22: E2E-Regressionstest (test_e2e.py)"
description: Die T1/T2/T7-Kette des A17-Abnahmelaufs als dauerhaften, eingecheckten E2E-Test überführen.
task_status: im Review
phase: 5 Review
priority: mittel
assigned_to: coder
user_story: /projekt/user-stories/us-7.md
owner: ai
aktuell: "reviewer: A22 Review (Mutantenproben gegen Produktivcode + Urteil)"
freigabe: true
---

# Ziel

Die im A17-Abnahmelauf ad hoc gefahrene T1/T2/T7-Kette (aus den Skripten `/tmp/opencode/a17_*.py`) wird als dauerhafter E2E-Test `test_e2e.py` ins Repository überführt, damit die End-to-End-Absicherung nicht nur als Einmal-Nachweis existiert.

# Akzeptanzkriterien

- `test_e2e.py` ist eingecheckt und läuft als Teil der Gesamtsuite.
- T1 API-E2E (Overview → Nachtrag → Klarung → owner) ist automatisiert und konsistent.
- T2 (Frontmatter intakt: `type`/`title` unverändert, genau 1 Marker) ist automatisiert.
- T7 (Reset reproduzierbar) ist automatisiert.
- Der Test läuft ausschließlich gegen ein Test-Bundle unter `/tmp/opencode/…`; `/content/pmTool/wissen` wird nie beschrieben (Hash-Nachweis wie bei A17).

# Testfälle (TDD)

- **T1 E2E-Kette:** API-Sequenz gegen Test-Bundle → konsistente Zustände über alle Schritte.
- **T2 Frontmatter-Invarianten:** `type`/`title` unverändert, genau 1 Nachtrag-Marker.
- **T7 Reset:** Wiederholter Lauf ist reproduzierbar (gleiche Ergebnisse).
- **Isolation:** Echt-Bundle-Hash vor/nach dem Lauf identisch.

# Kontext

- **Ursprung:** A17-Abnahmelauf (bestanden) — die Ad-hoc-Skripte unter `/tmp/opencode/a17_*.py` sind nicht Teil des Repos; PM-Entscheidung: MVP-Abnahme mit dokumentiertem Einmal-Nachweis, dauerhafte Regression als A22 post-MVP.
- **Abhängigkeiten:** A1–A20 abgeschlossen; nutzt das Test-Bundle-Muster aus A17.
- **Verweise:** [A17](a17-e2e.md), [Technische Spec](/projekt/technische-spec.md#build--start--test-befehle), [Phasenmodell](/projekt/phasen.md).

# Betroffene Dateien

- `definitions/app/tests/test_e2e.py` (neu)
- ggf. `definitions/app/tests/conftest.py` (Fixtures)

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

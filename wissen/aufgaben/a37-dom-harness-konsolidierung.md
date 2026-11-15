---
type: Task
title: "A37: DOM-Harness-Konsolidierung (A14-6)"
description: tests/dom_helfer.py wird zur einzigen Harness-Quelle — die vier Altkopien und die
  UI-Testdateien werden umgestellt, ohne Verhaltenswechsel.
task_status: offen
phase: 2 Planung
priority: niedrig
assigned_to: coder
owner: ai
---

# Ziel

Der DOM-Test-Harness existiert in mehreren Kopien (`test_detail`, `test_suche`, `test_features`, `test_welle_zuordnung`); A30 legt `tests/dom_helfer.py` als gemeinsame Quelle an. Diese Aufgabe stellt alle UI-Testdateien darauf um (kein Verhaltenswechsel, reine Konsolidierung).

# Akzeptanzkriterien

Noch keine Einträge — der `planner` ergänzt/schärft sie (wichtig: keine Assertion wird abgeschwächt; Testzahlen bleiben identisch).

# Testfälle (TDD)

Noch keine Einträge — der `planner` ergänzt die Testfälle.

# Kontext

- Ausgegliedert aus [A33](a33-kleinbefunde-aufräum-takt.md) (PM-Entscheidung 2026-11-15).
- **Reihenfolge:** nach A29 (alle Testdateien stabil); nutzt `dom_helfer.py` aus A30.
- **Nachtrag (A28-Review, K3):** Beim Umstellen auch die Harness-Lücke beheben, der `detail.js` aktuell ausweicht (`document.createTextNode` fehlt im A12-Harness → Produktivcode nutzt leeres `span` mit `" "` als Trenner, `detail.js:585-588`); `dom_helfer.py` kann `createTextNode` — nach dem Umstieg den Produktivcode-Weg rückgängig machen (Trenner sauber) und `test_detail.py` schärfen.
- Aufwand laut A33-Plan: 5–8 h.

# Betroffene Dateien

Noch keine Einträge — die Planung ergänzt die betroffenen Dateien.

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

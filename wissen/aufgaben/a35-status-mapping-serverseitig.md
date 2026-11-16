---
type: Task
title: "A35: Status-Mapping server-seitig (A12-1)"
description: Status.py ist die einzige Mapping-Quelle — overview.details liefert ui_status/hinweis/owner_default,
  der JS-Spiegel TASK_STATUS_UI/OWNER_DEFAULTS in detail.js entfällt.
task_status: offen
phase: 2 Planung
priority: mittel
assigned_to: coder
owner: ai
freigabe: true
---

# Ziel

Der Status-Mapping-Spiegel in `detail.js` (`TASK_STATUS_UI`/`OWNER_DEFAULTS`) dupliziert `status.py` und kann driftieren (Befund A12-1, ausgegliedert aus [A33](a33-kleinbefunde-aufräum-takt.md)). Abhilfe: `overview.details` liefert `ui_status`/`hinweis`/`owner_default` direkt aus `status.py` (analog zu A30s `arbeitsstatus`), `detail.js` nutzt die Werte und der JS-Spiegel entfällt.

# Akzeptanzkriterien

Noch keine Einträge — der `planner` ergänzt/schärft sie (Grundlage: Mapping-Matrix über die API + UI-Regression).

# Testfälle (TDD)

Noch keine Einträge — der `planner` ergänzt die Testfälle.

# Kontext

- Ausgegliert aus [A33](a33-kleinbefunde-aufräum-takt.md) (PM-Entscheidung 2026-11-15, Nummer bestätigt).
- **Reihenfolge:** nach A29 (`detail.js`, `overview.py`); danach A36 (`schreibgeschuetzt`-Signal) darauf aufbauend.
- Aufwand laut A33-Plan: 4–6 h.

# Betroffene Dateien

Noch keine Einträge — die Planung ergänzt die betroffenen Dateien.

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

---
type: Task
title: "A36: schreibgeschuetzt-Signal (A12-Schreib-UI-Grenze)"
description: Die API markiert reservierte Dateien als schreibgeschützt, die UI blendet Schreibaktionen
  aus — der Server-403 bleibt zweite Barriere.
task_status: offen
phase: 2 Planung
priority: mittel
assigned_to: coder
owner: ai
freigabe: true
---

# Ziel

Die Schreib-UI bietet auf reservierten Dateien (index.md/features.md/log.md) Aktionen an, die der Server mit 403 ablehnt (fail-loud, Befund A12-Grenze). Abhilfe: die API liefert ein `schreibgeschuetzt`-Signal, die UI blendet Schreibaktionen aus. **Keine clientseitige Duplizierung der reservierten Namensliste** (Mapping-Drift-Regel aus A12-1!).

# Akzeptanzkriterien

Noch keine Einträge — der `planner` ergänzt/schärft sie. Server-403 bleibt als zweite Barriere unverändert bestehen.

# Testfälle (TDD)

Noch keine Einträge — der `planner` ergänzt die Testfälle.

# Kontext

- Ausgegliedert aus [A33](a33-kleinbefunde-aufräum-takt.md) (PM-Entscheidung 2026-11-15; ursprünglich PM-Entscheidung im A14-Review: „dokumentieren statt clientseitiger Ausblendung — Ausblendung erst mit `schreibgeschuetzt`-Signal").
- **Reihenfolge:** nach A35 (dort wird `overview.details` bereits erweitert).
- Aufwand laut A33-Plan: 3–4 h.

# Betroffene Dateien

Noch keine Einträge — die Planung ergänzt die betroffenen Dateien.

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

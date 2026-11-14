---
type: Task
title: "A2: Status-Mapping status.py"
description: Reine Funktionen für die Abbildung von task_status/status auf die 6 UI-Status und den owner-Default, ohne Dateizugriffe.
task_status: offen
phase: 2 Planung
priority: hoch
assigned_to: coder
user_story: /projekt/user-stories/us-1.md
owner: ai
---

# Ziel

`definitions/app/status.py` stellt `ui_status(frontmatter) -> (status, hinweis|None)` und `owner_default(frontmatter)` gemäß der Mapping-Tabelle der Technischen Spec bereit. Das Modul enthält keine Dateizugriffe.

# Akzeptanzkriterien

- Alle 11 Mapping-Zeilen der Spec werden 1:1 abgebildet (parametrisierter Test).
- Ohne `task_status` wird `status` direkt verwendet; ohne beide Felder → `("Offen", "ohne Status")`.
- `pausiert` → `("Offen", "pausiert")`.
- `owner` fehlt → `None`.
- Unbekannte Werte führen zu keiner Exception.

# Testfälle (TDD)

- **T1 Mapping vollständig (parametrisiert, alle 11 Paare):** `ui_status` → exakt erwarteter UI-Status.
- **T2 `abgeschlossen`:** → `("Geschlossen", None)`, `owner_default` → `None`.
- **T3 `pausiert`:** → `("Offen", "pausiert")`.
- **T4 Welle ohne `task_status` (`status: In Arbeit`):** → `("In Arbeit", None)`.
- **T5 Kein Statusfeld:** → `("Offen", "ohne Status")`.
- **T6 Unbekannter `task_status`:** → `("Offen", <wert>)`, keine Exception.
- **T7 owner-Defaults:** `offen` → `ai`, `in Klärung` → `mensch`, `status: Klarung` → `mensch`.
- **T8 owner fehlt:** → `None`.

# Kontext

- **Abhängigkeiten:** keine (reine Funktionen) — **parallel zu A1**.
- **Konfliktgruppe G2:** `status.py` exklusiv für A2; kein `conftest.py` anfassen (das gehört A1).
- **Nachfolger:** A6 und A8 konsumieren das Mapping; A2 muss daher vor A6/A8 abgeschlossen sein.
- **Entscheidungen:** R3 (`owner` fehlt in Bestandsdateien → Anzeige „—", Filteroption „ohne owner"; keine automatische Migration).
- **Verweise:** Mapping-Tabelle in [Technischer Spec](/projekt/technische-spec.md#mapping-task_status--ui-status-6-werte); Statuswerte in [Phasenmodell](/projekt/phasen.md).

# Betroffene Dateien

- `definitions/app/status.py`
- `definitions/app/tests/test_status.py`

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

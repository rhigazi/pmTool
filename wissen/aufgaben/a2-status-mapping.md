---
type: Task
title: "A2: Status-Mapping status.py"
description: Reine Funktionen für die Abbildung von task_status/status auf die 6 UI-Status und den owner-Default, ohne Dateizugriffe.
task_status: abgeschlossen
phase: 8 Abgeschlossen
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

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-14 — coder (Umsetzung, Red-Green-Refactor)

- **Ergebnis:** `definitions/app/status.py` (Mapping `task_status` → UI-Status inkl. owner-Default-Regel mit Vorrang des expliziten `owner`-Felds) und `tests/test_status.py` angelegt.
- **Belege:** Red — Import-Fehler, 0 Tests grün. Green — 38 Tests passed.
- **Befunde:** Interpretationen zur owner-Vorrang-Regel und zu den Status-Owner-Defaults wurden vom Projektmanager bestätigt und in der Spec festgehalten.
- **Offene Punkte:** keine.

## 2026-11-14 — coder (Nachbesserung aus Review)

- **Ergebnis:** Test-Lücke geschlossen (parametrisierter Test über alle 6 `status`-Owner-Defaults), Docstring präzisiert, `UI_STATUS_WERTE` als eigene Konstante entkoppelt, Parameter `ui_status` → `status_wert` umbenannt.
- **Belege:** 44 Tests passed.
- **Offene Punkte:** keine.

## 2026-11-14 — reviewer (Review)

- **Ergebnis:** Gesamturteil **ohne kritische Befunde**. Alle Akzeptanzkriterien erfüllt, alle 11 Mapping-Zeilen 1:1 zur Spec, Edge Cases korrekt, keine Konflikte zu anderen Konfliktgruppen.
- **Befunde:** Minor-Empfehlungen (Test-Lücke, Docstring, Konstante) — wurden nachgebessert (siehe Eintrag coder/Nachbesserung).
- **Einschränkung:** Testlauf in der Review-Session nicht möglich (kein Shell-Werkzeug); Nachweis erfolgte durch den `tester`.
- **Offene Punkte:** keine.

## 2026-11-14 — tester (Test)

- **Ergebnis:** Gesamturteil **bestanden**. `pytest definitions/app/tests/test_status.py -q`: 44 passed. Gesamtsuite: 99 passed (keine Regression).
- **Befunde:** Abdeckungsabgleich T1–T8 vollständig — alle acht TDD-Fälle durch konkrete Tests gedeckt. Ad-hoc-Prüfungen: keine Dateizugriffe, Trimming/Fallback robust, Fixture-Isolation gegeben.
- **DoD-Beleg aus Test-Sicht:** alle Akzeptanzkriterien erfüllt und nachgewiesen.
- **Offene Punkte:** keine.

## 2026-11-14 — documenter (Abschluss)

- **Ergebnis:** Aufgabe als **abgeschlossen** dokumentiert: Umsetzung, Review ohne kritische Befunde, Test bestanden und Doku liegen vor (siehe obige Einträge); Verschiebung unter „Abgeschlossene Aufgaben" im [Aufgaben-Index](index.md). (Quelle: Übergabeprotokoll, Aufgabenstatus A2.)
- **Offene Punkte:** Commit des Stands durch den Projektmanager (DoD-Punkt „Stand ist in Git committed").

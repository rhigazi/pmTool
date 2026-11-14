---
type: User Story
title: US-5: Status und owner verwalten (Klärung und Abnahme)
description: Die Person kann owner umschalten sowie Klärung setzen und nach Abnahme schließen; die Pipeline-Status pflegt weiterhin die KI.
story_status: offen
priority: hoch
---

# Story
Als Projektleitung möchte ich in der App sehen und gezielt steuern, wer als Nächstes dran ist — ohne in den technischen Status der KI-Pipeline eingreifen zu müssen, damit die Zusammenarbeit reibungslos bleibt und die autonome Arbeitsweise der KI gewahrt bleibt.

# Akzeptanzkriterien
- Jeder Punkt zeigt `owner` (mensch / ai) und die Person kann `owner` jederzeit umschalten (Übergabe an KI: `ai`, Rückfrage/beantwortet: `mensch`).
- Die Person darf aus der App setzen: Status **Klarung** (Rückfrage/Unklarheit an die KI) und Status **Geschlossen** (fachliche Abnahme am Ende).
- Alle übrigen Statuswechsel der Pipeline (`task_status`/`phase` laut Phasenmodell) vornimmt ausschließlich die KI (Projektmanager/documenter) — die App greift hier nur lesend zu oder übersetzt über das definierte Mapping.
- Der Status `Klarung` ist in Übersicht und Listenansicht prominent sichtbar (offene Rückfragen laufen nie verloren).
- Eine auf `Klarung`/`Offen` stehende Aufgabe bleibt bestehen, bis sie weiterbearbeitet oder `Geschlossen` ist (kein automatisches Verschwinden).
- Statuswechsel werden mit Zeitstempel/„zuletzt geändert“ sichtbar gemacht.

# Technische Hinweise
Schreibrechte-Matrix: siehe Technische Spec. Ziel laut Projektleitung: Tool ist primär ein **Tracker** zur Steuerung; die KI erledigt die eigentliche Bearbeitung und pflegt `index.md`, `features.md`, `log.md`.

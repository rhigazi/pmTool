---
type: User Story
title: US-1: Tracker-Übersicht mit Status und Zuständigkeit
description: Listenansicht über fünf Navigationspunkte zeigt jeden Punkt mit Status, owner und letzter Änderung.
story_status: offen
priority: hoch
---

# Story
Als Projektleitung möchte ich in einer klaren Listenansicht sofort sehen, was im Projekt läuft, welchen Status ein Punkt hat und ob Mensch oder KI als Nächstes dran ist (`owner`), damit ich das Projekt steuern kann, ohne Dateien manuell durchzusuchen.

# Akzeptanzkriterien
- Die App zeigt fünf Navigationspunkte: **Übersicht**, **Wellen**, **Aufgaben**, **Entscheidungen**, **Projekt** (letzterer enthält Konzept, Technische Spec, User Stories, Phasen und das Projekt-Log als Unterpunkt).
- Jede Listenzeile zeigt mindestens: **Titel**, **Status** (Klarung / Offen / In Arbeit / Testing / Dokumentation / Geschlossen), **owner** (mensch / ai), **zuletzt geändert**.
- Filter nach Status und owner sind möglich (einfache Auswahlfelder, keinSuche-Overlay nötig).
- Die Übersicht zeigt zusätzlich die zuletzt geänderten Punkte und offene Rückfragen (Status `Klarung`), damit kein offener Faden verloren geht.
- Offene Punkte bleiben in der Liste bestehen, bis ihr Status `Geschlossen` lautet (kein automatisches Ausblenden/Entfernen).
- Die UI-Status ergeben sich aus dem bestehenden `task_status`/`phase` der Aufgaben über das in der Technischen Spec definierte Mapping (zweites Statusmodell wird nicht eingeführt).

# Technische Hinweise
Mapping-Tabellen und Datenmodell siehe [Technische Spec](/projekt/technische-spec.md); Statuswerte/Workflow bleiben laut [Phasenmodell](/projekt/phasen.md) verbindlich.

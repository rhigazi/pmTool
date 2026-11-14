---
type: User Story
title: US-4: Wellen anlegen und mit Aufgaben verknüpfen
description: Wellen werden als eigener OKF-Punkt je Welle angelegt und mit zugehörigen Aufgaben verlinkt.
story_status: offen
priority: hoch
---

# Story
Als Projektleitung möchte ich Projekt-Wellen (Waves) als eigene Strukturpunkte anlegen und zugehörige Aufgaben ihnen zuordnen, damit Fortschritt und Umfang je Welle sichtbar bleiben und beide Seiten dieselbe Gliederung teilen.

# Akzeptanzkriterien
- Neuer Navigationspunkt „Wellen“ zeigt alle Wellen mit Titel, Status (gleiche sechs UI-Status), `owner` und letzter Änderung.
- Anlegen per Formular: Titel, Ziel/Beschreibung, Status, `owner` → erzeugt `wissen/wellen/<kuerzel>.md` mit `type: Welle` und gültigem Frontmatter.
- Aufgaben können einer Welle zugeordnet werden (Verlinkung aus der Welle auf die Aufgaben-Dateien und/oder aus der Aufgabe auf die Welle); die Zuordnung ist in beiden Ansichten erkennbar.
- Wellen nutzen dasselbe Statusmodell wie alles andere (einheitlich, kein zweites Modell).
- Die Wellen-Liste ist aus `wissen/wellen/` ableitbar (auch ohne App lesbar, da OKF-konform im Bundle).
- Löschen von Wellen ist im MVP nicht vorgesehen (Nicht-Ziel: kein Strukturverlust durch die App).

# Technische Hinweise
Wellen-OKF-Punkt und gemeinsames Statusmodell: siehe Entscheidungslog 2026-11-14 und PRD Abschnitt 7. Ordner `wissen/wellen/` wird bei Erstanlage angelegt.

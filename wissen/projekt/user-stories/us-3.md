---
type: User Story
title: US-3: Neue Aufgabe anlegen und an die KI übergeben
description: Neue Aufgaben werden als OKF-konforme Datei im Phasen-Format angelegt und stehen der KI sofort zur Bearbeitung bereit.
story_status: offen
priority: hoch
---

# Story
Als Projektleitung möchte ich aus der App heraus einen neuen Punkt (Aufgabe) anlegen, der formatkonform in der Wissensdatenbank liegt und der KI zur Bearbeitung übergeben werden kann, damit ich die Struktur erweitere, ohne Dateien von Hand anlegen zu müssen.

# Akzeptanzkriterien
- Ein Formular erfasst mindestens: Titel, Ziel, Akzeptanzkriterien (mehrzeilig), Priorität.
- Die App erzeugt daraus `wissen/aufgaben/<id>.md` im Aufgabenformat des Phasenmodells (`type: Task`, `task_status: offen`, `phase`, `priority`, `owner: ai`, Verweis auf `user_story` falls angegeben).
- Die neue Aufgabe erscheint unmittelbar in der Listenansicht mit Status `Offen` und `owner: ai`.
- Die Übergabe an die KI erfolgt über den definierten gemeinsamen Kanal (Dateien + Status im Bundle, Session-Start liest `wissen/index.md`); die App erzeugt dafür optional einen kopierbaren Kurzkontext (Titel, Pfad, Ziel).
- Ungültige/leere Eingaben werden mit verständlicher Meldung abgelehnt; es entstehen keine unvollständigen Dateien.
- Namens-/ID-Konvention und Ablageort entsprechen den Regeln aus dem Phasenmodell.

# Technische Hinweise
Aufgabenformat: siehe [Phasenmodell](/projekt/phasen.md), Abschnitt „Format einer Aufgaben-Datei“. Priorisierung der Aufgabenpakete obliegt dem Projektmanager, nicht der Person (siehe Entscheidungslog).

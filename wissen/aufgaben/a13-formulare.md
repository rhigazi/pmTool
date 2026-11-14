---
type: Task
title: "A13: Formulare Aufgabe und Welle anlegen"
description: Formulare zum Anlegen von Aufgaben und Wellen mit Inline-Validierung, Erfolgsanzeige inklusive kopierbarem Kurzkontext und Doppelklickschutz.
task_status: offen
phase: 2 Planung
priority: hoch
assigned_to: coder
user_story: /projekt/user-stories/us-3.md
owner: ai
---

# Ziel

`static/js/formulare.js` enthält das Formular Aufgabe (Titel, Ziel, Akzeptanz mehrzeilig, Priorität, optional Welle/User Story) und das Formular Welle (Titel, Ziel, Status, owner). Nach Erfolg werden der Pfad und ein kopierbarer Kurzkontext für die KI-Übergabe angezeigt; die Validierung erfolgt inline; der Button ist während des Requests deaktiviert.

# Akzeptanzkriterien

- Aufgabe anlegen funktioniert über das Formular; die neue Aufgabe erscheint in der Liste mit `Offen` und `ai`.
- Pflichtfelder werden inline validiert; bei Fehler entsteht kein Eintrag.
- Akzeptanzkriterien werden mehrzeilig erfasst und als `- `-Zeilen in die Datei geschrieben.
- Erfolgsanzeige enthält Titel, Pfad und Ziel als kopierbaren Kurzkontext.
- Welle anlegen funktioniert; die Welle erscheint in der Wellenliste mit korrekten Spalten.
- Ungültige Wellen-Eingaben erzeugen Feldfehler und keinen Eintrag.
- Doppelklick erzeugt genau eine Datei.
- Eine Wellen-Zuordnung ist in beiden Ansichten erkennbar.

# Testfälle (TDD)

Alle Szenarien sind UI-Szenarien für den `tester` (Moli-Browser).

- **T1 Aufgabe anlegen:** Formular ausfüllen, absenden → Erfolg mit Pfad; Liste zeigt Titel, `Offen`, `ai`.
- **T2 Pflichtfeld leer:** Pflichtfeld leeren, absenden → Feldfehler, kein Eintrag.
- **T3 Akzeptanz mehrzeilig:** 3 Zeilen eingeben → 3 `- `-Einträge in der Datei.
- **T4 Kurzkontext:** nach Erfolg → Titel, Pfad, Ziel sichtbar/kopierbar.
- **T5 Welle anlegen:** Formular ausfüllen, absenden → Welle in der Liste, Spalten korrekt.
- **T6 Welle ungültig:** ungültigen Status/owner wählen → Feldfehler, kein Eintrag.
- **T7 Doppelklick:** Button doppelt klicken → genau eine Datei.
- **T8 Wellen-Zuordnung:** Aufgabe mit Welle anlegen → Zuordnung in beiden Ansichten erkennbar.

# Kontext

- **Abhängigkeiten:** A9 (`POST /api/task`, `POST /api/welle`), A10 (Gerüst).
- **Konfliktgruppe G9:** **nach A12**; `formulare.js` gehört A13.
- **Entscheidungen:** R2 (Slug/Kollision entstehen serverseitig in A4/A5, das Formular zeigt nur den zurückgegebenen Pfad), R10 (`feature:` optional, Welle/User-Story als optionale Felder).
- **Verweise:** [US-3](/projekt/user-stories/us-3.md), [US-4](/projekt/user-stories/us-4.md), [Phasenmodell](/projekt/phasen.md#format-einer-aufgaben-datei).

# Betroffene Dateien

- `definitions/app/static/js/formulare.js`
- `definitions/app/static/js/app.js` (Verdrahtung, additiv)
- `definitions/app/static/style.css` (Formularstile, additiv)

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

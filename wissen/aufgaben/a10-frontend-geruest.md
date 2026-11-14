---
type: Task
title: "A10: Frontend-Gerüst Navigation, Layout, Router, API-Client"
description: index.html mit fünf Navigationspunkten, style.css, fetch-Wrapper api.js und Hash-Router app.js als Startpunkt der Frontend-Kette.
task_status: im Test
phase: 6 Test
priority: hoch
assigned_to: coder
user_story: /projekt/user-stories/us-1.md
owner: ai
---

# Ziel

`static/index.html` erhält fünf Navigationspunkte (Übersicht, Wellen, Aufgaben, Entscheidungen, Projekt mit den Unterpunkten Konzept, Technische Spec, User Stories, Phasen, Log), alle benötigten Container-IDs, `<meta viewport>` und `<script type="module" src="/static/js/app.js">`. Dazu `static/style.css`, `static/js/api.js` (fetch-Wrapper mit einheitlicher Fehleranzeige) und `static/js/app.js` (Hash-Router). **Alle späteren JS-Arbeiten erfolgen in eigenen Modulen — `index.html` wird danach nicht mehr angefasst.** Kein CDN, kein Build.

# Akzeptanzkriterien

- `index.html` enthält die fünf Navigationspunkte und die fünf Projekt-Unterpunkte.
- Alle von den späteren Modulen benötigten Container-IDs sind vorhanden (`ansicht`, `fehler`, `tabelle` u. a.).
- `api.js` exportiert `getJson`/`postJson` und zeigt Fehler einheitlich an.
- `app.js` ist als ES-Modul eingebunden und routet per Hash.
- Keine externen Ressourcen (kein CDN), kein Build-Schritt.

# Testfälle (TDD)

Statische Prüfungen (T1–T4) laufen ohne Browser; T5–T8 sind UI-Szenarien für den `tester` (Moli-Browser).

- **T1 Navigation vorhanden (statisch):** `index.html` prüfen → 5 Labels + 5 Unterpunkte.
- **T2 Container-IDs:** `ansicht`, `fehler`, `tabelle` u. a. vorhanden.
- **T3 Modul-Einbindung:** `type="module"` + `app.js`.
- **T4 API-Wrapper:** `getJson`/`postJson` exportiert.
- **T5 Moli:** Seite öffnen → 5 Navigationspunkte sichtbar.
- **T6 Moli:** alle Punkte nacheinander anklicken → Ansicht wechselt, aktiver Punkt markiert, keine Konsolenfehler.
- **T7 Moli:** Projekt öffnen → Unterpunkte gelistet.
- **T8 Moli:** Server nicht erreichbar/Serverfehler → sichtbare Fehlermeldung, keine leere Seite.

# Kontext

- **Abhängigkeiten:** keine für den Aufbau; die Moli-Tests brauchen A7 (laufender Server).
- **Konfliktgruppe G8:** Startpunkt der Frontend-Kette; `index.html`/`style.css`/`app.js` gehören A10, danach nur noch additive Module durch A11–A14.
- **Reihenfolge:** A10 → A11 → A12 → A13 → A14; parallel zur Backend-Kette (keine gemeinsamen Dateien).
- **Entscheidungen:** R6 (eigener Minimal-Renderer, `textContent`, kein CDN), R7 („zuletzt geändert" lokal formatiert), R3 (fehlender owner als „—", Filteroption „ohne owner" vorbereiten).
- **Verweise:** Architektur in [Technischer Spec](/projekt/technische-spec.md); Navigationsumfang in [US-1](/projekt/user-stories/us-1.md).

# Betroffene Dateien

- `definitions/app/static/index.html`
- `definitions/app/static/style.css`
- `definitions/app/static/js/api.js`
- `definitions/app/static/js/app.js`
- `definitions/app/tests/test_static.py` (statische Prüfungen)

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

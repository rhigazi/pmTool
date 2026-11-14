---
type: Task
title: "A14: Entscheidungen- und Projekt-Ansicht"
description: Entscheidungsliste aus entscheidungen/log.md und Projekt-Ansicht mit den fünf Unterpunkten, beide über GET /api/file ohne neuen Server-Endpunkt.
task_status: im Review
phase: 5 Review
priority: mittel
assigned_to: coder
user_story: /projekt/user-stories/us-1.md
owner: ai
---

# Ziel

`static/js/projekt.js`: „Entscheidungen" listet die Einträge aus `entscheidungen/log.md` (`## YYYY-MM-DD: Titel` → Datum + Titel, Klick öffnet das Detail). „Projekt" listet die fünf Unterpunkte (Konzept, Technische Spec, User Stories, Phasen, Log) und öffnet sie. **Kein neuer Server-Endpunkt** — es wird ausschließlich `GET /api/file` genutzt.

# Akzeptanzkriterien

- Entscheidungen-Ansicht listet alle Einträge mit Datum und Titel.
- Klick auf einen Eintrag öffnet das Detail der Log-Datei.
- Projekt-Ansicht listet die fünf Unterpunkte und öffnet sie als Detail mit gerendertem Inhalt.
- Fehlende Datei erzeugt eine Fehlermeldung statt eines leeren Screens.
- Es wird kein neuer Server-Endpunkt eingeführt.

# Testfälle (TDD)

Alle Szenarien sind UI-Szenarien für den `tester` (Moli-Browser).

- **T1 Entscheidungen:** Entscheidungen öffnen → alle Einträge mit Datum + Titel.
- **T2 Eintrag öffnen:** Eintrag anklicken → Detail der Log-Datei.
- **T3 Projekt-Unterpunkte:** Projekt öffnen → 5 Unterpunkte gelistet.
- **T4 Spec öffnen:** Technische Spec anklicken → Detail mit gerendertem Inhalt.
- **T5 Fehlende Datei:** nicht existierenden Pfad öffnen → Fehlermeldung, kein leerer Screen.

# Kontext

- **Abhängigkeiten:** A8 (`GET /api/file`), A10 (Gerüst, Navigation).
- **Konfliktgruppe G9:** **nach A13**; `projekt.js` gehört A14 — letzter Schritt der Frontend-Kette.
- **Entscheidungen:** R6 (Minimal-Renderer, kein CDN), R10 (Feature-Dateien erst bei Feature-Beginn — hier nicht nötig).
- **Verweise:** [US-1](/projekt/user-stories/us-1.md), [Entscheidungslog](/entscheidungen/log.md), [Projekt-Index](/index.md).

# Betroffene Dateien

- `definitions/app/static/js/projekt.js`
- `definitions/app/static/js/app.js` (Verdrahtung, additiv)

# Ergebnisse

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-14 — coder (Umsetzung, abgeschlossen)

- **Ergebnis:** `projekt.js` (neu, Ansichten „Entscheidungen" + „Projekt"), `app.js` (additiv verdrahtet), `test_projekt.py` (neu, 55 Tests; rot 55 → grün 55). Nur `GET /api/file` (test-abgesichert: `test_projekt_js_nutz_nur_den_file_endpunkt`), `index.html` unverändert (A10-Vertrag), XSS-sicher (`textContent`/`createElement`, `rendereMarkdown` aus `detail.js`). T1–T5 im DOM-Stab + HTTP gegen Test-Bundle abgedeckt.
- **Belege:** Gesamtsuite serialisiert **731 grün**.
- **Befunde:** (a) Klick-Ziele interpretiert — T2 über `#/detail/entscheidungen/log.md`, T4 inline `#/projekt/<x>` gemäß A10-Nav-Routen (Review bestätigt). (b) Moli-E2E T1–T5 beim `tester` offen. (c) Parser-Toleranz der Datums-Trennzeichen als bewusste Designgrenze.
- **Offene Punkte:** Review + Testphase laufen.

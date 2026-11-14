---
type: Task
title: "A14: Entscheidungen- und Projekt-Ansicht"
description: Entscheidungsliste aus entscheidungen/log.md und Projekt-Ansicht mit den fünf Unterpunkten, beide über GET /api/file ohne neuen Server-Endpunkt.
task_status: abgeschlossen
phase: 8 Abgeschlossen
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

## 2026-11-14 — tester (Testphase, BESTANDEN)

- **Ergebnis:** **Testphase BESTANDEN** — 55/55 Tests (2× serialisiert); Szenarien T1–T5 doppelt belegt (Node-DOM-Harness + HTTP gegen Test-Bundle + Moli: Entscheidungsliste, Klick → Detail der Log-Datei, fünf Projekt-Unterpunkte, gerendertes Spec-Detail, fehlende Datei → Fehlermeldung).
- **Befunde:** Kein neuer Endpunkt (`test_projekt_js_nutz_nur_den_file_endpunkt`), R6-Renderer-Wiederverwendung, XSS-frei.
- **Offene Punkte:** Review läuft noch; danach reif für Doku/Abschluss (wie A12/A13).

## 2026-11-14 — reviewer (Review)

- **Ergebnis:** **Freigegeben** — keine kritischen/wesentlichen Befunde; Sicherheit sauber, kein neuer Endpunkt, `index.html` bytegenau unverändert, AK 1–5 durch 55 Tests belegt.
- **Befunde:** Die Interpretationsfrage ist ausdrücklich **bestätigt**: T2 über `#/detail/entscheidungen/log.md`, T4 inline über `#/projekt/<x>` passt zur A10-Routen-Intention (Routen-Vertrag, Navigationsmodell, fachliche Zuordnung — im Review begründet). Befunde 2/3/4/8 → Batch D (Kleintests + Leer-Hinweis); 5/6/7/9 → Aufräum/Post-MVP (siehe [features.md](/features.md)).
- **Hinweis:** Der Reviewer hat „731 grün" nicht nachvollzogen (kein Testlauf im Review); die Zahlen sind durch den `tester` separat bestätigt (55/55 A14, 52/81 A12/A13).
- **Offene Punkte:** Doku/Abschluss; offene Befunde 2–9 in der Kleinbefunde-Liste.

## 2026-11-14 — coder (Kleinbefunde-Takt, Batch D)

- **Ergebnis:** [Befund 2] Container-Vertragstest (`index.html`-IDs) + `meldeFehlendenContainer` statt Silent-Return; [Befund 3] XSS-Laufzeitnachweis (HTML-Payload bleibt Text); [Befund 4] T2 rendert echt (browser-naher `app_lauf`-Harness, echter `GET /api/file`); [Befund 8] Leer-Hinweis „Keine Inhalte." für leere Unterpunkt-Dateien.
- **Belege:** Kleinbefunde-Takt Batch D (+8 Tests); Gesamtsuite 761 grün.
- **Offene Punkte:** Befunde 5/6/7/9 (Aufräum/Post-MVP); Doku/Abschluss.

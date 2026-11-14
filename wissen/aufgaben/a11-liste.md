---
type: Task
title: "A11: Listenansicht mit Filtern und Klarung-Hervorhebung"
description: Tabellenrendering aus der Overview-API mit Status- und owner-Filter, Hervorhebung offener Klärungen sowie Leer- und Fehlerzustand.
task_status: in Doku
phase: 7 Dokumentation
priority: hoch
assigned_to: coder
user_story: /projekt/user-stories/us-1.md
owner: ai
---

# Ziel

`static/js/liste.js` rendert eine Tabelle (Titel, Status, owner, zuletzt geändert) aus `/api/overview` bzw. `/api/aufgaben` und `/api/wellen`. Dropdown-Filter für Status (6 Werte + „alle") und owner (alle/mensch/ai/ohne), Hervorhebung von „Klarung"-Zeilen, Leer- und Fehlerzustand. Kein automatisches Ausblenden von Einträgen.

# Akzeptanzkriterien

- Tabelle enthält die Spalten Titel, Status, owner, zuletzt geändert; Zeilenanzahl entspricht den API-Daten.
- Statusfilter (6 UI-Werte + „alle") und owner-Filter (alle/mensch/ai/ohne) wirken einzeln und kombiniert.
- „Klarung"-Zeilen sind visuell hervorgehoben.
- Leerzustand („Keine Einträge") und Fehlerzustand sind sichtbar; keine JS-Exception.
- Aufgaben- und Wellen-Ansicht nutzen dieselbe Listendarstellung mit den jeweiligen Endpunkten.
- Einträge werden nie automatisch ausgeblendet (auch `Geschlossen` bleibt sichtbar).

# Testfälle (TDD)

Alle Szenarien sind UI-Szenarien für den `tester` (Moli-Browser).

- **T1 Moli (Seite laden):** Übersicht öffnen → Kopfzeile vollständig, Zeilenanzahl = Fixture.
- **T2 Moli (Statusfilter):** Filter `Klarung` wählen → nur Klarung-Zeilen.
- **T3 Moli (owner-Filter):** Filter `mensch` wählen → nur mensch-Zeilen.
- **T4 Moli (Kombination):** Status `Klarung` + owner `mensch` → Schnittmenge.
- **T5 Moli (Reset):** beide Filter auf „alle" → alle Zeilen wieder da.
- **T6 Moli (Hervorhebung):** Klarung-Zeile vergleichen → abweichende Farbe/Klasse sichtbar.
- **T7 Moli (Leerzustand):** Filter ohne Treffer setzen → „Keine Einträge".
- **T8 Moli (Fehlerzustand):** API-Fehler provozieren → sichtbare Meldung, keine JS-Exception.
- **T9 Moli (Aufgabenpunkt):** Aufgaben öffnen → nur Aufgaben, keine Wellen.

Alle Szenarien werden vom `tester` mit dem Moli-Browser gegen die laufende App durchgespielt.

# Kontext

- **Abhängigkeiten:** A8 (Overview-/Listen-Endpunkte), A10 (Gerüst, Router, `api.js`).
- **Konfliktgruppe G9:** **nach A10**, `liste.js` gehört A11.
- **Reihenfolge:** A10 → A11 → A12 → A13 → A14.
- **Entscheidungen:** R3 (owner fehlt → „—", Filteroption „ohne owner"), R7 („zuletzt geändert" lokal formatiert), R6 (kein CDN).
- **Verweise:** [US-1](/projekt/user-stories/us-1.md), [Technische Spec](/projekt/technische-spec.md#mapping-task_status--ui-status-6-werte).

# Betroffene Dateien

- `definitions/app/static/js/liste.js`
- `definitions/app/static/js/app.js` (Verdrahtung, additiv)

# Ergebnisse

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-14 — coder (Nachbesserung, Stand zum Halt)

- **Ergebnis:** Nachbesserung sauber abgeschlossen: Fehlerzustand bleibt sichtbar (auch bei Filterwechsel), fail-loud bei Nicht-Array, `classList` statt `className` (A13-tauglich), toter Code entfernt, XSS-Verbot erweitert. (Quelle: Session-Rückmeldung „A11-Nachbesserung" im Übergabeprotokoll.)
- **Belege:** 54 Tests.
- **Offene Punkte:** Testphase und Doku (Review laut Übergabeprotokoll abgeschlossen).

## 2026-11-14 — tester (Gebündelte Testphase)

- **Ergebnis:** **Testphase BESTANDEN** (DoD-Beleg): 54 Tests grün; UI-Szenarien T1–T9 via Node-DOM-Harness bestanden (Moli-Abweichung dokumentiert). Gesamtlauf: 549 passed (Start = Ende, kein Zuwachs), 0 rot, 0 geskippt.
- **Offene Punkte:** Review-Bestätigung.

## 2026-11-14 — reviewer (Review-Runde 1)

- **Ergebnis:** **Freigegeben** — keine kritischen Befunde. 1 Kleinbefund.
- **Befunde:** [A11-1] klein: `className`-Initialisierungen (Rest nach Umstellung auf `classList`).
- **Offene Punkte:** A11-1 (Aufräum-Takt, siehe [features.md](/features.md)); Doku/Abschluss.

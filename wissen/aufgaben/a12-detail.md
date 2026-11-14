---
type: Task
title: "A12: Detailansicht Markdown, Nachtrag, owner/Status-Bedienung"
description: Detailansicht mit Frontmatter-Kopf, sicherem Markdown-Rendering, Nachtragsformular sowie owner-Umschalter und den Status-Buttons Klarung/Geschlossen.
task_status: im Review
phase: 5 Review
priority: hoch
assigned_to: coder
user_story: /projekt/user-stories/us-2.md
owner: ai
---

# Ziel

`static/js/detail.js`: Klick auf eine Listenzeile öffnet die Detailansicht mit Frontmatter-Kopf und gerendertem Markdown (Minimal-Renderer, XSS-sicher via `textContent`). Dazu das Formular „Nachtrag einfügen" (POST, sofortige Anzeige), ein owner-Umschalter und **ausschließlich** die Status-Buttons `Klarung`/`Geschlossen`.

# Akzeptanzkriterien

- Detailansicht zeigt Titel, Frontmatter-Kopf und gerenderten Markdown-Inhalt.
- Nachtrag wird per POST gespeichert und erscheint sofort; nach Reload genau einmal.
- Leerer Nachtrag erzeugt eine Fehlermeldung und keinen Eintrag.
- owner ist umschaltbar (`mensch`/`ai`) und die Änderung ist in der Liste sichtbar.
- Es existieren genau die Status-Buttons `Klarung` und `Geschlossen` — keine Pipeline-Status.
- HTML-Eingaben im Markdown werden als Text dargestellt, nicht ausgeführt.
- Serverfehler (z. B. 403) werden sichtbar gemeldet, ohne die Datei zu verändern.

# Testfälle (TDD)

Alle Szenarien sind UI-Szenarien für den `tester` (Moli-Browser).

- **T1 Detail öffnen:** Zeile anklicken → Titel, FM-Kopf, gerenderter Text.
- **T2 Nachtrag speichern:** Text eingeben, speichern → Marker sofort sichtbar.
- **T3 Persistenz:** Seite neu laden → Nachtrag genau einmal vorhanden.
- **T4 Leerer Nachtrag:** leeres Feld absenden → Fehlermeldung, kein Eintrag.
- **T5 owner umschalten:** owner wechseln → Anzeige wechselt, in der Liste sichtbar.
- **T6 Status-Buttons:** Detailansicht prüfen → genau „Klarung" und „Geschlossen".
- **T7 Klarung setzen:** `Klarung` klicken → Liste zeigt `Klarung` + `mensch`, hervorgehoben.
- **T8 Geschlossen setzen:** `Geschlossen` klicken → `Geschlossen`, bleibt in der Liste.
- **T9 XSS-Schutz:** `<script>` in den Nachtrag schreiben → als Text sichtbar, keine Ausführung.
- **T10 403-Pfad:** verbotenen Status per API/Netzwerk erzwingen → Fehlermeldung sichtbar, Datei unverändert.

# Kontext

- **Abhängigkeiten:** A8 (Detail-/Overview-API), A9 (Schreib-API), A10 (Gerüst).
- **Konfliktgruppe G9:** **nach A11**; `detail.js` gehört A12.
- **Entscheidungen:** R1 (nur `Klarung`/`Geschlossen` sind über die UI setzbar; Pipeline-Status bleibt der KI vorbehalten), R6 (Minimal-Renderer mit `textContent`, kein CDN), R13 (Datum im Marker als Serverparameter), R3 (owner-Anzeige).
- **Verweise:** [US-2](/projekt/user-stories/us-2.md), [US-5](/projekt/user-stories/us-5.md), [Technische Spec](/projekt/technische-spec.md#schreibrechte-verbindlich).

# Betroffene Dateien

- `definitions/app/static/js/detail.js`
- `definitions/app/static/js/app.js` (Verdrahtung, additiv)

# Ergebnisse

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-14 — coder (Umsetzung, Stand zum Halt)

- **Ergebnis:** `detail.js` mit XSS-sicherem Minimal-Renderer, Nachtrag-Formular, owner-Umschalter, ausschließlich `Klarung`/`Geschlossen`-Buttons, strikte Payload ohne leere Felder. (Quelle: Session-Rückmeldung „A12 Detailansicht" im Übergabeprotokoll.)
- **Belege:** 49 Tests + E2E-Smoke; Gesamtsuite 539+ grün (Stand zum Halt).
- **Offene Punkte:** Review, Testphase (Moli/Harness), Doku.

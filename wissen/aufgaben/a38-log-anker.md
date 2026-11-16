---
type: Task
title: "A38: Log-Anker (A14-9)"
description: Jeder Log-Eintrag bekommt einen eigenen Anker — Verweise öffnen den konkreten Eintrag,
  nicht immer den Anfang der Seite.
task_status: im Review
phase: 5 Review
priority: niedrig
assigned_to: coder
owner: ai
aktuell: "reviewer: A38 Review (Mutanten + Urteil)"
freigabe: true
---

# Ziel

Log-Einträge (`wissen/log.md`, `wissen/entscheidungen/log.md`) verlinken alle auf dieselbe Detailseite; ein Anker je Eintrag (`#/detail/entscheidungen/log.md#<anker>`) öffnet den konkreten Eintrag.

# Akzeptanzkriterien

Noch keine Einträge — der `planner` ergänzt/schärft sie (IDs im Markdown-Renderer, stabile Anker auch bei Umlauten/Format).

# Testfälle (TDD)

Noch keine Einträge — der `planner` ergänzt die Testfälle.

# Kontext

- Ausgegliedert aus [A33](a33-kleinbefunde-aufräum-takt.md) (PM-Entscheidung 2026-11-15).
- **Reihenfolge:** nach A29; betrifft `projekt.js`/`detail.js` (Markdown-Renderer).
- Aufwand laut A33-Plan: 2–3 h.

# Betroffene Dateien

Noch keine Einträge — die Planung ergänzt die betroffenen Dateien.

# Ergebnisse
## 2026-11-16 — coder (Welle C): Log-Anker — 24 neue Tests grün

- **Ergebnis:** `detail.js`: `erstelleAnker` (stabiler Slug `[a-z0-9-]+`, Umlaute `ae/oe/ue/ss`, max. 80 Zeichen, Fallback `abschnitt` — XSS-sicher als `id`), `erstelleAnkerVergabe` (Duplikate `-2`, `-3`; dieselbe Vergabe für Renderer und Verweis-Liste), `rendereMarkdown` vergibt `id` je Überschrift (nur `textContent`/`id`), `springeZuAnker` (Klasse `anker-ziel`, `tabindex=-1`, `scrollIntoView` + `focus()`), `trenneAnker` (`pfad#anker` — `ladeDetail` lädt nur den Pfad und springt danach). `projekt.js`: `parseEntscheidungen` liefert `{datum, titel, anker}` (Anker-Vergabe über alle Überschriften, exakt deckungsgleich zum Renderer); Entscheidungen-Links `#/detail/<pfad>#<anker>`; `ladeProjektAnsicht` akzeptiert `unterpunkt#anker`.
- **Tests:** neu `test_log_anker.py` (17 rot → **24 grün**); `test_projekt.py` an den erweiterten Parser-Vertrag angepasst (**63 grün**). Anrainer: `test_detail` 58, `test_features` 98, `test_welle_zuordnung` 43, weitere 159 — grün.
- **Bewusste Abweichungen:** Router-Vertrag (`app.js`) unangetastet (Trennung in `detail.js`/`projekt.js`); Link-Format mit kodiertem Slash (`entscheidungen%2Flog.md#<anker>`) konventionskonform zum bestehenden Detail-Route; Hervorhebung nur als Klasse + Fokusring (kein `style.css`-Eingriff — `.anker-ziel` kann später gestylt werden); Parser-Vertrag `parseEntscheidungen` erweitert (+`anker`).
- **Offen:** Review läuft; AK-Block der Aufgaben-Datei war leer (aus A33 A14-9 + Spec abgeleitet) → Doku-Runde.


Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

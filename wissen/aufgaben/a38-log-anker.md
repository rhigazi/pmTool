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

- **AK-1 (stabile Anker):** Der Markdown-Renderer vergibt jeder Überschrift eine `id`: nur `[a-z0-9-]`, Umlaute `ä/ö/ü/ß` → `ae/oe/ue/ss`, NFD-Faltung (Akzente entfallen), Mehrfachtrenner zu `-`, keine führenden/abschließenden Bindestriche, max. 80 Zeichen, Fallback `abschnitt`. Die `id` entsteht ausschließlich aus `textContent`/`id` (XSS-sicher, kein `innerHTML`).
- **AK-2 (Duplikate):** Gleiche Überschriften im selben Dokument erhalten `-2`, `-3`, … — Renderer und Verweis-Liste nutzen dieselbe Vergabe, damit Verweise exakt auf die gerenderten IDs zeigen.
- **AK-3 (Verweise):** Die Entscheidungen-Liste verlinkt **jeden** Eintrag einzeln als `#/detail/entscheidungen%2Flog.md#<anker>` (kodierter Slash = bestehende Detail-Route-Konvention; der Router akzeptiert auch die unkodierte Form); Anker aus `## YYYY-MM-DD: Titel`.
- **AK-4 (Sprung):** `ladeDetail` trennt `pfad#anker`, lädt **nur den Pfad** (kein `#` in der API-Anfrage) und springt nach dem Rendern. Das Ziel erhält `anker-ziel`, `tabindex=-1`, `scrollIntoView` und `focus()`. Ohne Anker bleibt die Seite am Anfang; ein unbekannter Anker ist robust (kein Fehler, Inhalt sichtbar).
- **AK-5 (Projekt-Ansicht):** `ladeProjektAnsicht({ unterpunkt: "log#<anker>" })` lädt `log.md` und springt zum Eintrag.
- **AK-6 (Bestand):** Der Router (`app.js`) bleibt unverändert — die Trennung liegt in `detail.js`/`projekt.js`; beide Pfadformen (`%2F` und `/`) funktionieren. A14-9-Kernfall „Entscheidungen" ist erfüllt; eine UI-Liste für Log-Eintragslinks bleibt K6 (nicht A38).

# Testfälle (TDD)

- `definitions/app/tests/test_log_anker.py` (**24**): statische Export-/Senken-Prüfungen; reine Logik `erstelleAnker` (Log-Überschrift, Umlaute/Sonderzeichen, ASCII-Whitelist, Fallback/Länge, Duplikat-Suffixe); Renderer-IDs (einfach, doppelt, HTML im Titel literal); Detail-Sprung (`anker-ziel`, `tabindex`, `scrollIntoView`/`focus`, nur Pfad geladen, ohne/unbekannter Anker); `parseEntscheidungen` inkl. `anker`; Verweis-Hrefs (`…%2Flog.md#…`) und Suffix-Gleichlauf; Projekt-Ansicht `log#anker`; Router-Lauf über den echten Hash `#/detail/entscheidungen%2Flog.md#<anker>`.
- **Regression:** `definitions/app/tests/test_projekt.py` (**63**) an den erweiterten Parser-Vertrag (`+anker`) angepasst; Anrainer `test_detail` 58, `test_features` 98, `test_welle_zuordnung` 43 grün.

# Kontext

- Ausgegliedert aus [A33](a33-kleinbefunde-aufräum-takt.md) (PM-Entscheidung 2026-11-15).
- **Reihenfolge:** nach A29; betrifft `projekt.js`/`detail.js` (Markdown-Renderer).
- **Link-Format (tatsächlich, A38-K4):** `#/detail/entscheidungen%2Flog.md#<anker>` — der Slash ist mit `encodeURIComponent` kodiert (`entscheidungen%2Flog.md`), das ist die bestehende Konvention der Detail-Route. Der Router (`app.js` teilt vor dem Dekodieren) akzeptiert daneben auch die unkodierte Form `#/detail/entscheidungen/log.md#<anker>`.
- Aufwand laut A33-Plan: 2–3 h.

# Betroffene Dateien

- `definitions/app/static/js/detail.js` — `erstelleAnker`, `erstelleAnkerVergabe`, Renderer-IDs, `springeZuAnker`, `trenneAnker`
- `definitions/app/static/js/projekt.js` — `parseEntscheidungen` (+`anker`), Entscheidungen-Links, `ladeProjektAnsicht` (`unterpunkt#anker`)
- `definitions/app/tests/test_log_anker.py` (neu, 24), `definitions/app/tests/test_projekt.py` (Parser-Vertrag, 63)
- `definitions/app/static/js/app.js` — unverändert (Router-Vertrag)

# Ergebnisse
## 2026-11-16 — documenter: AK-/Testfall-/Datei-Blöcke + Link-Format nachgezogen (Reviews A38-K4/K5)

- Aus dem Code-Stand belegt: AK-1–AK-6 (Anker-Slug, Duplikate, Verweise, Sprung, Projekt-Ansicht, Bestand) und die Testzuordnung (24 neue Tests + `test_projekt.py` 63). **Tatsächliches Link-Format:** `#/detail/entscheidungen%2Flog.md#<anker>` (kodierter Slash = bestehende Konvention; der Router akzeptiert auch die unkodierte Form `#/detail/entscheidungen/log.md#<anker>`) — im Kontext ergänzt.

## 2026-11-16 — reviewer (kombiniert mit A40): FREIGEGEBEN — Rücklauf W1 läuft

- **Urteil:** FREIGEGEBEN — 7/8 Mutanten getötet (Sanitizing, Duplikat-Zähler, `trenneAnker`, `focus`, Renderer-IDs, Link-Anker, Umlaut-Mapping); M8 (Sanitizer lässt `é` durch) überlebt = **Testlücke W1** (Test prüft `islower()` statt ASCII-Whitelist). Produktivcode korrekt. Link-Format (`%2F`-Konvention), Parser-Erweiterung, Fokus-Hervorhebung ohne CSS: alle akzeptiert. **K-Klammern:** K1 `trenneAnker` bei `#` im Pfad (Test ergänzen), K2 globale `getElementById`-Auflösung (Slug vs. feste Seiten-IDs), K3 CSS-Hervorhebung `.anker-ziel` (späterer Takt), K4 Doku zeigt künftig die `%2F`-Form, K5 AK-Block nachziehen (Doku-Runde), K6 keine UI-Liste für Log-Eintragslinks (A14-9-Kernfall: Entscheidungen — erfüllt).

## 2026-11-16 — coder (Welle C): Log-Anker — 24 neue Tests grün

- **Ergebnis:** `detail.js`: `erstelleAnker` (stabiler Slug `[a-z0-9-]+`, Umlaute `ae/oe/ue/ss`, max. 80 Zeichen, Fallback `abschnitt` — XSS-sicher als `id`), `erstelleAnkerVergabe` (Duplikate `-2`, `-3`; dieselbe Vergabe für Renderer und Verweis-Liste), `rendereMarkdown` vergibt `id` je Überschrift (nur `textContent`/`id`), `springeZuAnker` (Klasse `anker-ziel`, `tabindex=-1`, `scrollIntoView` + `focus()`), `trenneAnker` (`pfad#anker` — `ladeDetail` lädt nur den Pfad und springt danach). `projekt.js`: `parseEntscheidungen` liefert `{datum, titel, anker}` (Anker-Vergabe über alle Überschriften, exakt deckungsgleich zum Renderer); Entscheidungen-Links `#/detail/<pfad>#<anker>`; `ladeProjektAnsicht` akzeptiert `unterpunkt#anker`.
- **Tests:** neu `test_log_anker.py` (17 rot → **24 grün**); `test_projekt.py` an den erweiterten Parser-Vertrag angepasst (**63 grün**). Anrainer: `test_detail` 58, `test_features` 98, `test_welle_zuordnung` 43, weitere 159 — grün.
- **Bewusste Abweichungen:** Router-Vertrag (`app.js`) unangetastet (Trennung in `detail.js`/`projekt.js`); Link-Format mit kodiertem Slash (`entscheidungen%2Flog.md#<anker>`) konventionskonform zum bestehenden Detail-Route; Hervorhebung nur als Klasse + Fokusring (kein `style.css`-Eingriff — `.anker-ziel` kann später gestylt werden); Parser-Vertrag `parseEntscheidungen` erweitert (+`anker`).
- **Offen:** Review läuft; AK-Block der Aufgaben-Datei war leer (aus A33 A14-9 + Spec abgeleitet) → Doku-Runde.


Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

---
type: Task
title: "A37: DOM-Harness-Konsolidierung (A14-6)"
description: tests/dom_helfer.py wird zur einzigen Harness-Quelle — die vier Altkopien und die
  UI-Testdateien werden umgestellt, ohne Verhaltenswechsel.
task_status: abgeschlossen
phase: 8 Abgeschlossen
priority: niedrig
assigned_to: coder
owner: ai
aktuell: ""
freigabe: true
---

# Ziel

Der DOM-Test-Harness existiert in mehreren Kopien (`test_detail`, `test_suche`, `test_features`, `test_welle_zuordnung`); A30 legt `tests/dom_helfer.py` als gemeinsame Quelle an. Diese Aufgabe stellt alle UI-Testdateien darauf um (kein Verhaltenswechsel, reine Konsolidierung).

# Akzeptanzkriterien

Noch keine Einträge — der `planner` ergänzt/schärft sie (wichtig: keine Assertion wird abgeschwächt; Testzahlen bleiben identisch).

# Testfälle (TDD)

Noch keine Einträge — der `planner` ergänzt die Testfälle.

# Kontext

- Ausgegliedert aus [A33](a33-kleinbefunde-aufräum-takt.md) (PM-Entscheidung 2026-11-15).
- **Reihenfolge:** nach A29 (alle Testdateien stabil); nutzt `dom_helfer.py` aus A30.
- **Nachtrag (A28-Review, K3):** Beim Umstellen auch die Harness-Lücke beheben, der `detail.js` aktuell ausweicht (`document.createTextNode` fehlt im A12-Harness → Produktivcode nutzt leeres `span` mit `" "` als Trenner, `detail.js:585-588`); `dom_helfer.py` kann `createTextNode` — nach dem Umstieg den Produktivcode-Weg rückgängig machen (Trenner sauber) und `test_detail.py` schärfen.
- Aufwand laut A33-Plan: 5–8 h.
- **Nachtrag (A34-P3-Review, 2026-11-16):** `definitions/app/tests/test_unteraufgabe_ui.py` (T35) nutzt einen lokalen `Knoten.prototype.focus`-Stub, weil der Mini-DOM `focus` nicht kennt. Diese Überbrückung fällt weg, sobald A37 den Harness konsolidiert — dann die Fokus-Assertion über den echten DOM prüfen.

# Betroffene Dateien

Noch keine Einträge — die Planung ergänzt die betroffenen Dateien.

# Ergebnisse
## 2026-11-16 — coder (Rücklauf) + PM: W4/W5 behoben → **abgeschlossen**

- **W4:** Zwei-Hash-Navigation in `test_features.py` (`SZENARIO_ROUTER_WECHSEL` + `test_t3_routenwechsel_raeumt_aria_current_beim_altlink_ab`: `#/features` → `#/projekt/konzept`, `aria-current` wandert, genau ein aktiver Link je Zustand) — Mutante M10 (`removeAttribute` als No-op) jetzt **getötet**.
- **W5:** veralteter `abgeben`-Helfer + falscher Kommentar in `test_unteraufgabe_ui.py` entfernt (beide Submit-Stellen nutzen `ausloesen`); Bonus-Beleg: die `preventDefault`-Mutante wird nun von 6 Tests erwischt (vorher durch den lokalen Helfer verdeckt).
- Review FREIGEGEBEN, Rücklauf erledigt — **A37 abgeschlossen** (PM, 2026-11-16).

## 2026-11-16 — reviewer (kombiniert mit A35): FREIGEGEBEN — Rücklauf W4/W5 läuft

- **Urteil:** FREIGEGEBEN — 6/7 A37-Mutanten getötet (focus/ausloesen/toggle/Import/querySelectorAll/globales ausloesen); eine überlebende (M10 `removeAttribute` als No-op) = **Testlücke W4**. Funktions-/Assert-Deltas exakt aufgeklärt (nur Helfer-Asserts weg), Baseline/Endstand 368→368 bestätigt, API additiv.
- **Befunde:** W4 Zwei-Hash-Navigation testen (`aria-current` muss wandern); W5 veralteter `abgeben`-Helfer + falscher Kommentar in `test_unteraufgabe_ui.py`; W6 Commit-Schnitt (s. A35); W7 Doku-Doppelüberschrift (PM-Bug, behoben).


## 2026-11-16 — coder (Welle A): DOM-Harness konsolidiert — 368→368 identisch

- **Ergebnis:** `dom_helfer.py` ist die einzige Harness-Quelle; **fünf** Altkopien entfernt (`test_detail`, `test_suche`, `test_features`, `test_welle_zuordnung`, `test_projekt` — fünfte Kopie, in der Aufgabe nur vier genannt), alle migrierten Dateien importieren den Harness. API **additiv** erweitert: `classList.toggle`, `removeAttribute`, `Knoten.ausloesen(art, ereignis)` (mit `target`/`preventDefault`), `focus()` setzt `document.activeElement`, `document.querySelectorAll`/`addEventListener`/`readyState`/`activeElement`, Helfer `sichtbar`/`links`/`knotenMitKlasse`. Bestehende API unverändert.
- **Testzahlen vorher/nachher exakt identisch:** 56 + 72 + 98 + 43 + 63 + 36 = **368**; alle übrigen Harness-Nutzer zusammen **551 passed**.
- **A34-K-Punkt gelöst:** lokaler `Knoten.prototype.focus`-Stub in `test_unteraufgabe_ui.py` entfällt (Harness-Fokus).
- **Fremd-Koordination A35:** `detail.js` wurde parallel auf `ui_status` umgestellt — der Fetch-Stub in `test_features.py` liefert nun `"ui_status": "In Arbeit"` (Assertions unverändert); gegen `git show HEAD:…/detail.js` nachgewiesen: 98/98 auch ohne Fremdänderung.
- **Offen (Folge an A36):** Produktivcode-Weg `detail.js:595-598` (leeres `span`-Trennzeichen) konnte nicht zurückgebaut werden (A37-Rahmen: kein `static/`) — Harness kann `createTextNode`; Folgeauftrag: Trenner auf `document.createTextNode(" ")` umstellen + Assertion schärfen (A28-K3-Rest).

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

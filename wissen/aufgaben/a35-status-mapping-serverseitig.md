---
type: Task
title: "A35: Status-Mapping server-seitig (A12-1)"
description: Status.py ist die einzige Mapping-Quelle — overview.details liefert ui_status/hinweis/owner_default,
  der JS-Spiegel TASK_STATUS_UI/OWNER_DEFAULTS in detail.js entfällt.
task_status: abgeschlossen
phase: 8 Abgeschlossen
priority: mittel
assigned_to: coder
owner: ai
aktuell: ""
freigabe: true
---

# Ziel

Der Status-Mapping-Spiegel in `detail.js` (`TASK_STATUS_UI`/`OWNER_DEFAULTS`) dupliziert `status.py` und kann driftieren (Befund A12-1, ausgegliedert aus [A33](a33-kleinbefunde-aufräum-takt.md)). Abhilfe: `overview.details` liefert `ui_status`/`hinweis`/`owner_default` direkt aus `status.py` (analog zu A30s `arbeitsstatus`), `detail.js` nutzt die Werte und der JS-Spiegel entfällt.

# Akzeptanzkriterien

Noch keine Einträge — der `planner` ergänzt/schärft sie (Grundlage: Mapping-Matrix über die API + UI-Regression).

# Testfälle (TDD)

Noch keine Einträge — der `planner` ergänzt die Testfälle.

# Kontext

- Ausgegliert aus [A33](a33-kleinbefunde-aufräum-takt.md) (PM-Entscheidung 2026-11-15, Nummer bestätigt).
- **Reihenfolge:** nach A29 (`detail.js`, `overview.py`); danach A36 (`schreibgeschuetzt`-Signal) darauf aufbauend.
- Aufwand laut A33-Plan: 4–6 h.

# Betroffene Dateien

Noch keine Einträge — die Planung ergänzt die betroffenen Dateien.

# Ergebnisse
## 2026-11-16 — coder (Rücklauf) + PM: W1/W2 behoben → **abgeschlossen**

- **W1:** `test_t5_ohne_server_status_kein_js_mapping` um `{"status": "Geschlossen"}` und `{"frontmatter": {"status": "Geschlossen"}}` parametrisiert — Mutante M15 (JS-Fallback auf `frontmatter.status`) jetzt **getötet** (18 → 20 Tests in `test_status_mapping_ui.py`).
- **W2:** `test_owner_explizit_hat_vorrang` → `test_owner_default_vor_rohem_frontmatter` (Werte gespreizt + bidirektionale Assertions); Präzedenz-Tausch-Mutante jetzt getötet. Begründung im Rücklauf-Bericht: der alte Name behauptete das Gegenteil des Vertrags (R3: `owner_default` ist bereits aufgelöst).
- Review FREIGEGEBEN, Rücklauf erledigt — **A35 abgeschlossen** (PM, 2026-11-16). Verbleibend: K1 Doku (Spec/README um die drei neuen `/api/file`-Felder) → Doku-Runde.

## 2026-11-16 — reviewer (kombiniert mit A37): FREIGEGEBEN — Rücklauf W1/W2 läuft

- **Urteil:** FREIGEGEBEN — 7/7 A35-Mutanten getötet (M1 `hinweis` weg, M2 `owner_default` getauscht, M3 Mapping vertauscht, M4 Spiegel zurück, M5 JS-Fallback, M6 owner-Vorrang, M14 nur-Task); eine überlebende Mutante (M15 JS-Fallback auf `frontmatter.status`) = **Testlücke W1**. Mapping-Matrix 11/11 deckungsgleich zur Spec.
- **Befunde:** W1 `test_t5` parametrisieren (auch `status`-Zweig pinnen); W2 `test_owner_explizit_hat_vorrang` spreizen (beide Werte `mensch` → keine Aussage); W3 Doku-Doppelüberschrift (PM-Bug, behoben); K1 Spec/README um `ui_status`/`hinweis`/`owner_default` ergänzen → Doku-Runde. W6 (Commit-Schnitt `e2ef34f` allein rot) = Prozess-Lektion: Testanpassungen mit der Produktänderung committen.


## 2026-11-16 — coder (Welle A): Status-Mapping server-seitig — 37 neue Tests grün

- **Ergebnis:** `overview.details()` liefert top-level `ui_status`, `hinweis` (immer vorhanden, `null` wenn keiner), `owner_default` aus `status.py` (einzige Mapping-Quelle, für alle Dateitypen); `detail.js` verbraucht die Serverfelder, der JS-Spiegel (`TASK_STATUS_UI`/`OWNER_DEFAULTS`/`UI_STATUS_WERTE`/`OHNE_STATUS`) ist **entfernt** — A12-1-Drift geschlossen. Kein Status-Fallback im JS (fehlendes `ui_status` → „Offen", bewusst keine zweite Mapping-Quelle).
- **Tests:** neu `test_status_mapping_server.py` (19: Mapping-Matrix alle 11 `task_status`, owner-Vorrang, unbekannte Werte, `hinweis` immer) + `test_status_mapping_ui.py` (18: Spiegel weg, Serverfelder genutzt, DOM-Regression, XSS). TDD: 33 failed/4 passed → 37 passed. Anrainer 171/348/241/576 grün (Sätze laut Coder-Bericht).
- **Bewusste Abweichungen:** (1) drei bestehende Testdateien mussten mit (alte Assertions pinnten den alten Vertrag): `test_detail.py` (7 Spiegeltests auf Server-Vertrag), `test_arbeitsstand.py` T12 (exakte Schlüsselmenge +3), `test_unteraufgabe_ui.py` (2 Stubs `ui_status="Geschlossen"`); diese liegen gemischt mit A37-Harness-Migration im Baum. (2) `hinweis` immer vorhanden statt weggelassen (stabileres Format). (3) Aufgaben-Datei hatte keine AK/Testfälle — Grundlage war Ziel/Kontext + A33 + Spec-Mapping-Tabelle + `test_status.py` (AK-Ergänzung → documenter).
- **Offen:** Review (kombiniert mit A37) läuft; Doku (Spec-API-Tabelle `/api/file`, README, features) → Doku-Runde; A36 kann `schreibgeschuetzt` analog top-level in `details()` ergänzen.

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

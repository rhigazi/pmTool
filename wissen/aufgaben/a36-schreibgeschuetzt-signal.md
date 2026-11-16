---
type: Task
title: "A36: schreibgeschuetzt-Signal (A12-Schreib-UI-Grenze)"
description: Die API markiert reservierte Dateien als schreibgeschützt, die UI blendet Schreibaktionen
  aus — der Server-403 bleibt zweite Barriere.
task_status: im Review
phase: 5 Review
priority: mittel
assigned_to: coder
owner: ai
aktuell: "reviewer: A36 Review (Mutanten + Urteil)"
freigabe: true
---

# Ziel

Die Schreib-UI bietet auf reservierten Dateien (index.md/features.md/log.md) Aktionen an, die der Server mit 403 ablehnt (fail-loud, Befund A12-Grenze). Abhilfe: die API liefert ein `schreibgeschuetzt`-Signal, die UI blendet Schreibaktionen aus. **Keine clientseitige Duplizierung der reservierten Namensliste** (Mapping-Drift-Regel aus A12-1!).

# Akzeptanzkriterien

Noch keine Einträge — der `planner` ergänzt/schärft sie. Server-403 bleibt als zweite Barriere unverändert bestehen.

# Testfälle (TDD)

Noch keine Einträge — der `planner` ergänzt die Testfälle.

# Kontext

- Ausgegliedert aus [A33](a33-kleinbefunde-aufräum-takt.md) (PM-Entscheidung 2026-11-15; ursprünglich PM-Entscheidung im A14-Review: „dokumentieren statt clientseitiger Ausblendung — Ausblendung erst mit `schreibgeschuetzt`-Signal").
- **Reihenfolge:** nach A35 (dort wird `overview.details` bereits erweitert).
- Aufwand laut A33-Plan: 3–4 h.

# Betroffene Dateien

- `definitions/app/overview.py` — `details()` top-level `schreibgeschuetzt` (symlink-sicher)
- `definitions/app/static/js/detail.js` — `istSchreibgeschuetzt`, Ausblendung aller Schreibaktionen, Hinweis, `createTextNode`-Trenner
- `definitions/app/tests/test_schreibschuetzt_server.py` (neu, 16), `test_schreibschuetzt_ui.py` (neu, 9)
- `definitions/app/tests/test_detail.py` (+2 Trenner-Assertions), `test_arbeitsstand.py` (T12 +`schreibgeschuetzt`)

# Ergebnisse
## 2026-11-16 — reviewer: NACHBESSERUNG (W1/W2/W3 + K1–K5) — Rücklauf läuft

- **Urteil:** NACHBESSERUNG — Implementierung/Server-Signal korrekt und symlink-sicher (M1/M2/M3 getötet); 10/13 Mutanten tot. **W1** Anlegen-UI-Ausblendung ungepinnt (M8 überlebt), **W2** `/api/wellen`-Guard: `aufrufe` gesammelt, nie ausgewertet (M9 überlebt), **W3** Doku (Spec-Read-Modell, A37-Rest, Betroffene-Dateien — inzwischen vom PM nachgezogen). **K1** Hinweis-Negativfall fehlt (M12), **K2** AK-/Testfall-Blöcke leer (Prozess), **K3** „kein Listen-Feld" zu absolut (Symlink-Kante in Listen möglich), **K4** UX-Kante Welle-Feld zeigt rohen Pfad, **K5** Kosmetik. Rücklauf W1/W2/K1/K3 läuft; K4/K5 → Klammer.


## 2026-11-16 — coder (Welle B): `schreibgeschuetzt`-Signal — 25 neue Tests grün

- **Ergebnis:** `overview.details()` liefert top-level `schreibgeschuetzt` (`okf_bundle.ist_reserviert(pfad) or ist_reserviert(aufgeloest)` — Symlink auf `log.md` gilt als gesperrt; keine eigene Namensliste). `detail.js`: neuer Export `istSchreibgeschuetzt(daten)` (**nur exakt `true`** sperrt, analog `freigabe`-Muster); bei gesperrten Dateien entfallen Nachtragsformular, owner-Umschalter (Wert als Text), Statusknöpfe, Welle-Auswahl, Freigabe-/Wellen-Freigabe-Knopf, Anlegen-Knopf; Freigabe-Zustand bleibt lesbar; erklärender Hinweis `detail-schreibgeschuetzt-hinweis`; `/api/wellen` wird für gesperrte Dateien nicht geladen. Server-403 unverändert (zweite Barriere).
- **Bewusst kein Listen-Feld:** `okf_bundle.scan()` filtert reservierte Dateien aus — in den Listen kann `schreibgeschuetzt: true` nie auftreten (als Test T5 festgehalten).
- **A28-K3-Rest gelöst:** Trenner zwischen Zustand und Knopf jetzt `document.createTextNode(" ")` (Aufgaben- und Wellen-Freigabe, beide Trenner); in `test_detail.py` zwei **scharfe** Trenner-Assertions ergänzt (es existierte vorher kein Trenner-Test) — `test_detail.py` 56 → **58**.
- **Tests:** neu `test_schreibschuetzt_server.py` (16: reservierte Wurzel-/Nested-Dateien, Symlink-Fall, normale Dateien `false`, Listen ohne reservierte Einträge, 403-Bestandsschutz, Signal-Quelle `ist_reserviert`) + `test_schreibschuetzt_ui.py` (9: keine Schreibaktionen + Hinweis, Wellen-/Aufgaben-Variante, kein exaktes `true` → volle UI, keine Dateinamen im JS). TDD: 15 failed/68 passed → alles grün. `test_arbeitsstand.py` T12 um `schreibgeschuetzt` ergänzt. Anrainer **691** grün.
- **Bewusste Abweichungen:** AK/Testfelder der Aufgaben-Datei waren leer (Grundlage: A33-Befund A12-Schreib-UI + Schreibrechte-Matrix der Spec + A37-Nachtrag); kein Listen-Feld (s. o.).
- **Offen:** Review läuft; Doku (`schreibgeschuetzt` im Read-Modell der Spec, A37-Rest als erledigt) → Doku-Runde.

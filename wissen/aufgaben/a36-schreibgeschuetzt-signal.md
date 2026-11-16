---
type: Task
title: "A36: schreibgeschuetzt-Signal (A12-Schreib-UI-Grenze)"
description: Die API markiert reservierte Dateien als schreibgeschützt, die UI blendet Schreibaktionen
  aus — der Server-403 bleibt zweite Barriere.
task_status: abgeschlossen
phase: 8 Abgeschlossen
priority: mittel
assigned_to: coder
owner: ai
aktuell: ""
freigabe: true
---

# Ziel

Die Schreib-UI bietet auf reservierten Dateien (index.md/features.md/log.md) Aktionen an, die der Server mit 403 ablehnt (fail-loud, Befund A12-Grenze). Abhilfe: die API liefert ein `schreibgeschuetzt`-Signal, die UI blendet Schreibaktionen aus. **Keine clientseitige Duplizierung der reservierten Namensliste** (Mapping-Drift-Regel aus A12-1!).

# Akzeptanzkriterien

- **AK-1 (Signal):** `GET /api/file` liefert **top-level** `schreibgeschuetzt` für jede Datei, immer vorhanden (`true`/`false`). Berechnet aus `okf_bundle.ist_reserviert(pfad) or ist_reserviert(ziel)` — keine eigene Namensliste in `overview.py` oder im JavaScript.
- **AK-2 (Reservierte Dateien):** `index.md`, `log.md`, `features.md` und verschachtelte `aufgaben/index.md` sind `true`; normale Aufgaben/Wellen `false`. Ein Symlink auf eine reservierte Datei gilt ebenfalls als gesperrt. Lesen bleibt vollständig (Frontmatter, Markdown, Nachtrag-Liste).
- **AK-3 (UI-Ausblendung):** Nur ein exaktes `schreibgeschuetzt === true` sperrt. Dann entfallen Nachtragsformular, owner-Umschalter (Wert bleibt als Text), Statusknöpfe, Wellen-Auswahl, Freigabe-/Wellen-Freigabe-Knopf und Anlegen-Knopf; ein erklärender Hinweis (`detail-schreibgeschuetzt-hinweis`) erscheint; `/api/wellen` wird nicht geladen.
- **AK-4 (Fail-open nur ohne Signal):** Fehlt das Feld oder ist es nicht exakt `true` (`false`, `null`, `"true"`, `1`), bleibt die volle Schreib-UI bedienbar und es gibt **keinen** Sperrhinweis.
- **AK-5 (Zweite Barriere):** Der Server-403 für Schreibzugriffe auf reservierte Dateien (`/api/nachtrag`, `/api/meta`, `/api/freigabe`) bleibt unverändert bestehen.
- **AK-6 (Listen):** `/api/overview`, `/api/aufgaben`, `/api/wellen` führen keine reservierten Dateien und kein Schreibschutz-Feld (dort keine Schreibaktionen); eine Symlink-Kante kann in Listen erscheinen und ist dokumentiert.

# Testfälle (TDD)

- `definitions/app/tests/test_schreibschuetzt_server.py` (**16**): T1 reservierte Details `true` (parametrisiert), T2 normale Dateien `false`, T3 Inhalt bleibt lesbar, T4 Symlink auf `log.md` ist gesperrt, T5 Listen ohne reservierte Einträge/ohne Markierung, T6 Schreibzugriffe bleiben 403 (parametrisiert), T7 Signalquelle ist `okf_bundle.ist_reserviert` (Monkeypatch).
- `definitions/app/tests/test_schreibschuetzt_ui.py` (**9**): T1 reservierte Datei ohne Schreibaktionen + Sperrhinweis, T2 reservierte Welle (Zustand lesbar, kein Knopf), T3 reservierte Aufgabe (Werte statt Bedienung, kein Anlegen, keine Wellenliste), T4 ohne exaktes Signal volle UI inkl. Negativfall „kein Hinweis" (parametrisiert), T5 keine reservierte Namensliste in `detail.js`.
- **Regression:** `test_detail.py` (+2 scharfe `createTextNode`-Trenner-Assertions, 56→58), `test_arbeitsstand.py` T12 (+`schreibgeschuetzt`); A37-Harness-Überbrückung entfällt (Fokus über echten DOM).

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
## 2026-11-16 — coder (K-Sammlung): K4 behoben, K5 dokumentiert

- **K4:** Welle-Feld zeigt bei gesperrten Aufgaben jetzt `Titel (Pfad)` wie überall (fail-safe Dateistamm `w1` bei fehlendem/unlesbarem Titel); `/api/wellen` wird nur bei gesetzter `welle` geladen. 4 neue Tests (9 → 13).
- **K5 (Kosmetik):** nicht umsetzbar ohne `style.css`-Eingriff (der `.detail-aktionen`-Container ist nie leer — immer der Zurück-Link; Abstand aus `style.css`) → Vermerk für einen späteren CSS-Takt. `istSchreibgeschuetzt`-Export bewusst belassen.

## 2026-11-16 — documenter: AK-/Testfall-Blöcke nachgezogen (Review A36-K2)

- Aus den Ergebnis-Einträgen und dem Code-Stand belegt: AK-1–AK-6 (Signal, reservierte Dateien/Symlink, UI-Ausblendung nur bei exakt `true`, Fail-open ohne Signal, Server-403, Listen) und die Testzuordnung (16 Server + 9 UI + Regression). K5 (Kosmetik) bleibt als Klammer offen.

## 2026-11-16 — coder (Rücklauf) + PM: W1/W2/K1/K3 behoben → **abgeschlossen**

- **W1:** `schreibAktionen()` prüft jetzt auch `anlegen` (`#unteraufgabe-anlegen`); T1/T3 `anlegen is False`, T4-Kontrollprobe `is True` — Mutante M8 (Anlegen-Guard entfernt) **getötet**.
- **W2:** `detail_lauf`-Skripte liefern `aufrufe` (normalisiert); T1/T3 assertieren `"/api/wellen" not in aufrufe` (gesperrt), T4 `in` (frei) — Mutante M9 **getötet** (Killer ist T3; T1 sichert zusätzlich den `istAufgabe`-Zweig).
- **K1:** Negativfall „kein Sperrhinweis bei ungesperrter Datei" (alle 4 Signal-Varianten) — Mutante M12 (Hinweis immer) **getötet** (4 rot).
- **K3:** Docstring/Kommentare präzisiert (Symlink-Kante in Listen möglich, `scan` filtert namensbasiert) — nur Text.
- 25 grün (16+9, nur Assertions ergänzt). Vermerk des Coders: die Review-Zeilennummern waren durch A38 verschoben (Guards jetzt 960–966/1044–1046), inhaltlich geprüft. **A36 abgeschlossen** (PM, 2026-11-16). K4/K5 (UX-Kante Welle-Feld, Kosmetik) → Härtungs-Klammer.

## 2026-11-16 — reviewer: NACHBESSERUNG (W1/W2/W3 + K1–K5) — Rücklauf läuft

- **Urteil:** NACHBESSERUNG — Implementierung/Server-Signal korrekt und symlink-sicher (M1/M2/M3 getötet); 10/13 Mutanten tot. **W1** Anlegen-UI-Ausblendung ungepinnt (M8 überlebt), **W2** `/api/wellen`-Guard: `aufrufe` gesammelt, nie ausgewertet (M9 überlebt), **W3** Doku (Spec-Read-Modell, A37-Rest, Betroffene-Dateien — inzwischen vom PM nachgezogen). **K1** Hinweis-Negativfall fehlt (M12), **K2** AK-/Testfall-Blöcke leer (Prozess), **K3** „kein Listen-Feld" zu absolut (Symlink-Kante in Listen möglich), **K4** UX-Kante Welle-Feld zeigt rohen Pfad, **K5** Kosmetik. Rücklauf W1/W2/K1/K3 läuft; K4/K5 → Klammer.


## 2026-11-16 — coder (Welle B): `schreibgeschuetzt`-Signal — 25 neue Tests grün

- **Ergebnis:** `overview.details()` liefert top-level `schreibgeschuetzt` (`okf_bundle.ist_reserviert(pfad) or ist_reserviert(aufgeloest)` — Symlink auf `log.md` gilt als gesperrt; keine eigene Namensliste). `detail.js`: neuer Export `istSchreibgeschuetzt(daten)` (**nur exakt `true`** sperrt, analog `freigabe`-Muster); bei gesperrten Dateien entfallen Nachtragsformular, owner-Umschalter (Wert als Text), Statusknöpfe, Welle-Auswahl, Freigabe-/Wellen-Freigabe-Knopf, Anlegen-Knopf; Freigabe-Zustand bleibt lesbar; erklärender Hinweis `detail-schreibgeschuetzt-hinweis`; `/api/wellen` wird für gesperrte Dateien nicht geladen. Server-403 unverändert (zweite Barriere).
- **Bewusst kein Listen-Feld:** `okf_bundle.scan()` filtert reservierte Dateien aus — in den Listen kann `schreibgeschuetzt: true` nie auftreten (als Test T5 festgehalten).
- **A28-K3-Rest gelöst:** Trenner zwischen Zustand und Knopf jetzt `document.createTextNode(" ")` (Aufgaben- und Wellen-Freigabe, beide Trenner); in `test_detail.py` zwei **scharfe** Trenner-Assertions ergänzt (es existierte vorher kein Trenner-Test) — `test_detail.py` 56 → **58**.
- **Tests:** neu `test_schreibschuetzt_server.py` (16: reservierte Wurzel-/Nested-Dateien, Symlink-Fall, normale Dateien `false`, Listen ohne reservierte Einträge, 403-Bestandsschutz, Signal-Quelle `ist_reserviert`) + `test_schreibschuetzt_ui.py` (9: keine Schreibaktionen + Hinweis, Wellen-/Aufgaben-Variante, kein exaktes `true` → volle UI, keine Dateinamen im JS). TDD: 15 failed/68 passed → alles grün. `test_arbeitsstand.py` T12 um `schreibgeschuetzt` ergänzt. Anrainer **691** grün.
- **Bewusste Abweichungen:** AK/Testfelder der Aufgaben-Datei waren leer (Grundlage: A33-Befund A12-Schreib-UI + Schreibrechte-Matrix der Spec + A37-Nachtrag); kein Listen-Feld (s. o.).
- **Offen:** Review läuft; Doku (`schreibgeschuetzt` im Read-Modell der Spec, A37-Rest als erledigt) → Doku-Runde.

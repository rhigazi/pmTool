---
type: Feature Overview
title: Features-Überblick
description: Zeigt für jedes Feature, ob es umgesetzt ist oder noch offen, mit Verweis auf die zugehörigen Aufgaben.
tags: [features, steuerung]
---

# Statuswerte

`offen` · `in Umsetzung` · `umgesetzt` · `pausiert`

# Regeln

* Jeder Eintrag verlinkt auf seine Feature-Datei unter `/features/` und auf die zugehörigen Aufgaben unter `/aufgaben/`.
* Jeder Feature-Eintrag trägt eine Priorität (`hoch`/`mittel`/`niedrig`); die Planung leitet daraus Reihenfolge und Meilensteine ab.
* Zu jedem offenen Punkt müssen die Aufgaben so dokumentiert sein, dass ein `coder` sie eigenständig abarbeiten kann (siehe [Phasenmodell](/projekt/phasen.md)).
* Jede Umsetzung wird hier eingetragen und ins [Projekt-Log](/log.md) protokolliert.

# Offene Features

* [OKF Projekt-Manager (SPA)](features/okf-projekt-manager-spa.md) — Tracker auf das OKF-Bundle: Status/owner anzeigen, Nachträge, Aufgaben und Wellen anlegen, Colab-Start · **umgesetzt — MVP abnahmefähig (Abnahme durch Projektleitung ausstehend)** · Priorität **hoch**
  * **Meilenstein 2026-11-14: MVP-Abnahme vorbereitet (A17 bestanden)** — alle Aufgaben A1–A20 abgeschlossen; Abnahmelauf: 23/23 API-E2E, 761 passed, `verify.sh` Exit 0, Moli 0 Konsolenfehler, Hash-Nachweis. Gesamtsuite nach dem Kleinbefunde-Takt **761 grün** (serialisiert).
  * **Umgesetzt (Review/Test/Doku bzw. Nachbesserung):** [A1](aufgaben/a1-okf-bundle.md) `okf_bundle.py` (Fundament, Pfadschutz, zentrale Exceptions), [A3](aufgaben/a3-nachtrag.md) `nachtrag.py`, [A4](aufgaben/a4-neu-aufgabe.md) `neu_aufgabe.py`, [A5](aufgaben/a5-neu-welle.md) `neu_welle.py`, [A6](aufgaben/a6-meta.md) `meta.py`, [A7](aufgaben/a7-server.md) `server.py`, [A8](aufgaben/a8-api-lesen.md) Lese-API (4 GET-Routen, inkl. Kleinnachtrag), [A9](aufgaben/a9-api-schreiben.md) Schreib-API (4 POST-Routen), [A10](aufgaben/a10-frontend-geruest.md) Frontend-Gerüst (Testphase bestanden), [A11](aufgaben/a11-liste.md) Listenansicht, [A12](aufgaben/a12-detail.md) Detailansicht (inkl. T10), [A13](aufgaben/a13-formulare.md) Formulare (81 Tests), [A14](aufgaben/a14-projekt-ansicht.md) Entscheidungen-/Projekt-Ansicht (55 Tests), [A15](aufgaben/a15-setup-verify.md) `setup.sh`/`verify.sh`/README (App-Verteilung, Nummerierung 1–10), [A16](aufgaben/a16-start-colab.md) `start_colab.py`, [A18](aufgaben/a18-start-skript.md) `start.sh` + `docs/colab-start.md`, [A19](aufgaben/a19-verify-app-fallback.md) verify.sh-Fallback, [A20](aufgaben/a20-setup-haertung.md) setup.sh-Härtung
  * **Abgeschlossen:** [A2](aufgaben/a2-status-mapping.md) `status.py` (44 Tests, Test bestanden, Doku)
  * **Offen:** nur noch **MVP-Abnahme durch die Projektleitung**; danach Post-MVP: [A22](aufgaben/a22-e2e-regression.md) (E2E-Regression), A21 (Desktop-Modus) und die Post-MVP/Aufräum-Punkte (siehe unten). Abgeschlossen sind: Bestätigungs-Review (A1/A5/A7/A9/A15/A19), A13-/A14-Review, Testphase 2, Kleinbefunde-Takt und A17-Abnahmelauf.
  * **Vorgemerkt:** **A21 „Desktop-Modus/Lokal-Betrieb"** — Nummer reserviert, noch keine Aufgaben-Datei; pywebview-Desktop-Modus nach MVP (Entscheidung der Projektleitung 2026-11-14)

# Offene Punkte

## Erledigt — Kleinbefunde-Takt 2026-11-14 (4 Batches, je eigener Commit; Gesamtsuite 761 grün)

* **Batch A (Backend, +12 Tests):** echte Fixes `MAX_KANDIDATEN`-Off-by-One, A16-2 (`_installiere` → bool/Exit 1), A16-3 (`_port_belegt` bindet `0.0.0.0`); Regressionssicherungen N1–N4, A3-2; N7 als Überschrift „T7b" (Konsistenz zu T6b/T8b).
* **Batch B (Frontend, +7 Tests):** A13-1 (Label `Titel (Pfad)`), A13-2 (Auswahl-Erhalt), A11-1 (`classList.add` + Wächtertest), A12-3 (unbekannter owner fail-loud), A12-T4 (DOM-Test Fehlertext).
* **Batch C (Shell, +2 Tests):** A18-1 bis A18-3; R12 — `tools/`-Abschnitt nutzt `copy_tree` + Cache-Filter.
* **Batch D (A14, +8 Tests):** Befunde 2/3/4/8 (Container-Vertrag, XSS-Laufzeitnachweis, echtes T2-Rendern, Leer-Hinweis „Keine Inhalte.").
* **A20 vollständig umgesetzt** (Commits `c1a1a23`, `4d1f335`, `f0a37c8`, `cd91b78`) → in Doku.

## Offen (Post-MVP / Aufräum)

* [A22](aufgaben/a22-e2e-regression.md) E2E-Regressionstest (`test_e2e.py`) — T1/T2/T7-Kette aus dem A17-Abnahmelauf dauerhaft überführen.
* [A12-1] Status-Mapping-Spiegel (Mapping-Drift langfristig lösen).
* [A13-3] Linktext-Kosmetik (bräuchte Wellen-Titel-Lookup) — bewusst ausgelassen.
* [A4-1] `ziel`-Zeilen mit `#`-Beginn maskieren erwägen; [A4-2] `welle`-Feld in [Phasenmodell](/projekt/phasen.md)/Spec als optionales Feld ergänzen.
* [A5-B3] `description`-Feld bei Wellen; [A5-B4] Slug-Logik-Duplikat zu `neu_aufgabe`.
* [A6-1/A6-2] H1/H5/H7-Belege je H-Punkt mit Testnamen (H-Definitionen fehlen im Bundle); T2 Body-Hash optional.
* [A7-2] Startfehler-Meldung nennt absoluten Pfad.
* [A9-K3] 403-Notiz präzisieren (im Ergebnisprotokoll erfolgt; Spec-Abgleich offen); [A9-K4] TOCTOU als R8-Einschränkung (bekanntes Risiko).
* [A14-5] `istDatei`/Meldungen nach `api.js` ziehen; [A14-6] DOM-Harness-Fork `MINI_DOM` in `tests/harness_dom.py` konsolidieren; [A14-7] Request-Sequenz-Guard gegen Races (geerbt von A12); [A14-9] Anker je Log-Eintrag (UX).
* [A16-1] R11-Zitat korrigieren oder Ausweichport vormerken; [A16-4] Env-Weitergabe.
* [N5] Cache-Fixture schreibt ins Definitions-Repo (kosmetisch); [N8] T7 verschärft sich mit neuen Testdateien automatisch (Betriebshinweis).
* [A20] Pin-Pflege: URL + SHA256 bei Moli-Updates zusammen ändern.
* [A12] Grenze: Schreib-UI auf reservierten Dateien bleibt sichtbar (fail-loud 403, Datei unverändert) — Ausblendung erst mit `schreibgeschuetzt`-Signal der API (post-MVP).
* [A21] Desktop-Modus/Lokal-Betrieb (vorgemerkt, nach MVP).

## Umgebung / Projekt

* Root-Suite `pytest -q` bricht am doppelten Testdateinamen `test_telegram_send.py` (`tools/tests/` vs. `definitions/tools/tests/`) — vom `tester` bestätigt; kleine eigene Aufgabe (umbenennen oder pytest-`ignore`).
* Doppelte Sektionsnummer „8)" in `setup.sh --global` — **behoben** (Nummerierung durchgehend 1–10; `docs/uebergabeprotokoll.md` mitgezogen).
* Doku-Kosmetik A18 — **erledigt** (2026-11-14): `--dry-run`-Hinweis zu `verify.sh` (`docs/colab-start.md` + `start.sh`), `BUNDLE_ROOT`-Wortlaut (`$PROJEKT/wissen`, absolut), Reihenfolge Telegram-Secrets-Zelle vereinheitlicht (einheitlich nach `bash start.sh --colab`, Schritt 3).
* Detail-Endpunkt: unlesbare Datei → 500 statt neutraler Meldung (für A9-Review/A17 vormerken).
* Moli-Frage: **geklärt** (2026-11-14) — Moli wird installiert, der Node-DOM-Harness bleibt Fallback (Entscheidung „Moli-Integration").
* Moli-Browser-Szenarien beim `tester` offen: T1–T10 (A12) und T1–T8 (A13).
* A19-Nachlauf: nach A19-Ablage einmalig `test_setup_verteilung.py` + `test_verify_fallback.py` serialisiert nachlaufen — die Gesamtzahl steigt dann planmäßig über die Ausgangsbasis (neue Tests), das ist kein Befund.
* Flaky-Zone Parallelbetrieb: App-Test-Suite/verify-Läufe bei paralleler Tester-/Coder-Arbeit gelegentlich rot, serialisiert grün — Empfehlung: Testläufe serialisieren.

# Umgesetzte Features

*Noch keine.*

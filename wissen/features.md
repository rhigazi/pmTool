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

* [OKF Projekt-Manager (SPA)](features/okf-projekt-manager-spa.md) — Tracker auf das OKF-Bundle: Status/owner anzeigen, Nachträge, Aufgaben und Wellen anlegen, Colab-Start · **in Umsetzung** · Priorität **hoch**
  * **Meilenstein 2026-11-14:** Alle geplanten Feature-Aufgaben A1–A20 sind umgesetzt (A13/A14 als letzte Frontend-Aufgaben); Gesamtsuite **731 grün** (serialisiert).
  * **Umgesetzt (Review/Test/Doku bzw. Nachbesserung):** [A1](aufgaben/a1-okf-bundle.md) `okf_bundle.py` (Fundament, Pfadschutz, zentrale Exceptions), [A3](aufgaben/a3-nachtrag.md) `nachtrag.py`, [A4](aufgaben/a4-neu-aufgabe.md) `neu_aufgabe.py`, [A5](aufgaben/a5-neu-welle.md) `neu_welle.py`, [A6](aufgaben/a6-meta.md) `meta.py`, [A7](aufgaben/a7-server.md) `server.py`, [A8](aufgaben/a8-api-lesen.md) Lese-API (4 GET-Routen, inkl. Kleinnachtrag), [A9](aufgaben/a9-api-schreiben.md) Schreib-API (4 POST-Routen), [A10](aufgaben/a10-frontend-geruest.md) Frontend-Gerüst (Testphase bestanden), [A11](aufgaben/a11-liste.md) Listenansicht, [A12](aufgaben/a12-detail.md) Detailansicht (inkl. T10), [A13](aufgaben/a13-formulare.md) Formulare (81 Tests), [A14](aufgaben/a14-projekt-ansicht.md) Entscheidungen-/Projekt-Ansicht (55 Tests), [A15](aufgaben/a15-setup-verify.md) `setup.sh`/`verify.sh`/README (App-Verteilung, Nummerierung 1–10), [A16](aufgaben/a16-start-colab.md) `start_colab.py`, [A18](aufgaben/a18-start-skript.md) `start.sh` + `docs/colab-start.md`, [A19](aufgaben/a19-verify-app-fallback.md) verify.sh-Fallback, [A20](aufgaben/a20-setup-haertung.md) setup.sh-Härtung
  * **Abgeschlossen:** [A2](aufgaben/a2-status-mapping.md) `status.py` (44 Tests, Test bestanden, Doku)
  * **Offen:** [A17](aufgaben/a17-e2e.md) E2E-/Moli-Abnahmelauf (Moli-Smoke bereits erfolgreich); dazu das A14-Review, der Kleinbefunde-Takt (3 Batches), die Doku-Runde und die MVP-Abnahme — Bestätigungs-Review (A1/A5/A7/A9/A15/A19) und Testphase 2 (A12/A13/A14) sind bestanden.
  * **Vorgemerkt:** **A21 „Desktop-Modus/Lokal-Betrieb"** — Nummer reserviert, noch keine Aufgaben-Datei; pywebview-Desktop-Modus nach MVP (Entscheidung der Projektleitung 2026-11-14)

# Offene Punkte

## Kleinbefunde für einen späteren Aufräum-/Kleinbefunde-Takt (nicht jetzt beheben)

* [A1] `[B2]` Docstring `lesen_tolerant` — behoben (Verhaltenskorrektur, siehe Ergebnisprotokoll); verbleibend: H-Definitionen H1/H5/H7 zu A6 klären (siehe A6).
* [A3] `[A3-1]` **behoben** (reservierte, nicht existierende Datei → 403 statt 500); `[A3-2]` Testlücke: Zweig „`# Nachträge` vor weiteren Überschriften" ungetestet.
* [A4] `[A4-1]` `ziel`-Zeilen mit `#`-Beginn können Abschnittsstruktur vortäuschen — Maskierung erwägen; `[A4-2]` `welle`-Feld ist Spec-Erweiterung — in [Phasenmodell](/projekt/phasen.md)/Spec als optionales Feld ergänzen.
* [A5] `[B2]` **per PM-Entscheidung geschlossen** (`FALLBACK_KUERZEL` bleibt bewusst robuster Fallback, im Ergebnisprotokoll begründet); `[B3]` `description`-Feld fehlt bei Wellen; `[B4]` Slug-Logik dupliziert zu `neu_aufgabe`.
* [A6] `[A6-2]` T2 Body-Hash optional (Testzusatz); H1/H5/H7-Definitionen im Bundle nicht dokumentiert (Doku-Punkt aufgegriffen, Zuordnung H-Punkt → Testname offen).
* [A7] `[A7-2]` Startfehler-Meldung nennt absoluten Pfad.
* [A9] `[K3]` Doku-Präzisierung 403-Verhalten im Ergebnisprotokoll erledigt; `[K4]` TOCTOU als bekannte Einschränkung dokumentiert (R8).
* [A11] `[A11-1]` `className`-Initialisierungen vereinheitlichen.
* [A12] `[A12-1]` Status-Mapping-Spiegel (langfristig lösen); `[A12-3]` Owner-Auswahl „—"; Owner-Umschalter ohne eigenen Doppel-Wechsel-Schutz (bewusst nicht beauftragt).
* [A13] `(a)` T8 „beide Ansichten": eine Wellen-Spalte erfordert Änderungen in `liste.js`/`detail.js` (nicht beauftragt) — Klärungspunkt; `(b)` 200-Antwort mit `null`-Body via `postJson` nicht von Fehler unterscheidbar (fail-loud-Grenze).
* [A15] `[A15-2]` behoben; verbleibend: `tools/`-Abschnitt in `setup.sh` kopiert `__pycache__` (R12) — läuft im Kleinbefunde-Batch C.
* [A16] `[A16-1]` R11-Zitat in a16/a7 korrigieren oder Ausweichport vormerken; `[A16-2]` `pip`-Rückgabe ignorieren; `[A16-3]` `_port_belegt` 127.0.0.1 vs. 0.0.0.0; `[A16-4]` Env-Weitergabe.
* [A18] `[A18-1]` `hilfe()` `sed` off-by-one; `[A18-2]` 2 Zusatztests; `[A18-3]` Colab-Trap.
* [A20] **Pin-Pflege:** URL und SHA256 des Moli-Installers müssen bei Moli-Updates zusammen geändert werden (Folgeaufgabe vormerken, ggf. Teil von A21 oder eigene Kleinigkeit).

## Bestätigungs-Review N1–N8 (Kleinbefunde-Takt, läuft in 3 Batches)

* N1: Guard-Zweig `_sichere_meldung` ist ungetestet.
* N2: Fail-Closed-Reihenfolge (403) ist ungetestet.
* N3: Ungültiges YAML → 200 mit `frontmatter: {}` ist undokumentiert.
* N4: Assertions auf exakte 400 prüfen.
* N5: Cache-Fixture schreibt ins Definitions-Repo (kosmetisch).
* N6: `MAX_KANDIDATEN`-Range 999.
* N7: Doppelte T7-Nummerierung.
* N8: T7 verschärft sich mit neuen Testdateien automatisch (Betriebshinweis).

Zusätzlich: optionales Hardening — DOM-Test für den Fehlertext „Bitte einen Nachtrag eingeben." (Batch B).

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

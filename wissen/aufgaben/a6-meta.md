---
type: Task
title: "A6: Meta-Update meta.py (owner/Status mit Rechteprüfung)"
description: Serverseitige Rechteprüfung für owner- und Status-Änderungen mit atomarem Schreiben in einem Vorgang.
task_status: in Doku
phase: 7 Dokumentation
priority: hoch
assigned_to: coder
user_story: /projekt/user-stories/us-5.md
owner: ai
---

# Ziel

`definitions/app/meta.py` implementiert `setzen(pfad, owner=None, status=None)` und prüft die Schreibrechte-Matrix **serverseitig**: `owner` ∈ {`mensch`, `ai`}; `status` ∈ {`Klarung`, `Geschlossen`} — bei Aufgaben als `task_status: in Klärung`/`abgeschlossen` (Entscheidung R1), bei Punkten ohne `task_status` als `status`-Feld. Alles andere → `RechteFehler` (HTTP 403). Reservierte Dateien und Dateien ohne Frontmatter werden abgewiesen. `owner` und `status` werden in **einem** atomaren Schreibvorgang gesetzt.

# Akzeptanzkriterien

- `owner` akzeptiert ausschließlich `mensch` und `ai`; andere Werte → `RechteFehler`, Datei unverändert.
- `status` akzeptiert ausschließlich `Klarung` und `Geschlossen`.
- Bei Aufgaben wird der Status als `task_status: in Klärung` bzw. `abgeschlossen` geschrieben.
- Bei Wellen/Punkten ohne `task_status` wird das `status`-Feld geschrieben.
- Pipeline-Status (`In Arbeit` u. a.) → `RechteFehler` (HTTP 403), Datei unverändert.
- Reservierte Dateien → `RechteFehler`; fehlendes Frontmatter → `FrontmatterFehler`, keine Änderung.
- `owner` und `status` werden in einem Schreibvorgang gesetzt; der Body bleibt byte-identisch.
- Pfade außerhalb `BUNDLE_ROOT` → `BundlePfadFehler`.

# Testfälle (TDD)

- **T1 owner → ai:** gesetzt, Body-SHA256 identisch.
- **T2 owner → mensch:** gesetzt.
- **T3 owner ungültig:** `RechteFehler`, Hash unverändert.
- **T4 Status Klarung (Aufgabe):** `task_status: in Klärung`.
- **T5 Status Geschlossen (Aufgabe):** `task_status: abgeschlossen`.
- **T6 Status Klarung (Welle):** `status: Klarung`.
- **T7 Pipeline-Status verboten (`In Arbeit`):** `RechteFehler` (403), Datei unverändert.
- **T8 Reservierte Dateien** (`index.md`, `log.md`, `features.md`): jeweils `RechteFehler`.
- **T9 Fehlendes Frontmatter:** `FrontmatterFehler`, keine Änderung.
- **T10 Kombiniert:** beide Felder, ein Schreibvorgang.
- **T11 „zuletzt geändert":** mtime nachher ≥ vorher.
- **T12 Pfad außerhalb:** `BundlePfadFehler`.

# Kontext

- **Abhängigkeiten:** A1 und A2 (`ui_status`/`owner_default` für die Statusinterpretation).
- **Konfliktgruppe G6:** `meta.py` exklusiv; parallel zu A3–A5 und A7.
- **Nachfolger:** A9 (`POST /api/meta`) und A12 (owner-/Status-Bedienung in der Detailansicht) nutzen dieses Modul.
- **Entscheidungen:** R1 (die App darf `task_status` ausschließlich auf `in Klärung` und `abgeschlossen` setzen; alles andere 403 — bestätigt im Entscheidungslog), R3 (`owner` fehlt in Bestandsdateien, keine Migration).
- **Verweise:** Schreibrechte-Tabelle in [Technischer Spec](/projekt/technische-spec.md#schreibrechte-verbindlich), [Entscheidungslog](/entscheidungen/log.md).

# Betroffene Dateien

- `definitions/app/meta.py`
- `definitions/app/tests/test_meta.py`

# Ergebnisse

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-14 — coder (Zwischenstand zum Halt)

- **Ergebnis:** Umsetzung abgeschlossen; Review ohne kritische Befunde; Testhärtung H1/H5/H7. (Quelle: Übergabeprotokoll, Abschnitt „Aufgabenstatus".)
- **Belege:** 30 Tests.
- **Offene Punkte:** formale Testphase (gebündelt vorgesehen) und Doku.

## 2026-11-14 — tester (Gebündelte Testphase)

- **Ergebnis:** **Testphase BESTANDEN** (DoD-Beleg): 30 Tests grün, keine offenen Testbefunde. Gesamtlauf: 549 passed (Start = Ende, kein Zuwachs), 0 rot, 0 geskippt.
- **Offene Punkte:** Review ausstehend.

## 2026-11-14 — reviewer (Review-Runde 1)

- **Ergebnis:** **Freigegeben** — keine kritischen Befunde. 2 Kleinbefunde.
- **Befunde:** [A6-1] klein: H1/H5/H7-Belege im Ergebnisprotokoll je H-Punkt mit Testnamen benennen (Doku-Punkt, wurde in der Doku-Runde aufgegriffen — siehe documenter-Eintrag). [A6-2] klein/optional: T2 zusätzlicher Body-Hash-Test.
- **Offene Punkte:** A6-1 (Doku-Runde), A6-2 (Aufräum-Takt, siehe [features.md](/features.md)).

## 2026-11-14 — documenter (Doku-Punkt A6-1: H1/H5/H7-Belege)

- **Ergebnis:** Testhärtung belegt über die Zusatztests in `definitions/app/tests/test_meta.py` (Commit `9f42200`, „Testhärtung (H1/H5/H7, Mutantenprobe bestanden)"): `test_kombiniert_verboten_kein_schreibvorgang`, `test_ohne_aenderung_kein_schreibvorgang`, `test_owner_wird_nicht_doppelt_geschrieben`, `test_fehlende_datei`, `test_crlf_body_bleibt_bytegleich`, `test_task_status_ziele_passen_zum_status_mapping`.
- **Befund:** Die H-Kennungen H1/H5/H7 selbst sind im Bundle nicht dokumentiert (nur im Commit-Text genannt) — eine 1:1-Zuordnung H-Punkt → Testname ist daraus nicht belegbar.
- **Offene Punkte:** H-Definitionen nachreichen oder Zuordnung bestätigen lassen (Rückfrage an den `reviewer`); A6-2 (T2 Body-Hash) offen.

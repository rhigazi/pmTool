---
type: Task
title: "A6: Meta-Update meta.py (owner/Status mit Rechteprüfung)"
description: Serverseitige Rechteprüfung für owner- und Status-Änderungen mit atomarem Schreiben in einem Vorgang.
task_status: abgeschlossen
phase: 8 Abgeschlossen
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

## 2026-11-16 — documenter (A6-1: H-Definitionen geprüft — nicht rekonstruierbar, Punkt geschlossen)

- **Ergebnis:** A6-1 wird als **bewusste Dokumentationslücke** geschlossen. Die H1/H5/H7-Definitionen sind weder im Bundle noch in der Git-Historie überliefert; es wird **keine** H-Punkt→Test-Zuordnung erfunden. Vollständiges Protokoll: [A41](/aufgaben/a41-a6-1-h-definitionen.md).
- **Belegkette (Recherche):**
  - Die Kennungen stehen **nur** im Sammel-Commit `9f42200` (2026-11-14 06:26), Bullet „test_meta.py Testhaertung (H1/H5/H7, Mutantenprobe bestanden)". Dieser Commit ändert `test_meta.py` **nicht** (`git show --stat`: `liste.js`, `test_liste.py`, `test_setup_verteilung.py`, `a12-detail.md`, `a8-api-lesen.md`, `a9-api-schreiben.md`).
  - `definitions/app/tests/test_meta.py` kam bereits mit `17d5320` (06:14) **vollständig inkl. der 6 Zusatztests** ins Repo; vorher (`aaa400d`) existierte sie nicht. Es gibt **keine Vor-Härtungs-Fassung** und **keinen Härtungs-Diff**. Der Commit-Text `9f42200` fasst damit Arbeit zusammen, die schon in `17d5320` lag — die frühere Angabe „Commit `9f42200`" im Eintrag vom 2026-11-14 ist als **Belegzuordnung unpräzise** (Inhalt korrekt, Commit falsch).
  - Der Reviewer-Eintrag (2026-11-14) nennt nur die Kleinbefunde A6-1/A6-2 — **kein H-Katalog**. `git log -S "H1"`/`-S "H5"`/`-S "H7"` über alle Pfade findet nur **Verweise** auf „H1/H5/H7" (A6, [Planung](/projekt/planung.md), `docs/uebergabeprotokoll.md`, `docs/lueckenliste-a39.md`), keine Definition. Keine gelöschten Review-Dateien, keine weiteren Branches/Stashes/Notes.
  - H = Review-Hinweis (Konvention wie A24-H1–H3, A32-H1–H6); Präzedenz: **A24-H2** ist genauso als „nur im Review-Text außerhalb des Bundles, nicht rekonstruierbar" dokumentiert.
- **Belegt (ohne H-Zuordnung):** Testdatei-Umfang 18 Testfunktionen; T1–T12 parametrisiert 24 Fälle + 6 Zusatzfunktionen = **30 Tests** (deckungsgleich mit dem Tester-Beleg). Zusatzfunktionen: `test_kombiniert_verboten_kein_schreibvorgang`, `test_task_status_ziele_passen_zum_status_mapping`, `test_ohne_aenderung_kein_schreibvorgang`, `test_owner_wird_nicht_doppelt_geschrieben`, `test_fehlende_datei`, `test_crlf_body_bleibt_bytegleich`. Eine 1:1-Zuordnung ist ausgeschlossen: 6 Zusatztests vs. 3 genannte H-Nummern (Nummerierung belegt mindestens H1–H7).
- **Offene Punkte:** keine für A6-1 (abgeschlossen). A6-2 ist mit A33-B6 (`ef68598`) erledigt. Reicht der ursprüngliche Reviewer den H-Katalog nach, kann er hier als Nachtrag ergänzt werden (kein Code).

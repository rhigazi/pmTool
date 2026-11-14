---
type: Task
title: "A3: Nachtrag anfügen nachtrag.py"
description: Nachträge als Blockquote-Marker am Dateiende anfügen, ohne bestehende Inhalte oder Frontmatter zu verändern.
task_status: abgeschlossen
phase: 8 Abgeschlossen
priority: hoch
assigned_to: coder
user_story: /projekt/user-stories/us-2.md
owner: ai
---

# Ziel

`definitions/app/nachtrag.py` implementiert `anfuegen(bundle_rel_pfad, text, datum)`: Der Abschnitt `# Nachträge` wird am Dateiende angelegt bzw. am Ende ergänzt. Format: `> **Nachtrag (Mensch, YYYY-MM-DD):** <Text>`, mehrzeilig zeilenweise als Blockquote. Alles andere bleibt byte-identisch.

# Akzeptanzkriterien

- Bestehender Inhalt bleibt byte-identisch (SHA256-Präfixvergleich).
- Es wird ausschließlich angefügt, nie überschrieben.
- Leere Eingabe → `EingabeFehler`, Datei unverändert.
- Markerformat per Regex geprüft.
- Das Datum ist als Parameter injizierbar.

# Testfälle (TDD)

- **T1 Abschnitt fehlt:** Datei endet mit `# Nachträge` + Markerzeile.
- **T2 Markerformat:** Regex `^> \*\*Nachtrag \(Mensch, \d{4}-\d{2}-\d{2}\):\*\* .+$` trifft zu.
- **T3 Abschnitt vorhanden:** 2 Einträge, alter Eintrag unverändert und oberhalb.
- **T4 Inhaltsschutz:** SHA256-Präfix identisch.
- **T5 Frontmatter unverändert:** identisch inkl. `type`.
- **T6 Leere Eingabe:** `EingabeFehler`, Datei-Hash unverändert.
- **T7 Mehrzeilig:** zwei `>`-Zeilen, kein Formatbruch.
- **T8 Pfad außerhalb:** `BundlePfadFehler`, keine Datei.
- **T9 Reserviertes Ziel:** `anfuegen("log.md", ...)` (auch `index.md`, `features.md`) → abgewiesen (Exception), Datei unverändert — reservierte Dateien sind für die App generell gesperrt (Guard in `okf_bundle`).

# Kontext

- **Abhängigkeiten:** A1 (`okf_bundle.py` für Pfadschutz und atomares Schreiben).
- **Konfliktgruppe G3:** `nachtrag.py` exklusiv; parallel zu A4–A7 möglich.
- **Nachfolger:** A9 (`POST /api/nachtrag`) und A12 (UI-Formular) nutzen dieses Modul.
- **Entscheidungen:** R13 (Datum = Serverzeit UTC, Format `YYYY-MM-DD`, als Parameter injizierbar), R4 (Reserve-Dateien sind nur anfügend bearbeitbar).
- **Verweise:** Nachtragsformat in [Technischer Spec](/projekt/technische-spec.md), Schreibrechte-Tabelle ebenda.

# Betroffene Dateien

- `definitions/app/nachtrag.py`
- `definitions/app/tests/test_nachtrag.py`

# Ergebnisse

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-14 — coder (Zwischenstand zum Halt, inkl. Sammel-Nachbesserung)

- **Ergebnis:** Umsetzung abgeschlossen (19 Tests). Sammel-Nachbesserung „zentrale Exceptions": T9-Test parametrisiert über alle reservierten Dateien (`index.md`/`log.md`/`features.md` → jeweils abgewiesen), `EingabeFehler` zentral aus `okf_bundle` (lokale Definition entfernt). (Quelle: Übergabeprotokoll, Abschnitte „Aufgabenstatus" und „Session-Rückmeldungen zum Halt".)
- **Belege:** 102 Tests im Sammel-Lauf; Gesamtsuite 549 grün (Endstand zum Halt).
- **Offene Punkte:** Review, Testphase, Doku.

## 2026-11-14 — tester (Gebündelte Testphase)

- **Ergebnis:** **Testphase BESTANDEN** (DoD-Beleg): 21 Tests grün, keine offenen Testbefunde. Gesamtlauf: 549 passed (Start = Ende, kein Zuwachs), 0 rot, 0 geskippt.
- **Offene Punkte:** Review ausstehend.

## 2026-11-14 — reviewer (Review-Runde 2)

- **Ergebnis:** **Freigegeben** — keine kritischen Befunde. 2 Kleinbefunde als offene Punkte.
- **Befunde:** [A3-1] klein: Reserviert-Guard läuft erst beim Schreiben — bei nicht existierender reservierter Datei entsteht `FileNotFoundError` statt `ReservierteDateiFehler` (API 500 statt 403). [A3-2] klein: Testlücke — Zweig „`# Nachträge` vor weiteren Überschriften" ist ungetestet.
- **Offene Punkte:** A3-1/A3-2 (Aufräum-Takt, siehe [features.md](/features.md)); Doku.

## 2026-11-14 — coder (Nebenbei-Fix [A3-1])

- **Ergebnis:** [A3-1] behoben: Bei einer reservierten, aber nicht existierenden Datei greift der Guard jetzt vor dem Dateizugriff → **403** statt vorher 500 (`FileNotFoundError`).
- **Belege:** Teil des Sicherheits-Blocks (29 neue Tests, Gesamtsuite 676 grün).
- **Offene Punkte:** [A3-2] Testlücke (Aufräum-Takt); Doku/Abschluss.

## 2026-11-14 — coder (Kleinbefunde-Takt, Batch A)

- **Ergebnis:** [A3-2] geschlossen: Testfall für einen `# Nachträge`-Abschnitt in der Dateimitte ergänzt (Nachtrag wird korrekt am Abschnittsende ergänzt, Struktur unverändert).
- **Belege:** Kleinbefunde-Takt Batch A (+12 Tests); Gesamtsuite 761 grün.
- **Offene Punkte:** Doku/Abschluss.

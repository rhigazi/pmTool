---
type: Task
title: "A3: Nachtrag anfügen nachtrag.py"
description: Nachträge als Blockquote-Marker am Dateiende anfügen, ohne bestehende Inhalte oder Frontmatter zu verändern.
task_status: offen
phase: 2 Planung
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
- **T9 Reserve `log.md`:** nur anfügend erlaubt, Präfix-Hash identisch.

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

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

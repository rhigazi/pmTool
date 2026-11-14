---
type: Task
title: "A4: Aufgabe anlegen neu_aufgabe.py"
description: Neue Aufgaben-Datei im Phasen-Format inklusive Frontmatter, Body-Abschnitten, Slug-Normalisierung und Kollisionsbehandlung anlegen.
task_status: offen
phase: 2 Planung
priority: hoch
assigned_to: coder
user_story: /projekt/user-stories/us-3.md
owner: ai
---

# Ziel

`definitions/app/neu_aufgabe.py` implementiert `anlegen({titel, ziel, akzeptanz[], prioritaet, welle?, user_story?})` → `aufgaben/<slug>.md` im Phasen-Format inkl. `owner: ai`, `task_status: offen`, `phase: 2 Planung`, `assigned_to: coder`. Slug-Normalisierung: Umlaute → ASCII, Sonderzeichen → `-`, maximal 60 Zeichen; Kollisionssuffix `-2`, `-3`.

# Akzeptanzkriterien

- Frontmatter exakt nach Phasenmodell, ergänzt um `owner: ai`.
- Body enthält `# Ziel`, `# Akzeptanzkriterien`, `# Testfälle (TDD)`, `# Kontext`, `# Betroffene Dateien`, `# Ergebnisse`.
- Ungültige Eingaben → `EingabeFehler` ohne Datei.
- Bestehende Dateien werden nie überschrieben.
- OKF-konform: Datei beginnt mit `---\n` und endet mit genau einem `\n`.
- Die neue Aufgabe ist sofort als `Offen`/`ai` sichtbar (Integrationstest mit A2/A8).

# Testfälle (TDD)

- **T1 Happy Path:** Aufruf mit gültigen Feldern → Datei existiert, Rückgabe = relativer Pfad.
- **T2 Frontmatter:** `type: Task`, `task_status: offen`, `phase: 2 Planung`, `priority`, `assigned_to: coder`, `owner: ai`.
- **T3 user_story-Verweis:** Feld gesetzt.
- **T4 Body-Abschnitte:** alle 6 Überschriften vorhanden.
- **T5 Akzeptanzliste:** 3 Einträge als `- `-Zeilen.
- **T6 Slug:** `Übersicht: Status & owner!` → `uebersicht-status-owner.md`.
- **T7 Kollision:** zweite Datei `…-2.md`, erste unverändert.
- **T8 Ungültige Eingaben (je einzeln):** `EingabeFehler`, Dateianzahl unverändert.
- **T9 Pfad-Traversal im Titel:** Datei bleibt in `aufgaben/`, Slug bereinigt.
- **T10 Zeilenende:** letztes Byte ist `\n`.

# Kontext

- **Abhängigkeiten:** A1; **parallel zu A5/A6/A7** möglich.
- **Konfliktgruppe G4:** `neu_aufgabe.py` exklusiv.
- **Nachfolger:** A9 (`POST /api/task`) und A13 (Formular) nutzen dieses Modul.
- **Entscheidungen:** R2 (ASCII-Slug aus Titel, max. 60 Zeichen, Kollision `-2`/`-3`), R10 (`feature:`-Feld im MVP optional; Feature-Dateien erst bei Feature-Beginn).
- **Verweise:** Format einer Aufgaben-Datei in [Phasenmodell](/projekt/phasen.md#format-einer-aufgaben-datei), Struktur neuer Punkte in [Technischer Spec](/projekt/technische-spec.md).

# Betroffene Dateien

- `definitions/app/neu_aufgabe.py`
- `definitions/app/tests/test_neu_aufgabe.py`

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

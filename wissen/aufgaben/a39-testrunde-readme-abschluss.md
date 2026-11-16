---
type: Task
title: "A39: Gemeinsame Test- und Abstimmungsrunde + README-Abschluss"
description: Nach Abschluss aller ausstehenden Features ausgiebig testen (mit der Projektleitung),
  feststellen was für sauberes Zusammenarbeiten noch fehlt — danach die README im Repo final aktualisieren.
task_status: offen
phase: 2 Planung
priority: hoch
assigned_to: coder
owner: mensch
---

# Ziel

Vorgabe der Projektleitung (2026-11-15): „Wenn wir alle ausstehenden Features fertig haben, machen wir erst mal eine Pause und testen ausgiebig, um festzustellen was noch fehlt um gemeinsam sauber zu arbeiten. Wenn du alles fertig hast, aktualisiere die Dokumentation in der Readme im Repo."

Damit ist A39 der **Abschluss-Meilenstein** der aktuellen Feature-Strecke:
1. **Gemeinsame Test- und Abstimmungsrunde** mit der Projektleitung — ausgiebiges Durchspielen des Gesamt-Workflows (App: Listen/Filter/Suche/Detail/Nachträge/Anlegen/Wellen-Zuordnung/Freigabe/Unter-Aufgaben/Arbeitsstatus/Neues-Projekt-Flow; CLI: PM-Workflow, Push-Regeln, Freigabe-Gate) und Erhebung: **Was fehlt für sauberes Zusammenarbeiten?**
2. **README-Abschluss:** Die `README.md` im Repo wird auf den finalen Stand aktualisiert (Nutzung, Befehle, Abläufe, neuer Workflow inkl. Freigabe-Gate/Neues-Projekt-Flow, Teststand).

# Akzeptanzkriterien (vorläufig, PM schärft in der Runde)

- **AK-1:** Alle ausstehenden Features sind abgeschlossen, bevor die Runde startet (A28–A38 inkl. A33-Batches; A22/A21 nach Priorität der Projektleitung).
- **AK-2:** Die Testrunde läuft mit der Projektleitung gemeinsam (App + CLI); Ergebnis ist eine dokumentierte Lückenliste „was fehlt für sauberes Zusammenarbeiten" (jeder Punkt: Beobachtung, Auswirkung, Vorschlag).
- **AK-3:** Aus der Lückenliste werden — nach Priorisierung durch die Projektleitung — Folgeaufgaben abgeleitet (ID + Titel + Sofort-Push-Regel).
- **AK-4:** `README.md` spiegelt den Abschlussstand (Installation/Start, Neues-Projekt-Flow, Arbeitsweise, Freigabe-Gate, Teststand mit festem Zählumfang); Test-Befehle lauffähig.
- **AK-5:** Danach bewusste **Pause** — kein neuer Feature-Takt ohne Weisung der Projektleitung.

# Testfälle (TDD)

Keine Code-Tests — Prüfschritte des `documenter`/PM: README-Befehle im frischen Klon durchspielen (Copy-Paste-Test), Lückenliste im Entscheidungs-/Projekt-Log.

# Kontext

- **Vorgabe der Projektleitung 2026-11-15** (Menschen-Kanal) — als Entscheidung im Entscheidungslog festgehalten.
- Startbedingung: Feature-Strecke A28–A38 + A33-B1–B9 abgeschlossen (Review/Testphase je Aufgabe).
- `owner: mensch` — die Projektleitung führt die Testrunde gemeinsam mit dem PM.

# Betroffene Dateien

- `README.md` (final), `docs/uebergabeprotokoll.md`, `wissen/entscheidungen/log.md`, `wissen/log.md`, `wissen/features.md`.

# Ergebnisse
## 2026-11-16 — PM/tester/documenter: Technische Testrunde + README-Abschluss erledigt

- **Gemeinsame Test-/Abstimmungsrunde (technische Seite) abgeschlossen:** Sammellauf-Welle 2026-11-16 bestanden (App 1690/1690, Root 1789/1789, `verify.sh` Exit 0, Verteilungs-Probe sauber, UI S1–S5 + Kurzchecks ohne Konsolenfehler). **Lückenliste** `docs/lueckenliste-a39.md` dokumentiert alle Befunde (V1 Verify/Teilgerüst → per A40 behoben, V2 Moli-Version, V3 Szenario-Ausführung, A11y-Vermerk V1 der Endrunde) inkl. Folgeaufgaben-Kandidaten und Prozess-Lektionen (W6 Commit-Schnitt, Anrainer-Zahlen mit Datei-Satz).
- **README final aktualisiert:** Abschlussstand A1–A38 + A40–A42, Funktionen (inkl. A35/A36/A38/A21), Test-Endzahlen 1690/1789, A40-Teilgerüst-Hinweis, Desktop-Abschnitt.
- **Offen (diese Aufgabe bleibt aktiv):** (1) **Test-Befunde der Projektleitung** — keine eingegangen bis 2026-11-16 Abend (Klon `/content/pmTool-test` nicht vorhanden, Telegram-Rückfrage offen); (2) **Abnahme-Restvermerk A21:** Fenster-Smoke des Desktop-Modus auf einer Maschine mit Display; (3) K-Klammern der Lückenliste (Abschnitt 3). Nach Eingang der Befunde: Folgeaufgaben ableiten (ID + Titel + Sofort-Push) und A39 schließen.


Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

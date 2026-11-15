---
type: Playbook
title: Phasenmodell & Zuständigkeiten
description: Definiert die Pipeline jeder Aufgabe, Rollen, TDD-Regeln, DoD, Nachbesserungspfad, Abnahme und die Formate von User Stories und Aufgaben-Dateien.
tags: [prozess, phasen, aufgaben, tdd]
generated: { by: opencode/mimo-v2.6-pro, at: 2026-11-13T07:04:49Z }
---

# Rollen

| Rolle | Wer | Verantwortung |
|---|---|---|
| Projektmanager | Hauptagent (OpenCode) | Konzeption, Klärungsfragen, Erzeugt User Stories & Technische Spec, Projektplan & Steuerung, Parallelisierung, Pflege der Wissensdatenbank, Commits |
| Planer | Subagent `planner` | Granulare, TDD-basierte Aufgabenplanung aus User Stories und Technischer Spec |
| Documenter | Subagent `documenter` | Legt Aufgaben im OKF an; dokumentiert die Ergebnisse von `coder`, `reviewer` und `tester` je Aufgabe; Dokumentation; unterstützt die Statuspflege |
| Coder | Subagent `coder` | Umsetzung von Aufgaben nach Red-Green-Refactor |
| Reviewer | Subagent `reviewer` | Prüft Anforderung, Qualität und Umsetzung (rein lesend) |
| Tester | Subagent `tester` | TDD-Testfälle und Szenario-Tests über den Moli-Browser |
| Projektleitung | human | Fachliche Abnahme am Ende von Features und Meilensteinen |

# Pipeline

| Phase | Verantwortlich | Ergebnis / Voraussetzung für den Wechsel |
|---|---|---|
| 1. Konzeption | Projektmanager | Anforderungen geklärt; User Stories und Technische Spec erstellt |
| 2. Planung (TDD) | planner | Granulare Aufgaben mit Testfällen, Akzeptanzkriterien, Priorität, betroffenen Dateien |
| 3. Aufgabenanlage | documenter | Aufgaben-Dateien in [/aufgaben/](/aufgaben/index.md) angelegt |
| 3b. Freigabe | Projektleitung (human) | Aufgabe geklärt und geplant (`geplant`); `freigabe: true` gesetzt (Menschen-Recht, `POST /api/freigabe`) — Voraussetzung für die Beauftragung |
| 4. Umsetzung | coder | Red-Green-Refactor abgeschlossen |
| 5. Review | reviewer | Keine kritischen Befunde (Anforderung, Qualität, Umsetzung) |
| 6. Test | tester | TDD-Testfälle und Moli-Szenarien grün |
| 7. Dokumentation | documenter | Doku aktuell; alle Ergebnisse der Aufgabe im OKF dokumentiert |
| 8. Abgeschlossen | Projektmanager | DoD erfüllt; [/features.md](/features.md) und [Projekt-Log](/log.md) aktualisiert; Stand committed |
| 9. Abnahme | Projektleitung (human) | Abgenommen oder Änderungswünsche → neue Aufgaben |

**3b. Freigabe (Projektleitung, human):** Nach Klärung und Planung ist `geplant` der **Wartestatus**: Die Aufgabe wird nicht beauftragt, solange die Projektleitung nicht `freigabe: true` gesetzt hat. Die Freigabe ist ein **Menschen-Recht** — sie wird ausschließlich über die App (`POST /api/freigabe`) gesetzt; der KI-Weg (`meta.setzen`, `POST /api/meta`) liefert 403. Fehlt das Feld oder ist es nicht exakt `true`, gilt die Aufgabe als nicht freigegeben (fail-closed). Ein Entzug sperrt weitere Beauftragungen, bricht aber keine laufende Umsetzung ab. Der Ablauf ist verbindlich: wahrnehmen → annehmen (Kennung/Titel/Datei) → sofort pushen → planen → `geplant` → auf `freigabe: true` warten → umsetzen. Die Abnahme der fertigen Arbeit findet am Ende statt (siehe „Abnahme & Meilensteine"); der Coder meldet eine abgeschlossene Aufgabe an den Reviewer, dieser an den Tester.

# Projektplan & Parallelisierung

Der Projektmanager hält den Projektplan und weiß jederzeit, wer was macht und wo wir stehen. Grundlage: `task_status` und `phase` aller Aufgaben-Dateien sowie die `# Ergebnisse`-Einträge. Kernaufgabe ist es, so viel wie möglich parallel laufen zu lassen, damit das Projekt schnell abgeschlossen ist.

* Unabhängige Aufgaben werden parallel an Subagenten vergeben.
* Phasen laufen über Aufgaben hinweg überlappt: während `coder` an Aufgabe B arbeitet, prüft `reviewer` Aufgabe A und `tester` Aufgabe C.
* Der `documenter` protokolliert Ergebnisse ebenfalls parallel, sobald sie vorliegen.
* Nur echte Abhängigkeiten (Inhalts- oder Schnittstellenkonflikte) serialisieren den Ablauf — sie müssen in der Planung benannt sein.
* Die Planung nennt je Aufgabe die betroffenen Dateien; Aufgaben mit sich überschneidenden betroffenen Dateien laufen **nicht** parallel.
* Subagenten laufen in eigenen Hintergrund-Sessions; mehrere können gleichzeitig aktiv sein.

# Nachbesserung & Fehlerpfad

Die Pipeline hat einen definierten Rücklauf — sie läuft nicht nur vorwärts:

* Kritische Review-Befunde oder fehlgeschlagene Tests → Rücklauf an `coder`; `task_status` zurück auf `in Umsetzung`.
* Der Projektmanager entscheidet auf Basis der Ergebnis-Einträge: nachbessern, Aufgabe neu planen/teilen oder verwerfen.
* Jede Nachbesserungsrunde wird im `# Ergebnisse`-Abschnitt protokolliert (Runde, Anlass, Ergebnis).
* Nach drei erfolglosen Nachbesserungsrunden geht die Aufgabe zurück an den `planner` (Neu- oder Umplanung), statt weiter zu drehen.

# Definition of Done (DoD)

Eine Aufgabe gilt als abgeschlossen, wenn alle Punkte erfüllt sind:

* Alle Akzeptanzkriterien sind erfüllt und im Ergebnisprotokoll nachgewiesen.
* Die TDD-Testfälle sind grün (Red-Green-Refactor abgeschlossen).
* Das Review ist ohne kritische Befunde abgeschlossen.
* Bei UI-Aufgaben: die Moli-Szenarien sind bestanden.
* Alle Ergebnisse sind im OKF dokumentiert (`# Ergebnisse` der Aufgaben-Datei).
* [/features.md](/features.md) und [Projekt-Log](/log.md) sind aktualisiert.
* Der Stand ist in Git committed.

# Abnahme & Meilensteine

* Nach abgeschlossenen Features (DoD erfüllt) weist der Projektmanager sie der Projektleitung zur Abnahme vor — mit Kurzbericht: was umgesetzt wurde, Stand und Testnachweis.
* Meilensteine fassen mehrere zusammengehörige Features zusammen; nach jedem Meilenstein erfolgt eine Abnahme.
* Die Abnahme endet mit „abgenommen" oder mit Änderungswünschen; Änderungswünsche werden als neue Aufgaben in den Projektplan aufgenommen.
* Die Abnahme ersetzt nicht die Klärung: Offenheiten werden weiterhin vor der Umsetzung geklärt.

# User Stories & Technische Spec

Der Projektmanager erzeugt in Phase 1 aus den Anforderungen:

* **User Stories** unter [/projekt/user-stories/](/projekt/user-stories/index.md) — je Story eine Datei.
* **Technische Spec** unter [/projekt/technische-spec.md](/projekt/technische-spec.md) — Architektur, Technologien, Datenmodell, Schnittstellen, Build-/Start-/Test-Befehle.

Der `planner` plant ausschließlich aus User Stories und Technischer Spec. Jede Aufgabe verweist über `user_story` auf ihre Story.

## Format einer User Story

```markdown
---
type: User Story
title: US-x: <Kurztitel>
description: <Ein Satz>
story_status: offen
priority: hoch
---

# Story
Als <Rolle> möchte ich <Ziel>, damit <Nutzen>.

# Akzeptanzkriterien
- <Kriterium 1>
- <Kriterium 2>

# Technische Hinweise
<Verweise in die Technische Spec>
```

# TDD-Regeln

* **Test-first**: Testfälle und Akzeptanzkriterien entstehen in der Planung, vor der Umsetzung.
* **Red-Green-Refactor**: Test schreiben → fehlschlagen lassen → Minimum zum Grün implementieren → refactorisieren.
* Jeder Testfall ist beobachtbar und überprüfbar — erwartetes Ergebnis explizit benannt.
* UI-relevante Aufgaben: Die Szenarien werden vom `tester` mit dem Moli-Browser (`/root/.local/bin/moli`, `moli fetch` / `moli serve`) gegen die laufende Anwendung durchgespielt, um die gesamte Funktionalität abzudecken.

# Statuswerte einer Aufgabe

`offen` → `in Klärung` → `in Planung` → `geplant` → `in Umsetzung` → `im Review` → `im Test` → `in Doku` → `zur Abnahme` → `abgeschlossen`

Pausierung: `pausiert` (mit Grund in der Aufgaben-Datei).

# Regeln

* Jeder Phasen- und Statuswechsel wird in der Aufgaben-Datei vermerkt (Frontmatter-Felder `task_status` und `phase`).
* Status und Phase ändern ausschließlich der Projektmanager und `documenter`.
* Jede Umsetzung wird in [/features.md](/features.md) und im [Projekt-Log](/log.md) nachvollziehbar gemacht.
* Jede Entscheidung wird im [Entscheidungslog](/entscheidungen/log.md) festgehalten.
* Nach abgeschlossenen Aufgaben und Meilensteinen committe der Projektmanager den Stand (Git).

# Format einer Aufgaben-Datei

Jede Aufgabe liegt als `wissen/aufgaben/<id>.md` vor und ist so dokumentiert, dass ein `coder` sie eigenständig abarbeiten kann:

```markdown
---
type: Task
title: <Kurztitel>
description: <Ein Satz>
task_status: offen
phase: 2 Planung
priority: hoch
assigned_to: coder
user_story: /projekt/user-stories/us-<x>.md
feature: /features/<feature>.md
aktuell: "<Rolle>: <Was passiert gerade>"
freigabe: false
---

# Ziel
<WAS erreicht werden soll.>

# Akzeptanzkriterien
- <messbare Bedingung 1>
- <messbare Bedingung 2>

# Testfälle (TDD)
- <Testfall: Ausführung, erwartetes Ergebnis>
- <UI-Szenario für den tester: Schritte, erwartetes Ergebnis>

# Kontext
<Relevanter Hintergrund, Verweise ins Bundle, betroffene Bereiche.>

# Betroffene Dateien
<Welche Dateien voraussichtlich geändert werden — Grundlage der Konfliktprüfung bei Parallelität.>

# Ergebnisse
<Vom documenter gepflegt: je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte.>
```

Das boolesche Feld `freigabe` im Frontmatter dokumentiert die Freigabe der Projektleitung: nur ein exaktes `true` gilt als freigegeben (fail-closed, fehlt = nicht freigegeben). Neue Aufgaben werden mit `freigabe: false` angelegt; gesetzt/entzogen wird sie ausschließlich über den Menschen-Kanal der App.

Das Feld `aktuell` im Frontmatter ist der **Live-Arbeitsstand** im Format `<Rolle>: <Was passiert gerade>` (z. B. `coder: Umsetzung Paket 2`): Live-Feld, nur Anzeige, bei Abschluss leeren — die App leitet daraus den Arbeitsstatus ab (Rolle + Text) und schreibt es nie. Rollen (case-insensitiv, mit Aliassen): `planner`/`planer` (Planer), `coder` (Coder), `tester` (Tester), `reviewer`/`review` (Review), `documenter`/`doku` (Documenter), `pm`/`projektmanager`/`projektleitung` (PM). Unbekannte Rollen werden unverändert angezeigt.

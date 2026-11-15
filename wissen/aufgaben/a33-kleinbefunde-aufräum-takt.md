---
type: Task
title: "A33: Kleinbefunde-/Aufräum-Takt (gebündelt)"
description: Gebündelte Behebung der offenen Kleinbefunde aus Reviews und Post-MVP (A24-K1–K3,
  A23-Fixture, A4-1/2, A5-B3/B4, A6-1/2, A7-2, A9-K3/K4, A13-3, A14-5/6/7/9, A16-1/4, N5/N8,
  A20-Pin-Pflege) in eigenen Batches mit je eigenem Commit.
task_status: in Planung
phase: 2 Planung
priority: mittel
assigned_to: coder
owner: ai
aktuell: "planner: Batches planen"
---

# Ziel

Über die Reviews und Post-MVP-Takte haben sich viele kleine, unkritische Befunde gesammelt (Übergabeprotokoll „Offene Punkte", Review-Nachläufe A23/A24/A25). Sie werden **gebündelt** in einem Aufräum-Takt behoben — je Batch ein eigener Commit, Tests vorher rot/nachher grün, keine Verhaltensänderungen über die Befunde hinaus.

# Akzeptanzkriterien (vorläufig, der `planner` schärft sie und gruppiert die Batches)

1. Jeder Befund wird genau einmal behoben, mit Testbeleg (vorher/nachher) und Verweis auf seine Herkunft (Aufgabe/Review).
2. Batches sind dateiweise getrennt, sodass je Batch ein eigener Commit entsteht und ein Fehlschlag den Batch isoliert zurückrollt.
3. Bestehende Tests bleiben grün (nur präzisierende Erweiterungen); keine neuen Abhängigkeiten.
4. Der Befund-Katalog wird nach Abschluss in `features.md`/Übergabeprotokoll abgehakt.

# Befund-Katalog (Ausgangsbestand)

- **A24-Review (2026-11-15):** K1 zweite Backup-Barriere ohne Test, K2 baumelnder Symlink auf automatischem Backup-Namen, K3 Ausweichen `-2`/`-3` nicht deterministisch getestet; H1 verify-Meldungstest prüft Wortlaut statt Eigenschaft, H2 Testlücken a–e einzeln dokumentieren, H3 Rollback-Meldung ohne Wiederherstellungsschritt.
- **A23:** H1-Nachtrag: Fixture `test_bundle` umbenennen (kosmetisch).
- **Post-MVP-Liste (Übergabeprotokoll):** A12-1 Mapping-Spiegel, A12-Schreib-UI-Grenze (`schreibgeschuetzt`-Signal — prüfen ob aufwändig → ggf. eigene Aufgabe), A13-3 Linktext-Kosmetik, A4-1 `#`-Maskierung in `ziel`, A4-2 `welle`-Feld in Spec/phasen.md, A5-B3 `description`-Feld bei Wellen, A5-B4 Slug-Logik-Duplikat, A6-1 H-Belege je H-Punkt, A6-2 T2 Body-Hash optional, A7-2 Startfehler absoluter Pfad, A9-K3 403-Notiz/Spec-Abgleich, A9-K4 TOCTOU (R8, dokumentiert — vermutlich nur Vermerk), A14-5 `istDatei`/Meldungen nach `api.js`, A14-6 DOM-Harness-Fork `MINI_DOM` konsolidieren, A14-7 Request-Sequenz-Guard, A14-9 Anker je Log-Eintrag, A16-1 R11-Zitat/Ausweichport, A16-4 Env-Weitergabe, N5 Cache-Fixture ins Definitions-Repo, N8 T7-Betriebshinweis, A20-Pin-Pflege (Hinweis).

# Testfälle (TDD)

Noch keine Einträge — der `planner` ergänzt die Testfälle (je Befund: mindestens ein prüfender Test oder dokumentierte Prüfung).

# Kontext

- Sammel-Aufgabe angelegt vom PM 2026-11-15 (Aufgaben-Regel: ID + Titel im Moment der Annahme).
- Reihenfolge: **nach** A30/A31/A32 (parallel zu A28/A29 möglich, sobald die UI-Strecke frei ist), einzeln priorisierte Batches; größere Befunde (z. B. A12-1, A14-6) werden ggf. als eigene Aufgabe ausgegliedert.

# Betroffene Dateien

Noch keine Einträge — die Planung ergänzt die betroffenen Dateien.

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

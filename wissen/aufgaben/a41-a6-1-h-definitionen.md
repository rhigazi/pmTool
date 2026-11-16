---
type: Task
title: "A41: A6-1 — fehlende H-Definitionen klären (rekonstruieren oder abschließen)"
description: Die im Bundle fehlenden H-Definitionen (H1/H5/H7) zum Doku-Eintrag 2026-11-14 werden belegt rekonstruiert oder abschließend als nicht rekonstruierbar dokumentiert — der offene Punkt A6-1 wird geschlossen.
freigabe: true
task_status: offen
phase: 2 Planung
priority: niedrig
assigned_to: coder
owner: ai
aktuell: ""
---

# Ziel

Offener Punkt A6-1 (K-Sammlung/„H-Definitionen fehlen im Bundle"): Der Doku-Eintrag 2026-11-14 verweist auf H-Definitionen (H1/H5/H7 u. a.) zu A6, die im Bundle nicht auffindbar sind — eine 1:1-Zuordnung ist nicht belegbar. Aufgabe: **belegt** rekonstruieren (wo Quellen existieren) **oder** abschließend als „nicht rekonstruierbar" dokumentieren und den Punkt schließen. **Keine erfundenen Fakten.**

# Akzeptanzkriterien

- **AK-1:** Recherche-Protokoll: alle durchsuchten Quellen (git history inkl. `git log -S`, `wissen/log.md`, `wissen/entscheidungen/log.md`, `wissen/aufgaben/a6-meta.md`, `wissen/projekt/planung.md`, Ergebnisprotokolle) mit Ergebnis je Quelle.
- **AK-2:** Bei Rekonstruktion: H-Definitionen werden an der fachlich richtigen Stelle ergänzt (A6-Ergebnis und/oder `planung.md`) — mit Herkunftsbeleg (Commit/Zitat).
- **AK-3:** Ohne rekonstruierbare Quelle: expliziter Abschluss-Vermerk „nicht rekonstruierbar" + Begründung an derselben Stelle; der Punkt gilt dann als **abgeschlossen** (bewusste Dokumentationslücke, nicht als „offen" weitergeführt).
- **AK-4:** `wissen/features.md` und A33-Klammer werden aktualisiert (A6-1 nicht mehr „offen"); A41-Ergebnisprotokoll führt die Belege.

# Testfälle (TDD)

Keine (reine Doku/Recherche) — Prüfschritt: PM/Review liest das Protokoll gegen die genannten Quellen.

# Kontext

- Herkunft: `docs/lueckenliste-a39.md` (Abschnitt 3), Freigabe der Projektleitung 2026-11-16 („alles frei").
- B9-Doku-Sammelbatch (2026-11-15) hatte A6-1 als Vermerk in `planung.md` stehen gelassen; die Definitionen H1/H5/H7 sind nirgends belegt.

# Betroffene Dateien

- `wissen/aufgaben/a6-meta.md` (Ergebnis-/Kontext-Ergänzung)
- `wissen/projekt/planung.md` (ggf. Vermerk-Korrektur)
- `wissen/features.md` (A6-1-Status)
- `wissen/aufgaben/a33-kleinbefunde-aufräum-takt.md` (Klammer-Vermerk A6-1)

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle, Ergebnis, Befunde und Belege.

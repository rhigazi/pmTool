---
type: Task
title: "A41: A6-1 — fehlende H-Definitionen klären (rekonstruieren oder abschließen)"
description: Die im Bundle fehlenden H-Definitionen (H1/H5/H7) zum Doku-Eintrag 2026-11-14 werden belegt rekonstruiert oder abschließend als nicht rekonstruierbar dokumentiert — der offene Punkt A6-1 wird geschlossen.
freigabe: true
task_status: abgeschlossen
phase: 8 Abgeschlossen
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

Je Eintrag Datum, Rolle, Ergebnis, Befunde, Belege. Neueste Einträge unten.

## 2026-11-16 — documenter (Recherche + Abschluss A6-1)

- **Ergebnis:** Die fehlenden H-Definitionen (H1/H5/H7) sind **nicht rekonstruierbar**. A6-1 wird als **bewusste Dokumentationslücke** geschlossen (AK-3); es wird **keine** H-Punkt→Test-Zuordnung erfunden.
- **Auftrag:** AK-1 (Recherche-Protokoll), AK-2/AK-3 (rekonstruieren oder abschließen), AK-4 (features.md, A33-Klammer, dieses Protokoll).

### AK-1 — Recherche-Protokoll (Quelle → Ergebnis)

| Quelle | Prüfung | Ergebnis |
|---|---|---|
| `git log --oneline` (117 Commits, 2026-11-14 bis 2026-11-16) | A6-Strecke und Doku-Commits identifiziert | A6: `aaa400d` (Anlage), `17d5320` (Testdatei), `9f42200` (Commit-Text H1/H5/H7), `d241295` (Übergabeprotokoll), `8f88052`/`ee7049f`/`eb9ae2d` (A6-Ergebnis/Doku), `b19ba7b`/`c7e1c5c` (A33-Doku). **Keine H-Definition.** |
| `git log -S "H5"` bzw. `-S "H7"`/`-S "H1"` (alle Pfade) | Wo die Kennungen in Dateiinhalten eingeführt/geändert wurden | Treffer ausschließlich in **Verweis**-Dokumenten (`a6-meta.md`, `planung.md`, `docs/uebergabeprotokoll.md`-Historie, `docs/lueckenliste-a39.md`, `features.md`). Keine Datei führt einen H-Katalog (H1…H7 mit Bedeutung) ein. |
| `git log -1 --format=full 9f42200` + `git show --stat 9f42200` | Der im Bundle zitierte „Härtungs-Commit" | Kennungen stehen **nur** im Commit-Text (Bullet „test_meta.py Testhaertung (H1/H5/H7, Mutantenprobe bestanden)"). Der Commit ändert **6 andere Dateien** (`liste.js`, `test_liste.py`, `test_setup_verteilung.py`, `a12-detail.md`, `a8-api-lesen.md`, `a9-api-schreiben.md`) — **`test_meta.py` ist nicht dabei**. |
| `git log --diff-filter=A -- definitions/app/tests/test_meta.py` | Erste Fassung der Testdatei | Erstmals in `17d5320` (2026-11-14 06:14), also **12 Minuten vor** `9f42200`; in `aaa400d` existiert sie nicht. Die Datei kam **vollständig inkl. der 6 Zusatztests** ins Repo — es gibt **keine Vor-Härtungs-Fassung** und **keinen Härtungs-Diff**. |
| `wissen/aufgaben/a6-meta.md` (komplette Dateihistorie, 7 Commits) | Ergebnisprotokoll A6 | Coder-Eintrag (`8f88052`) nennt „Testhärtung H1/H5/H7" ohne Definition; Reviewer-Eintrag (`ee7049f`) nennt nur die Kleinbefunde **A6-1/A6-2**, keinen H-Katalog; später nur Status-/Abschluss-Änderungen. |
| `wissen/log.md` | A6-Erwähnungen | Nur Status/Testzahlen (u. a. „A6 30", Review „A6 (2 Klein)") — **keine** H-Definitionen. |
| `wissen/entscheidungen/log.md` | Einträge zu A6, Testhärtung, H-Punkten | **Kein** Eintrag zu A6-H/H-Definitionen; A6 erscheint nur in Schreibrechte-/Reserviert-Entscheidungen (R1/R3). |
| `wissen/projekt/planung.md` | A6-Abschnitt + Vermerk | Testtabelle T1–T12 und der A6-1-Vermerk (Zeile 185) — **keine** H-Definitionen. |
| `docs/uebergabeprotokoll.md` (inkl. Historie) | Abschnitt „Aufgabenstatus" (die im A6-Eintrag genannte Quelle) | Dort steht nur: „A6 … 30 Tests, **Testhärtung H1/H5/H7**" (mit `d241295` eingeführt). Keine Definition. |
| Ergebnisprotokolle mit H-Verweisen (A24-H1–H3, A32-H1–H6, A16-1) | Vergleich der H-Namenskonvention | H = **Review-Hinweis**, Definitionen stehen üblicherweise im Review-Text (A24/A32) bzw. im A33-Katalog. Präzedenz: **A24-H2** ist ebenfalls „nur im Review-Text außerhalb des Bundles, nicht rekonstruierbar" dokumentiert ([A24](/aufgaben/a24-neues-projekt.md), 2026-11-15) — gleiche Sachlage, gleiche Behandlung. |
| `definitions/app/tests/test_meta.py` (Stand `17d5320`) | Rückverfolgung H → Testname | Keine H-Kennungen in Namen, Docstrings oder Kommentaren; Docstrings nennen T-Nummern bzw. `A33-T14`. Eine H-Zuordnung ist aus dem Code **nicht** ableitbar. |
| Gelöschte Dateien / weitere Refs (`--diff-filter=D`, `git branch -a`, `git stash list`, `git notes list`), `git grep` über den gesamten Baum | Vollständigkeit | Keine gelöschte Review-Datei (einzige Löschung: `wissen/aufgaben/die-feature-list-fehlt.md`), keine weiteren Branches/Stashes/Notes, kein weiterer Treffer mit einer Definition. |

### AK-2/AK-3 — Bewertung: nicht rekonstruierbar (Begründung)

1. **Überlieferung nur als Sammelverweis:** Die Kennungen H1/H5/H7 existieren nur in einem Satz im Commit-Text `9f42200` und in daraus abgeleiteten Doku-Vermerken. Der dort behauptete Härtungsstand ist in diesem Commit **nicht enthalten**.
2. **Kein Diff als Ersatzquelle:** `test_meta.py` wurde mit `17d5320` in einem Zug (inkl. der 6 Zusatztests) eingebracht. Ohne Vorher-Fassung lässt sich nicht bestimmen, welche Änderung zu welchem H-Punkt gehörte.
3. **Kein H-Katalog im Bundle:** Das Reviewer-Protokoll (`ee7049f`) listet nur A6-1/A6-2. Der H-Katalog (H1…H7) hat es nie in `wissen/` oder `docs/` geschafft.
4. **Zahlenverhältnis schließt 1:1-Zuordnung aus:** 6 Zusatztests stehen 3 genannten H-Nummern gegenüber (die Nummerierung belegt mindestens H1–H7). Jede Zuordnung „H1 = Test X" wäre Spekulation und damit ein erfundener Fakt.
5. **Keine mildere Rekonstruktion möglich:** Auch eine Teilzuordnung (z. B. nur H1) hätte keine belastbare Quelle; die Testliste bleibt daher **ohne** H-Buchstaben dokumentiert.

### Belegt (unverändert gültig, ohne H-Zuordnung)

- **Testdatei:** `definitions/app/tests/test_meta.py`, erste Fassung `17d5320` (2026-11-14 06:14).
- **Umfang:** 18 Testfunktionen; die T1–T12-Fälle ergeben parametrisiert 24 Fälle, plus 6 Zusatzfunktionen = **30 Tests** — deckungsgleich mit dem Tester-Beleg „A6 30" (`wissen/log.md`, 2026-11-14).
- **6 Zusatzfunktionen (die „Testhärtung", ohne H-Nummern):** `test_kombiniert_verboten_kein_schreibvorgang`, `test_task_status_ziele_passen_zum_status_mapping`, `test_ohne_aenderung_kein_schreibvorgang`, `test_owner_wird_nicht_doppelt_geschrieben`, `test_fehlende_datei`, `test_crlf_body_bleibt_bytegleich`.
- **A6-2** (T2 Body-Hash) ist mit A33-B6 (`ef68598`) erledigt — `test_t2_owner_mensch` prüft `_hash(body_nachher) == _hash(body_vorher)` (Docstring: „A33-T14 (A6-2)").

### Abschluss-Vermerk (A6-1)

**A6-1 ist abgeschlossen: bewusste Dokumentationslücke, nicht rekonstruierbar.** Die H1/H5/H7-Definitionen sind weder im Bundle noch in der Git-Historie überliefert (Belege oben). Es wird keine H-Punkt→Test-Zuordnung ergänzt; die Testbelege selbst sind über Testnamen und Commit `17d5320` dokumentiert. Der Punkt wird **nicht** weiter als „offen" geführt.

### Geänderte Dateien

- `wissen/aufgaben/a6-meta.md` — neuer documenter-Eintrag (2026-11-16) mit Abschluss-Vermerk und Belegkette.
- `wissen/projekt/planung.md` — A6-1-Vermerk um Abschluss (nicht rekonstruierbar) ergänzt.
- `wissen/features.md` — A6-1 abgeschlossen, A6-2 erledigt.
- `wissen/aufgaben/a33-kleinbefunde-aufräum-takt.md` — A6-1-Zeile und T22 um A41-Abschluss ergänzt.
- `wissen/aufgaben/a41-a6-1-h-definitionen.md` — dieses Protokoll + Status `abgeschlossen`.

### Offene Punkte

- Keine inhaltlichen für A6-1. Falls der ursprüngliche Reviewer den H-Katalog (H1–H7) später nachreicht, kann er in [A6](/aufgaben/a6-meta.md) als Nachtrag ergänzt werden — **kein Code, kein Testlauf**.
- PM-Nachlauf außerhalb meines Datei-Rahmens: `wissen/index.md` (A41-Zeile steht dort noch auf „offen"), `wissen/log.md` (Abschluss-Eintrag), `docs/lueckenliste-a39.md` (A6-1 noch als offener Punkt) und `docs/uebergabeprotokoll.md` (Zeile 57) nachziehen.

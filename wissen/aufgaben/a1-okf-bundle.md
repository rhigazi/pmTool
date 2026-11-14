---
type: Task
title: "A1: Fundament okf_bundle.py (Pfadschutz, Frontmatter-I/O, Scan)"
description: Zentrale, framework-freie Zugriffsschicht für Pfadschutz, Frontmatter-/Datei-I/O mit atomarem Schreiben und Bundle-Scan.
task_status: abgeschlossen
phase: 8 Abgeschlossen
priority: hoch
assigned_to: coder
user_story: /projekt/user-stories/us-7.md
owner: ai
---

# Ziel

`definitions/app/okf_bundle.py` wird die zentrale, getestete Zugriffsschicht auf das Bundle: `resolve_path(rel)` mit Ausbruchsschutz (normalisiert, `realpath`-Präfix-Check, Symlink-Ausbruch), `lesen(pfad)` (strikt, Frontmatter via `yaml.safe_load`), `lesen_tolerant(pfad)` (ohne Frontmatter → `{}`), `set_meta(pfad, updates)` (nur Frontmatter-Keys, Body byte-identisch), `scan()` (alle `.md` außer `index.md`/`log.md`/`features.md`), atomares Schreiben (`tmp` + `os.replace`) und `ist_reserviert(pfad)`. Das Modul ist framework-frei (kein Flask-Import).

# Akzeptanzkriterien

- Pfade außerhalb `BUNDLE_ROOT` werden mit `BundlePfadFehler` abgewiesen — vor jedem Dateizugriff.
- `resolve_path` normalisiert den Pfad, prüft per `realpath`-Präfixzugehörigkeit und erkennt Symlink-Ausbrüche.
- `set_meta` verändert ausschließlich die angegebenen Frontmatter-Keys; übrige Keys und Body bleiben byte-identisch.
- Schreibvorgänge sind atomar: bei Fehler bleibt die Originaldatei unverändert.
- `scan()` liefert alle `.md`-Dateien außer `index.md`, `log.md` und `features.md`; `ist_reserviert` erkennt alle drei.
- `lesen` wirft bei fehlendem Frontmatter `FrontmatterFehler`, `lesen_tolerant` nicht.
- Tests arbeiten ausschließlich auf Fixture-Kopien unter `tmp_path`; `/content/pmTool/wissen` wird von pytest nie beschrieben.

# Testfälle (TDD)

- **T1 Pfad im Bundle:** `resolve_path("aufgaben/a1.md")` → absoluter Pfad unter `BUNDLE_ROOT`.
- **T2 Ausbruch `..`:** `resolve_path("../../etc/passwd")` → `BundlePfadFehler`, kein Zugriff.
- **T3 Absoluter Pfad:** `resolve_path("/etc/passwd")` → `BundlePfadFehler`.
- **T4 Verschleierter Ausbruch:** `aufgaben/../../x.md` und `a/%2e%2e/b.md` → `BundlePfadFehler`.
- **T5 Symlink-Ausbruch:** Symlink im Bundle zeigt nach außerhalb → `BundlePfadFehler`.
- **T6 Frontmatter lesen:** Fixture `aufgaben/a1.md` → `fm["type"] == "Task"`, Body ohne `---`-Block.
- **T7 Frontmatter fehlt (strikt):** Datei ohne `---` → `FrontmatterFehler`.
- **T8 Frontmatter fehlt (tolerant):** `lesen_tolerant()` → `({}, volltext)`, keine Exception.
- **T9 Frontmatter-Erhalt:** `set_meta(p, {"owner": "ai"})` → `type`/`title`/`user_story` unverändert, Body-SHA256 identisch.
- **T10 Atomarität:** `os.replace` per monkeypatch auf `OSError` → Original byte-identisch, Exception propagiert.
- **T11 Scan:** Bundle mit `index.md`, `log.md`, `features.md` und 2 Punkten → genau die 2 nicht-reservierten Dateien.
- **T12 Reserviert:** `ist_reserviert` für `index.md`, `log.md`, `features.md`, Punkt → `True, True, True, False`.

# Kontext

- **Abhängigkeiten:** keine — Startpunkt der Backend-Kette; A3–A7 bauen auf diesem Modul auf.
- **Konfliktgruppe G1:** `okf_bundle.py` und `tests/conftest.py` gehören A1 allein; erst nach Abschluss dürfen A3–A7 parallel starten.
- **Testregeln:** Testbefehl Quelle `python3 -m pytest definitions/app/tests -q`, installiert `python3 -m pytest app/tests -q`; Importstil `sys.path.insert(0, str(Path(__file__).resolve().parents[1]))`; Fixture-Vorlage `tests/fixtures/bundle_min/**` wird je Test nach `tmp_path` kopiert.
- **Entscheidungen:** R8 (MVP: atomares Schreiben + Re-Read, kein Locking; bekanntes Risiko dokumentiert), R4 (Scan-Umfang und Reserve-Dateien).
- **Verweise:** [Technische Spec](/projekt/technische-spec.md) (Datenintegrität, Pfadschutz), [Phasenmodell](/projekt/phasen.md) (TDD-Regeln).

# Betroffene Dateien

- `definitions/app/okf_bundle.py`
- `definitions/app/tests/conftest.py`
- `definitions/app/tests/test_okf_bundle.py`
- `definitions/app/tests/fixtures/bundle_min/**`

# Ergebnisse

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-14 — coder (Zwischenstand zum Halt, inkl. Sammel-Nachbesserung)

- **Ergebnis:** Umsetzung abgeschlossen; Review-Nachbesserung erledigt (u. a. Guard reservierter Dateien `ReservierteDateiFehler`, zentrale Exceptions). Sammel-Nachbesserung „zentrale Exceptions": `EingabeFehler` wird zentral aus `okf_bundle` geführt, lokale Definitionen in den Nutzer-Modulen entfernt. (Quelle: Übergabeprotokoll, Abschnitte „Aufgabenstatus" und „Session-Rückmeldungen zum Halt".)
- **Belege:** 45 Tests (A1), 102 Tests im Sammel-Lauf; Gesamtsuite 549 grün (Endstand zum Halt).
- **Offene Punkte:** formale Testphase (gebündelt vorgesehen) und Doku.

## 2026-11-14 — tester (Gebündelte Testphase)

- **Ergebnis:** **Testphase BESTANDEN** (DoD-Beleg): 45 Tests grün, keine offenen Testbefunde. Gesamtlauf der gebündelten Testphase: **549 passed (Start = Ende, kein Zuwachs), 0 rot, 0 geskippt**.
- **Befunde:** Flaky-Paar `test_t1b`/`test_t2` (`test_setup_verteilung.py`) bei serialisierten Läufen stabil (3× bestätigt) — Empfehlung: Testläufe serialisieren.
- **Offene Punkte:** Review ausstehend.

## 2026-11-14 — reviewer (Review-Runde 2)

- **Ergebnis:** **Nachbesserung läuft** (Rücklauf an `coder`). Sicherheit sauber (keine Befunde zu Pfad-/Reserviert-Schutz).
- **Befunde:** [B1] wesentlich: `set_meta`-Wertkorruption bei mehrzeiligen Frontmatter-Werten mit Leerzeilen (`okf_bundle._setze_zeilen`). [B2] klein: Docstring `lesen_tolerant`.
- **Offene Punkte:** [B1] in Umsetzung (Rücklauf läuft); [B2] als Kleinbefund geführt (Aufräum-Takt, siehe [features.md](/features.md)).

## 2026-11-14 — coder (Sicherheits-Nachbesserung, abgeschlossen)

- **Ergebnis:** [B1] behoben: `set_meta`-Wertblock-Grenzen korrekt (`_zum_wertblock`). [B2] behoben: `lesen_tolerant` liefert bei ungültigem YAML `({}, body)` (bewusste Verhaltenskorrektur statt reiner Doku-Anpassung).
- **Belege:** 29 neue Tests im Sicherheits-Block (alle rot→grün belegt), Gesamtsuite 676 grün.
- **Offene Punkte:** Bestätigungs-Review läuft parallel.

## 2026-11-14 — reviewer (Bestätigungs-Review, Runde 2)

- **Ergebnis:** **Review-frei** — [B1] (Wertblock `_zum_wertblock`) und [B2] (`lesen_tolerant` bei ungültigem YAML) sind behoben und durch echte, nicht abgeschwächte Tests belegt.
- **Befunde:** keine kritischen/wesentlichen Befunde offen.
- **Offene Punkte:** Doku/Abschluss.

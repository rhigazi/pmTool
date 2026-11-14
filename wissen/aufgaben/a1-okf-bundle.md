---
type: Task
title: "A1: Fundament okf_bundle.py (Pfadschutz, Frontmatter-I/O, Scan)"
description: Zentrale, framework-freie Zugriffsschicht für Pfadschutz, Frontmatter-/Datei-I/O mit atomarem Schreiben und Bundle-Scan.
task_status: in Umsetzung
phase: 4 Umsetzung
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

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

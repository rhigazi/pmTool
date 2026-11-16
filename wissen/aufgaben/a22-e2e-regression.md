---
type: Task
title: "A22: E2E-Regressionstest (test_e2e.py)"
description: Die T1/T2/T7-Kette des A17-Abnahmelaufs als dauerhaften, eingecheckten E2E-Test überführen.
task_status: abgeschlossen
phase: 8 Abgeschlossen
priority: mittel
assigned_to: coder
user_story: /projekt/user-stories/us-7.md
owner: ai
aktuell: ""
freigabe: true
---

# Ziel

Die im A17-Abnahmelauf ad hoc gefahrene T1/T2/T7-Kette (aus den Skripten `/tmp/opencode/a17_*.py`) wird als dauerhafter E2E-Test `test_e2e.py` ins Repository überführt, damit die End-to-End-Absicherung nicht nur als Einmal-Nachweis existiert.

# Akzeptanzkriterien

- `test_e2e.py` ist eingecheckt und läuft als Teil der Gesamtsuite.
- T1 API-E2E (Overview → Nachtrag → Klarung → owner) ist automatisiert und konsistent.
- T2 (Frontmatter intakt: `type`/`title` unverändert, genau 1 Marker) ist automatisiert.
- T7 (Reset reproduzierbar) ist automatisiert.
- Der Test läuft ausschließlich gegen ein Test-Bundle unter `/tmp/opencode/…`; `/content/pmTool/wissen` wird nie beschrieben (Hash-Nachweis wie bei A17).

# Testfälle (TDD)

- **T1 E2E-Kette:** API-Sequenz gegen Test-Bundle → konsistente Zustände über alle Schritte.
- **T2 Frontmatter-Invarianten:** `type`/`title` unverändert, genau 1 Nachtrag-Marker.
- **T7 Reset:** Wiederholter Lauf ist reproduzierbar (gleiche Ergebnisse).
- **Isolation:** Echt-Bundle-Hash vor/nach dem Lauf identisch.

# Kontext

- **Ursprung:** A17-Abnahmelauf (bestanden) — die Ad-hoc-Skripte unter `/tmp/opencode/a17_*.py` sind nicht Teil des Repos; PM-Entscheidung: MVP-Abnahme mit dokumentiertem Einmal-Nachweis, dauerhafte Regression als A22 post-MVP.
- **Abhängigkeiten:** A1–A20 abgeschlossen; nutzt das Test-Bundle-Muster aus A17.
- **Verweise:** [A17](a17-e2e.md), [Technische Spec](/projekt/technische-spec.md#build--start--test-befehle), [Phasenmodell](/projekt/phasen.md).

# Betroffene Dateien

- `definitions/app/tests/test_e2e.py` (neu)
- ggf. `definitions/app/tests/conftest.py` (Fixtures)

# Ergebnisse
## 2026-11-16 — coder (K-Sammlung): A22-K1/K2/K5/K8 behoben

- **K1:** tautologische Schluss-Assertion ersetzt (Klammer `len(protokoll) == 12` + Eindeutigkeit + konkrete Fachwerte: Marker, UND-Gate-Zwischenstände, Endübersicht, SHA-Format). **K2:** Datei-Hash vor/nach Schritt 11 (403) — „kein Schreibvorgang" byte-genau belegt. **K5:** Mitternachts-Kante gelöst (Lauf-Fenster + tatsächliches Datei-Datum; T7 datumsnormalisiert; Simulationsbeleg „Protokolle identisch über Mitternacht"). **K8:** Isolations-Skip explizit (Pfad + Grund), im Dev-Repo läuft die Probe regulär. 114 → **127 Assertions**, 4 grün (dreifach stabil).


## 2026-11-16 — reviewer: Review FREIGEGEBEN → **abgeschlossen**

- **Urteil:** FREIGEGEBEN (keine W-Befunde; 8 K-Punkte, davon 2 Doku). Mutantenproben gegen den Produktivcode: **8/11 getötet** (Marker-Dopplung/-Fehlen, echter Append-Bruch ×2, fehlender Body-Abschnitt, fehlendes `freigabe: false`, Freigabe-Durchgriff `/api/meta`, Status-Feld, fail-open-Freigabe); 3 Überlebende = belegte Schichtungs-/Redundanz-Fälle (M6 Meta-Guard redundant zum Server-Guard; M10 `bool(raw)` deckt `test_freigabe.py`; M11 Whitelist-Aufweichung deckt `test_meta.py`). SHA-Restaurierung aller Mutanten belegt. Testläufe: `test_e2e.py` 4 passed (Snapshot **und** aktueller Arbeitsbaum), Anrainer 89/475 passed, App-Suite ohne Setup-Verteilung **1571 passed / 0 failed**.
- **K-Punkte (Klammer):** K1 tautologische Schluss-Assertion (Schrittnamen-Liste) — optional straffen; K2 „byte-identisch/403" im E2E nur semantisch geprüft (Hash vor/nach Schritt 11 ergänzen); K3/K4 Negativfälle der Meta-Whitelist/Fail-closed-Schwäche bewusst in `test_meta.py`/`test_freigabe.py` geschichtet (dort scharf belegt); K5 Mitternachts-Kante bei `heute` (Datum vor/nach vergleichen — seltener Flake-Pfad); K8 Isolationsprobe T3 überspringt still bei fehlendem `wissen/`. K1/K2/K5/K8 → Härtungs-Klammer (Lückenliste).
- **„Nicht rekonstruierbar" (A17-Ad-hoc-Skripte) akzeptabel, keine Vertragslücke:** Die Skripte `/tmp/opencode/a17_*.py` waren nie im Repo (Einmal-Nachweis lt. Entscheidungslog 2026-11-14); ein 1:1-Port ist unmöglich. Die Kette ist eine dokumentationsgetreue Nachbildung, überzeichnet nicht (keine „23/23"-Behauptung) und prüft an den Zuständen mehr als der damalige Einmal-Lauf. **Restvermerk:** die exakte A17-Schrittfolge ist nachträglich nicht mehr verifizierbar — als Lücke dokumentiert (dieser Eintrag).

## 2026-11-16 — coder (Welle A): `test_e2e.py` umgesetzt — 4 grün

- **Ergebnis:** Neue Datei `definitions/app/tests/test_e2e.py` (4 Tests, 114 Assertions): **T1** durchgängige API-Kette über `server.create_app(...).test_client()` gegen tmp-Kopie von `fixtures/bundle_min` unter `/tmp/opencode/a22-e2e-*` (Overview → Nachtrag append-only → Aufgabe A99 → Welle → owner/status/welle per `POST /api/meta` → Freigabe-Gate Welle+Aufgabe (UND, beide Zwischenzustände) → KI-Weg `freigabe` 403 → Endkonsistenz, Datei-SHA-256 im Protokoll); **T2** Frontmatter-Invarianten (vor/nach exakt gleich, 1 Marker, append-only); **T7** Reset reproduzierbar (Bundle zurückgesetzt → Kette erneut → identisches Protokoll mtime-frei, inkl. Datei-SHA-256); **T3** echtes `wissen/` unberührt (Baum-SHA-256 vor/nach, Bundles ausschließlich unter `/tmp/opencode`).
- **TDD-Beleg:** rot (Datei fehlt, Exit 4) → grün (4 passed, wiederholt stabil).

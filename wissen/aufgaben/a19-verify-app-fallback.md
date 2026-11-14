---
type: Task
title: "A19: verify.sh akzeptiert definitions/app als Fallback"
description: Verify-Abschnitt 7 prüft die App unter app/ oder definitions/app/ (Fallback analog zu start.sh) inklusive passender Tests.
task_status: in Doku
phase: 7 Dokumentation
priority: mittel
assigned_to: coder
user_story: /projekt/user-stories/us-6.md
owner: ai
---

# Ziel

`definitions/verify.sh` Abschnitt „7) App" akzeptiert derzeit ausschließlich `app/` im Ziel. Im Dev-Repo liegt die App jedoch in `definitions/app/` (Single Source of Truth); `start.sh` hat dafür bereits einen Fallback (prüft `app/`, sonst `definitions/app/`). Ziel: `verify.sh` prüft beide Ablageorte — `app/` oder `definitions/app/` als Fallback analog zu `start.sh` — und schlägt nur noch fehl, wenn beide fehlen. Passende Tests werden ergänzt.

# Akzeptanzkriterien

- `verify.sh` Abschnitt 7 findet die App-Dateien unter `app/` **oder** (Fallback) unter `definitions/app/`.
- Im Dev-Repo (`/content/pmTool`, App in `definitions/app/`) liefert `verify.sh` Exit 0.
- Im verteilten Ziel (App in `app/`) bleibt das Verhalten unverändert (Exit 0).
- Fehlen beide Orte, schlägt `verify.sh` mit Exit 1 fehl und die Meldung nennt beide geprüften Pfade (pfad-frei im Fehlerfall analog zu den übrigen Abschnitten).
- Die übrigen Abschnitte von `verify.sh` bleiben funktional unverändert (Regel R12 analog zu A15).
- Passende Tests in `test_verify_fallback.py` ergänzen und grün.

# Testfälle (TDD)

- **T1 Verify im Dev-Repo:** Bundle/Repo mit App nur in `definitions/app/` → `verify.sh` Exit 0 (vorher: Exit 1).
- **T2 Verify im verteilten Ziel:** Ziel mit `app/` → `verify.sh` Exit 0 (Regression).
- **T3 Beide fehlen:** weder `app/` noch `definitions/app/` → Exit 1, Ausgabe nennt beide geprüften Pfade.
- **T4 Keine Regression:** übrige Abschnitte von `verify.sh` unverändert funktionsfähig (R12).

# Kontext

- **Anlass:** `verify.sh` Abschnitt 7 schlug im Dev-Repo allein deshalb fehl, weil er nur `app/` akzeptiert; `start.sh` löst dieselbe Situation per Fallback auf `definitions/app/`.
- **Entscheidung:** „verify.sh akzeptiert definitions/app als Fallback" (2026-11-14) — siehe [Entscheidungslog](/entscheidungen/log.md).
- **Abhängigkeiten:** A15 (Abschnitt „7) App" in `verify.sh`); kleine Nachbesserung, keine Schnittstellenänderung.
- **Konfliktgruppe G10:** `setup.sh`/`verify.sh` exklusiv — nicht parallel zu anderen verify/setup-Arbeiten.
- **Verweise:** Fallback-Muster in `start.sh` (Zeilen mit `app/server.py` bzw. `definitions/app/server.py`); [A15](a15-setup-verify.md).

# Betroffene Dateien

- `definitions/verify.sh`
- `definitions/app/tests/test_verify_fallback.py`

# Ergebnisse

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-14 — coder (Umsetzung, abgeschlossen)

- **Ergebnis:** `verify.sh` Abschnitt 7 akzeptiert `app/…` oder `definitions/app/…` (Vorrang `app/`, Fallback analog `start.sh`); `bad` nur bei Fehlen beider Varianten; die App-Suite wird im gefundenen Verzeichnis gesucht. `bash definitions/verify.sh .` vorher Exit 1 → **nachher Exit 0**. A20-Teil 2 mit erledigt: `verify.sh` Zeile 70 Hinweistext „wird von container.sh installiert" → „wird über `setup.sh --global` installiert"; im Kontroll-Lauf zeigt Abschnitt 6 „✓ moli Browser" (moli per Symlink im PATH — Umgebungslösung des PM).
- **Belege:** Neue Testdatei `definitions/app/tests/test_verify_fallback.py` (5 Tests, rot 3 → grün 5); serialisierte Gesamtsuite 644 grün; Commit `4d1f335`.
- **Befunde:** PM-Entscheidung zum offenen Punkt: Eine rote App-Suite bleibt `bad`/Exit-1-Grund (Korrektur läuft als letzter Kleinschritt). `test_setup_verteilung.py` wurde bewusst nicht angefasst und ist nicht betroffen.
- **Offene Punkte:** Review (Bestätigung im Nachbesserungs-Batch); Flaky-Vermerk zu parallelen verify-Läufen siehe [Projekt-Log](/log.md).

## 2026-11-14 — reviewer (Bestätigungs-Review, Runde 2)

- **Ergebnis:** **Review-frei** — der Fallback `app/` bzw. `definitions/app/` (inkl. „rote Suite = bad") ist durch echte, nicht abgeschwächte Tests belegt; der Testphase-Beleg liegt vor (5 Tests, `verify.sh` Exit 0 im Dev-Repo).
- **Befunde:** keine kritischen/wesentlichen Befunde offen.
- **Offene Punkte:** Doku/Abschluss.

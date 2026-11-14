---
type: Task
title: "A20: setup.sh-Härtung (Moli/Skill-Installation)"
description: Die --global-Sektion der setup.sh (Projektleitungs-Änderung 2026-11-14) wird gegen ungeprüften Remote-Code abgesichert und idempotent gemacht.
task_status: in Doku
phase: 7 Dokumentation
priority: mittel
assigned_to: coder
user_story: /projekt/user-stories/us-6.md
owner: ai
---

# Ziel

Die `--global`-Sektion der `setup.sh` (Projektleitungs-Änderung vom 2026-11-14) wird abgesichert.

# Akzeptanzkriterien

1. Moli-Installer nicht mehr `latest` + `curl | sh` ungeprüft — feste Version pinnen und SHA256-Checksumme vor Ausführung prüfen (Fallback: zumindest striktes Version-Pinning mit dokumentierter Herkunft).
2. `command -v moli`-Guard vor der Installation (Idempotenz, kein erneuter Download wenn vorhanden).
3. npx-Quelle dokumentieren (Repo, Zweck, Hinweis auf Fremdcode).
4. `verify.sh` Abschnitt 6: Hinweistext „moli … wird von container.sh installiert" an die Realität angleichen („optional, wird über `setup.sh --global` installiert").
5. Tests ergänzen/anpassen (Guard-Verhalten, keine Doppelinstallation).

# Testfälle (TDD)

- **T9–T11 (Quelltext-Marker-Tests):** Guard (`command -v moli`), Version-Pinning + SHA256-Prüfung sowie Download in `mktemp` statt `curl | sh` sind im Quelltext belegt.
- **Guard-Verhalten:** bei vorhandenem `moli` im PATH wird die Installation übersprungen („übersprungen (vorhanden)"), kein erneuter Download.
- **Keine Doppelinstallation:** wiederholter Lauf mit vorhandenem `moli` installiert nicht erneut.

# Kontext

- **Ursprung:** Review-Hinweis zur Härtung (Version/Checksum pinnen, `command -v moli`-Guard, npx-Quelle dokumentieren) zur Projektleitungs-Änderung in `definitions/setup.sh` (Sektion „8) Global: Wichtige Skills & Browser", Commit `5bc453f`).
- **Nummerierung:** Das Nummerierungsdoppeln „8)" ist behoben — `setup.sh` ist jetzt durchgehend eindeutig 1–10 (8) Global = Ende der Globalsequenz, 9) Dev-Abhängigkeiten, 10) App); `docs/uebergabeprotokoll.md` wurde vom coder mitgezogen.
- **Reihenfolge:** Startet erst, wenn die laufenden Arbeiten an `setup.sh` (A15/Nummerierung) und `verify.sh` (A19) abgeschlossen sind — Konfliktvermeidung. Teil 2 (AK 4) wurde vorab als Teil des A19-Abschlusses erledigt.
- **PM-Entscheidung zur Semantik (läuft als Korrektur):** Checksummen-Abweichung = hart abbrechen; Download-/Netzfehler = Warnung + Setup läuft weiter (moli optional).
- **Verweise:** [A15](a15-setup-verify.md), [A19](a19-verify-app-fallback.md), [Entscheidungslog](/entscheidungen/log.md).

# Betroffene Dateien

- `definitions/setup.sh`
- `definitions/verify.sh` (nur Hinweistext)
- `definitions/app/tests/test_setup_verteilung.py` (ggf. Anpassungen)

# Ergebnisse

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-14 — coder (Teil 2 von 2: verify-Hinweistext, abgeschlossen)

- **Ergebnis:** AK 4 erledigt — `verify.sh` Hinweistext Abschnitt 6 von „wird von container.sh installiert" auf „wird über `setup.sh --global` installiert" geändert; im Kontroll-Lauf zeigt Abschnitt 6 „✓ moli Browser" (moli per Symlink im PATH). Details im [A19-Ergebnis](a19-verify-app-fallback.md).
- **Belege:** Commit `4d1f335` (gemeinsamer A19/A20-Teil-2-Abschluss).

## 2026-11-14 — coder (Teil 1 von 2: setup.sh-Härtung, umgesetzt)

- **Ergebnis:** Idempotenz-Guard `command -v moli` („übersprungen (vorhanden)"), **Pin v1.1.24** mit **SHA256-Prüfung** gegen den offiziellen GitHub-Release-Digest (Fallback „nur Pinning" war nicht nötig), Download in `mktemp` statt `curl | sh`, npx-Kommentar (Repo, Zweck, Fremdcode-Hinweis). T9–T11 als Quelltext-Marker-Tests.
- **Befunde:** PM-Entscheidung zur Semantik (läuft als Korrektur): Checksummen-Abweichung = hart abbrechen; Download-/Netzfehler = Warnung + Setup läuft weiter (moli optional).
- **Offene Punkte:** Semantik-Korrektur läuft; **Pin-Pflege** — URL und SHA256 müssen bei Moli-Updates zusammen geändert werden (offener Punkt, Folgeaufgabe vormerken — ggf. Teil von A21 oder eigene Kleinigkeit).

## 2026-11-14 — coder (Abschluss Kleinbefunde-Takt)

- **Ergebnis:** A20 vollständig umgesetzt — Teil 1 (setup.sh-Härtung), Teil 2 (verify-Hinweistext) und die Semantik-Entscheidung; alles grün und gepusht.
- **Belege:** Commits `c1a1a23`, `4d1f335`, `f0a37c8`, `cd91b78`; Gesamtsuite 761 grün.
- **Offene Punkte:** Doku/Abschluss; Pin-Pflege (URL+SHA256) bleibt Post-MVP-Notiz.
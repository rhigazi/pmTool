---
type: Task
title: "A32: Neues-Projekt-Flow — start.sh --neu + Erststart-Hinweis"
description: Nach einem Repo-Pull startet start.sh in einem neuen Container mit pmTool-Projektdaten
  vorbefüllt — start.sh soll den Reset auf die saubere Vorlage anbieten (Hinweis + --neu-Flag).
task_status: in Planung
phase: 2 Planung
priority: hoch
assigned_to: coder
owner: ai
aktuell: "coder: Umsetzung start.sh --neu + Erststart-Hinweis"
---

# Ziel

Wenn ein neues Projekt per Repo-Pull entsteht, ist `wissen/` mit den pmTool-Projektdaten **vorbefüllt** (Feststellung der Projektleitung 2026-11-15). Der Reset über `python3 tools/neues_projekt.py --ja` ist umgesetzt (A24), wird aber nicht gefunden. Gewünschter Flow (Entscheidung der Projektleitung, 2026-11-15, Variante „start.sh --neu + Erststart-Hinweis"):

1. **Erststart-Hinweis:** `start.sh` erkennt beim Start, dass `wissen/` pmTool-Projektdaten enthält (Marker), und schlägt **interaktiv** den Reset auf die saubere Vorlage vor — inklusive Rückfrage (kein destruktives Verhalten ohne Bestätigung), Hinweis auf Backup-Ort und auf `tools/neues_projekt.py`.
2. **Explizites Flag `--neu`:** `bash start.sh --neu` stößt den Reset gezielt an (mit Backup, dann Start der App mit leerem Projekt) — für alle, die den Hinweis nicht abwarten wollen.

# Akzeptanzkriterien (vorläufig, der `planner` schärft sie)

- **AK-1 (Erkennung):** `start.sh` erkennt „pmTool-Projektdaten in `wissen/`" zuverlässig über einen Marker (Begründung wählen: z. B. `wissen/aufgaben/a1-okf-bundle.md` bzw. pmTool-spezifische Dateien) und unterscheidet: frisches Vorlagen-`wissen/` (kein Hinweis), vorbefülltes `wissen/` (Hinweis), fehlendes `wissen/` (Vorlage wird wie bisher aufgebaut).
- **AK-2 (Hinweis, interaktiv):** Beim Start mit vorbefülltem `wissen/` erscheint ein klarer deutscher Hinweis („Dieses Repo enthält Projekt-Daten … Neues leeres Projekt beginnen?"), mit Ja/Nein-Rückfrage. **Nein/Abbruch = unveränderter Normalstart** (nichts wird gelöscht!). Ja = Reset wie `neues_projekt.py --ja` (Backup vor dem Löschen) und Start mit leerem Projekt.
- **AK-3 (`--neu`-Flag):** `bash start.sh --neu` führt den Reset ohne Umweg aus (Backup + Vorlage + Start); `--neu --dry-run` zeigt nur den Plan (analog `neues_projekt.py` ohne `--ja`). Kombinierbar mit `--colab`. Unbekannte Flags bleiben Fehler.
- **AK-4 (Sicherheit):** Der Reset läuft ausschließlich über `tools/neues_projekt.py` (A24-Logik, Backup-Pflicht, Sicherheitsinvarianten — **keine zweite Lösch-Implementierung** in `start.sh`). Ohne explizite Bestätigung wird nichts gelöscht; `--dry-run` ändert nichts.
- **AK-5 (Doku):** README („Neues Projekt beginnen") und `docs/colab-start.md` beschreiben den neuen Flow (Pull → `bash start.sh --colab` → Hinweis/`--neu`); die bestehende manuelle Variante bleibt dokumentiert.
- **AK-6 (Regression):** `test_start_skript.py` bleibt grün (bisheriges Verhalten inkl. `--dry-run`, Ctrl+C, Fallback `definitions/app/server.py`); keine neuen Abhängigkeiten.

# Testfälle (TDD)

Noch keine Einträge — der `planner` ergänzt die Testfälle.

# Kontext

- **Entscheidung der Projektleitung 2026-11-15:** Variante „start.sh --neu + Erststart-Hinweis" (aus vier vorgeschlagenen Varianten gewählt).
- **Abhängigkeiten:** A24 (`tools/neues_projekt.py` — Reset-Logik, abgeschlossen), A26 (Spiegel `definitions/tools/` + Verteilung durch `setup.sh`, in Review). Der Reset darf nur die eine Quelle nutzen.
- **Betroffene Dateien (Vorabannahme):** `start.sh`, `definitions/app/tests/test_start_skript.py`, README, `docs/colab-start.md` — ggf. `definitions/start.sh` falls gespiegelt (prüfen).

# Betroffene Dateien

Noch keine Einträge — die Planung ergänzt die betroffenen Dateien.

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

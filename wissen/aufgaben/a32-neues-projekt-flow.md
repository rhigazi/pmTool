---
type: Task
title: "A32: Neues-Projekt-Flow — start.sh --neu + Erststart-Hinweis"
description: Nach einem Repo-Pull startet start.sh in einem neuen Container mit pmTool-Projektdaten
  vorbefüllt — start.sh soll den Reset auf die saubere Vorlage anbieten (Hinweis + --neu-Flag).
task_status: in Nachbesserung
phase: 4 Nachbesserung
priority: hoch
assigned_to: coder
owner: ai
aktuell: "tester: S1–S7 BESTANDEN (16/16) — coder: Rücklauf W1+K1–K5/K7/K8 läuft"
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

## Präzisierung `coder` (2026-11-15, bei der Umsetzung)

- **Marker:** Liste aus zwei Referenzdateien — `wissen/aufgaben/a1-okf-bundle.md` und `wissen/features/okf-projekt-manager-spa.md`. Keine davon legt die Vorlage an; eine Liste verhindert stilles Versagen bei Umbenennung einer Datei. Der Treffer genügt (Oder-Verknüpfung). Geprüft wird am **Reset-Ziel** `<Projekt>/wissen` (Nachbesserung W1: `tools/neues_projekt.py` ignoriert `BUNDLE_ROOT`).
- **Reihenfolge:** neuer Schritt 5 „Projektstand" läuft **vor** `verify.sh` (Schritt 6), damit die Prüfung nach einem Reset den leeren Zustand sieht; App-Start ist Schritt 7. Hinweistexte nennen Backup-Ort (`wissen-backup-YYYYMMDD-HHMMSS.tar.gz`) und `tools/neues_projekt.py`.
- **Ja/Nein:** Zustimmung nur bei `j`, `ja`, `y`, `yes` (Groß-/Kleinschreibung egal). Leere Eingabe, alles andere, `Strg+D` und Lesefehler = **Nein** (unveränderter Start). Kein TTY (`[ ! -t 0 ]`) = nur Hinweis, kein Prompt, kein Reset (fail-safe). `--dry-run` fragt grundsätzlich nicht.
- **`--neu --dry-run`:** ruft das Werkzeug **ohne** `--ja` auf (Planausgabe) und setzt danach den normalen Trockenlauf fort („würde starten"); kein Backup, keine Änderung. `--neu` ist mit `--colab` kombinierbar (Reihenfolge der Flags egal).
- **Fehlerpfad:** Fehlt `tools/neues_projekt.py` oder endet das Werkzeug mit Exit ≠ 0, meldet `start.sh` den Fehler auf stderr (`✗ …`) und beendet sich mit Exit 1 — kein App-Start. Ein Teilreset wird nie als Erfolg behandelt. Ohne Werkzeug lautet die Meldung „Werkzeug fehlt: tools/neues_projekt.py — Reset nicht möglich".
- **Abweichung/Klarstellung zu AK-1:** Ein **fehlendes** `wissen/` ist ohne `--neu` weiterhin ein Abbruch der Strukturprüfung (Schritt 2); mit `--neu` prüft Schritt 2 nur `definitions/`, und das Werkzeug legt das Bundle aus der Vorlage an (Nachbesserung K3). Die Erkennung liefert bei fehlendem Bundle „kein Hinweis".
- **Entwicklungs-Repo:** Der Reset nutzt ausschließlich `tools/neues_projekt.py`; die Quelle `definitions/tools/neues_projekt.py` ist **kein** Fallback (Nachbesserung K1).

# Testfälle (TDD)

Alle in `definitions/app/tests/test_start_skript.py`, jeweils in einem Mini-Projekt
unter `tmp_path` (eigenes `wissen/`, eigene Vorlage, Dummy-Server und
Dummy-`start_colab.py`, `tools/neues_projekt.py`-Kopie) — das echte `wissen/`
wird nie berührt:

- `test_erststart_hinweis_ohne_tty_setzt_nichts_zurueck` — vorbefüllt + kein TTY: Hinweis, kein Prompt, keine Löschung, Start läuft.
- `test_dry_run_zeigt_nie_einen_prompt` — Trockenlauf fragt nicht, löscht nicht, zeigt „würde starten".
- `test_frische_vorlage_zeigt_keinen_hinweis` — leeres Vorlagen-`wissen/`: kein Hinweis, kein `--neu`-Tipp.
- `test_jeder_marker_erkennt_vorbefuelltes_wissen[marker0|marker1]` — jeder Marker einzeln genügt.
- `test_interaktiv_nein_startet_unveraendert` — TTY + „nein": Prompt erscheint, nichts gelöscht, App startet.
- `test_interaktiv_abbruch_ist_wie_nein` — TTY + Strg+D: wie Nein, nichts gelöscht.
- `test_interaktiv_ja_setzt_zurueck_und_startet` — TTY + „ja": Backup existiert, Marker weg, App startet.
- `test_neu_setzt_ohne_rueckfrage_zurueck_und_startet` — `--neu`: eigene Aufgabe weg, Backup vorhanden, kein Prompt, Start.
- `test_neu_dry_run_zeigt_nur_den_plan` — `--neu --dry-run`: Plan-Titel, kein Backup, Marker bleibt, „würde starten".
- `test_neu_ist_mit_colab_kombinierbar` — `--neu --colab --dry-run`: Plan + `start_colab.py`, kein Backup.
- `test_reset_fehler_bricht_den_start_ab` — unvollständige Vorlage: Exit ≠ 0, Fehler auf stderr, nichts gelöscht, kein Serverstart.
- `test_ohne_reset_werkzeug_kein_loeschen` — ohne Werkzeug: Exit ≠ 0, Hinweis auf `neues_projekt.py`, nichts gelöscht.

Rot-Stand vor der Implementierung: 12 failed / 10 passed; nach der Implementierung
22 passed (9 bestehende + 13 neue). TTY-Pfade laufen über ein echtes `pty`, damit
`[ -t 0 ]` greift.

## Nachbesserung `coder` (2026-11-15, Review W1 + K1–K5/K7/K8)

Zusätzliche Tests (alle grün, gleiche Isolation):

- `test_fremdes_bundle_loest_keinen_reset_aus` / `test_lokale_marker_bleiben_trotz_fremdem_bundle_ausloeser` — W1: Marker zählen nur am Reset-Ziel; fremdes `BUNDLE_ROOT` löst weder aus noch unterdrückt es.
- `test_neu_setzt_lokales_wissen_trotz_fremdem_bundle_zurueck` — W1/K5: `--neu` resettet `<Projekt>/wissen` und nennt das abweichende `BUNDLE_ROOT`.
- `test_kein_fallback_auf_definitions_tools` — K1: `definitions/tools/` ersetzt den installierten Pfad nicht; fail-loud „Werkzeug fehlt".
- `test_neu_ohne_wissen_legt_bundle_ohne_backup_an` — K3: `--neu` legt fehlendes `wissen/` aus der Vorlage an (kein Backup nötig).
- `test_ohne_wissen_ohne_neu_bricht_ab` — K3: ohne `--neu` bleibt der Abbruch unverändert.
- `test_belegter_port_verhindert_reset_vor_der_rueckfrage` — K7: Port-Hinweis vor der Rückfrage, kein Reset, kein zweiter Start.
- `test_interaktiv_leere_eingabe_ist_nein` + `test_zustimmung_ignoriert_gross_kleinschreibung[y|Y|YES|yes]` — K5: Enter = Nein, `y`/`Y`/`YES`/`yes` = Ja.

Rot-Stand der Nachbesserung: 7 failed / 26 passed (33 Tests); der 34. Test
(`--neu` mit abweichendem `BUNDLE_ROOT`) kam beim Nachziehen derselben W1-Note
hinzu. Nach der Umsetzung 34 passed. K2 (Werkzeug im TTY-Hinweis) prüft
`test_interaktiv_nein_startet_unveraendert`, K8 (Kopfkommentar) deckt
`test_help_zeigt_hilfe_ohne_shelloptionen` mit ab.

# Kontext

- **Entscheidung der Projektleitung 2026-11-15:** Variante „start.sh --neu + Erststart-Hinweis" (aus vier vorgeschlagenen Varianten gewählt).
- **Abhängigkeiten:** A24 (`tools/neues_projekt.py` — Reset-Logik, abgeschlossen), A26 (Spiegel `definitions/tools/` + Verteilung durch `setup.sh`, in Review). Der Reset darf nur die eine Quelle nutzen.
- **Betroffene Dateien (Vorabannahme):** `start.sh`, `definitions/app/tests/test_start_skript.py`, README, `docs/colab-start.md` — ggf. `definitions/start.sh` falls gespiegelt (prüfen).

# Betroffene Dateien

- `start.sh` — Marker-Erkennung, interaktiver Hinweis, `--neu`, Reset-Aufruf, Schritt „Projektstand", Hilfe.
- `definitions/app/tests/test_start_skript.py` — 13 neue Tests (tmp-Projekt + pty), Help-Test um `--neu` ergänzt; Nachbesserung: +12 Tests (BUNDLE_ROOT, Fallback, Port, `--neu` ohne `wissen/`, Eingabe-Randfälle) → 34 Tests.
- `README.md` — Options-Tabelle (`--neu`), Abschnitt „Neues Projekt beginnen" (neuer Flow vor der manuellen Variante; Nachbesserung: Reset-Ziel/`BUNDLE_ROOT`, Port, `--neu` ohne `wissen/`).
- `docs/colab-start.md` — Options-Tabelle und Abschnitt „Neues Projekt beginnen (optional)" (Hinweis/`--neu`, manuelle Zellen als Alternative; Nachbesserung: Reset-Ziel/`BUNDLE_ROOT`, `--neu` ohne `wissen/`).
- Geprüft: kein `definitions/start.sh` vorhanden — `start.sh` ist reines Repo-Root-Werkzeug, keine Spiegelung nötig.

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

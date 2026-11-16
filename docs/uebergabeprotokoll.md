---
type: Document
title: Übergabeprotokoll — OKF Projekt-Manager (SPA)
description: Gesamtstand zum Sitzungswechsel 2026-11-15 (Abend-Pause): Takte 1–7 der Parallelwelle, WIP A34-P3, Rest-Umfang, K-Sammlung, Weiterführung.
tags: [uebergabe, status, protokoll]
generated: { by: opencode/mimo-v2.6-pro, at: 2026-11-15T19:00:00Z }
status: aktuell
---

# Zweck dieses Protokolls

**Pause 2026-11-15 Abend (Anweisung der Projektleitung: „alles anhalten, Übergabe für morgen").** Die Parallelwelle ist weit fortgeschritten (Takte 1–7 gepusht); ein WIP-Strang (A34-P3 UI) wartet auf sein Review. Dieses Protokoll sichert den gesamten Stand inkl. WIP-Commit `4e98f42`.

**Lesereihenfolge für eine neue Session (Projektmanager):** erst dieses Protokoll, dann `wissen/index.md`, dann `wissen/entscheidungen/log.md`. Den Startprompt aus `docs/startprompt.md` als erste Nachricht schicken.

# Projekt in Kürze

**OKF Projekt-Manager (SPA)** — browserbasierte Ein-Personen-Oberfläche zur Verwaltung eines OKF-Projekts in Mensch-KI-Zusammenarbeit. Tracker über dem OKF-Bundle `wissen/` (keine Zweitdatenbank); die eigentliche Arbeit läuft über den OpenCode-CLI-Chat (PM + Subagenten). Regeln: `AGENTS.md` (+ `definitions/AGENTS.md` = Single Source of Truth). Workflow: PM + `planner`/`coder`/`reviewer`/`tester`/`documenter`, TDD, Commits je Takt, Sofort-Push bei angenommenen Aufgaben.

# Aktueller Stand (2026-11-16, Abend) — Welle abgeschlossen

- **Komplett abgeschlossen: A1–A38, A40–A42.** Am 2026-11-16 wurden erledigt: Vormittag A26 (Bestätigungs-Review) + A34 (Sammellauf+Delta, Spiegel-Drift gefixt); Abend-Welle „alles frei" (Freigabe der Projektleitung): **A21** (Desktop-Modus, 70 Tests), **A22** (E2E-Regression, 127 Assertions), **A35** (Status-Mapping server-seitig, 37 Tests, JS-Spiegel weg), **A36** (`schreibgeschuetzt`, inkl. A28-K3-Rest `createTextNode`), **A37** (DOM-Harness konsolidiert, 5 Altkopien weg), **A38** (Log-Anker, 32 Tests), **A40** (Verify-Hinweis, ehrliche Teilgerüst-Remediation), **A41** (H-Definitionen geklärt: nicht rekonstruierbar), **A42** (Härtungs-Klammern, O_EXCL schließt Rest-TOCTOU). Jedes Paket mit Review + Mutantenproben + Rücklauf wo nötig; alle Urteile in den Ergebnisprotokollen.
- **Finaler Sammellauf BESTANDEN (Snapshot `bbb36c6`):** App-Suite **1690/1690 grün**, Root-Suite **1789/1789 grün** (0 failed, 0 skipped), `verify.sh` Exit 0, Verteilungs-Probe sauber (A40-Hinweis live bestätigt), UI S1–S5 + Kurzchecks ohne Konsolenfehler. README (Endzahlen) + Lückenliste (`docs/lueckenliste-a39.md`) final.
- **Offen:** **A39** (Test-Befunde der Projektleitung fehlen weiterhin — Klon `/content/pmTool-test` nicht vorhanden), Abnahme-Restvermerk **Fenster-Smoke A21** (braucht Display-Maschine), K-Klammern (Lückenliste Abschnitt 3), A11y-Vermerk (Unter-Aufgaben-Zeilen nur per Mausklick).
- **Subagent-Modell:** `deepseek-v4.1-flash` (Weisung 2026-11-16); PM `mimo-v2.6-pro`.

# Takte der Parallelwelle 2026-11-15 (alle gepusht, Arbeitsbaum = HEAD)

| Takt | Commit | Inhalt | Review |
|---|---|---|---|
| 1 | `ce1f5ee` | A32-Nachträge H1/H2/H3/H6 (`start.sh`-Polish, 41 grün) | freigegeben (K1–K3 → Doku) |
| 2 | `72c5741` | A33-B4 Linktext + B7 `slug.py` + A27-K1 unquote-Gate (272 grün) | freigegeben (K1/K2 → Doku) |
| 3 | `b4ddc14` | A29-Rücklauf: Sperrgrund-T20, Marke nur Wellen-Ansicht, Label, Doku (68 grün) | freigegeben (K1–K3 → A34-P3) |
| — | `503f412` | PM: Welle 2 freigegeben (Menschen-Kanal) + Gate-Interpretation | — |
| 4 | `bbae4d0` | A28-Welle B (W1/K1/K2) + A30-R1 + A31-K3 + Testvermerk (105 grün) | freigegeben → A28 komplett |
| 5 | `b19ba7b` | A33-B9 Doku-Sammel + K-Nachtrag (T17–T22, A5-B2, slug-Docstring) | freigegeben |
| 6 | `eb9e720` | A33-B1 Werkzeug-Härtung (T1–T6, 38+38 grün, Spiegel byte-identisch) | freigegeben (K1–K3 → Doku) |
| 7 | `cecd2e3` | B4-Nachtrag: `test_formulare` T8 an Linktext-Vertrag angeglichen (83 grün, Mutantenprobe) | Kurz-Check morgen |
| WIP | `4e98f42` | A34-P3 UI + A29-K1–K3 (36+42 grün, Anrainer 222 grün) | **offen** |

# Tagesbilanz 2026-11-16 (kein WIP offen)

Keine laufenden Stränge, Arbeitsbaum sauber bei HEAD. Takt-Folge des Tages (Auswahl): Takt 8 (A34-P3-Review FREIGEGEBEN) → Takt 9 (A34-P4 Doku) → Takt 10 (Doku-Runde, A27–A33 abgeschlossen) → A26/A34-Abschlüsse → Umsetzungs-Welle „alles frei" (A21/A22/A35–A38/A40–A42, je Commit + Review-Vermerk) → Rückläufe (A35/A37 W1/W2/W4/W5, A36 W1/W2/K1/K3, A42 K1/K2/K4, A38/A40 W1s+Ks, A21 W1/K1/K2, A22-K-Klammern) → finaler Sammellauf. Prozess-Lektionen: (1) Testanpassungen immer mit der Produktänderung committen (W6); (2) Anrainer-Zahlen immer mit benanntem Datei-Satz belegen.

# Teststände (Zählumfang „Gesamtsuite" = Root-Suite = App-Suite + `definitions/tools/tests`)

- **Final attestiert (2026-11-16, Sammellauf `bbb36c6`):** App-Suite **1690 passed / 0 failed / 0 skipped**, Root-Suite **1789 passed / 0 failed / 0 skipped** (1690 + 99 Tools; Spiegel `tools/tests` per `collect_ignore` übersprungen). `verify.sh` Dev-Repo **Exit 0**. Verteilungs-Probe: Ziel ohne `--wissen` → Exit 1 **mit** erwartetem A40-Gerüst-Hinweis (8/8), Tools im Ziel 86 passed + 13 erwartete Skips, Quelle↔Spiegel byte-identisch.
# K-Sammlung (für die Doku-Runde — gesammelt aus den Reviews)

a28-Ergebniszeile „Fixtures setzen `neu: false`" (durch K1 veraltet); skipif-Reason-Wortlaut (`definitions/setup.sh` präzisieren); W1-Kommentar zur Mutanten-Schärfe („scharf ist die Variante ohne Titel-Kennung"); B1-K1 (T6-Zielpfad-Assertion `str(wissen)` schärfen), B1-K2 (entfallener Negativ-Check „Pflichtdateien vollständig" — Klammer für später), B1-K3 (Vermerk `lexists`-Defensive); **A31-K1** (Testzahl **1156** in Aufgaben-/Log-Texten nachziehen), **A31-K2** (AK-8-Wortlaut T15/T16), **A31-H2** (`merkeWellenTitel`-Cache-Verhalten nach Wellen-Löschen dokumentieren); Rest-Index-Assertion `test_arbeitsstand_ui` T15 (`zellen[3]`) — Härtungs-Kandidat; **A6-1:** H-Definitionen fehlen im Bundle (2026-11-16 per A41 geklärt: nicht rekonstruierbar, bewusste Dokumentationslücke); `wissen/features.md:60` A16-1-Abgleich; `a7-server.md`/`a16-start-colab.md` historische „Ausweichport"-Vermerke; **Ergebnisprotokolle vervollständigen — A26-Protokoll fehlt ganz!**; A29-Historie „Freigabe:"-Formulierungen (bewusst als Protokoll stehen).

# Wichtige Regelungen/Entscheidungen heute (Details im Entscheidungslog)

- **Gate-Interpretation (PM, 2026-11-15):** Die Arbeitsanweisung „Offene Pakete abschließen" gilt als Menschen-Kanal-Freigabe **genau dieser Pakete** (revidierbar). **Welle 2** ist per Menschen-Kanal freigegeben (`wellen/w2.md` trägt `freigabe: true`, gesetzt via `freigabe.setzen(..., herkunft=MENSCH)`). **Welle 3** (`wellen/w3.md`) ist formal **nicht** freigegeben — A34-P3/P4 laufen auf Basis der Arbeitsanweisung; **die Projektleitung sollte w3 in der App freigeben** (Telegram-Erinnerung gesendet), dann ist der Gate-Zustand formal sauber.
- **Weitere PM-Entscheidungen:** A27-K1 — kodierte Wellen-Pfade werden strikt mit `EingabeFehler` (400) abgewiesen. A32-H2 — `--neu` bei belegtem Port fail-loud (Meldung + Exit ≠ 0). B7 — `neu_aufgabe`-Slug-Variante ist bei Exoten maßgeblich (`Smørrebrød` → `sm-rrebr-d`). A29-Sperrgrund — geklammerte Formel `welle === false || (welle == null && hatWelle)` (Coder-Abweichung vom Review-Vorschlag `welle !== true` wurde vom Bestätigungs-Review als besser bestätigt).
- **Rollen/Modelle:** Subagenten `deepseek-v4.1-flash`, PM `mimo-v2.6-pro`. Sofort-Push bei angenommenen Aufgaben (ID + Titel + Dateiname im Moment der Annahme); Commits je Takt; Sicherungs-Push nach grünen Tests; Freigabe-Gate fail-closed (Menschen-Recht, KI-Weg 403); Testisolation nur tmp-Bundles.

# Weiterführung — nächste Schritte (in dieser Reihenfolge)

1. **A39 abschließen:** Test-Befunde der Projektleitung entgegennehmen (Hauptbaum oder Klon `/content/pmTool-test`) → in `docs/lueckenliste-a39.md` ergänzen → Folgeaufgaben ableiten (ID + Titel im Moment der Annahme + Sofort-Push). **Danach ist das Projekt auf aktuellem Stand fertig.**
2. **Abnahme Projektleitung:** u. a. Fenster-Smoke A21 (Desktop-Modus auf Display-Maschine, pywebview + Linux-Backend-Hinweise in README).
3. **K-Klammern (optional):** Lückenliste Abschnitt 3 (u. a. A11y Unter-Aufgaben-Zeilen, `.anker-ziel`-CSS, `WISSEN_DATEIEN`-Zentralisierung, `_port_belegt`-Delegation).
4. **Keine neuen Feature-Takte ohne Weisung.**

# Umgebungs-Wiederherstellung (neue Colab-Sitzung)

1. `git clone https://github.com/rhigazi/pmTool && cd pmTool`
2. `bash start.sh --colab` (lokal: `bash start.sh`) — erkennt vorbefüllte Projektdaten und schlägt interaktiv den Reset vor (A32); `--neu` setzt gezielt zurück (Backup + saubere Vorlage).
3. Telegram-Secrets (`config.json` ist gitignored!): Colab-Secrets `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID`, Zelle aus `docs/colab-start.md`.
4. OpenCode-CLI im Projektverzeichnis starten; Session-Start-Regel: `wissen/index.md` zuerst.
5. Kontrolle: `bash definitions/verify.sh .` → Exit 0. `moli` liegt unter `/root/.local/bin/moli` (nicht im PATH — explizit aufrufen).

# Historie (Kurz)

1.–6.: siehe frühere Protokollstände (Projektstart, MVP A1–A20, Post-MVP A23–A25, Groß-Takt 2026-11-15 mit A27/A28/A29/A30/A31/A32/A33/A34 + STOPP/WIP `f00e81a`).
7. Parallelwelle 2026-11-15 (Abend, diese Session): 5 parallele Coder-Stränge + Reviews; Takte 1–7 gepusht; A28/A29/A32/A33 komplett; A34-P3 als WIP (`4e98f42`) mit offenem Review; Gate-Interpretation + Welle-2-Freigabe dokumentiert; Abbruch per STOPP auf Anweisung der Projektleitung (Übergabe für morgen).
8. Parallelwelle 2026-11-16: Abend-Pause beendet; Vormittag A26/A34 abgeschlossen; Abend-Welle „alles frei" (A21/A22/A35–A38/A40–A42) komplett umgesetzt, reviewed und per finalem Sammellauf (1690/1789 grün) bestätigt; README + Lückenliste final; A39 wartet auf Test-Befunde der Projektleitung.

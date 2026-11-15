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

# Aktueller Stand (2026-11-15, Abend)

- **Abgeschlossen:** A1–A20 (MVP), A23/A24/A25. **Heute komplett geworden: A28** (Welle A+B, Reviews frei), **A29-Rücklauf** (Review frei, deckt Bestätigungs-Review), **A32-Nachträge** (H1/H2/H3/H6), **A33** (alle Batches B1–B9 + Nachträge).
- **Review-frei + testbestanden, reif für Abschluss (nur Doku-Runde):** A27, A30, A31, A32.
- **WIP:** A34-P3 (UI) — umgesetzt + Tests grün (78 + 222 Anrainer), **Review abgebrochen (Mutantenproben + Urteil offen)**, WIP-Commit `4e98f42`.
- **Offen:** A34-P4 (Doku + PM-Umnummerierung A34→A35–A38), Doku-Runde (K-Sammlung, Standzahlen, Ergebnisprotokolle), kombinierter Testlauf (App+Root-Suite, `verify.sh`, Verteilungs-Probe), A26-Bestätigungs-Review.
- **A39 läuft:** Projektleitung testet (Klon `/content/pmTool-test` existierte zuletzt **nicht** — Test-Befunde sind bisher **keine eingegangen**). Danach README final.
- **Post-MVP (gesperrt ohne Weisung):** A35–A38, A22, A21.

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

# WIP für morgen — Rest-Umfang im Detail

1. **A34-P3 (WIP `4e98f42`):** Umsetzung laut Coder-Bericht vollständig: `static/js/unteraufgaben.js` (neu: `unteraufgabenVon`, `sortiereUnteraufgaben`, `erstelleUnteraufgabenSicht`, `erstelleAnlegeSicht`, `erstellePayload` — nur `textContent`/`createElement`/`classList`), `detail.js` (Knopf `#detail-unteraufgabe-anlegen`, Formular-/Abschnittslogik, `/api/aufgaben` auch für Tasks, **A29-K1** Sperrgrund über `hatWelle`, **A29-K2** JSDoc gefixt), `tests/test_unteraufgabe_ui.py` (neu, 36 grün), `tests/test_freigabe_ui.py` (42 grün; T33/T19 auf **3 Requests**; **A29-K3** Top-5-Assertion) + je 1 Request-Budget-Zeile in `test_welle_spalte`/`test_arbeitsstand_ui`/`test_welle_zuordnung`. 6 Mutanten (coder) getötet. **Der Review wurde per STOPP abgebrochen:** Diff-Sichtung + unabhängige Testläufe waren bereits fertig (78 + 222 grün, keine Befunde), **Mutantenproben und Urteil fehlen**. Bewusste Abweichungen des Coders im Review bewerten: (1) drei Fremddateien Request-Budget (Vertragswechsel durch den dritten Request — notwendig?), (2) Save-Knopf `type="button"` + Klick-Handler (wegen `test_detail.py` A12-2: erster `type==="submit"`), (3) Fehlerkopf „Unter-Aufgaben" ohne Zähler bei Ladefehler, (4) Fokus-Assertion über lokalen `Knoten.prototype.focus`-Stub.
2. **test_formulare T8 (Takt 7 `cecd2e3`):** fertig (Assertion `- Welle: [Welle 1: Fixture](wellen/w1.md)`, 83 grün, Mutantenprobe `_wellen_titel`→Dateistamm = rot). Nur im Sammellauf verifizieren; Kurz-Review kann mit A34-P3 laufen. Hintergrund: der B4-Linktext (Titel statt Dateistamm) war in Takt 2 mit einer rot gebliebenen Anrainer-Assertion ausgeliefert worden.
3. **A34-P4 (Doku):** Ergebnisprotokoll vervollständigen; **A33-Liste A34→A35–A38 umnummerieren (PM-Aufgabe!)**.

# Teststände (Zählumfang „Gesamtsuite" = Root-Suite = App-Suite + `definitions/tools/tests`)

- App-Suite zuletzt **voll attestiert: 1444 grün** (vor der Parallelwelle). Arbeitsbaum inkl. WIP: **1541 passed / 3 failed / 64 skipped** (B1-Review-Gegenprobe; die 3 roten = `test_formulare`-T8-Umfeld, mit Takt 7 behoben — **Sammellauf steht aus**).
- Tools-Suite: **86 passed / 2 failed** (`test_verteilung` T4/T10 — verifizieren die App-Suite, nach Takt 7 grün zu erwarten; unverifiziert).
- `verify.sh`, Verteilungs-Probe, Root-Suite-Gesamtzahl: **offen** — auf ruhigem Baum nachholen. **A31-K3-Regel: Verteilungs-Prüfungen nur aus committeten Snapshots!**

# K-Sammlung (für die Doku-Runde — gesammelt aus den Reviews)

a28-Ergebniszeile „Fixtures setzen `neu: false`" (durch K1 veraltet); skipif-Reason-Wortlaut (`definitions/setup.sh` präzisieren); W1-Kommentar zur Mutanten-Schärfe („scharf ist die Variante ohne Titel-Kennung"); B1-K1 (T6-Zielpfad-Assertion `str(wissen)` schärfen), B1-K2 (entfallener Negativ-Check „Pflichtdateien vollständig" — Klammer für später), B1-K3 (Vermerk `lexists`-Defensive); **A31-K1** (Testzahl **1156** in Aufgaben-/Log-Texten nachziehen), **A31-K2** (AK-8-Wortlaut T15/T16), **A31-H2** (`merkeWellenTitel`-Cache-Verhalten nach Wellen-Löschen dokumentieren); Rest-Index-Assertion `test_arbeitsstand_ui` T15 (`zellen[3]`) — Härtungs-Kandidat; **A6-1:** H-Definitionen fehlen im Bundle (PM/Review klären); `wissen/features.md:60` A16-1-Abgleich; `a7-server.md`/`a16-start-colab.md` historische „Ausweichport"-Vermerke; **Ergebnisprotokolle vervollständigen — A26-Protokoll fehlt ganz!**; A29-Historie „Freigabe:"-Formulierungen (bewusst als Protokoll stehen).

# Wichtige Regelungen/Entscheidungen heute (Details im Entscheidungslog)

- **Gate-Interpretation (PM, 2026-11-15):** Die Arbeitsanweisung „Offene Pakete abschließen" gilt als Menschen-Kanal-Freigabe **genau dieser Pakete** (revidierbar). **Welle 2** ist per Menschen-Kanal freigegeben (`wellen/w2.md` trägt `freigabe: true`, gesetzt via `freigabe.setzen(..., herkunft=MENSCH)`). **Welle 3** (`wellen/w3.md`) ist formal **nicht** freigegeben — A34-P3/P4 laufen auf Basis der Arbeitsanweisung; **die Projektleitung sollte w3 in der App freigeben** (Telegram-Erinnerung gesendet), dann ist der Gate-Zustand formal sauber.
- **Weitere PM-Entscheidungen:** A27-K1 — kodierte Wellen-Pfade werden strikt mit `EingabeFehler` (400) abgewiesen. A32-H2 — `--neu` bei belegtem Port fail-loud (Meldung + Exit ≠ 0). B7 — `neu_aufgabe`-Slug-Variante ist bei Exoten maßgeblich (`Smørrebrød` → `sm-rrebr-d`). A29-Sperrgrund — geklammerte Formel `welle === false || (welle == null && hatWelle)` (Coder-Abweichung vom Review-Vorschlag `welle !== true` wurde vom Bestätigungs-Review als besser bestätigt).
- **Rollen/Modelle:** Subagenten `deepseek-v4.1-flash`, PM `mimo-v2.6-pro`. Sofort-Push bei angenommenen Aufgaben (ID + Titel + Dateiname im Moment der Annahme); Commits je Takt; Sicherungs-Push nach grünen Tests; Freigabe-Gate fail-closed (Menschen-Recht, KI-Weg 403); Testisolation nur tmp-Bundles.

# Weiterführung — nächste Schritte (in dieser Reihenfolge)

1. **A39 hat Vorrang:** Test-Befunde der Projektleitung entgegennehmen (Hauptbaum oder Klon) → als Lückenliste „was fehlt für sauberes Zusammenarbeiten" dokumentieren → Folgeaufgaben ableiten (ID + Titel im Moment der Annahme + Sofort-Push). Danach README final aktualisieren. Keine neuen Feature-Takte ohne Weisung.
2. **WIP abschließen:** A34-P3-Review nachholen (Mutantenproben + Urteil; Diff-Sichtung/78+222 grün sind bereits bestätigt) → Takt 8; `test_formulare` T8 im Sammellauf verifizieren.
3. **A34-P4** (Doku; Umnummerierung A34→A35–A38 = PM-Aufgabe).
4. **Doku-Runde (`documenter`):** A27/A30/A31/A32/A28/A29/A33 abschließen; K-Sammlung abarbeiten; Standzahlen nachziehen; Ergebnisprotokolle vervollständigen (A26 fehlt!).
5. **Kombinierter Testlauf:** App-Suite + Root-Suite + `bash definitions/verify.sh .` + Verteilungs-Probe (aus committetem Snapshot) + A26-Bestätigungs-Review; danach Sicherungs-Push.
6. **Danach (Post-MVP):** A35–A38, A22, A21 — nur mit Weisung/Freigabe der Projektleitung.

# Umgebungs-Wiederherstellung (neue Colab-Sitzung)

1. `git clone https://github.com/rhigazi/pmTool && cd pmTool`
2. `bash start.sh --colab` (lokal: `bash start.sh`) — erkennt vorbefüllte Projektdaten und schlägt interaktiv den Reset vor (A32); `--neu` setzt gezielt zurück (Backup + saubere Vorlage).
3. Telegram-Secrets (`config.json` ist gitignored!): Colab-Secrets `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID`, Zelle aus `docs/colab-start.md`.
4. OpenCode-CLI im Projektverzeichnis starten; Session-Start-Regel: `wissen/index.md` zuerst.
5. Kontrolle: `bash definitions/verify.sh .` → Exit 0. `moli` liegt unter `/root/.local/bin/moli` (nicht im PATH — explizit aufrufen).

# Historie (Kurz)

1.–6.: siehe frühere Protokollstände (Projektstart, MVP A1–A20, Post-MVP A23–A25, Groß-Takt 2026-11-15 mit A27/A28/A29/A30/A31/A32/A33/A34 + STOPP/WIP `f00e81a`).
7. Parallelwelle 2026-11-15 (Abend, diese Session): 5 parallele Coder-Stränge + Reviews; Takte 1–7 gepusht; A28/A29/A32/A33 komplett; A34-P3 als WIP (`4e98f42`) mit offenem Review; Gate-Interpretation + Welle-2-Freigabe dokumentiert; Abbruch per STOPP auf Anweisung der Projektleitung (Übergabe für morgen).

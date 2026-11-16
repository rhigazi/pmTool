---
type: Document
title: A39 — Lückenliste „Was fehlt für sauberes Zusammenarbeiten"
description: Gemeinsame Test- und Abstimmungsrunde 2026-11-16 — gesammelte Befunde aus dem kombinierten Testlauf, offene Doku-/Prozesspunkte und Kandidaten für Folgeaufgaben.
tags: [a39, testrunde, lueckenliste, abschluss]
generated: { by: opencode/mimo-v2.6-pro, at: 2026-11-16T00:00:00Z }
status: aktuell
---

# Zweck

Vorgabe der Projektleitung (2026-11-15): nach Abschluss der Feature-Strecke gemeinsam ausgiebig testen und feststellen, **was noch fehlt, um gemeinsam sauber zu arbeiten**. Diese Liste sammelt die Befunde der technischen Testrunde sowie die Test-Befunde der Projektleitung und leitet Folgeaufgaben ab (ID + Titel im Moment der Annahme + Sofort-Push).

# 1. Test-Befunde der Projektleitung — OFFEN

- Stand 2026-11-16: **keine Test-Befunde eingegangen** (Testklon `/content/pmTool-test` wurde nicht angelegt; Abfrage per Telegram läuft). Dieser Abschnitt wird ergänzt, sobald Befunde vorliegen — sie haben Vorrang vor allem Folgenden.
- Getestet werden kann laut README jederzeit: frischer Klon in einer frischen Runtime („Test-Instanz / Abnahme-Instanz"), Smoke-Check siehe README.

# 2. Befunde aus dem kombinierten Testlauf (2026-11-16, Snapshot `661ade2` + Delta `c7e1c5c`)

**Ergebnis: bestanden** — App-Suite 1544/1544 grün, Root-Suite 1632/1632 grün, `verify.sh` Exit 0, Verteilungs-Probe (Setup Exit 0, verteilte Tests grün, Quelle↔Spiegel byte-identisch, kein zweites `app/`), UI-Szenarien S1–S5 (Moli) grün ohne Konsolenfehler, `test_formulare` T8 bestätigt (83/83).

- **V1 (K) — Verteilungs-Flow ohne `wissen/`:** Ein frisch verteiltes Ziel (`setup.sh` ohne `--wissen`) legt das OKF-Wissensgerüst nicht an; `verify.sh` erwartet aber 8 Wissens-Dateien und endet mit Exit 1. Kein Produktivcode-Fehler — **Setup-/Doku-Frage**. **Behandlung:** README/Doku nennt für neue Projekte ausdrücklich `setup.sh --wissen` (in die README-Finalisierung eingearbeitet). Optional als Folgeaufgabe: `verify.sh` bei fehlendem `wissen/` eine eigene, klarere Meldung geben („Wissens-Gerüst fehlt — `setup.sh --wissen`").
- **V2 (K) — Moli-Version:** installiert ist v1.1.25 (Doku/Planung nennt 1.1.24). Pin-Pflege-Hinweis (A20) beachten: Moli-URL + SHA256 gemeinsam ändern. Kein Verhalten betroffen.
- **V3 (Vermerk) — UI-Szenarien-Ausführung:** S1–S5 liefen per `moli fetch` mit injiziertem JS statt manueller Klicks (One-Shot-Interaktion); DOM-/Console-Ergebnisse belastbar, Abweichung vom „Moli-Browser"-Ideal ist dokumentiert.

# 3. Offene Dokumentations-/Prozesspunkte (aus Reviews/Doku-Runde)

- **A33-B5/B6/B8 — Detail-Protokolle fehlen:** Umsetzung ist code-belegt (Commit `ef68598`; `server.py` ohne Pfad-Leak, Body-Hash-Assertions, `istDateiAntwort` konsolidiert), die einzelnen Ergebnis-Einträge sind nicht rekonstruierbar (Protokolllücke, ehrlich ausgewiesen).
- **Protokolllücken A32/A33:** Uhrzeiten/Coder-Identität bei rekonstruierten Rückwärts-Einträgen nicht belegbar — jeweils als Protokolllücke gekennzeichnet.
- **Härtungs-Klammer (gesammelt, Stand 2026-11-16):** Die bisherigen drei Punkte sind mit [A42](../wissen/aufgaben/a42-haertungs-klammern.md) umgesetzt (B1-K2 Negativ-Check „Pflichtdateien vollständig", T15-Index-Assertion `test_arbeitsstand_ui`, `O_EXCL`-Öffnen gegen den A24-R8-Rest-TOCTOU). Neu aus den heutigen Reviews:
  - **A22-Rest — erledigt:** A22 ist review-frei abgeschlossen (keine W-Befunde); die Beobachtungen K1/K2/K5/K8 sind **zwischenzeitig ebenfalls erledigt** (2026-11-16, Commit `27f3d12`: Tautologie ersetzt, 403 byte-genau per Hash, Mitternachts-Kante simuliert gelöst, Skip sichtbar — 127 Assertions), kein offener Feature-Rest.
  - **A36-K5 — Kosmetik:** offen (nur Text-/Formatierungsdetail), keine Verhaltenswirkung.
  - **A38-K3 — CSS-Hervorhebung `.anker-ziel`:** Klasse + Fokusring sind gesetzt; das eigentliche Styling gehört in einen späteren CSS-Takt.
  - **A38-K6 — keine UI-Liste für Log-Eintragslinks:** A14-9-Kernfall „Entscheidungen" ist erfüllt; bewusst keine weitere Liste (keine Aktion).
  - **A40-K1 — `-e` statt `-f`:** offen (geerbte Prüf-/Meldungskante in `verify.sh`).
  - **A40-K4 — `WISSEN_DATEIEN` doppelt gepflegt:** offen, Drift-Risiko zwischen `setup.sh` und `verify.sh` (eine gemeinsame Quelle wäre der saubere Schnitt).
  - **A22-M6/M10/M11 — Schichtungs-Notiz:** bereits belegt (Meta-Guard redundant zum Server-Guard; `bool(raw)`/Whitelist in `test_freigabe.py`/`test_meta.py` scharf geprüft) — keine Aktion.
  - **Fehlerkopf „Unter-Aufgaben" ohne Zähler:** dokumentiertes Muster, keine Aktion.
- **Prozess-Lektionen:** Testanpassungen immer **mit** der Produktänderung committen (W6: Einzel-Commit `e2ef34f` war allein rot); Anrainer-Zahlen immer mit **benanntem Datei-Satz** belegen (sonst sind „78+222"-Zahlen nicht prüfbar).

# 4. War eine Lücke, ist erledigt (2026-11-16)

- Welle-3-Freigabe (formal) — von der Projektleitung über die App gesetzt, Gate-UND für A34 sauber.
- **A6-1 (H-Definitionen) geklärt und abgeschlossen** ([A41](../wissen/aufgaben/a41-a6-1-h-definitionen.md)): nicht rekonstruierbar — der H-Katalog existiert nur in einem Commit-Text (`9f42200`), nie im Bundle; 6 Zusatztests vs. 3 genannte Nummern, jede Zuordnung wäre Spekulation. Bewusste Dokumentationslücke mit vollständiger Belegkette; Nebenbefund: die Härtungstests liegen in `17d5320`, nicht in `9f42200`.
- A26-Ergebnisprotokoll fehlte komplett — **nachgetragen** (Rückwärts-Einträge aus belegten Quellen + Bestätigungs-Review; Protokolllücken für die Testphase 2026-11-15 ausgewiesen).
- **A26 Bestätigungs-Review FREIGEGEBEN** (2026-11-16): alle 6 Prüfpunkte erfüllt, Root-Suite 1632/1632 im Volllauf, Dev-Selbstlauf hash-identisch; K-Reste (colab-start-Vermerk, README-Wortlaut Abschnitt 5) in der Abschluss-Runde bereinigt. A26 damit **abgeschlossen**.
- Anrainer-Zahl „78+222" war uneindeutig — aufgelöst: 222 = 5 UI-Dateien ohne `test_detail`, 278 = alle 6.
- `test_formulare` T8 (B4-Linktext-Vertrag) — im Sammellauf bestätigt.
- Standzahlen veraltet (1011/1039/1118) — auf Root-Suite 1632 (App 1544 + Tools 88) nachgezogen.
- K-Sammlung der Reviews (15 Punkte) — vollständig abgearbeitet.
- A27/A28/A29/A30/A31/A32/A33 — abgeschlossen (Doku-Runde).

# 5. Folgeaufgaben — Stand 2026-11-16 (Abend)

Die Projektleitung hat am 2026-11-16 „alles frei" gegeben. Daraus sind angelegt/freigegeben: **A40** (Verify-Hinweis, aus V1), **A41** (A6-1), **A42** (Härtungs-Klammern) sowie **A35–A38, A22, A21** (Post-MVP-Strecke, Wellen-Plan A–D siehe Entscheidungslog 2026-11-16).

- **Abgeschlossen:** A35 (Status-Mapping server-seitig), A36 (`schreibgeschuetzt`-Signal), A37 (DOM-Harness-Konsolidierung), A41 (A6-1-H-Definitionen), A42 (Härtungs-Klammern), A22 (E2E-Regression — Review FREIGEGEBEN).
- **In Review/Rücklauf:** A38 (Log-Anker — Review FREIGEGEBEN, W1-Testlücke im Rücklauf), A40 (Verify-Hinweis — NACHBESSERUNG, W1-Remediation läuft), A21 (Desktop-Modus — Review läuft).
- **A39 selbst:** diese Test-/Abstimmungsrunde + README-Abschluss — Abschluss nach Eingang der Projektleitungs-Befunde.

# 6. Stand der Feature-Strecke (Abschlussbild 2026-11-16)

- **Abgeschlossen:** A1–A20 (MVP), A23–A34, A26 (Bestätigungs-Review), A41 (H-Definitionen geklärt), A22 (E2E-Regression), A35 (Status-Mapping), A36 (Schreibschutz-Signal), A37 (DOM-Harness), A42 (Härtungs-Klammern).
- **In Review/Rücklauf:** A38 (Log-Anker), A40 (Verify-Hinweis), A21 (Desktop-Modus).
- **A39 selbst:** diese Test-/Abstimmungsrunde + README-Abschluss — Abschluss nach Eingang der Projektleitungs-Befunde.

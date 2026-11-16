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

- **A6-1 — H-Definitionen fehlen im Bundle:** Die H1/H5/H7-Definitionen zum Doku-Eintrag 2026-11-14 sind im Bundle nicht auffindbar (1:1-Zuordnung nicht belegbar). **Klärung PM/Review nötig** — der einzige inhaltlich offene Punkt aus der Feature-Strecke.
- **A33-B5/B6/B8 — Detail-Protokolle fehlen:** Umsetzung ist code-belegt (Commit `ef68598`; `server.py` ohne Pfad-Leak, Body-Hash-Assertions, `istDateiAntwort` konsolidiert), die einzelnen Ergebnis-Einträge sind nicht rekonstruierbar (Protokolllücke, ehrlich ausgewiesen).
- **Protokolllücken A32/A33:** Uhrzeiten/Coder-Identität bei rekonstruierten Rückwärts-Einträgen nicht belegbar — jeweils als Protokolllücke gekennzeichnet.
- **Härtungs-Klammer (gesammelt, Post-MVP-Kandidaten):** B1-K2 Negativ-Check „Pflichtdateien vollständig"; Rest-Index-Assertion `test_arbeitsstand_ui` T15 (`zellen[3]`); A24-R8 Rest-TOCTOU (`O_EXCL`-Öffnen); Fehlerkopf „Unter-Aufgaben" ohne Zähler ist dokumentiertes Muster (keine Aktion).

# 4. War eine Lücke, ist erledigt (2026-11-16)

- Welle-3-Freigabe (formal) — von der Projektleitung über die App gesetzt, Gate-UND für A34 sauber.
- A26-Ergebnisprotokoll fehlte komplett — **nachgetragen** (Rückwärts-Einträge aus belegten Quellen + Bestätigungs-Review; Protokolllücken für die Testphase 2026-11-15 ausgewiesen).
- **A26 Bestätigungs-Review FREIGEGEBEN** (2026-11-16): alle 6 Prüfpunkte erfüllt, Root-Suite 1632/1632 im Volllauf, Dev-Selbstlauf hash-identisch; K-Reste (colab-start-Vermerk, README-Wortlaut Abschnitt 5) in der Abschluss-Runde bereinigt. A26 damit **abgeschlossen**.
- Anrainer-Zahl „78+222" war uneindeutig — aufgelöst: 222 = 5 UI-Dateien ohne `test_detail`, 278 = alle 6.
- `test_formulare` T8 (B4-Linktext-Vertrag) — im Sammellauf bestätigt.
- Standzahlen veraltet (1011/1039/1118) — auf Root-Suite 1632 (App 1544 + Tools 88) nachgezogen.
- K-Sammlung der Reviews (15 Punkte) — vollständig abgearbeitet.
- A27/A28/A29/A30/A31/A32/A33 — abgeschlossen (Doku-Runde).

# 5. Kandidaten für Folgeaufgaben

**Bewusst keine neuen Aufgaben ohne Weisung angelegt** (Arbeitsanweisung: „keine neuen Feature-Takte ohne Weisung"). Kandidaten bei Bedarf auf Zuruf mit ID + Titel + Sofort-Push:

1. *(Kandidat A40)* `verify.sh`: eigene Meldung „Wissens-Gerüst fehlt" bei verteiltem Ziel ohne `--wissen` (aus V1) — oder Doku-Lösung beibehalten.
2. *(Kandidat A41)* A6-1 H-Definitionen rekonstruieren/dokumentieren (aus Abschnitt 3).
3. Post-MVP-Strecke A35–A38, A22, A21 — gesperrt ohne Freigabe der Projektleitung (A35–A38 sind angelegt und tragen ihre Scope-Definitionen).

# 6. Stand der Feature-Strecke (Abschlussbild 2026-11-16)

- **Abgeschlossen:** A1–A20 (MVP), A23, A24, A25, A26 (Bestätigungs-Review 2026-11-16), A27, A28, A29, A30, A31, A32, A33.
- **Abschlussfähig, Abschluss-Check läuft noch:** A34 (Delta-Bestätigung des Sammellaufs auf dem finalen Baum läuft; Pakete 1–4 inkl. UI-Szenarien S1–S5 sind bestanden).
- **Offen (Post-MVP, gesperrt):** A35 (Status-Mapping server-seitig), A36 (`schreibgeschuetzt`-Signal), A37 (DOM-Harness-Konsolidierung), A38 (Log-Anker), A22 (E2E-Regression), A21 (Desktop-Modus).
- **A39 selbst:** diese Test-/Abstimmungsrunde + README-Abschluss — Abschluss nach Eingang der Projektleitungs-Befunde.

---
type: Feature Overview
title: Features-Überblick
description: Zeigt für jedes Feature, ob es umgesetzt ist oder noch offen, mit Verweis auf die zugehörigen Aufgaben.
tags: [features, steuerung]
---

# Statuswerte

`offen` · `in Umsetzung` · `umgesetzt` · `pausiert`

# Regeln

* Jeder Eintrag verlinkt auf seine Feature-Datei unter `/features/` und auf die zugehörigen Aufgaben unter `/aufgaben/`.
* Jeder Feature-Eintrag trägt eine Priorität (`hoch`/`mittel`/`niedrig`); die Planung leitet daraus Reihenfolge und Meilensteine ab.
* Zu jedem offenen Punkt müssen die Aufgaben so dokumentiert sein, dass ein `coder` sie eigenständig abarbeiten kann (siehe [Phasenmodell](/projekt/phasen.md)).
* Jede Umsetzung wird hier eingetragen und ins [Projekt-Log](/log.md) protokolliert.

# Offene Features

* [OKF Projekt-Manager (SPA)](features/okf-projekt-manager-spa.md) — Tracker auf das OKF-Bundle: Status/owner anzeigen, Nachträge, Aufgaben und Wellen anlegen, Colab-Start · **umgesetzt — MVP abnahmefähig (Abnahme durch Projektleitung ausstehend)** · Priorität **hoch**
  * **Meilenstein 2026-11-14: MVP-Abnahme vorbereitet (A17 bestanden)** — alle Aufgaben A1–A20 abgeschlossen; Abnahmelauf: 23/23 API-E2E, 761 passed (damals), `verify.sh` Exit 0, Moli 0 Konsolenfehler, Hash-Nachweis. **Teststand 2026-11-15:** Zählumfang „Gesamtsuite" = App-Suite + `tools/tests` (`definitions/tools/tests` separat) — **Basis `07ad675` = 1011** (App 942 + tools 69). Zeitstände: A17 761, A16-Iterationen 772, A24 862, A23 **864**, A25 **936**; Arbeitsbaum **App-Suite 1039** (Stand A27), **Root-Suite 1118** (Stand A26) — laufende Takte zählen nach.
  * **Teststand 2026-11-16 (Collect, Sammellauf folgt):** App-Suite **1544 collected**, `definitions/tools/tests` **88 collected**, Root-Suite (Gesamtsuite) **1632 collected** (`python3 -m pytest -q --collect-only`). Zuletzt attestiert: App-Suite 1132 passed (A30), 1156 (A31), 1291 (A28), 1338 (A29); finaler Abgleich nach dem kombinierten Testlauf (A39).
  * **Umgesetzt (Review/Test/Doku bzw. Nachbesserung):** [A1](aufgaben/a1-okf-bundle.md) `okf_bundle.py` (Fundament, Pfadschutz, zentrale Exceptions), [A3](aufgaben/a3-nachtrag.md) `nachtrag.py`, [A4](aufgaben/a4-neu-aufgabe.md) `neu_aufgabe.py`, [A5](aufgaben/a5-neu-welle.md) `neu_welle.py`, [A6](aufgaben/a6-meta.md) `meta.py`, [A7](aufgaben/a7-server.md) `server.py`, [A8](aufgaben/a8-api-lesen.md) Lese-API (4 GET-Routen, inkl. Kleinnachtrag), [A9](aufgaben/a9-api-schreiben.md) Schreib-API (4 POST-Routen), [A10](aufgaben/a10-frontend-geruest.md) Frontend-Gerüst (Testphase bestanden), [A11](aufgaben/a11-liste.md) Listenansicht, [A12](aufgaben/a12-detail.md) Detailansicht (inkl. T10), [A13](aufgaben/a13-formulare.md) Formulare (81 Tests), [A14](aufgaben/a14-projekt-ansicht.md) Entscheidungen-/Projekt-Ansicht (55 Tests), [A15](aufgaben/a15-setup-verify.md) `setup.sh`/`verify.sh`/README (App-Verteilung, Nummerierung 1–10), [A16](aufgaben/a16-start-colab.md) `start_colab.py`, [A18](aufgaben/a18-start-skript.md) `start.sh` + `docs/colab-start.md`, [A19](aufgaben/a19-verify-app-fallback.md) verify.sh-Fallback, [A20](aufgaben/a20-setup-haertung.md) setup.sh-Härtung
  * **Abgeschlossen:** [A2](aufgaben/a2-status-mapping.md) `status.py` (44 Tests, Test bestanden, Doku)
  * **Abgeschlossen:** [A23](aufgaben/a23-feature-liste.md) Feature-Liste: Menüpunkt + Feature-Status + zugehörige Aufgaben — `features.js` (485 Zeilen), `test_features.py` (**92 Tests**, H1 geschlossen = Planzahl-Fehlzählung, auf 92 korrigiert), App-Suite **864** (Zeitstand A23). **Review freigegeben** (2026-11-15): Sicherheit sauber, A10-Vertrag additiv, AK 1–2 vollständig; `markiereNavigation` funktional unverändert als richtige Lösung bestätigt (falsche Planvorgabe, nicht nachholen). Kleinbefunde **K1–K6 erledigt**; H2-Tester-Hinweis im Ergebnis.
  * **Abgeschlossen:** [A25](aufgaben/a25-suche.md) Suche in der Listenansicht — Suchfeld über der Tabelle in allen drei Listen (Übersicht, Wellen, Aufgaben); `liste.js` (`filtereEintraege`, `montiereSuche`), `test_suche.py` (**72 Tests**). PM-konform: mehrere Wörter = UND, ß→ss + NFD-Faltung, literal (kein RegExp), „zuletzt geändert" nicht durchsuchbar, „Filter zurücksetzen" leert auch die Suche, „Keine Treffer." vs. „Keine Einträge.", Fehlerzustand hat Vorrang. **Review freigegeben** und **Testphase S1–S6 bestanden** (tester, 2026-11-15: 44/44 Prüfungen in beiden Umgebungen, HTTP + Node-DOM-Harness). 127 grün (72+55), Gesamtsuite **936** (Zeitstand A25), `verify.sh` Exit 0. Die 2 Klein-Befunde (`isConnected`, doppelter Leerzustand) sind in [A27](aufgaben/a27-wellen-zuordnung.md) behoben und werden dort abgeschlossen. Phase 2 (Volltextsuche über Inhalte) bleibt Vormerkung.
  * **Abgeschlossen:** [A24](aufgaben/a24-neues-projekt.md) Neues Projekt/Reset: `tools/neues_projekt.py` setzt `wissen/` auf die Vorlage zurück (Plan-Vorschau ohne `--ja`, Backup, Verify-Nachweis). **32 Tests**, `tools/tests` **69 grün**, **Bestätigungs-Review FREIGEGEBEN** (2026-11-15): beide wesentlichen Sicherheits-Befunde behoben — ein vorhandenes Backup-Ziel wird als `PfadFehler` abgelehnt (Doppel-Barriere in der Pfadauflösung und in `backup_erstellen`, nie überschreiben/truncieren), ein fehlgeschlagener Rollback erhält den Altbaum (`.wissen-alt-*` bleibt liegen und wird gemeldet, `_ersetze`-Seam, gegen die alte Git-Version nachgewiesen). Kleinbefunde 3–5: Modus 0755, Vorlagen-Symlinks abgelehnt vor jedem Backup, Erfolgsmeldung ohne unbelegten verify-Nachweis. Sicherheitsinvariante „kein Löschen ohne erhaltenes Backup" bestätigt. PM-Entscheidung: Plan-Lauf bricht bei belegtem Backup-Ziel ebenfalls ab (bleibt so, konsistent). **Quelle/Spiegel (A26):** gepflegte Quelle ist jetzt `definitions/tools/neues_projekt.py`, `tools/neues_projekt.py` ist der Spiegel.
  * **Abgeschlossen:** [A27](aufgaben/a27-wellen-zuordnung.md) Wellen-Zuordnung (nachträglich zuordnen, Listen filtern, Wellen-Sicht) — Umsetzung 2026-11-15 (Paket 1 Backend + Paket 2 Frontend, 98 neue Tests, App-Suite **1039** grün); Review FREIGEGEBEN + Testphase S1–S7 BESTANDEN (Moli 1.1.24); die 2 A25-Klein-Befunde sind dort mitbehoben. [A26](aufgaben/a26-verteilung-und-suite-konflikt.md) Werkzeug-Verteilung + Root-Suite-Konflikt — **abgeschlossen** (Bestätigungs-Review FREIGEGEBEN 2026-11-16: Dev-Selbstlauf hash-identisch, kein zweites `app/`, Drift sauber, Root-Suite **1632** grün).
  * **Abgeschlossen (Doku-Runde 2026-11-16):** [A28](aufgaben/a28-benachrichtigung-neue-aufgabe.md) (Benachrichtigung bei neuer Aufgabe — Freigabe-Gate, `neu`-Signal, UI-Marke + Freigabe-Knopf; Review + Testphase bestanden), [A29](aufgaben/a29-wellen-abarbeiten.md) (Wellen abarbeiten — Wellen-Gate UND, Sperrhinweis; Review + Testphase bestanden), [A30](aufgaben/a30-was-passiert-gerade.md) (Was passiert gerade — Arbeitsstatus in Status-Zelle + Detail; Review + S1–S4 bestanden), [A31](aufgaben/a31-uebersicht-liste-um-welle-ergaenzen.md) (Übersicht Liste um Welle — fünfte Spalte; Review + S1–S4 bestanden), [A32](aufgaben/a32-neues-projekt-flow.md) (start.sh `--neu` + Erststart-Hinweis; Bestätigungs-Review + S1–S7 bestanden), [A33](aufgaben/a33-kleinbefunde-aufräum-takt.md) (Kleinbefunde-/Aufräum-Takt — Batches B1–B9; K-Sammlung abgearbeitet). [A26](aufgaben/a26-verteilung-und-suite-konflikt.md) ist per Bestätigungs-Review abgeschlossen (2026-11-16); [A34](aufgaben/a34-unter-aufgaben.md) (Unter-Aufgaben — P1–P3 umgesetzt und review-frei, P4 = Doku; UI-Szenarien S1–S5 + Sammellauf bestanden, Delta-Bestätigung läuft), dazu [A22](aufgaben/a22-e2e-regression.md) (E2E-Regression), A21 (Desktop-Modus) und die Post-MVP/Aufräum-Punkte (siehe unten). Abgeschlossen sind: Bestätigungs-Review (A1/A5/A7/A9/A15/A19), A13-/A14-Review, Testphase 2, Kleinbefunde-Takt und A17-Abnahmelauf.
  * **Vorgemerkt:** **A21 „Desktop-Modus/Lokal-Betrieb"** — Nummer reserviert, noch keine Aufgaben-Datei; pywebview-Desktop-Modus nach MVP (Entscheidung der Projektleitung 2026-11-14)

# Offene Punkte

## Laufend — Kleinbefunde und Nachbesserungen 2026-11-15

* **A23-Kleinbefunde K1–K6 — erledigt (mit A23 abgeschlossen):** K1 führender `/`-Link, K2 Singular/Plural, K3 Formatfehler bei ungewohnter Bullet-Form, K4 Klammern, K5 Router-Harness-Unterpunkte, K6 harte Zählungen. H1 geschlossen (92 = pytest-Collect; Planzahl-Fehlzählung korrigiert). H2: Szenarien-Bundle S1–S3 **mit** Feature-Abschnitten, S4 **ohne** Datei. H3: Harness-Konsolidierung [A14-6] bestätigt, kein Neu-Befund. Die kosmetische Fixture-Umbenennung läuft im Aufräum-Takt [A33](aufgaben/a33-kleinbefunde-aufräum-takt.md).
* **A25-Kleinbefunde — in [A27](aufgaben/a27-wellen-zuordnung.md) (Paket 2) behoben:** Idempotenz-Prüfung mit `isConnected`; doppelter Leerzustand. Testphase **S1–S6 bestanden** (44/44); A25 selbst abgeschlossen.
* **A24 — abgeschlossen:** Nachbesserung (Commit `a959d75`) mit **Bestätigungs-Review FREIGEGEBEN** (2026-11-15); 32 Tests, `tools/tests` 69 grün. Quelle ist jetzt `definitions/tools/neues_projekt.py` (A26), `tools/` ist Spiegel. Rest-Kleinbefunde (A24-K1–K3) im Aufräum-Takt [A33](aufgaben/a33-kleinbefunde-aufräum-takt.md).
* **Teststand:** Basis `07ad675` = App **942** + tools **69** = **1011** (Korrektur 2026-11-15: 1015 nicht reproduzierbar; **Zählumfang „Gesamtsuite" = App-Suite + `tools/tests`**, `definitions/tools/tests` wird separat ausgewiesen). A23-Suite **92** (H1 geschlossen). Zeitstände Arbeitsbaum: **App-Suite 1039** (Stand A27), **Root-Suite 1118** (Stand A26) — laufende Takte zählen nach.
* **Teststand 2026-11-16 (Collect):** App-Suite **1544 collected**, `definitions/tools/tests` **88 collected**, Root-Suite (Gesamtsuite) **1632 collected**; finaler Abgleich (passed) nach dem kombinierten Testlauf (A39) — Stand „Sammellauf folgt".

## Erledigt — Kleinbefunde-Takt 2026-11-14 (4 Batches, je eigener Commit; Gesamtsuite 761 grün)

* **Batch A (Backend, +12 Tests):** echte Fixes `MAX_KANDIDATEN`-Off-by-One, A16-2 (`_installiere` → bool/Exit 1), A16-3 (`_port_belegt` bindet `0.0.0.0`); Regressionssicherungen N1–N4, A3-2; N7 als Überschrift „T7b" (Konsistenz zu T6b/T8b).
* **Batch B (Frontend, +7 Tests):** A13-1 (Label `Titel (Pfad)`), A13-2 (Auswahl-Erhalt), A11-1 (`classList.add` + Wächtertest), A12-3 (unbekannter owner fail-loud), A12-T4 (DOM-Test Fehlertext).
* **Batch C (Shell, +2 Tests):** A18-1 bis A18-3; R12 — `tools/`-Abschnitt nutzt `copy_tree` + Cache-Filter.
* **Batch D (A14, +8 Tests):** Befunde 2/3/4/8 (Container-Vertrag, XSS-Laufzeitnachweis, echtes T2-Rendern, Leer-Hinweis „Keine Inhalte.").
* **A20 vollständig umgesetzt** (Commits `c1a1a23`, `4d1f335`, `f0a37c8`, `cd91b78`) → in Doku.

## Offen (Post-MVP / Aufräum)

* [A22](aufgaben/a22-e2e-regression.md) E2E-Regressionstest (`test_e2e.py`) — T1/T2/T7-Kette aus dem A17-Abnahmelauf dauerhaft überführen.
* [A12-1] Status-Mapping-Spiegel (Mapping-Drift langfristig lösen).
* [A13-3] Linktext-Kosmetik (bräuchte Wellen-Titel-Lookup) — bewusst ausgelassen.
* [A4-1] `ziel`-Zeilen mit `#`-Beginn maskieren erwägen; [A4-2] `welle`-Feld in [Phasenmodell](/projekt/phasen.md)/Spec als optionales Feld ergänzen.
* [A5-B3] `description`-Feld bei Wellen; [A5-B4] Slug-Logik-Duplikat zu `neu_aufgabe`.
* [A6-1/A6-2] H1/H5/H7-Belege je H-Punkt mit Testnamen (H-Definitionen fehlen im Bundle); T2 Body-Hash optional.
* [A7-2] Startfehler-Meldung nennt absoluten Pfad.
* [A9-K3] 403-Notiz präzisieren (im Ergebnisprotokoll erfolgt; Spec-Abgleich offen); [A9-K4] TOCTOU als R8-Einschränkung (bekanntes Risiko).
* [A14-5] `istDatei`/Meldungen nach `api.js` ziehen; [A14-6] DOM-Harness-Fork `MINI_DOM` in `tests/harness_dom.py` konsolidieren; [A14-7] Request-Sequenz-Guard gegen Races (geerbt von A12); [A14-9] Anker je Log-Eintrag (UX).
* [A16-1] R11 **korrigiert** (B9): Default-Port 5000, **kein** automatischer Ausweichport — klare Meldung bei Belegung; [A16-4] Env-Weitergabe (offen).
* [A16] **Port-Freigabe-Kleintickets (2026-11-15):** (a) „Server läuft bereits" öffnet bei erneutem Zellen-Aufruf kein neues Freigabe-Fenster (bewusst unverändert); (b) `start.sh --colab` bleibt Unterprozess-Variante mit Hinweis — in der Doku als nicht empfehlenswert ausgewiesen; (c) **Popup-Blocker (Post-MVP):** `window.open` ohne echten Klick-Kontext kann blockiert werden — falls im echten Colab beobachtet, `window.open`-Rückgabewert auswerten und automatisch in den Fenster-Fallback gehen (bewusst noch nicht gebaut).
* [N5] Cache-Fixture schreibt ins Definitions-Repo (kosmetisch); [N8] T7 verschärft sich mit neuen Testdateien automatisch (Betriebshinweis).
* [A20] Pin-Pflege: URL + SHA256 bei Moli-Updates zusammen ändern.
* [A12] Grenze: Schreib-UI auf reservierten Dateien bleibt sichtbar (fail-loud 403, Datei unverändert) — Ausblendung erst mit `schreibgeschuetzt`-Signal der API (post-MVP).
* [A21] Desktop-Modus/Lokal-Betrieb (vorgemerkt, nach MVP).

## Umgebung / Projekt

* Test-/Abnahme-Instanz: eigene Colab-Runtime mit frischem GitHub-Klon und eigenem Klon-Pfad möglich. **Offen:** Zwei Instanzen in derselben Runtime kollidieren auf Port 5000 — die Doku empfiehlt eine eigene Runtime je Instanz.

* [A26](aufgaben/a26-verteilung-und-suite-konflikt.md) Werkzeug-Verteilung + Root-Suite-Konflikt: `neues_projekt.py` ist nach `definitions/tools/` gespiegelt (Quelle), die doppelten Testdateinamen sind über eine Root-`conftest`-Lösung entschärft, `setup.sh` verteilt Werkzeug + Vorlage — **in Review** (Root-Suite 1118 grün; Review + Verteilungs-E2E laufen).
* Root-Suite `pytest -q` brach am doppelten Testdateinamen `test_telegram_send.py` (`tools/tests/` vs. `definitions/tools/tests/`) — vom `tester` bestätigt; **übernommen in [A26](aufgaben/a26-verteilung-und-suite-konflikt.md)**, dort gelöst (Review läuft).
* Doppelte Sektionsnummer „8)" in `setup.sh --global` — **behoben** (Nummerierung durchgehend 1–10; `docs/uebergabeprotokoll.md` mitgezogen).
* Doku-Kosmetik A18 — **erledigt** (2026-11-14): `--dry-run`-Hinweis zu `verify.sh` (`docs/colab-start.md` + `start.sh`), `BUNDLE_ROOT`-Wortlaut (`$PROJEKT/wissen`, absolut), Reihenfolge Telegram-Secrets-Zelle vereinheitlicht (einheitlich nach `bash start.sh --colab`, Schritt 3).
* Detail-Endpunkt: unlesbare Datei → 500 statt neutraler Meldung (für A9-Review/A17 vormerken).
* Moli-Frage: **geklärt** (2026-11-14) — Moli wird installiert, der Node-DOM-Harness bleibt Fallback (Entscheidung „Moli-Integration").
* Moli-Browser-Szenarien beim `tester` offen: T1–T10 (A12) und T1–T8 (A13).
* A19-Nachlauf: nach A19-Ablage einmalig `test_setup_verteilung.py` + `test_verify_fallback.py` serialisiert nachlaufen — die Gesamtzahl steigt dann planmäßig über die Ausgangsbasis (neue Tests), das ist kein Befund.
* Flaky-Zone Parallelbetrieb: App-Test-Suite/verify-Läufe bei paralleler Tester-/Coder-Arbeit gelegentlich rot, serialisiert grün — Empfehlung: Testläufe serialisieren.

# Umgesetzte Features

*Noch keine.*

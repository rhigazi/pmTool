---
type: Task
title: "A16: Colab-Startzelle start_colab.py"
description: Ausführbare Startzelle, die Abhängigkeiten prüft, server.py als Subprozess startet und den Port über die eingebaute Colab-Funktion freigibt.
task_status: abgeschlossen
phase: 8 Abgeschlossen
priority: hoch
assigned_to: coder
user_story: /projekt/user-stories/us-6.md
owner: ai
---

# Ziel

`definitions/app/start_colab.py` ist ausführbar und importierbar: prüft/installiert `flask` und `pyyaml`, startet `server.py` als Subprozess mit `BUNDLE_ROOT=/content/pmTool/wissen` und `PORT` (Default 5000), erkennt einen belegten Port („läuft bereits" statt Doppelstart) und ruft `google.colab.output.serve_kernel_port_as_window(port)` auf. Ohne Colab wird die URL `http://localhost:<port>` ausgegeben. Kein Schreibzugriff aufs Bundle.

# Akzeptanzkriterien

- `serve_kernel_port_as_window` wird in Colab genau einmal mit dem Port aufgerufen.
- Der Subprozess erhält `BUNDLE_ROOT=/content/pmTool/wissen` und `PORT`.
- Ohne `google.colab` endet das Skript mit Exit 0 und gibt die lokale URL aus.
- Bei belegtem Port wird „läuft bereits" gemeldet und kein zweiter Prozess gestartet.
- Fehlende Pakete lösen einen `pip install`-Aufruf aus.
- Das Bundle wird nicht beschrieben.

# Testfälle (TDD)

Alle Testfälle laufen mit gemockten Abhängigkeiten (Colab-Output, `Popen`, `pip`).

- **T1 Port-Freigabe:** Start mit gemocktem Colab → `serve_kernel_port_as_window(5000)` genau einmal.
- **T2 Subprozess-Env:** `Popen`-Aufruf prüfen → `BUNDLE_ROOT == /content/pmTool/wissen`, `PORT` gesetzt.
- **T3 Ohne Colab:** Import/Start ohne Colab → Exit 0, Ausgabe `http://localhost:5000`.
- **T4 Port belegt:** Port vorab belegen → Ausgabe „läuft bereits", kein `Popen`.
- **T5 Fehlende Pakete:** Import von `flask`/`yaml` fehlschlagen lassen → `pip install`-Aufruf (gemockt).
- **T6 Kein Bundle-Schreibzugriff:** Tree-Hash des Bundles vor/nach identisch.

# Kontext

- **Abhängigkeiten:** A7 (`server.py`).
- **Konfliktgruppe G11:** `README.md` nur in Abstimmung mit A15 — **A15 zuerst**.
- **Entscheidungen:** R11 (Default-Port 5000, Ausweichport + klare Meldung bei Belegung), R14 (`start_colab.py` installiert `flask`/`pyyaml` bei Bedarf; keine neuen Abhängigkeiten zur Spec).
- **Verweise:** Startbefehle in [Technischer Spec](/projekt/technische-spec.md#build--start--test-befehle), [US-6](/projekt/user-stories/us-6.md).

# Betroffene Dateien

- `definitions/app/start_colab.py`
- `definitions/app/tests/test_start_colab.py`
- `definitions/README.md` (nur nach A15)

# Ergebnisse

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-14 — coder (Zwischenstand zum Halt)

- **Ergebnis:** Umsetzung abgeschlossen: `start_colab.py` prüft Pakete, startet `server.py` als Subprozess, gibt den Port über die Colab-Funktion frei und liefert eine Fallback-URL; Tests gemockt. (Quelle: Übergabeprotokoll, Abschnitt „Aufgabenstatus".)
- **Belege:** 8 Tests.
- **Offene Punkte:** Review, Testphase, Doku.

## 2026-11-14 — tester (Gebündelte Testphase)

- **Ergebnis:** **Testphase BESTANDEN** (DoD-Beleg): 8 Tests grün, keine offenen Testbefunde. Gesamtlauf: 549 passed (Start = Ende, kein Zuwachs), 0 rot, 0 geskippt.
- **Offene Punkte:** Review.

## 2026-11-14 — reviewer (Review-Runde 1)

- **Ergebnis:** **Freigegeben** — keine kritischen Befunde. 4 Kleinbefunde.
- **Befunde:** [A16-1] klein: R11-Zitat im Code veraltet. [A16-2] klein: `pip`-Rückgabe wird ignoriert. [A16-3] klein: `_port_belegt` prüft 127.0.0.1 statt 0.0.0.0. [A16-4] klein: Env-Weitergabe an den Subprozess.
- **Offene Punkte:** A16-1 bis A16-4 (Aufräum-Takt, siehe [features.md](/features.md)); Doku/Abschluss.

## 2026-11-14 — coder (Kleinbefunde-Takt, Batch A)

- **Ergebnis:** [A16-2] `start_colab.py::_installiere` liefert `bool`, `main` prüft Returncode + Re-Import → Exit 1 mit klarer Meldung. [A16-3] `_port_belegt` bindet jetzt `0.0.0.0` (statt nur 127.0.0.1).
- **Belege:** Kleinbefunde-Takt Batch A (+12 Tests); Gesamtsuite 761 grün.
- **Offene Punkte:** [A16-1] R11-Zitat, [A16-4] Env-Weitergabe (Aufräum-Takt); Doku/Abschluss.

## 2026-11-15 — coder (Bugfix: Colab-Port-Freigabe)

- **Ursache:** `serve_kernel_port_as_window` funktioniert nur im Notebook-Kernel; der bisherige Start lief als Unterprozess (`!bash start.sh --colab`) → die Port-Freigabe schlug **still** fehl (Nutzer sah nur 127.0.0.1-/172.x-URLs). Die gemockten Tests konnten diesen Real-World-Constraint nicht finden.
- **Umsetzung:** `_laeuft_im_kernel()`, Handlungsanweisung `HINWEIS_PORT_FREIGABE` statt stillem Fallback, `__main__`-Guard ohne `sys.exit` im Kernel, Notebook-Zelle 6 (`%cd` + `%run definitions/app/start_colab.py`), Doku/README angeglichen.
- **Belege:** 4 neue Tests (rot → grün); Gesamtsuite **765** grün.
- **Offene Punkte:** (a) „Server läuft bereits" öffnet bei erneutem Zellen-Aufruf kein neues Freigabe-Fenster (bewusst unverändert) — Kleinticket; (b) `start.sh --colab` bleibt Unterprozess-Variante mit Hinweis (Doku weist sie als nicht empfehlenswert aus).

## 2026-11-15 — coder (Bugfix 2. Real-World-Runde: iframe-Freigabe)

- **Ursache:** `serve_kernel_port_as_window` ist bei Colab veraltet — es gibt nur noch `https://localhost:5000/` aus (Deprecation-Warnung); die Freigabe war damit praktisch unbrauchbar.
- **Umsetzung:** Freigabe-Kette umgestellt: **primär `serve_kernel_port_as_iframe(port)`** (App rendert in der Notebook-Zelle), Fenster nur noch Fallback mit Veraltet-Notiz, letzter Fallback = Handlungs-Hinweis (absoluter Pfad). Meldungen ohne irreführende localhost-URL. README/`docs/colab-start.md`: iframe als Empfehlung, Window als deprecated markiert.
- **Belege:** 3 neue Tests (rot → grün); Gesamtsuite **768** grün.
- **Offene Punkte:** (a) Die iframe-Höhe ist Colab-Standard — falls die App abgeschnitten wirkt, `height`-Argument als Kleinticket; (b) unverändert: `start.sh --colab` ohne Freigabe (als nicht empfehlenswert markiert).

## 2026-11-15 — coder (Bugfix 3. Iteration: App im neuen Browser-Tab)

- **Vorgabe:** Die App soll in einem **neuen Browser-Tab** öffnen (iframe „nicht nutzbar").
- **Umsetzung (finale Freigabe-Kette):** (1) primär `google.colab.kernel.proxyPort(<port>)` per `eval_js` (sicherer, authentifizierter Colab-Link) + `window.open(…, '_blank')` → neuer Tab; (2) Fallback = Nutzer-Snippet `output.serve_kernel_port_as_window(5000)` (Notiz: lieferte aus `%run` nur `https://localhost:5000/`); (3) iframe nur Notbehelf; (4) Handlungs-Hinweis (absoluter `%run`-Pfad + beide Nachhol-Snippets). Meldungen ohne localhost-URL. README/`docs/colab-start.md` auf „neuer Browser-Tab" umgestellt.
- **Belege:** Gesamtsuite **769** grün (19 Tests in `test_start_colab.py`).
- **Offene Punkte:** (a) **Popup-Blocker (Post-MVP):** `window.open` ohne echten Klick-Kontext kann blockiert werden — falls im echten Colab beobachtet, `window.open`-Rückgabewert auswerten und automatisch in den Fenster-Fallback gehen (bewusst noch nicht gebaut); (b) „iframe-Höhe" entfällt — iframe ist nur noch Notbehelf (Thema erledigt); (c) unverändert: `start.sh --colab` ohne Freigabe (nicht empfohlen); (d) „Server läuft bereits" öffnet kein neues Freigabe-Fenster (bewusst unverändert).

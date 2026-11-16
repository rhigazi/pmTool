---
type: Task
title: "A21: Desktop-Modus/Lokal-Betrieb"
description: Die App läuft als Desktop-Fenster (pywebview, Option B) mit direktem Zugriff auf die lokalen Domänen-Module — als eigener Startweg neben dem Browser-Betrieb.
freigabe: true
task_status: abgeschlossen
phase: 8 Abgeschlossen
priority: niedrig
assigned_to: coder
owner: ai
aktuell: ""
---

# Ziel

Desktop-Modus für lokale Nutzung ohne Browser-Fenster: **Option B** (pywebview-Desktop-Fenster mit direktem Aufruf der Domänen-Module — Entscheidung der Projektleitung 2026-11-14, Umsetzung mit Freigabe 2026-11-16). Der bestehende Server-/Browser-Betrieb (MVP/Colab) bleibt unverändert; der Desktop-Modus ist ein zusätzlicher Startweg.

# Akzeptanzkriterien

- **AK-1:** Eigener Startweg (z. B. `bash start.sh --desktop` bzw. `python3 definitions/app/desktop.py`) öffnet die Oberfläche als Desktop-Fenster; `BUNDLE_ROOT`-Semantik unverändert (Default `<Projekt>/wissen`).
- **AK-2:** `pywebview` ist eine **optionale** Abhängigkeit: fehlt sie, gibt der Start eine klare, deutsche Meldung (Installation/Hinweis) und endet sauber — der Server-/Browser-Betrieb funktioniert ohne pywebview unverändert.
- **AK-3:** Bestehende Features (Listen, Detail, Formulare, Freigabe-Gate, Unter-Aufgaben) sind im Desktop-Fenster nutzbar — die Oberfläche bleibt dieselbe (kein zweites Frontend).
- **AK-4:** Tests: Startlogik/Import-Guard/Argumente headless testbar (kein Fenster im Test); bestehende Suites bleiben grün; `verify.sh` Exit 0.
- **AK-5:** Doku: README (Desktop-Abschnitt), `docs/colab-start.md`-Vermerk (Desktop-Modus ist **nicht** der Colab-Weg), `definitions/README.md` bei Bedarf.
- **AK-6:** Abhängigkeits-Regel: pywebview wird in `requirements`/Doku ausdrücklich als optional geführt; kein `curl | sh`, keine weiteren neuen Abhängigkeiten.

# Testfälle (TDD)

**Zuordnung AK → Testfälle:** **AK-1** → T3–T6, T8, T12–T17. **AK-2** → T1–T3, T18.
**AK-3** → T6, T8, T13. **AK-4** → T1–T18 + Sammellauf (Abschnitt „Reihenfolge").
**AK-5** → P4 (Doku-Prüfschritte, kein pytest). **AK-6** → T18, P4.

Reihenfolge = Red-Green-Takt: je Test zuerst den Fall schreiben, rot laufen lassen, das
Minimum implementieren, grün laufen lassen, dann der nächste Test. Jede Nummer ist ein
eigener pytest-Fall. Neue Datei `definitions/app/tests/test_desktop.py` (T1–T11);
`definitions/app/tests/test_start_skript.py` wird nur **additiv** erweitert (T12–T18).

**Testregeln (headless, parallel-sicher):** Kein Test öffnet ein echtes Fenster, startet
einen Subprozess, schreibt ins echte Bundle oder belegt Port 5000. Fenster, Server und
Konfiguration werden an Modulnähten ersetzt (`desktop._lade_webview`,
`desktop._starte_server`, `desktop._starte_fenster`, `desktop._port_aus_umgebung`);
der einzige echte Server-Test (T8) bindet Port 0. Grund: fünf Coder arbeiten parallel im
selben Container; ein Test auf 5000 würde fremde Läufe stören.

**A. Import-Guard und Konfiguration (`tests/test_desktop.py`, AK-1, AK-2)**

- **T1 Import ohne pywebview:** Mit `sys.modules["webview"] = None` lässt sich `desktop`
  importieren; `desktop._lade_webview()` wirft `desktop.DesktopFehler`. **Rot:** ein
  Top-Level-`import webview` lässt bereits die Test-Sammlung mit `ImportError`
  scheitern. **Grün:** Import gelingt, kein `webview`-Import zur Importzeit.
- **T2 Meldungstexte:** `desktop._meldung_webview()` liefert bei fehlendem Paket eine
  deutsche Meldung mit „pywebview", „optional", Installationsbefehl
  `python3 -m pip install pywebview` und dem Hinweis, dass Server-/Browser-Betrieb ohne
  pywebview funktioniert; bei vorhandenem, aber nicht ladbarem Paket
  (`_webview_installiert() → True`) eine Meldung mit „installiert" und „nicht ladbar"
  (Fenster-Backend-Hinweis). **Rot:** Funktion fehlt (`AttributeError`) bzw. nur eine
  pauschale Meldung. **Grün:** beide Fälle unterscheidbar, keine Pfade/OS-Details.
- **T3 Start ohne pywebview:** `find_spec("webview") → None`, `main()` mit sonst
  funktionsfähigen Stubs → Exit **1**, stderr enthält „Start abgebrochen" und
  „pywebview", weder stdout noch stderr enthalten „Traceback"; `_starte_server` und
  `_starte_fenster` wurden **nicht** aufgerufen. **Rot:** Traceback, Exit 0 oder
  Serverstart ohne Fenster (Prozess bliebe hängen). **Grün:** sauberer Abbruch vor
  jedem Serverstart.
- **T4 `BUNDLE_ROOT`:** Kopie von `desktop.py` unter `<tmp>/definitions/app/` importieren
  (Muster `test_start_colab._lade_skript_kopie`): `REPO_ROOT`/`BUNDLE_ROOT` werden aus
  dem Skriptpfad abgeleitet (`<repo>/wissen`); ein gesetztes `BUNDLE_ROOT` hat Vorrang
  (`_bundle_root()`), auch relativ/`~` aufgelöst. **Rot:** hart kodierter Pfad oder
  fehlende Env-Auswertung. **Grün:** beide Wege; Verteilung nach `<projekt>/app/`
  funktioniert analog.
- **T5 `PORT`:** `PORT=8123` → 8123; ohne `PORT` → 5000; `PORT=abc` und `PORT=70000` →
  Exit **1**, stderr „Start abgebrochen" + „PORT", kein Fenster. **Rot:**
  `ValueError`-Traceback oder Fenster mit falschem Port. **Grün:** Wiederverwendung der
  bestehenden Validierung aus `server._port_aus_umgebung` (eine Regelquelle).

**B. Server, Fenster und Lebenszyklus (`tests/test_desktop.py`, AK-1, AK-3)**

- **T6 Fenster-Start (gestubbt):** Fake-`webview` mit Aufzeichnung von
  `create_window`/`start`; `PORT` frei, `BUNDLE_ROOT` = `bundle`-Fixture. `main()` →
  Exit 0; genau **ein** `create_window` mit Titel „OKF Projekt-Manager" und URL
  `http://127.0.0.1:<port>`; genau **ein** `start`; kein stderr. **Rot:** kein Aufruf
  oder URL mit `0.0.0.0`. **Grün:** Fenster lädt dieselbe SPA vom Loopback-Server.
- **T7 Lebenszyklus:** (a) `webview.start` kehrt zurück (Fenster geschlossen) → der
  Serverhandle wird per `shutdown()` beendet, stdout „Desktop-Fenster beendet.",
  Exit 0. (b) `start` wirft `KeyboardInterrupt` → gleiches Aufräumen, Exit 0, kein
  Traceback. (c) `start` wirft `RuntimeError` → `shutdown()` trotzdem, Exit **1**,
  deutsche Meldung, kein Traceback. **Rot:** Server-Thread läuft weiter/Hänger oder
  Traceback. **Grün:** `finally`-Aufräumen in allen drei Fällen.
- **T8 Echter In-Process-Server:** `server.create_app(bundle)` +
  `desktop._starte_server(app, 0)`; `urllib.request` GET `/` → 200 und „<html",
  GET `/api/overview` → 200/JSON-Liste; nach `shutdown()` ist der Port wieder bindbar
  (kurze Warteschleife, kein `sleep`-Festwert). `subprocess.Popen` ist als Sentinel
  ersetzt und wurde nie aufgerufen. **Rot:** Funktion fehlt oder Server erst nach dem
  Fenster bereit (Race). **Grün:** Binden erfolgt synchron vor der Rückgabe; damit ist
  der Server bereit, bevor das Fenster die URL lädt — und es ist dieselbe API/UI
  (AK-3).
- **T9 Belegter Port (Direktaufruf):** freien Port belegen, `PORT` darauf setzen,
  Fake-`webview`; `main()` → Exit **1**, stderr „belegt", `create_window` und
  `_starte_server` nicht aufgerufen. **Rot:** `OSError`/Traceback oder Fenster ohne
  Server. **Grün:** klare Meldung mit Ausweg (`PORT=<frei> …`).
- **T10 Ungültiges `BUNDLE_ROOT`:** nicht existierendes Verzeichnis; Fake-`webview` →
  Exit **1**, stderr „Start abgebrochen" + „kein Verzeichnis", der absolute tmp-Pfad
  kommt **nicht** vor (A7-2-Linie), kein Fenster. **Rot:** Traceback oder Pfad-Leak.
  **Grün:** `server.StartFehler` wird übersetzt, Semantik unverändert (AK-1).
- **T11 Bundle bleibt unverändert:** Hash über alle Bundle-Dateien vor/nach `main()` mit
  gestubbtem Fenster (ohne Requests) identisch, keine neue Datei. **Rot:** Start
  schreibt (z. B. Cache/Log) ins Bundle. **Grün:** rein lesender Start.

**C. `start.sh`-Dispatch (`tests/test_start_skript.py`, additiv, AK-1, AK-2, AK-4)**

Testaufbau: `baue_testprojekt` bekommt einen `desktop.py`-Stub
(`raise SystemExit(0)`); für T13/T16 schreibt der Stub einen Marker. Alle Läufe in
`tmp_path`, freier Port über `_umgebung`.

- **T12 Dry-Run:** `--desktop --dry-run` → Exit 0, stdout nennt `desktop.py`,
  „würde starten" und `BUNDLE_ROOT`, kein Fenster/Prozess. **Rot:** „Unbekannte
  Option: --desktop". **Grün:** Dispatch vorhanden.
- **T13 Dispatch real:** `--desktop --skip-verify` mit Marker-Stub → Exit 0, Marker
  existiert, „Server startet" fehlt, der `server.py`-Startstub wurde nicht aufgerufen.
  **Rot:** es startet der Browser-Server. **Grün:** nur `desktop.py` läuft.
- **T14 Exklusivität:** `--desktop --colab` → Exit ≠ 0, stderr „schließen sich aus",
  weder Desktop-Marker noch Serverstart. **Rot:** stiller Vorrang der letzten Option.
  **Grün:** fail-loud vor Schritt 1.
- **T15 Kombinationen:** `--desktop --neu --dry-run` → Reset-Plan **und**
  Desktop-Would-run; `--desktop --skip-verify` in frischem Mini-Projekt startet ohne
  Rückfrage den Desktop-Stub. **Rot:** `--neu` verliert den Desktop-Modus oder
  umgekehrt. **Grün:** Modus und Reset bleiben orthogonal.
- **T16 Belegter Port:** `--desktop --skip-verify` bei belegtem Port → Exit 0, genau
  **einmal** „bereits belegt"/„Kein zweiter Start", Desktop-Marker fehlt (kein
  Fensterstart). **Rot:** Fenster startet ohne Server. **Grün:** der bestehende
  Schritt-5-Guard gilt auch für Desktop.
- **T17 Hilfe und Bestandsschutz:** `--help` → Exit 0, nennt `--desktop` (und weiter
  `--colab`, `--neu`, `--dry-run`), kein `set -euo`; `--dry-run` **ohne** `--desktop`
  zeigt unverändert `server.py` und nicht `desktop.py`. **Rot:** `hilfe()`-`sed`-Range
  (`2,17p`) passt nach den neuen Kopfzeilen nicht mehr oder Flag fehlt. **Grün:**
  Hilfe vollständig, Browser-Weg unverändert.
- **T18 Keine pywebview-Installation:** `--desktop --dry-run` mit Fake-`python3`
  (Importprüfung schlägt für alle Pakete fehl) zeigt „würde installieren: flask pyyaml
  pytest" und **kein** pywebview, kein pip-Aufruf. Der bestehende Test
  `test_dry_run_installiert_keine_pakete` bleibt als zweiter Wächter unverändert.
  **Rot:** `PAKETE` wird um pywebview erweitert. **Grün:** optionale Abhängigkeit
  bleibt aus dem Pflicht-Set (AK-2/AK-6).

# Kontext

- Entscheidungslog 2026-11-14 „Lokal-Betrieb/Desktop-Modus — MVP/Colab zuerst": Option B als eigenes Feature vorgemerkt; Option A (Ein-Klick unsichtbar) ggf. klein vorab, Option C (File System Access API) verworfen.
- Freigabe der Projektleitung 2026-11-16 („alles frei") umfasst A21.
- **Reihenfolge:** nach A35–A38/A22 (größtes Stück zuletzt); Planung (planner) vor Umsetzung.
- **Lesart „direkter Aufruf der Domänen-Module" (entschieden):** Der Desktop-Prozess
  importiert `server.create_app` und hostet die Flask-App **im eigenen Prozess**; die
  Fachmodule (`overview`, `freigabe`, `nachtrag`, …) laufen damit direkt im
  Desktop-Prozess, ohne zweiten Server-Subprozess und ohne Netzwerk außer Loopback. Das
  Fenster lädt dieselbe SPA von `http://127.0.0.1:<port>`; die Oberfläche und der
  REST-Vertrag bleiben unverändert. **Verworfen:** (a) pywebview-`js_api`-Brücke, die
  Python-Funktionen direkt aus JS aufruft — das wäre ein zweiter Transport mit zweiter
  Validierung/Fehlerformat und erzwänge Frontend-Änderungen (widerspricht AK-3);
  (b) `file://` auf `static/` — `fetch('/api/…')` und CORS funktionieren so nicht.
- **Startmodell (`desktop.py`, neu):** Top-Level nur Standardbibliothek (Import-Guard!);
  `_lade_webview()` importiert `webview` erst zur Laufzeit und wirft `DesktopFehler` mit
  deutscher Meldung; `_meldung_webview()` unterscheidet „fehlt" (Installationshinweis)
  von „installiert, aber nicht ladbar" (Fenster-Backend fehlt, README-Hinweis).
  `main()`: Guard → `BUNDLE_ROOT`/`PORT` prüfen → Portfreiheit → Server binden/starten →
  Fenster starten → bei Rückkehr `shutdown()` im `finally` → Exit 0. Fehler werden als
  „Start abgebrochen: …" nach stderr geschrieben, nie als Traceback; Fensterfehler
  (außer `KeyboardInterrupt`) ergeben Exit 1 nach sauberem `shutdown()`.
  **Verworfen:** Auto-Installation von pywebview (AK-2/AK-6, Netzwerk/Nebenwirkungen,
  in Colab ohnehin nutzlos) und ein Top-Level-`try/except ImportError` (kaputte
  Installation bliebe ein Traceback, Meldung nicht unterscheidbar).
- **Server im Hintergrund:** `werkzeug.serving.make_server(("127.0.0.1", port), app,
  threaded=True)` bindet **synchron** (Server ist bereit, bevor das Fenster lädt) und
  läuft in einem Daemon-Thread; `shutdown()` im `finally` beendet ihn. **Verworfen:**
  `app.run` im Thread (Race zwischen Fenster-URL und Listening-Socket, kein sauberer
  Stopp) und Subprozess wie `start_colab.py` (kein In-Process-Modulzugriff, PID-/Signal-
  Pflege, doppelte Portprüfung).
- **Host:** `127.0.0.1` nur für den Desktop-Modus; der bestehende Server-/Browser-Modus
  bleibt bei `0.0.0.0` unverändert. **Verworfen:** `server.HOST` wiederverwenden — eine
  Desktop-App braucht keine LAN-Freigabe.
- **Port:** `PORT` aus der Umgebung, Default 5000; belegt → fail-loud mit Hinweis auf
  `PORT=<frei>`. `start.sh` behält seinen Schritt-5-Guard („läuft vermutlich schon") auch
  für `--desktop`. **Verworfen:** ephemerer Port 0 (URL nicht vorhersagbar, zwei
  Portbegriffe) und Default 5001 (weicht von Doku/`start.sh` ab; paralleler Betrieb von
  Browser- und Desktop-Modus ist kein Ziel).
- **`BUNDLE_ROOT`:** Env hat Vorrang, sonst Ableitung `<repo>/wissen` aus dem
  Skriptpfad (wie `start_colab.py`); Existenz/Verzeichnisprüfung und Fehlertexte kommen
  aus `server.create_app`/`StartFehler`. **Verworfen:** eigene Pfadprüfung (Drift) und
  Kopieren des Bundles (AK-1 verlangt unveränderte Semantik).
- **`start.sh`-Dispatch:** `--desktop` ist ein eigener Modus neben `lokal`/`colab`;
  `--desktop` + `--colab` sind ein Fehler („schließen sich aus", Exit ≠ 0),
  `--desktop` ist mit `--neu`, `--dry-run`, `--skip-verify` kombinierbar. Suchreihenfolge
  der Datei wie bei `starte_server`: `<projekt>/app/desktop.py`, dann
  `definitions/app/desktop.py`. **Verworfen:** „letzte Option gewinnt" (stiller
  Fehlstart) und eine Env-Variable `DESKTOP=1` (unsichtbarer Startweg).
- **Doku/Abhängigkeit:** pywebview bleibt aus `start.sh`-`PAKETE` und aus jedem
  Installationspfad; die Doku führt es ausdrücklich als optional (kein
  `requirements`-File im Projekt vorhanden — AK-6 erlaubt die Doku-Variante). Kein
  `curl | sh`, keine weiteren Pakete.
- **Paketaufteilung (ein Coder, A21-P1…P4):**
  - **P1 — Guard + Konfiguration:** `desktop.py` mit Konstanten/`_bundle_root`/
    `_port_aus_umgebung`/`_lade_webview`/`_meldung_webview`/`DesktopFehler` und
    `main()`-Gerüst ohne Server/Fenster. Tests T1–T5. Aufwand **2–3 h**.
  - **P2 — Server + Fenster + Lebenszyklus:** `_starte_server` (make_server/Thread),
    `_starte_fenster`, `main()`-Verdrahtung, Fehler-/`finally`-Pfade. Tests T6–T11.
    Aufwand **3–4 h**.
  - **P3 — `start.sh`:** Kopf/Hilfe (+`hilfe()`-Range), Flags/Exklusivität,
    `starte_desktop`, Schritt-7-`case`; Tests T12–T18 additiv. Aufwand **1,5–2 h**.
  - **P4 — Doku + manueller Smoke:** README (Tabelle + Desktop-Abschnitt),
    `docs/colab-start.md`-Vermerk („nicht der Colab-Weg"), `definitions/README.md`;
    Prüfschritte: `grep -n -- "--desktop" README.md`, `grep -n "pywebview" README.md
    definitions/README.md`, `grep -n "Desktop" docs/colab-start.md`; dazu ein manueller
    Fenster-Smoke auf einer Maschine mit Display (nicht CI). Aufwand **1–1,5 h**.
  - **Summe:** ca. **0,75–1,25 Personentage**.
- **Reihenfolge/Abhängigkeiten:** P1 → P2 (gleiche Datei, P2 braucht die Nähte aus P1).
  P3 nach P1 (Dispatch prüft `desktop.py`), kann parallel zu P2 laufen, weil es andere
  Dateien nutzt; bei einem Coder sequenziell P2 → P3. P4 parallel zu P3 möglich (Doku
  nennt den finalen Aufruf; Command-Text nach P3 einfrieren). Danach Review, dann
  Tester: `python3 -m pytest definitions/app/tests -q` **und**
  `bash definitions/verify.sh <projekt>` (Exit 0); zum Schluss P4-Smoke.
  Dateikonflikt: `start.sh`, `tests/test_start_skript.py`, `README.md`,
  `docs/colab-start.md`, `definitions/README.md` — keine Überschneidung mit den
  UI-/Backend-Modulen von A35/A36/A38; dennoch bleibt A21 laut Entscheidungslog
  **Welle D / zuletzt**.
- **Sammellauf AK-4:** `test_desktop.py` + `test_start_skript.py` +
  `test_start_colab.py` + `test_server.py` + restliche App-Suite grün; `verify.sh` Exit 0;
  kein Test hinterlässt einen Prozess, Thread, offenen Port oder eine Bundle-Änderung.
- **Risiken/Grenzen:**
  (a) **Kein Display/keine GUI im Container und in Colab:** pywebview ist hier nicht
  installiert und nicht sinnvoll testbar; T1–T11 prüfen nur Logik/Fakes, der echte
  Fensterstart ist ein manueller Smoke (P4). In Colab bleibt `start_colab.py` der Weg.
  (b) **Linux-Backend:** pip-pywebview allein genügt oft nicht (GTK/WebKit-Systempakete,
  z. B. `python3-gi`/`gir1.2-webkit2-4.1`, je nach Distribution). Das wird **nicht**
  automatisch installiert (AK-6); die Meldung verweist auf den README-Abschnitt.
  (c) **macOS:** `webview.start` muss im Hauptthread laufen — der Entwurf hält das ein
  (Server im Daemon-Thread), ist hier aber nicht verifizierbar.
  (d) **Port 5000:** Läuft bereits der Browser-Server, verhindert `start.sh` den zweiten
  Start (bestehende Semantik); Ausweg `PORT=5001 bash start.sh --desktop` dokumentieren.
  Tests dürfen 5000 nie belegen (Parallel-Coder).
  (e) **`hilfe()`-Kopplung:** Die neue Kopfzeile verschiebt die `sed`-Range; T17
  schlägt sonst fehl (bewusster Wächter).
  (f) **Fenster-Backend-Fehler** können plattformspezifisch sein; gefangen wird nur der
  Start-/Laufzeitfehler mit deutscher Meldung und Exit 1, keine Diagnose-Orgie.
  (g) **Doppelte Startwege:** Drei Wege (Browser, Colab, Desktop) müssen dauerhaft
  denselben REST-Vertrag nutzen; T8 hält `/` und `/api/overview` als gemeinsamen Kern
  fest.
- **Bewusst offen gelassen:** Fenstergröße/Icon/Titel-Feinschliff (Default
  1200×800, Titel „OKF Projekt-Manager", nicht getestet); ein `requirements-optional.txt`
  (Projekt hat keine Requirements-Datei — Doku genügt AK-6); Desktop als Default-Start
  (Browser bleibt Default, Bestandsschutz); native Datei-Dialoge/`js_api`, Tray,
  Ein-Klick-Launcher, Autoupdate; Anpassung von `wissen/projekt/technische-spec.md`
  (nicht Teil von AK-5, kann der `documenter` nachziehen); ein `verify.sh`-Check für
  `app/desktop.py` (Tests decken Import/Start ab).

# Betroffene Dateien

- `definitions/app/desktop.py` (**neu**) — Desktop-Start: Import-Guard
  (`DesktopFehler`, `_lade_webview`, `_meldung_webview`), `_bundle_root`,
  `_port_aus_umgebung`, `_port_belegt`, `_starte_server` (make_server + Daemon-Thread),
  `_starte_fenster`, `main`. Top-Level nur Standardbibliothek.
- `definitions/app/tests/test_desktop.py` (**neu**) — T1–T11, Fake-`webview`,
  Serverhandle/Fenster-Stubs, echter Server auf Port 0.
- `start.sh` — Kopfzeile/Hilfe für `--desktop` (und `hilfe()`-Range), Flags
  `--desktop`, Exklusivitätsprüfung gegen `--colab`, `starte_desktop`,
  `case`-Dispatch in Schritt 7; `PAKETE` **unverändert**.
- `definitions/app/tests/test_start_skript.py` (nur additiv) — `desktop.py`-Stub im
  Mini-Projekt, T12–T18; bestehende Fälle unverändert.
- `README.md` — Zeile `bash start.sh --desktop` in der Lokal-Tabelle, Abschnitt
  „Desktop-Modus (optional)" mit pywebview-Installation, `BUNDLE_ROOT`-Semantik,
  Port-/Backend-Hinweis und „nicht in Colab".
- `docs/colab-start.md` — kurzer Vermerk: Desktop-Modus ist **nicht** der Colab-Weg;
  dort bleibt `%run …/start_colab.py` der Start.
- `definitions/README.md` — `app/`-Zeile um `desktop.py` ergänzen, pywebview als
  optionale Abhängigkeit nennen.
- **Nicht geändert:** `definitions/app/server.py` (nur nutzen), `start_colab.py`,
  `definitions/setup.sh` (verteilt `app/*` automatisch, `desktop.py` inklusive),
  `definitions/verify.sh` (App-Tests laufen automatisch mit), `requirements`-Dateien
  (keine vorhanden), übrige UI-/Backend-Module.

# Ergebnisse
## 2026-11-16 — coder (Rücklauf) + PM: W1/K1/K2 behoben → **abgeschlossen**

- **W1:** `hilfe()`-Range jetzt beidseitig gewacht (`assert "fail-safe" in stdout` + `assert "!/usr/bin/env bash" not in stdout`) — Proben: `2,17p` rot, `1,17p` rot, `1,18p` rot (beide Grenzen sichtbar).
- **K1:** T8 assertiert `desktop.HOST == "127.0.0.1"` **und** `handle.server_address[0] == "127.0.0.1"` (Konstante + effektive Bind-Adresse) — Literal-Mutante `0.0.0.0` tot.
- **K2:** neuer Test `test_t7d_server_thread_laeuft_als_daemon` (Stub-Server + Thread-Stub, kein zusätzlicher echter Socket) — `daemon=False`-Mutante tot.
- 50 + **20** = **70 grün**; Produktivcode unverändert (byte-identisch). **A21 abgeschlossen** (PM, 2026-11-16).
- **Restvermerk (ausdrücklich offen):** echter Fenster-Smoke auf Maschine mit Display (Linux-Backend/macOS-Hauptthread) — bei der Abnahme der Projektleitung nachzuholen. K3–K7 (Socket-Release-Formulierung, `_port_belegt`-Delegation, README-Zahlen → Sammellauf-Sync, Berichtstreue, Port-Race-Meldung englisch) → Härtungs-/Doku-Klammern.

## 2026-11-16 — reviewer: NACHBESSERUNG (klein — nur Testwächter) — Rücklauf läuft

- **Urteil:** NACHBESSERUNG (klein) — Umsetzung funktional vollständig und korrekt (AK-1…AK-6 alle erfüllt, App-Suite **1670 passed**, `verify.sh` Exit 0, `bash -n`/`py_compile` sauber, keine neue Abhängigkeit, kein `innerHTML`). 18 Mutantenproben: 13/17 getötet (+1 äquivalent); 4 überlebt: **W1** `hilfe()`-Range-Wächter greift nicht (Mutant f: zu enge Range → Hilfe sichtbar kaputt, Test grün) — blockierend; **K1** Bind-Adresse nicht direkt geprüft (Literal `0.0.0.0` überlebt); **K2** `daemon=True` ungetestet; **l** Fenstergröße (bewusst offen, akzeptiert); **n** `server_close()` im Bedien-Thread = äquivalent (verifiziert). Rücklauf W1/K1/K2 läuft (nur Tests).
- **K-Notizen:** K3 „doppelte Socket-Freigabe" ist real dreifach (idempotent/harmlos, Kommentar präzisieren); K4 lokales `_port_belegt` dupliziert `server._port_belegt` (Delegation = eine Regelquelle, später); K5 README-Zahlen → Sammellauf-Sync; K6 Bericht nannte nur 3 von 6 Abweichungen; K7 Port-Race endet mit englischer Werkzeug-Meldung (akzeptabel). Alle 6 dokumentierten Abweichungen **akzeptabel** (Bewertungen im Review-Bericht).
- **Restvermerk (ausdrücklich offen):** echter Fenster-Smoke auf einer Maschine mit Display (inkl. Linux-Backend/macOS-Hauptthread) — bei der Abnahme nachholen, nicht still als erledigt werten.

## 2026-11-16 — coder (Welle D): Desktop-Modus P1–P4 — 69 Tests grün

- **Ergebnis:** `definitions/app/desktop.py` (neu): Lazy-Import-Guard (`DesktopFehler`, Meldung „fehlt" vs. „installiert, nicht ladbar", Exit 1 ohne Traceback/Server), `BUNDLE_ROOT`-Ableitung mit Env-Vorrang, `PORT`-Validierung über `server` (eine Regelquelle), `_starte_server` (`make_server(("127.0.0.1", port), app, threaded=True)` im Daemon-Thread, deterministischer Port-Release via `shutdown()`+`server_close()`), `_starte_fenster` (genau ein `create_window("OKF Projekt-Manager", url, width=1200, height=800)` + `start()`), `main()`-Lebenszyklus mit `finally`-Aufräumen. `start.sh --desktop`: eigener Modus, exklusiv zu `--colab` (reihenfolgeunabhängig, fail-loud), kombinierbar mit `--neu`/`--dry-run`/`--skip-verify`; `hilfe()`-Range `2,18p`; `PAKETE` ohne pywebview. Doku: README (Tabellenzeile + Abschnitt „Desktop-Modus (optional)" inkl. Linux-Backend-Hinweis), `docs/colab-start.md` („nicht der Colab-Weg"), `definitions/README.md`.
- **Tests (TDD, alle Planfälle T1–T18):** `test_desktop.py` neu **19** (davon T8: echter In-Process-Server auf Port 0, `/` + `/api/overview`, Port danach wieder bindbar), `test_start_skript.py` **41 → 50** (additiv). Gesamtlauf beider Dateien **69 passed**; `bash -n start.sh` + `py_compile` sauber.
- **Design-Entscheidungen 1–6 des Plans umgesetzt** (Option B In-Process-Flask, kein `js_api`/`file://`, Lazy Import, Loopback-Host, `--desktop`-Dispatch, Port 5000 fail-loud); 6 dokumentierte Klein-Abweichungen (u. a. `ValueError`-Fang in `_webview_installiert`, doppelte Socket-Freigabe für deterministischen Port-Release, `_repo_root` für beide Layouts) — Details im Bericht.
- **Echter Fenster-Smoke offen:** kein Display/pywebview im Container; headless verifiziert (Fake-Webview + echter Server: Fenster-URL `http://127.0.0.1:<port>`, genau ein `start`, sauberes Ende, Exit 0).
- **Offen:** Review läuft; Testzahlen README (1544/1632) → Sammellauf-Sync; Spec ohne Desktop-Abschnitt (bewusst, nicht AK-5).


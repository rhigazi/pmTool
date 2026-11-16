# OKF Projekt-Manager (SPA)

Browserbasierte Oberfläche für **eine Person**, die ein OKF-Projekt in Mensch-KI-Zusammenarbeit führt: Status, Zuständigkeit (`owner`), Nachträge und Wellen auf einen Blick — direkt über dem OKF-Bundle `wissen/` als **einziger Datenquelle**.

Die App ist ein **Tracker**. Die eigentliche Projektarbeit läuft im OpenCode-CLI-Chat: der Projektmanager-Agent steuert `planner`, `coder`, `reviewer`, `tester` und `documenter`; die Oberfläche macht den Stand sichtbar und erlaubt die menschlichen Eingriffe (Nachtrag, „Klarung", „Geschlossen", owner umschalten).

- **Status (2026-11-16):** MVP + Feature-Strecke abgeschlossen — A1–A20 sowie A23–A34 erledigt (u. a. Suche, Wellen-Zuordnung/-Filter, Arbeitsstatus, Freigabe-Gate, Unter-Aufgaben); A26/A34 in den Abschluss-Checks. **Root-Suite 1632 grün** (App-Suite 1544 + `definitions/tools/tests` 88; Sammellauf 2026-11-16). Offen (Post-MVP, gesperrt ohne Weisung): A35–A38, A21, A22. Laufend: **A39** (gemeinsame Test-/Abstimmungsrunde — [Lückenliste](docs/lueckenliste-a39.md)).
- **Projektstand & Historie:** [docs/uebergabeprotokoll.md](docs/uebergabeprotokoll.md), [wissen/log.md](wissen/log.md)
- **Projektwissen:** [wissen/index.md](wissen/index.md)

---

## Schnellstart — Colab

Der einfachste Weg ist das mitgelieferte Notebook **[PMTool.ipynb](PMTool.ipynb)** (Badge „Open in Colab" in der ersten Zelle). Es installiert OpenCode-CLI, klont das Repo und startet die App.

Manuell in einer Colab-Sitzung:

```bash
!git clone https://github.com/rhigazi/pmTool
```

```python
%run /content/pmTool/definitions/app/start_colab.py   # Umgebung + App starten (neuer Browser-Tab)
```

Alternativ relativ — dann `%cd` in einer eigenen Zeile davor:

```python
%cd /content/pmTool
%run definitions/app/start_colab.py
```

Ohne `%cd` schlägt der relative Pfad fehl (`File not found`), weil das
Notebook-Verzeichnis in einer frischen Sitzung `/content` ist.

Der Start **muss** als Kernel-Aufruf (`%run`) erfolgen: Colabs Port-Freigabe
wirkt nur im Notebook-Kernel. Ein `!`-Befehl läuft als Unterprozess ohne
Kernel-Kanal — dann bleibt nur die unbrauchbare Adresse `127.0.0.1:5000` stehen
(das Skript nennt dann den Ausweg).

Die App öffnet sich in einem **neuen Browser-Tab** über den sicheren,
authentifizierten Colab-Link (`google.colab.kernel.proxyPort`). Fallback ist
`serve_kernel_port_as_window` (Nutzer-Snippet, in Colab als veraltet markiert),
Notbehelf die Anzeige in der Zelle (`serve_kernel_port_as_iframe`).

Schritt-für-Schritt-Anleitung inkl. Colab-Secrets und Telegram-Zelle: **[docs/colab-start.md](docs/colab-start.md)**.

### Test-Instanz / Abnahme-Instanz

Für die Abnahme den echten Nutzerpfad testen — **frischer Clone von GitHub**
(nie den Dev-Ordner kopieren) in einer frischen Colab-Runtime, getrennt von der
Entwicklungs-Instanz:

```python
!git clone https://github.com/rhigazi/pmTool /content/pmTool-test
```

```python
%cd /content/pmTool-test
%run /content/pmTool-test/definitions/app/start_colab.py
```

Das Bundle wird aus dem Skriptpfad abgeleitet (`<Klon>/wissen`), ein gesetztes
`BUNDLE_ROOT` hätte Vorrang — der Klon-Name ist also egal.

Smoke-Check: Liste (Status/`owner`) → Detail (Markdown, nur `Klarung`/`Geschlossen`)
→ Nachtrag einfügen → Formular Aufgabe/Welle → Entscheidungen/Projekt.
Aktualisieren: `!cd /content/pmTool-test && git pull`, dann Startzeile erneut.

## Schnellstart — lokal

Voraussetzungen: Python 3 mit `flask`, `pyyaml`, `pytest` (fehlende Pakete installiert `start.sh` bei Bedarf). Optional für Browser-Tests: `moli` (Installation: `bash definitions/setup.sh --global`).

```bash
bash start.sh                  # Server auf http://localhost:5000
```

Der Server lauscht nur lokal. Nützliche Optionen:

| Aufruf | Wirkung |
|---|---|
| `bash start.sh` | lokal starten (`BUNDLE_ROOT=$PROJEKT/wissen`, Port 5000) |
| `bash start.sh --desktop` | Desktop-Fenster (pywebview, **optional**) auf `http://127.0.0.1:5000` — siehe „Desktop-Modus (optional)" |
| `bash start.sh --colab` | startet nur den Server ohne Port-Freigabe (Unterprozess); in Colab stattdessen `%run /content/pmTool/definitions/app/start_colab.py` in einer Code-Zelle |
| `bash start.sh --neu` | Reset von `wissen/` auf die leere Vorlage (mit Backup), dann Start — siehe „Neues Projekt beginnen" |
| `bash start.sh --dry-run` | Trockenlauf: zeigt nur, was getan würde (installiert/löscht/startet nichts; `verify.sh` wird dabei still übersprungen) |
| `bash start.sh --skip-verify` | ohne Setup-Prüfung |
| `bash start.sh --help` | Hilfe |

Beenden mit **Strg+C** (kein Traceback). `start.sh` ist ein Werkzeug der Repo-Wurzel und wird nicht in Zielprojekte verteilt.

### Desktop-Modus (optional)

Die App kann statt im Browser als eigenes Fenster laufen. Der Desktop-Modus ist ein **zusätzlicher** Startweg: Der Prozess hostet dieselbe Flask-App im eigenen Prozess und lädt dieselbe Oberfläche über Loopback (`http://127.0.0.1:5000`) — kein zweites Frontend, keine LAN-Freigabe.

```bash
bash start.sh --desktop          # Fenster auf http://127.0.0.1:5000
PORT=5001 bash start.sh --desktop  # wenn 5000 schon belegt ist
```

Voraussetzung ist das **optionale** Paket `pywebview` (wird bewusst nicht automatisch installiert und ist nicht Teil der Pflicht-Pakete in `start.sh`):

```bash
python3 -m pip install pywebview
```

- **Fehlt pywebview**, bricht nur der Desktop-Start mit einer deutschen Meldung und Exit 1 ab; der normale Server-/Browser-Betrieb funktioniert unverändert.
- **Linux:** pip-pywebview allein genügt oft nicht — zusätzlich wird ein Fenster-Backend (GTK/WebKit, z. B. `python3-gi`/`gir1.2-webkit2-4.1`) benötigt. Die Meldung weist auf diesen Abschnitt hin.
- **`BUNDLE_ROOT`:** gleiche Semantik wie im Browser-Betrieb — die Umgebungsvariable hat Vorrang, sonst `<Projekt>/wissen`. Das Bundle wird nur lesend verwendet.
- **Port:** `PORT` aus der Umgebung, Default 5000; ist er belegt, bricht der Start mit einem Hinweis auf `PORT=<frei>` ab. `--desktop` ist mit `--neu`, `--dry-run` und `--skip-verify` kombinierbar, aber **nicht** mit `--colab` (die Modi schließen sich aus).
- **Nicht der Colab-Weg:** In Colab gibt es kein Fenster-Backend; dort bleibt `%run /content/pmTool/definitions/app/start_colab.py` der Start (siehe [docs/colab-start.md](docs/colab-start.md)).

Direkt ohne `start.sh` (z. B. in einem per `setup.sh` verteilten Projekt): `python3 app/desktop.py`.

---

## Funktionen der Oberfläche

- **Listenansicht (Übersicht):** Tabelle aller Punkte mit Status, `owner`, „zuletzt geändert", **Welle** (A31) und Arbeitsstatus-Zeile (A30: `aktuell` der Subagenten); Filter nach den 6 UI-Status und nach `owner` (alle/mensch/ai/ohne), Filter nach Welle (A27); **Suchfeld** (A25, mehrere Wörter = UND, umlaut-/ß-tolerant, kombinierbar mit den Filtern). „Klarung"-Zeilen sind hervorgehoben; Aufgaben ohne zugewiesene Kennung tragen die Marke **„neu"** (A28) mit Kennungs-Hinweis und Freigabe-Knopf (Menschen-Kanal `POST /api/freigabe`).
- **Detailansicht:** Frontmatter-Kopf und gerendertes Markdown (eigener, XSS-sicherer Minimal-Renderer), Formular „Nachtrag einfügen", owner-Umschalter, ausschließlich die Status-Buttons `Klarung` und `Geschlossen`; **Wellen-Zuordnung** per Dropdown (A27) und **Sperrgrund-Anzeige**, solange Aufgabe oder zugeordnete Welle nicht freigegeben sind (A29).
- **Unter-Aufgaben (A34):** Knopf „Unter-Aufgabe anlegen" in der Detailansicht einer Aufgabe (Inline-Formular, Kennung `A{xxx}.{uuu}` vergibt die App, `welle` wird geerbt); Abschnitt „Unter-Aufgaben (n)" mit Tabelle, Tiefe genau eine Ebene.
- **Wellen:** Freigabe-Marke „freigegeben/nicht freigegeben" in der Wellen-Liste (A29), Freigabe-Knopf im Wellen-Detail (Menschen-Kanal), Ansicht „Aufgaben dieser Welle (n)".
- **Formulare:** neue **Aufgabe** oder **Welle** anlegen — mit Erfolgsanzeige und kopierbarem Kurzkontext für die Übergabe an die KI (Wellen-Linktext zeigt den Wellen-Titel).
- **Feature-Liste (A23):** Menüpunkt „Feature List" zeigt alle Features mit Status; Klick öffnet die zugehörigen Aufgaben (offen/in Bearbeitung/erledigt).
- **Entscheidungen-/Projekt-Ansicht:** zeigt die Einträge aus `wissen/entscheidungen/log.md` sowie die Projekt-Unterpunkte (Konzept, Technische Spec, User Stories, Phasen, Log) — über den bestehenden Datei-Endpunkt, ohne zusätzliche API.

**Statuswerte (UI):** `Klarung` · `Offen` · `In Arbeit` · `Testing` · `Dokumentation` · `Geschlossen`.
Sie sind eine Sicht auf das bestehende Workflow-Feld `task_status` (bzw. `status` bei Wellen) — es gibt kein zweites Statusmodell.
**Zuständigkeit:** `owner: mensch | ai` — `mensch` heißt „die Projektleitung ist dran" (z. B. Antwort auf eine Klärung, Abnahme), `ai` heißt „der Projektmanager/Agent ist dran".

## Datenhaltung

Alles liegt im OKF-Bundle **[wissen/](wissen/index.md)** — Markdown mit YAML-Frontmatter. Die App führt keine Zweitdatenbank.

- **Nachträge** der Projektleitung stehen als sichtbarer Block direkt in der jeweiligen Datei: `> **Nachtrag (Mensch, YYYY-MM-DD):** …`
- **Reservierte Dateien** wie `index.md`, `log.md`, `features.md` pflegt ausschließlich die KI (Projektmanager/`documenter`); die App lehnt Schreibzugriffe darauf mit **403** ab. Schreibbar sind über die App: Nachtrag anfügen, Aufgabe/Welle anlegen, `owner` ändern sowie `task_status` auf `Klarung` oder `Geschlossen` setzen.
- Schreibzugriffe erfolgen atomar; es gibt im MVP kein Locking (gleichzeitige Schreibzugriffe von KI und App sind ein bekanntes Risiko).

## Entwicklung & Tests

```bash
python3 -m pytest definitions/app/tests -q   # App-Suite (2026-11-16: 1544 grün)
python3 -m pytest -q                        # Root-Suite = App-Suite + definitions/tools/tests (1632 grün)
bash definitions/verify.sh .                 # Umgebungs-Check → Exit 0 = vollständig
```

- **UI-Tests** laufen über HTTP gegen den laufenden Server plus den Node-DOM-Harness; optional mit echtem `moli` (Browser-Szenarien, Screenshots).
- **Testisolation:** Tests arbeiten ausschließlich auf Fixture-Kopien unter `tmp_path` bzw. `/tmp/opencode/…` — das echte Bundle `wissen/` wird nie beschrieben.
- **Flaky-Zone:** Bei paralleler Tester-/Coder-Arbeit können App-Test-/verify-Läufe gelegentlich rot sein — serialisierte Läufe sind stabil (Empfehlung: Testläufe serialisieren).

## Neues Projekt einrichten

`definitions/` ist die Single Source of Truth für Regeln, Subagenten und die App. Mit `setup.sh` wird alles in ein Zielprojekt verteilt, `verify.sh` prüft die Installation:

```bash
bash definitions/setup.sh /pfad/zum/projekt          # Regeln, Subagenten, App verteilen
bash definitions/setup.sh --wissen /pfad/zum/projekt # zusätzlich OKF-Gerüst anlegen
bash definitions/verify.sh /pfad/zum/projekt         # Installation prüfen (Exit 0 = ok)
```

Optionen von `setup.sh`: `--wissen`, `--global` (Subagenten nach `~/.config/opencode/agents/`, Skills nach `~/.agents/skills/`, optional `moli`), `--force`. Vorhandene Dateien werden ohne `--force` nie überschrieben.

> **Hinweis:** `verify.sh` prüft das **vollständige** Projekt — inklusive OKF-Wissensgerüst (`wissen/index.md`, `features.md`, `log.md` u. a.). Ein Ziel **ohne** `--wissen` hat dieses Gerüst nicht und endet bei der Verify-Prüfung mit Exit 1. Für neue Projekte daher `setup.sh --wissen` nutzen (oder das Wissensgerüst separat anlegen).

Die **mitverteilte Vorlagen-README** liegt in [definitions/README.md](definitions/README.md) — sie beschreibt die Installation in Zielprojekten und wird hier bewusst nicht dupliziert.

## Neues Projekt beginnen

Ein frischer Klon bringt das Projektwissen des Vorbilds mit. `start.sh` erkennt das an pmTool-spezifischen Markerdateien (`wissen/aufgaben/a1-okf-bundle.md`, `wissen/features/okf-projekt-manager-spa.md`) und bietet beim Start den Reset auf die leere Vorlage an:

```bash
bash start.sh                  # fragt bei vorbefülltem wissen/: „Neues leeres Projekt beginnen? [j/N]"
bash start.sh --neu            # Reset ohne Rückfrage (Backup + Vorlage), dann Start
bash start.sh --neu --dry-run  # zeigt nur den Plan — ändert nichts
```

- **Ja** = Reset wie `tools/neues_projekt.py --ja` (erst Backup, dann Vorlage), danach Start mit leerem Projekt.
- **Nein / Strg+D** = unveränderter Normalstart, es wird nichts gelöscht.
- **Kein TTY** (Pipe, Skript, Hintergrund) = nur Hinweistext, kein Reset (fail-safe).
- **Laufender Server** auf dem Port = Hinweis vor der Rückfrage, kein Reset (kein zweiter Start).
- Der Reset wirkt immer auf `<Projekt>/wissen` (das Werkzeug ignoriert `BUNDLE_ROOT`); weicht `BUNDLE_ROOT` ab, nennt der Hinweis ausdrücklich das Reset-Ziel.
- `--neu` funktioniert auch, wenn `wissen/` fehlt (wird aus der Vorlage angelegt, ohne Backup); ohne `--neu` bleibt ein fehlendes `wissen/` ein Abbruch.
- `--neu` ist mit `--colab` kombinierbar. In Colab bleibt der Kernel-Aufruf von `start_colab.py` der Startweg; den Reset dort wie unten beschrieben ausführen (siehe [docs/colab-start.md](docs/colab-start.md)).

Der Reset läuft ausschließlich über `tools/neues_projekt.py` (eine Lösch-Implementierung, Backup-Pflicht); schlägt er fehl, bricht der Start ab. Die manuelle Variante bleibt:

```bash
python3 tools/neues_projekt.py        # 1. Plan: Löschziel, Backup-Pfad, Vorlage — ändert nichts
python3 tools/neues_projekt.py --ja   # 2. ausführen: erst Backup, dann Reset
bash definitions/verify.sh .          # 3. Umgebungs-Check → Exit 0 = vollständig
bash start.sh                         # 4. App startet mit leerem Projekt
```

Danach enthält `wissen/` exakt die Vorlage (`index.md`, `features.md`, `log.md`, `aufgaben/`, `entscheidungen/`, `projekt/`) — die App zeigt keine Aufgaben und keine Wellen; das Projekt wird über die App bzw. den Projektmanager neu angelegt. In Colab ist Schritt 4 stattdessen `%run /content/pmTool/definitions/app/start_colab.py`.

> **Achtung:** `--ja` löscht das **gesamte Projekt-Wissen** in `wissen/`, inklusive versteckter Dateien, Nachträgen und Entscheidungen. Vorher entsteht automatisch ein Backup `wissen-backup-YYYYMMDD-HHMMSS.tar.gz` im Repo-Root; schlägt das Backup fehl, wird **nichts** gelöscht. Das Backup ist danach die einzige Kopie dieses Wissens — sichern oder an einen sicheren Ort verschieben.

Details: Ohne `--ja` wird ausschließlich der Plan ausgegeben (Exit 0, Dateisystem unverändert). `--backup PFAD` legt das Backup-Ziel fest, muss aber innerhalb des Repo-Roots liegen. Fehlt oder unvollständig ist die Vorlage, bricht das Skript ab und nennt die fehlende Datei — ohne zu löschen. Ein zweiter Lauf direkt nach einem Reset ist idempotent (neues Backup, gleiches Ergebnis).

Das Werkzeug liegt in der Quelle `definitions/tools/neues_projekt.py`; `setup.sh` verteilt es samt Tests nach `tools/` und legt im Zielprojekt zusätzlich `definitions/wissen-vorlage/` sowie `definitions/verify.sh` an (die Vorlage braucht das Werkzeug, verify.sh verweist der Erfolgstext). Im Entwicklungs-Repo ist `tools/` nur die installierte Kopie — Änderungen immer in `definitions/tools/` vornehmen.

**Auffrischen im Dev-Repo:** Im Repo-Root liegt die Quelle bereits unter `definitions/`. Ein Lauf `bash definitions/setup.sh . --force` aktualisiert dort nur die vorhandenen Spiegel (`AGENTS.md`, `.opencode/agents/`, `opencode.jsonc`, `tools/`) und kopiert **nichts auf sich selbst**: `definitions/verify.sh`, `definitions/wissen-vorlage/` (Abschnitt 4b), `wissen/` (5, nur im `--wissen`-Lauf) und `app/` (10) werden übersprungen („übersprungen (Quelle = Ziel)"). So entsteht kein zweites `app/` neben `definitions/app/`, und `wissen/` bleibt unangetastet (der Plain-Lauf ohne `--wissen` führt Abschnitt 5 gar nicht aus). So entsteht kein zweites `app/` neben `definitions/app/`, und `wissen/` bleibt unangetastet. Einzige Ausnahme: Wer `setup.sh` direkt auf `definitions/` richtet, legt dort die Projektspiegel an — für die Auffrischung ist immer das Repo-Root das Ziel. Die Root-Suite (`pytest -q`) testet deshalb nur `definitions/tools/tests/` und ignoriert den Spiegel `tools/tests/` (`conftest.py`); eine Drift-Prüfung wacht darüber, dass beide Bäume inhaltsgleich bleiben.

## Telegram-Benachrichtigung

Der Projektmanager kann Statusmeldungen und Rückfragen per Telegram senden:

```bash
python3 tools/telegram_send.py --config config.json "Nachricht"
```

`config.json` (Schlüssel `bot_token`, `chat_id`) ist **gitignored** und wird nicht mitgeklont. Secrets nie committen — in Colab werden sie über die Secrets-Zelle aus [docs/colab-start.md](docs/colab-start.md) erzeugt.

## Weiterführendes

- **[docs/prd.md](docs/prd.md)** — Produktanforderungen und Produktentscheidungen
- **[docs/uebergabeprotokoll.md](docs/uebergabeprotokoll.md)** — Gesamtstand, Aufgabenstatus, offene Punkte
- **[docs/lueckenliste-a39.md](docs/lueckenliste-a39.md)** — A39-Testrunde: Befunde, Lücken und Folgeaufgaben-Kandidaten
- **[docs/colab-start.md](docs/colab-start.md)** — neue Colab-Sitzung starten
- **[wissen/index.md](wissen/index.md)** — Einstieg ins Projektwissen (Session-Start-Regel)
- **[wissen/projekt/phasen.md](wissen/projekt/phasen.md)** — Workflow, Phasenmodell, Aufgabenformat
- **[AGENTS.md](AGENTS.md)** — Arbeitsregeln des Projektmanagers und der Subagenten
- **[wissen/features.md](wissen/features.md)** — Features und offene Punkte

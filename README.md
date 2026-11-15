# OKF Projekt-Manager (SPA)

Browserbasierte Oberfläche für **eine Person**, die ein OKF-Projekt in Mensch-KI-Zusammenarbeit führt: Status, Zuständigkeit (`owner`), Nachträge und Wellen auf einen Blick — direkt über dem OKF-Bundle `wissen/` als **einziger Datenquelle**.

Die App ist ein **Tracker**. Die eigentliche Projektarbeit läuft im OpenCode-CLI-Chat: der Projektmanager-Agent steuert `planner`, `coder`, `reviewer`, `tester` und `documenter`; die Oberfläche macht den Stand sichtbar und erlaubt die menschlichen Eingriffe (Nachtrag, „Klarung", „Geschlossen", owner umschalten).

- **Status:** MVP abnahmefähig (alle Aufgaben A1–A20 abgeschlossen, Gesamtsuite 862 grün — Stand A24; die endgültige Zahl folgt nach A23/A25)
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
| `bash start.sh --colab` | startet nur den Server ohne Port-Freigabe (Unterprozess); in Colab stattdessen `%run /content/pmTool/definitions/app/start_colab.py` in einer Code-Zelle |
| `bash start.sh --dry-run` | Trockenlauf: zeigt nur, was getan würde (installiert/startet nichts; `verify.sh` wird dabei still übersprungen) |
| `bash start.sh --skip-verify` | ohne Setup-Prüfung |
| `bash start.sh --help` | Hilfe |

Beenden mit **Strg+C** (kein Traceback). `start.sh` ist ein Werkzeug der Repo-Wurzel und wird nicht in Zielprojekte verteilt.

---

## Funktionen der Oberfläche

- **Listenansicht:** Tabelle aller Punkte mit Status, `owner` und „zuletzt geändert"; Filter nach den 6 UI-Status und nach `owner` (alle/mensch/ai/ohne). „Klarung"-Zeilen sind hervorgehoben; Einträge werden nie automatisch ausgeblendet.
- **Detailansicht:** Frontmatter-Kopf und gerendertes Markdown (eigener, XSS-sicherer Minimal-Renderer), Formular „Nachtrag einfügen", owner-Umschalter sowie **ausschließlich** die Status-Buttons `Klarung` und `Geschlossen`.
- **Formulare:** neue **Aufgabe** oder **Welle** anlegen — mit Erfolgsanzeige und kopierbarem Kurzkontext für die Übergabe an die KI.
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
python3 -m pytest definitions/app/tests -q   # Gesamtsuite (aktuell 862 passed, Stand A24)
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

Die **mitverteilte Vorlagen-README** liegt in [definitions/README.md](definitions/README.md) — sie beschreibt die Installation in Zielprojekten und wird hier bewusst nicht dupliziert.

## Neues Projekt beginnen

Ein frischer Klon bringt das Projektwissen des Vorbilds mit. Für ein eigenes, leeres Projekt setzt `tools/neues_projekt.py` das Bundle `wissen/` auf die OKF-Vorlage `definitions/wissen-vorlage/` zurück:

```bash
python3 tools/neues_projekt.py        # 1. Plan: Löschziel, Backup-Pfad, Vorlage — ändert nichts
python3 tools/neues_projekt.py --ja   # 2. ausführen: erst Backup, dann Reset
bash definitions/verify.sh .          # 3. Umgebungs-Check → Exit 0 = vollständig
bash start.sh                         # 4. App startet mit leerem Projekt
```

Danach enthält `wissen/` exakt die Vorlage (`index.md`, `features.md`, `log.md`, `aufgaben/`, `entscheidungen/`, `projekt/`) — die App zeigt keine Aufgaben und keine Wellen; das Projekt wird über die App bzw. den Projektmanager neu angelegt. In Colab ist Schritt 4 stattdessen `%run /content/pmTool/definitions/app/start_colab.py`.

> **Achtung:** `--ja` löscht das **gesamte Projekt-Wissen** in `wissen/`, inklusive versteckter Dateien, Nachträgen und Entscheidungen. Vorher entsteht automatisch ein Backup `wissen-backup-YYYYMMDD-HHMMSS.tar.gz` im Repo-Root; schlägt das Backup fehl, wird **nichts** gelöscht. Das Backup ist danach die einzige Kopie dieses Wissens — sichern oder an einen sicheren Ort verschieben.

Details: Ohne `--ja` wird ausschließlich der Plan ausgegeben (Exit 0, Dateisystem unverändert). `--backup PFAD` legt das Backup-Ziel fest, muss aber innerhalb des Repo-Roots liegen. Fehlt oder unvollständig ist die Vorlage, bricht das Skript ab und nennt die fehlende Datei — ohne zu löschen. Ein zweiter Lauf direkt nach einem Reset ist idempotent (neues Backup, gleiches Ergebnis).

Das Werkzeug gehört zum Repo-Root (`tools/`) und wird derzeit **nicht** von `setup.sh` in Zielprojekte verteilt — diese Verteilungslücke ist als [A26](wissen/aufgaben/a26-verteilung-und-suite-konflikt.md) vorgemerkt.

## Telegram-Benachrichtigung

Der Projektmanager kann Statusmeldungen und Rückfragen per Telegram senden:

```bash
python3 tools/telegram_send.py --config config.json "Nachricht"
```

`config.json` (Schlüssel `bot_token`, `chat_id`) ist **gitignored** und wird nicht mitgeklont. Secrets nie committen — in Colab werden sie über die Secrets-Zelle aus [docs/colab-start.md](docs/colab-start.md) erzeugt.

## Weiterführendes

- **[docs/prd.md](docs/prd.md)** — Produktanforderungen und Produktentscheidungen
- **[docs/uebergabeprotokoll.md](docs/uebergabeprotokoll.md)** — Gesamtstand, Aufgabenstatus, offene Punkte
- **[docs/colab-start.md](docs/colab-start.md)** — neue Colab-Sitzung starten
- **[wissen/index.md](wissen/index.md)** — Einstieg ins Projektwissen (Session-Start-Regel)
- **[wissen/projekt/phasen.md](wissen/projekt/phasen.md)** — Workflow, Phasenmodell, Aufgabenformat
- **[AGENTS.md](AGENTS.md)** — Arbeitsregeln des Projektmanagers und der Subagenten
- **[wissen/features.md](wissen/features.md)** — Features und offene Punkte

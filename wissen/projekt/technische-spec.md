---
type: Specification
title: Technische Spec
description: Architektur, Technologien, Datenmodell, Schnittstellen und Start-/Test-Befehle der OKF-Projekt-Manager-SPA (Colab).
tags: [projekt, spezifikation, architektur]
status: aktuell
---

# Überblick

**OKF Projekt-Manager (SPA)** — browserbasierte Ein-Personen-Oberfläche auf das OKF-Bundle, gestartet aus Colab. Sie ist ein **Tracker zur Projektsteuerung**: Anzeigen von Status/Zuständigkeit, Einfügen von Nachträgen, Anlegen von Aufgaben und Wellen. Die eigentliche Bearbeitung erfolgt weiterhin autonome über die KI (OpenCode-CLI); Kommunikationskanal bleiben **Dateien + Status im Bundle**.

Keine Änderung des festgelegten Arbeitsablaufs (`AGENTS.md`, Phasenmodell). Die App ist eine zusätzliche Funktionalität in `definitions/`.

# Architektur

```
Colab-Zelle ──► startet server.py (Python, bindet 0.0.0.0:5000)
            └──► google.colab.output.serve_kernel_port_as_window(5000)  → Browser

Browser (SPA)                Server (Flask)              Daten
├── static/index.html   ◄──►  GET/POST /api/*      ◄──►  /content/pmTool/wissen/**/*.md
├── static/app.js            (Lese-/Schreib-           (Single Source of Truth,
└── static/style.css          operationen,              dieselben Dateien wie der
                              Validierung)              OpenCode-CLI-Chat)
```

- **Kein Frontend-Build:** reines Vanilla HTML/CSS/JS (keine Frameworks, kein Bundler).
- **Kein Zweitdatenbank:** der Server liest und schreibt ausschließlich die `.md`-Dateien des Bundles.
- **Rechteklarheit:** Die App darf nur die in „Schreibrechte“ genannten Operationen ausführen; alles Weitere bleibt der KI vorbehalten.
- **App-Quelle:** `definitions/app/` (Single Source of Truth); `setup.sh` verteilt sie nach `<projekt>/app/`.

# Technologien & Werkzeuge

| Baustein | Wahl | Begründung |
|---|---|---|
| Server | Python **Flask** | schlank, eine Abhängigkeit, statische Dateien + JSON-API in einem |
| Port-Freigabe in Colab | `google.colab.output.serve_kernel_port_as_window/iframe` | eingebaut, sicher, **kein externer Tunnel/pyngrok nötig** |
| Frontend | Vanilla HTML/CSS/JS | kein Build, direkt aus Colab bedienbar |
| Parser | `python-frontmatter` oder eigene YAML-Trennung (Standardbibliothek `yaml`) | Frontmatter lesend/schreibend erhalten |
| Tests | **pytest** (API/Logik) + **Moli-Browser** (UI-Szenarien) | wie im Phasenmodell definiert |
| Versionierung | Git (Commits durch Projektmanager) | bestehender Workflow |

# Build-, Start- & Test-Befehle

**Start aus Colab (eine Zelle):**
```python
!pip install -q flask pyyaml
from google.colab import output
import subprocess, sys
subprocess.Popen([sys.executable, "app/server.py"],
                 env={"BUNDLE_ROOT": "/content/pmTool/wissen", "PORT": "5000"})
output.serve_kernel_port_as_window(5000)   # öffnet das App-Fenster im Browser
```
Lokal (ohne Colab): `BUNDLE_ROOT=./wissen PORT=5000 python3 app/server.py`

**Tests:**
```sh
python3 -m pytest app/tests/ -q          # API-/Logik-Tests (Test-first!)
bash definitions/verify.sh <projekt>     # Setup-Prüfung wie gewohnt
```
UI-Szenarien: `moli` gegen `http://localhost:5000` (siehe `tester`-Aufgaben).

**Voraussetzungen:** `flask`, `pyyaml` (in der Start-Zelle installiert), `pytest` (über `setup.sh` vorhanden).

# Datenmodell

## Frontmatter-Erweiterungen

| Feld | Werte | Wo | Verantwortlich |
|---|---|---|---|
| `owner` | `mensch` \| `ai` | Aufgaben (`task_status`-führend), Wellen | Mensch darf umschalten; KI setzt es gemäß Pipeline |
| `status` | `Klarung`, `Offen`, `In Arbeit`, `Testing`, `Dokumentation`, `Geschlossen` | Wellen & Punkte **ohne** `task_status` | Mensch: nur `Klarung`/`Geschlossen`; KI: alle |
| `task_status` / `phase` | wie Phasenmodell | Aufgaben | ausschließlich KI (Projektmanager/documenter) |

## Mapping: `task_status` → UI-Status (6 Werte)

| `task_status` | UI-Status | owner (Default) |
|---|---|---|
| `offen` | Offen | ai |
| `in Klärung` | Klarung | mensch |
| `in Planung` | Offen | ai |
| `geplant` | Offen | ai |
| `in Umsetzung` | In Arbeit | ai |
| `im Review` | Testing | ai |
| `im Test` | Testing | ai |
| `in Doku` | Dokumentation | ai |
| `zur Abnahme` | Klarung | mensch |
| `abgeschlossen` | Geschlossen | — |
| `pausiert` | Offen (mit sichtbarem Hinweis `pausiert`) | — |

Es gibt **kein zweites Statusmodell in den Dateien**: Die sechs UI-Status sind eine reine Anzeige-/Filterebene über das bestehende Modell. Wellen/Punkte ohne `task_status` tragen `status` direkt.

**owner-Default-Regel:** Ein explizit gesetztes Frontmatter-Feld `owner` hat **immer Vorrang** vor jedem Status-Default (damit eine vom Menschen umgeschaltete Zuständigkeit sichtbar bleibt). Fehlt `owner`, gilt die Spalte „owner (Default)". Für Punkte mit `status`-Feld (ohne `task_status`) gelten die Defaults: `Klarung` → `mensch`, `Offen`/`In Arbeit`/`Testing`/`Dokumentation` → `ai`, `Geschlossen` → `None` (Anzeige „—“).

## Struktur neuer Punkte

- Aufgaben: `wissen/aufgaben/<id>.md` — Format exakt nach Phasenmodell, ergänzt um `owner: ai`.
- Wellen: `wissen/wellen/<kuerzel>.md` mit `type: Welle`, `title`, `status`, `owner`, Ziel-Abschnitt und OKF-Links auf zugehörige Aufgaben (Ordner wird bei Erstanlage angelegt).
- Nachträge: Abschnitt `# Nachträge` am Dateiende jeder bearbeitbaren Datei; Einträge als
  `> **Nachtrag (Mensch, YYYY-MM-DD):** <Text>` (Blockquote-Format, mehrfach möglich, immer anfügend).

## Schreibrechte (Verbindlich)

| Operation | Mensch (App) | KI (CLI) |
|---|---|---|
| Nachtrag einfügen | ✅ | ✅ |
| Aufgabe / Welle anlegen | ✅ | ✅ |
| `owner` umschalten | ✅ | ✅ |
| Status → `Klarung`, `Geschlossen` | ✅ | ✅ |
| Pipeline-Statuswechsel (`task_status`/`phase`) | ❌ | ✅ (Projektmanager, documenter) |
| `index.md` / `features.md` / `log.md` pflegen | ❌ | ✅ (Projektmanager, documenter) |

Als **reserviert** gelten `index.md`, `log.md` und `features.md` (KI-Dateien laut Schreibrechte-Matrix): Die App darf sie weder ersetzen noch in der Übersicht führen — auch `features.md` ist für die App schreibgeschützt (Entscheidung 2026-11-14). Der Schutz greift **generell für alle App-Schreibzugriffe, auch als Ziel von Nachträgen** (Guard in `okf_bundle`, `ReservierteDateiFehler` → HTTP 403).
| Löschen von Dateien/Wellen | ❌ (MVP) | ❌ ohne PM-Entscheidung |

# Schnittstellen (JSON-API des Servers)

| Methode & Pfad | Zweck | Payload / Rückgabe |
|---|---|---|
| `GET /api/overview` | Alle Punkte für Listenansicht | Liste: `path, typ, titel, status(6), owner, zuletzt_geaendert, welle?, hinweis?, arbeitsrolle?, arbeitsrolle_label?, arbeitsstatus?` |
| `GET /api/file?path=` | Dateiinhalt + Frontmatter (Detailansicht) | `{frontmatter, markdown, nachtraege[], arbeitsrolle?, arbeitsrolle_label?, arbeitsstatus?}` |
| `POST /api/nachtrag` | Nachtrag anfügen | `{path, text}` → aktualisierte Datei |
| `POST /api/task` | Neue Aufgabe anlegen | `{titel, ziel, akzeptanz[], prioritaet, welle?}` → Pfad der neuen Datei |
| `POST /api/welle` | Neue Welle anlegen | `{titel, ziel, status, owner}` → Pfad |
| `POST /api/meta` | `owner`/erlaubte Status setzen | `{path, owner?, status?}` → neue Metadaten |
| `GET /api/wellen` / `GET /api/aufgaben` | Rohdaten je Navigationspunkt | Listen (gleiches Feldschema wie `/api/overview`) |

- **Arbeitsstatus (abgeleitet, nur lesend):** `arbeitsrolle`, `arbeitsrolle_label` und `arbeitsstatus` werden beim Lesen aus dem Frontmatter-Feld `aktuell` abgeleitet (`<Rolle>: <Text>`) und **top-level** ausgeliefert — nur für Einträge mit `typ: Task`; Nicht-Tasks und Aufgaben ohne belegbares `aktuell` tragen keines der Felder (fehlend = keine Anzeige). Aufgaben mit UI-Status „Geschlossen" liefern keine Arbeitsstatus-Felder. `frontmatter.aktuell` bleibt unverändert roh erhalten; es gibt **keinen neuen Endpunkt** und keinen Schreibpfad (Single Source of Truth: `aktuell`).

- Alle `path`-Parameter werden gegen Ausbruch aus `BUNDLE_ROOT` geprüft (normalisiert, Präfix-Check) — **reject** bei Verstößen.
- Fehler: HTTP 4xx mit `{error: "<verständliche Meldung>"}`, nie Teil-Zustände (Schreiben erst nach vollständiger Validierung).

# Nicht-funktionale Anforderungen

- **Einfachheit:** Start mit einer Colab-Zelle; kein externer Dienst, keine Tokens, kein Tunnel.
- **Datenintegrität:** Nie überschreiben statt anfügen; Frontmatter erhalten; keine stillen Löschungen.
- **Autonomie der KI:** Die App greift nicht in die Pipeline-Steuerung ein; KI bleibt jederzeit in der Lage, das Projekt ohne App fortzusetzen (Bundle ist vollständig allein lesbar).
- **Kein Informationsverlust:** Offene Fragen/Aufgaben bleiben im Bundle bestehen, bis sie geschlossen werden.
- **Sicherheit:** Keine Secrets in Dateien; Telegram-/Git-Konfiguration unberührt; Zugriff nur auf `BUNDLE_ROOT`.

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
| `freigabe` | `true` \| `false`; fehlend oder ≠ `true` = **nicht freigegeben** (fail-closed) | Aufgaben und Wellen | ausschließlich Mensch (App, `POST /api/freigabe`); KI ❌ **403** |
| `welle` | Pfad `wellen/<x>.md` (optional) | Aufgaben | beim Anlegen (`POST /api/task`, KI/App) und über `POST /api/meta`; das Read-Modell liefert es als `welle` (`GET /api/overview`, `frontmatter` von `GET /api/file`) |
| `parent` | Pfad `aufgaben/<id>.md` (optional, A34) | Aufgaben (nur Tasks) | beim Anlegen (`POST /api/task` mit `parent?`); genau ein Elternteil, maximal eine Ebene; das Read-Modell liefert es als `parent` (`GET /api/aufgaben`, `GET /api/overview`, `frontmatter` von `GET /api/file`) |

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

- Aufgaben: `wissen/aufgaben/<id>.md` — Format exakt nach Phasenmodell, ergänzt um `owner: ai`; optional `welle: wellen/<x>.md` (Pfad der zugeordneten Welle, siehe API-Tabelle) und optional `parent: aufgaben/<id>.md` (Unter-Aufgabe, A34 — genau ein Elternteil, maximal eine Ebene).
- Wellen: `wissen/wellen/<kuerzel>.md` mit `type: Welle`, `title`, `status`, `owner`, Ziel-Abschnitt und OKF-Links auf zugehörige Aufgaben (Ordner wird bei Erstanlage angelegt).
- Nachträge: Abschnitt `# Nachträge` am Dateiende jeder bearbeitbaren Datei; Einträge als
  `> **Nachtrag (Mensch, YYYY-MM-DD):** <Text>` (Blockquote-Format, mehrfach möglich, immer anfügend).
- **Slug-Regel (R2):** ASCII, kleingeschrieben, nur `a-z`/`0-9`/`-`, max. 60 Zeichen, Kollisionssuffix `-2`/`-3`. **Bewusste Asymmetrie bei leerem Slug** (PM-Entscheidung 2026-11-15, A5-B2): `neu_aufgabe` bricht mit `EingabeFehler` ab (der Pflicht-Titel muss verwertbar sein), `neu_welle` nutzt den robusten `FALLBACK_KUERZEL` — die Welle bleibt anlegbar, statt an einer exotischen Zeichenfolge zu scheitern. Kein Fehler, sondern dokumentierte Entscheidung.

## Schreibrechte (Verbindlich)

| Operation | Mensch (App) | KI (CLI) |
|---|---|---|
| Nachtrag einfügen | ✅ | ✅ |
| Aufgabe / Welle anlegen | ✅ | ✅ |
| `owner` umschalten | ✅ | ✅ |
| Status → `Klarung`, `Geschlossen` | ✅ | ✅ |
| `freigabe` setzen/entziehen (Menschen-Recht) | ✅ | ❌ (**403** — nur Projektleitung) |
| `freigabe` einer **Welle** setzen/entziehen (zweite Stufe) | ✅ | ❌ (**403** — nur Projektleitung) |
| Pipeline-Statuswechsel (`task_status`/`phase`) | ❌ | ✅ (Projektmanager, documenter) |
| `index.md` / `features.md` / `log.md` pflegen | ❌ | ✅ (Projektmanager, documenter) |

**Status-Mapping und Schreibschutz (abgeleitet, nur lesend; A35/A36):** `ui_status`, `hinweis` und `owner_default` werden serverseitig aus `status.py` abgeleitet (einzige Mapping-Quelle — der JS-Spiegel `TASK_STATUS_UI`/`OWNER_DEFAULTS` in `detail.js` ist entfernt), `schreibgeschuetzt: true` markiert reservierte Dateien (symlink-sicher über `okf_bundle.ist_reserviert(pfad) or ist_reserviert(ziel)`). Alle vier Felder stehen **top-level** in der `/api/file`-Antwort, für alle Dateitypen (`hinweis` ist immer vorhanden, `null` wenn keiner). Listen (`/api/overview`, `/api/aufgaben`, `/api/wellen`) tragen `schreibgeschuetzt` nicht (dort keine Schreibaktionen); UI-Konsequenz: bei `schreibgeschuetzt === true` blendet `detail.js` alle Schreibaktionen aus (Server-403 bleibt zweite Barriere).

Als **reserviert** gelten `index.md`, `log.md` und `features.md` (KI-Dateien laut Schreibrechte-Matrix): Die App darf sie weder ersetzen noch in der Übersicht führen — auch `features.md` ist für die App schreibgeschützt (Entscheidung 2026-11-14). Der Schutz greift **generell für alle App-Schreibzugriffe, auch als Ziel von Nachträgen** (Guard in `okf_bundle`, `ReservierteDateiFehler` → HTTP 403).
| Löschen von Dateien/Wellen | ❌ (MVP) | ❌ ohne PM-Entscheidung |

# Schnittstellen (JSON-API des Servers)

| Methode & Pfad | Zweck | Payload / Rückgabe |
|---|---|---|
| `GET /api/overview` | Alle Punkte für Listenansicht | Liste: `path, typ, titel, status(6), owner, zuletzt_geaendert, welle?, parent?, hinweis?, arbeitsrolle?, arbeitsrolle_label?, arbeitsstatus?, freigabe?, freigabe_hinweis?, neu?` |
| `GET /api/file?path=` | Dateiinhalt + Frontmatter (Detailansicht) | `{frontmatter, markdown, nachtraege[], arbeitsrolle?, arbeitsrolle_label?, arbeitsstatus?, ui_status?, hinweis?, owner_default?, schreibgeschuetzt?, freigabe?, freigabe_hinweis?, neu?, kennung?, naechste_kennung?, welle_freigabe?, wirksam_freigegeben?}` |
| `POST /api/nachtrag` | Nachtrag anfügen | `{path, text}` → aktualisierte Datei |
| `POST /api/task` | Neue Aufgabe anlegen | `{titel, ziel, akzeptanz[], prioritaet, welle?, parent?}` → Pfad der neuen Datei |
| `POST /api/welle` | Neue Welle anlegen | `{titel, ziel, status, owner}` → Pfad |
| `POST /api/meta` | `owner`/erlaubte Status/`welle` setzen | `{path, owner?, status?, welle?}` → neue Metadaten (`welle: null`/leer entfernt die Zuordnung) |
| `POST /api/freigabe` | Freigabe setzen/entziehen (**Menschen-Kanal**) | `{path, wert: true\|false}` → `{path, freigabe, frontmatter}` |
| `GET /api/wellen` / `GET /api/aufgaben` | Rohdaten je Navigationspunkt | Listen (gleiches Feldschema wie `/api/overview`) |

- **Freigabe (Menschen-Recht):** Das boolesche Frontmatter-Feld `freigabe` liefert die Lese-API top-level für `typ in ("Task", "Welle")`; nur ein exaktes `true` gilt als freigegeben (fail-closed). Ein vorhandener, aber ungültiger Rohwert (z. B. `"true"`, `1`) ergibt `freigabe: false` plus `freigabe_hinweis`. Geschrieben wird ausschließlich über `POST /api/freigabe` (Projektleitung); `POST /api/meta` und `meta.setzen` verweigern `freigabe` mit **403** ohne Schreibvorgang — auch bei `false`.
- **Wellen-Gate (abgeleitet, nur lesend):** Für Aufgaben liefert `GET /api/file` `welle_freigabe` (`true`/`false`/`null`, immer vorhanden) und `wirksam_freigegeben` (bool, immer vorhanden). Regel: `wirksam_freigegeben = Aufgabe freigegeben AND (keine Welle zugeordnet OR Welle freigegeben)`; eine fehlende, unbekannte oder nicht freigegebene Welle setzt `welle_freigabe` auf `false`/`null` und sperrt (fail-closed). Der Status steht in der Wellenliste als Marke in der Titel-Zelle (nur in der Wellen-Ansicht, nicht in Übersicht/Aufgabenliste) und im Wellen-Detail als Feld samt Knopf; der Freigabe-Pfad (`POST /api/freigabe`) schreibt in die Wellen-Datei ausschließlich `freigabe` (`# Aufgaben` bleibt unverändert), während der A11/A27-Schreibpfad (`POST /api/meta`) weiterhin `owner`/`status`/`welle` schreiben darf. Kein neuer Endpunkt — `POST /api/freigabe` aus A28 wird wiederverwendet.
- **Kennungs-Signale (abgeleitet, nur lesend):** `neu` (Aufgaben ohne gültige Kennung — Titel `^A<N>:` bzw. `^A{xxx}.{uuu}:` und Dateiname `a<N>-…` bzw. `a{xxx}.{uuu}-…` müssen übereinstimmen, Unterkennungen wie `A34.001` eingeschlossen), `kennung` (aus dem Titel, z. B. `A28` oder `A34.001`) und `naechste_kennung` (Hinweis, Maximum aus Top-Level-Titeln und Dateinamen + 1, keine Reservierung) liefert nur `GET /api/file` bzw. `GET /api/overview`/`GET /api/aufgaben` für `typ: Task`. Grammatik der Unter-Kennung (A34): `A{xxx}.{uuu}` mit `xxx` = Nummer der Eltern-Aufgabe (`[1-9][0-9]*`, keine führende Null) und `uuu` = genau drei Ziffern `001`–`999`; maximal eine Ebene (keine Unter-Unter-Aufgaben). `naechste_kennung` bleibt **top-level-only**: Unter-Nummern beeinflussen sie nicht, es gibt kein Feld `naechste_unterkennung`. Nicht-Tasks tragen keines dieser Felder; dafür gibt es **keinen neuen Endpunkt**.
- **Arbeitsstatus (abgeleitet, nur lesend):** `arbeitsrolle`, `arbeitsrolle_label` und `arbeitsstatus` werden beim Lesen aus dem Frontmatter-Feld `aktuell` abgeleitet (`<Rolle>: <Text>`) und **top-level** ausgeliefert — nur für Einträge mit `typ: Task`; Nicht-Tasks und Aufgaben ohne belegbares `aktuell` tragen keines der Felder (fehlend = keine Anzeige). Aufgaben mit UI-Status „Geschlossen" liefern keine Arbeitsstatus-Felder. `frontmatter.aktuell` bleibt unverändert roh erhalten; es gibt **keinen neuen Endpunkt** und keinen Schreibpfad (Single Source of Truth: `aktuell`).

- Alle `path`-Parameter werden gegen Ausbruch aus `BUNDLE_ROOT` geprüft (normalisiert, Präfix-Check) — **reject** bei Verstößen.
- Fehler: HTTP 4xx mit `{error: "<verständliche Meldung>"}`, nie Teil-Zustände (Schreiben erst nach vollständiger Validierung).
- **Fehlercodes (A9-K3):** Bei `POST /api/meta` gilt die Whitelist: jeder Statuswert außer `Klarung`/`Geschlossen` — auch `Testing` (gültiger Wellen-Status, aber nicht über `meta` setzbar) oder unbekannte Werte — wird mit **403** abgewiesen, ebenso ein unbekannter `owner`; die Rechteprüfung greift fail-closed vor dem Lesen (403 auch bei nicht existierender Datei). Beim Anlegen (`POST /api/task`/`POST /api/welle`) führen ungültige Werte und Payload-Fehler (fehlende Pflichtfelder, leerer Text) zu **400**. Pfad-/Frontmatter-Fehler → 400, fehlende Datei → 404, Traversal → 400.

# Nicht-funktionale Anforderungen

- **Einfachheit:** Start mit einer Colab-Zelle; kein externer Dienst, keine Tokens, kein Tunnel.
- **Datenintegrität:** Nie überschreiben statt anfügen; Frontmatter erhalten; keine stillen Löschungen.
- **Nebenläufigkeit (R8, bekannte Grenze, A9-K4):** Schreiben erfolgt atomar (temporäre Datei + `os.replace`) mit Re-Read, aber **ohne Locking** im MVP. Das TOCTOU-Fenster zwischen Prüfung und Schreiben ist bekannt — gleichzeitige Schreibzugriffe von KI (CLI) und App können sich gegenseitig überschreiben (Lost-Update, letzter Schreiber gewinnt). Halbe Zustände entstehen dadurch nicht; das Risiko ist bewusst akzeptiert, Locking bleibt Post-MVP.
- **Autonomie der KI:** Die App greift nicht in die Pipeline-Steuerung ein; KI bleibt jederzeit in der Lage, das Projekt ohne App fortzusetzen (Bundle ist vollständig allein lesbar).
- **Kein Informationsverlust:** Offene Fragen/Aufgaben bleiben im Bundle bestehen, bis sie geschlossen werden.
- **Sicherheit:** Keine Secrets in Dateien; Telegram-/Git-Konfiguration unberührt; Zugriff nur auf `BUNDLE_ROOT`.

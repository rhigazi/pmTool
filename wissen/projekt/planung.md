---
type: Plan
title: TDD-Aufgabenplan OKF-Projekt-Manager (SPA) — MVP
description: Ergebnis der Planungsphase (planner): 17 Aufgaben A1–A17 mit Testfällen, Akzeptanzkriterien, Abhängigkeiten, Parallelisierung und PM-Entscheidungen zu den Risiken.
tags: [planung, aufgaben, tdd, mvp]
generated: { by: opencode/mimo-v2.6-pro, at: 2026-11-14T00:00:00Z }
status: freigegeben
---

# Grundlagen

Erstellt vom `planner` aus: `user-stories/us-1…7`, `technische-spec.md`, `phasen.md`, `prd.md`, `definitions/AGENTS.md`, `definitions/setup.sh`, `definitions/verify.sh`, bestehendem Teststil (`definitions/tools/tests/test_telegram_send.py`). Vom Projektmanager freigegeben (Risiken R1–R14 entschieden, siehe unten).

**Zielstruktur** (Quelle `definitions/app/`, Verteilung nach `<projekt>/app/`):

```
definitions/app/
  server.py          # Flask-App-Factory, Routen, JSON-Fehlerformat, CLI-Start
  okf_bundle.py      # Pfadschutz, Frontmatter-/Datei-I/O, atomares Schreiben, Bundle-Scan
  status.py          # Mapping task_status/status → 6 UI-Status + owner-Default
  overview.py        # Scan → Übersichtsliste
  nachtrag.py        # Nachtrag anfügen
  neu_aufgabe.py     # Aufgabe anlegen
  neu_welle.py       # Welle anlegen
  meta.py            # owner/Status setzen mit Rechteprüfung
  start_colab.py     # Colab-Startzelle (Port-Freigabe, Fallback)
  static/index.html
  static/style.css
  static/js/api.js       # fetch-Wrapper + Fehleranzeige
  static/js/liste.js     # Tabellen-/Filterrendering
  static/js/detail.js    # Detailansicht, Nachtrag, owner/Status
  static/js/formulare.js # Aufgabe/Welle anlegen
  static/js/projekt.js   # Entscheidungen-/Projekt-Ansicht
  static/js/app.js       # Router/Verdrahtung
  tests/                 # pytest (conftest.py + test_*.py)
```

**Verbindliche Testregeln für alle Aufgaben**
- Testbefehl Quelle: `python3 -m pytest definitions/app/tests -q`; installiert: `python3 -m pytest app/tests -q`.
- Tests arbeiten **ausschließlich** auf Fixture-Bundles unter `tmp_path` (Kopie einer Mini-Bundle-Vorlage). Das echte Bundle `/content/pmTool/wissen` wird von pytest **nie** beschrieben.
- Importstil: `sys.path.insert(0, str(Path(__file__).resolve().parents[1]))`.
- Jeder Task beginnt mit rotem Test (Red), dann Minimum-Implementierung (Green), dann Refactor.

# Aufgabenliste

## A1 — Fundament: `okf_bundle.py` (Pfadschutz, Frontmatter-I/O, Scan)

- **user_story:** US-7 (primär), US-1/2/3/4 (Basis) · **Priorität:** hoch · **Konfliktgruppe:** G1
- **Betroffene Dateien:** `definitions/app/okf_bundle.py`, `definitions/app/tests/conftest.py`, `definitions/app/tests/test_okf_bundle.py`, `definitions/app/tests/fixtures/bundle_min/**`
- **Abhängigkeiten:** keine — Startpunkt Backend-Kette

**Ziel:** Zentrale, getestete Zugriffsschicht: `resolve_path(rel)` mit Ausbruchsschutz (normalisiert, `realpath`-Präfix-Check, Symlink-Ausbruch), `lesen(pfad)` (strikt, Frontmatter via `yaml.safe_load`), `lesen_tolerant(pfad)` (ohne Frontmatter → `{}`), `set_meta(pfad, updates)` (nur Frontmatter-Keys, Body byte-identisch), `scan()` (alle `.md` außer `index.md`/`log.md`), atomares Schreiben (`tmp` + `os.replace`), `ist_reserviert(pfad)`. Framework-frei (kein Flask-Import).

**Akzeptanzkriterien**
- Pfade außerhalb `BUNDLE_ROOT` werden mit `BundlePfadFehler` abgewiesen — vor jedem Dateizugriff.
- `set_meta` verändert ausschließlich die angegebenen Frontmatter-Keys; übrige Keys und Body byte-identisch.
- Schreibvorgänge atomar: bei Fehler bleibt die Originaldatei unverändert.

**Testfälle (TDD)**
| # | Testfall | Ausführung | Erwartetes Ergebnis |
|---|---|---|---|
| 1 | Pfad im Bundle | `resolve_path("aufgaben/a1.md")` | absoluter Pfad unter `BUNDLE_ROOT` |
| 2 | Ausbruch `..` | `resolve_path("../../etc/passwd")` | `BundlePfadFehler`, kein Zugriff |
| 3 | Absoluter Pfad | `resolve_path("/etc/passwd")` | `BundlePfadFehler` |
| 4 | Verschleierter Ausbruch | `aufgaben/../../x.md`, `a/%2e%2e/b.md` | `BundlePfadFehler` |
| 5 | Symlink-Ausbruch | Symlink im Bundle → außerhalb | `BundlePfadFehler` |
| 6 | Frontmatter lesen | Fixture `aufgaben/a1.md` | `fm["type"]=="Task"`, Body ohne `---`-Block |
| 7 | FM fehlt (strikt) | Datei ohne `---` | `FrontmatterFehler` |
| 8 | FM fehlt (tolerant) | `lesen_tolerant()` | `({}, volltext)`, keine Exception |
| 9 | FM-Erhalt | `set_meta(p, {"owner":"ai"})` | `type`/`title`/`user_story` unverändert, Body-SHA256 identisch |
| 10 | Atomarität | `os.replace` monkeypatch → `OSError` | Original byte-identisch, Exception propagiert |
| 11 | Scan | Bundle mit `index.md`, `log.md`, 2 Punkten | genau die 2 Nicht-Reservierten |
| 12 | Reserviert | `ist_reserviert` für `index.md`/`log.md`/Punkt | `True, True, False` |

## A2 — Status-Mapping `status.py`

- **user_story:** US-1, US-5 · **Priorität:** hoch · **Konfliktgruppe:** G2 (kein `conftest.py`)
- **Betroffene Dateien:** `definitions/app/status.py`, `definitions/app/tests/test_status.py`
- **Abhängigkeiten:** keine (reine Funktionen) — **parallel zu A1**

**Ziel:** `ui_status(frontmatter) -> (status, hinweis|None)` und `owner_default(frontmatter)` gemäß Mapping-Tabelle der Spec; keine Dateizugriffe.

**Akzeptanzkriterien:** Alle 11 Mapping-Zeilen 1:1 (parametrisierter Test); ohne `task_status` → `status` direkt, ohne beide → `("Offen","ohne Status")`; `pausiert` → `("Offen","pausiert")`; `owner` fehlt → `None`; unbekannte Werte ohne Exception.

**Testfälle (TDD)**
| # | Testfall | Erwartetes Ergebnis |
|---|---|---|
| 1 | Mapping vollständig (parametrisiert, alle 11 Paare) | exakt erwarteter UI-Status |
| 2 | `abgeschlossen` | `("Geschlossen", None)`, `owner_default` → `None` |
| 3 | `pausiert` | `("Offen", "pausiert")` |
| 4 | Welle ohne task_status (`status: In Arbeit`) | `("In Arbeit", None)` |
| 5 | Kein Statusfeld | `("Offen", "ohne Status")` |
| 6 | Unbekannter task_status | `("Offen", <wert>)`, keine Exception |
| 7 | owner-Defaults | `offen`→`ai`, `in Klärung`→`mensch`, `status: Klarung`→`mensch` |
| 8 | owner fehlt | `None` |

## A3 — Nachtrag anfügen `nachtrag.py`

- **user_story:** US-2 · **Priorität:** hoch · **Konfliktgruppe:** G3 · **Abhängigkeiten:** A1

**Ziel:** `anfuegen(bundle_rel_pfad, text, datum)`: Abschnitt `# Nachträge` am Dateiende anlegen bzw. am Ende ergänzen; Format `> **Nachtrag (Mensch, YYYY-MM-DD):** <Text>`; mehrzeilig zeilenweise als Blockquote; alles andere byte-identisch.

**Akzeptanzkriterien:** Bestehender Inhalt byte-identisch (SHA256-Präfixvergleich); nur anfügen; leere Eingabe → `EingabeFehler`, Datei unverändert; Format per Regex; Datum als injizierbarer Parameter.

**Testfälle (TDD)**
| # | Testfall | Erwartetes Ergebnis |
|---|---|---|
| 1 | Abschnitt fehlt | Datei endet mit `# Nachträge` + Markerzeile |
| 2 | Markerformat | Regex `^> \*\*Nachtrag \(Mensch, \d{4}-\d{2}-\d{2}\):\*\* .+$` trifft zu |
| 3 | Abschnitt vorhanden | 2 Einträge, alter unverändert/oberhalb |
| 4 | Inhaltsschutz | SHA256-Präfix identisch |
| 5 | Frontmatter unverändert | identisch inkl. `type` |
| 6 | Leere Eingabe | `EingabeFehler`, Datei-Hash unverändert |
| 7 | Mehrzeilig | zwei `>`-Zeilen, kein Formatbruch |
| 8 | Pfad außerhalb | `BundlePfadFehler`, keine Datei |
| 9 | Reserve `log.md` | nur anfügend erlaubt, Präfix-Hash identisch |

## A4 — Aufgabe anlegen `neu_aufgabe.py`

- **user_story:** US-3 · **Priorität:** hoch · **Konfliktgruppe:** G4 · **Abhängigkeiten:** A1

**Ziel:** `anlegen({titel, ziel, akzeptanz[], prioritaet, welle?, user_story?})` → `aufgaben/<slug>.md` im Phasen-Format inkl. `owner: ai`, `task_status: offen`, `phase: 2 Planung`, `assigned_to: coder`; Slug-Normalisierung (Umlaute → ASCII, Sonderzeichen → `-`, max. 60), Kollisionssuffix `-2`, `-3`.

**Akzeptanzkriterien:** Frontmatter exakt nach Phasenmodell + `owner: ai`; Body mit `# Ziel`, `# Akzeptanzkriterien`, `# Testfälle (TDD)`, `# Kontext`, `# Betroffene Dateien`, `# Ergebnisse`; ungültige Eingaben → `EingabeFehler` ohne Datei; nie überschreiben; OKF-konform (`---\n` Beginn, genau ein `\n` am Ende); sofort als `Offen`/`ai` sichtbar (Integrationstest mit A2/A8).

**Testfälle (TDD)**
| # | Testfall | Erwartetes Ergebnis |
|---|---|---|
| 1 | Happy Path | Datei existiert, Rückgabe = relativer Pfad |
| 2 | Frontmatter | `type: Task`, `task_status: offen`, `phase: 2 Planung`, `priority`, `assigned_to: coder`, `owner: ai` |
| 3 | user_story-Verweis | Feld gesetzt |
| 4 | Body-Abschnitte | alle 6 Überschriften vorhanden |
| 5 | Akzeptanzliste | 3 Einträge als `- `-Zeilen |
| 6 | Slug | `Übersicht: Status & owner!` → `uebersicht-status-owner.md` |
| 7 | Kollision | zweite Datei `…-2.md`, erste unverändert |
| 8 | Ungültige Eingaben (je einzeln) | `EingabeFehler`, Dateianzahl unverändert |
| 9 | Pfad-Traversal im Titel | Datei bleibt in `aufgaben/`, Slug bereinigt |
| 10 | Zeilenende | letztes Byte `\n` |

## A5 — Welle anlegen `neu_welle.py`

- **user_story:** US-4 · **Priorität:** hoch · **Konfliktgruppe:** G5 · **Abhängigkeiten:** A1 — parallel zu A4

**Ziel:** `anlegen({titel, ziel, status, owner})` → `wellen/<kuerzel>.md` mit `type: Welle`, `title`, `status` (nur 6 UI-Werte), `owner`, Body `# Ziel` + `# Aufgaben` (Linkliste, leer startend). Ordner `wellen/` bei Erstanlage erzeugen.

**Akzeptanzkriterien:** Ordner wird angelegt; Status/owner validiert (sonst `EingabeFehler` ohne Datei); Kollisionssuffix; erscheint in `GET /api/wellen` (Integrationstest).

**Testfälle (TDD)**
| # | Testfall | Erwartetes Ergebnis |
|---|---|---|
| 1 | Happy Path | `wellen/<kuerzel>.md` existiert |
| 2 | Frontmatter | `type: Welle`, `title`, `status`, `owner` |
| 3 | Ordner-Erstanlage | Ordner + Datei entstehen |
| 4 | Ungültiger Status | `EingabeFehler`, keine Datei |
| 5 | Ungültiger owner | `EingabeFehler` |
| 6 | Leerer Titel | `EingabeFehler` |
| 7 | Kollision | `…-2.md`, erste unverändert |
| 8 | Body | `# Ziel` und `# Aufgaben` vorhanden |
| 9 | Kürzel | `Wave 1 — MVP` → `wave-1-mvp.md` |

## A6 — Meta-Update `meta.py` (owner/Status mit Rechteprüfung)

- **user_story:** US-5, US-7 · **Priorität:** hoch · **Konfliktgruppe:** G6 · **Abhängigkeiten:** A1, A2

**Ziel:** `setzen(pfad, owner=None, status=None)` prüft die Schreibrechte-Matrix **serverseitig**: `owner` ∈ {`mensch`,`ai`}; `status` ∈ {`Klarung`,`Geschlossen`} — bei Aufgaben als `task_status: in Klärung`/`abgeschlossen` (Entscheidung R1), bei Punkten ohne `task_status` als `status`-Feld. Alles andere → `RechteFehler` (HTTP 403). Reservierte Dateien/fehlendes Frontmatter abweisen. owner+status in **einem** atomaren Schreibvorgang.

**Testfälle (TDD)**
| # | Testfall | Erwartetes Ergebnis |
|---|---|---|
| 1 | owner → ai | gesetzt, Body-SHA256 identisch |
| 2 | owner → mensch | gesetzt |
| 3 | owner ungültig | `RechteFehler`, Hash unverändert |
| 4 | Status Klarung (Aufgabe) | `task_status: in Klärung` |
| 5 | Status Geschlossen (Aufgabe) | `task_status: abgeschlossen` |
| 6 | Status Klarung (Welle) | `status: Klarung` |
| 7 | Pipeline-Status verboten (`In Arbeit`) | `RechteFehler` (403), Datei unverändert |
| 8 | Reservierte Datei | `RechteFehler` |
| 9 | Fehlendes Frontmatter | `FrontmatterFehler`, keine Änderung |
| 10 | Kombiniert | beide Felder, ein Schreibvorgang |
| 11 | „zuletzt geändert" | mtime nachher ≥ vorher |
| 12 | Pfad außerhalb | `BundlePfadFehler` |

## A7 — Server-Gerüst & Start `server.py`

- **user_story:** US-6, US-1 · **Priorität:** hoch · **Konfliktgruppe:** G7a — **seriell zu A8, A9** · **Abhängigkeiten:** A1

**Ziel:** `create_app(bundle_root)` (App-Factory), statische Auslieferung, einheitlicher JSON-Fehlerhandler (`{error}` mit 4xx/5xx, nie HTML-Traceback), `main()` mit `BUNDLE_ROOT`/`PORT` aus env, Bindung `0.0.0.0`, Exit ≠ 0 bei belegtem Port/ungültigem `BUNDLE_ROOT`. Lokal ohne `google.colab` startbar.

**Testfälle (TDD)**
| # | Testfall | Erwartetes Ergebnis |
|---|---|---|
| 1 | Index erreichbar | 200, enthält `<html` |
| 2 | Statik | 200, `text/css` |
| 3 | 404-Format | 404 JSON mit `error` |
| 4 | 500-Format | 500 JSON `{error}`, kein `Traceback` im Body |
| 5 | Port belegt | Exit ≠ 0, stderr „belegt" |
| 6 | BUNDLE_ROOT fehlt | Exit ≠ 0, stderr nennt `BUNDLE_ROOT` |
| 7 | Bind-Adresse | `host == "0.0.0.0"` |
| 8 | Port aus env | `PORT=8123` → `port=8123` |

## A8 — Lese-API: overview / file / aufgaben / wellen

- **user_story:** US-1, US-4, US-7 · **Priorität:** hoch · **Konfliktgruppe:** G7b+G7a — **nicht parallel zu A7/A9** · **Abhängigkeiten:** A7, A1, A2

**Ziel:** `GET /api/overview` (Liste `path, typ, titel, status, owner, zuletzt_geaendert, hinweis?, welle?`), `GET /api/file?path=` (`{frontmatter, markdown, nachtraege[]}`), `GET /api/aufgaben`, `GET /api/wellen`. Sortierung `zuletzt_geaendert` absteigend, Tie-Breaker `path`.

**Akzeptanzkriterien:** Alle nicht-reservierten `.md` mit korrektem Mapping; ISO-8601-Zeitstempel; Traversal → 400 ohne Inhalte; fehlende Datei → 404; Datei ohne Frontmatter bricht nichts; `nachtraege[]` parst Markerzeilen.

**Testfälle (TDD)**
| # | Testfall | Erwartetes Ergebnis |
|---|---|---|
| 1 | Overview-Liste | 200, 3 Einträge |
| 2 | Feldschema | Keys ⊇ `path, typ, titel, status, owner, zuletzt_geaendert` |
| 3 | Status-Mapping (`in Umsetzung`) | `status == "In Arbeit"` |
| 4 | Sortierung | absteigend, Tie-Breaker path |
| 5 | Reserve ausgeschlossen | `index.md`/`log.md` nicht gelistet |
| 6 | Detaildatei | `frontmatter.type == "Task"`, `markdown` ohne FM, `nachtraege` Liste |
| 7 | Traversal | 400 `{error}`, Body ohne `root:` |
| 8 | Fehlende Datei | 404 `{error}` |
| 9 | Nur Aufgaben | nur `aufgaben/*` |
| 10 | Nur Wellen | nur `wellen/*`; leeres Verzeichnis → `[]` |
| 11 | Datei ohne FM | `typ == "unbekannt"`, 200 |
| 12 | Nachtrag-Parsing | Marker korrekt ausgelesen |

## A9 — Schreib-API: nachtrag / task / welle / meta

- **user_story:** US-2, US-3, US-4, US-5, US-7 · **Priorität:** hoch · **Konfliktgruppe:** G7c — **nach A8** · **Abhängigkeiten:** A8, A3, A4, A5, A6

**Ziel:** POST-Endpunkte gemäß Spec; Validierung vollständig **vor** dem Schreiben (kein Teilzustand), Fehler 4xx `{error}` mit korrektem Code (403 für Rechteverstöße), Pfade gegen `BUNDLE_ROOT`.

**Testfälle (TDD)**
| # | Testfall | Erwartetes Ergebnis |
|---|---|---|
| 1 | Nachtrag ok | 200, Antwort enthält Marker; Datei enthält Marker |
| 2 | Nachtrag leer | 400, Hash unverändert |
| 3 | Aufgabe ok | 200 `{path}`; in `/api/overview` mit `Offen`/`ai` |
| 4 | Aufgabe unvollständig | 400, keine neue Datei |
| 5 | Welle ok | 200 `{path}`; in `/api/wellen` |
| 6 | Welle ungültiger Status | 400 `{error}` |
| 7 | Meta owner | 200, `owner: ai` |
| 8 | Meta Status verboten (`Testing`) | 403 `{error}`, Datei unverändert |
| 9 | Meta reserviert (`index.md`) | 400/403 `{error}` |
| 10 | Traversal (alle 4 Endpunkte) | 400 `{error}` |
| 11 | JSON-Fehlerformat | `application/json`, `error` nicht leer |
| 12 | Kein Teilzustand | weder Datei noch Verzeichnis |

## A10 — Frontend-Gerüst: Navigation, Layout, Router, API-Client

- **user_story:** US-1, US-6 · **Priorität:** hoch · **Konfliktgruppe:** G8 — **Startpunkt Frontend-Kette** · **Abhängigkeiten:** keine (Moli-Test braucht A7)

**Ziel:** `index.html` mit fünf Navigationspunkten (Übersicht, Wellen, Aufgaben, Entscheidungen, Projekt mit Unterpunkten Konzept, Technische Spec, User Stories, Phasen, Log), allen Container-IDs, `<meta viewport>`, `<script type="module" src="/static/js/app.js">`; `style.css`; `api.js` (fetch-Wrapper, einheitliche Fehleranzeige); `app.js` (Hash-Router). **Alle späteren JS-Arbeiten in eigenen Modulen — `index.html` danach nicht mehr anfassen.** Kein CDN, kein Build.

**Testfälle**
| # | Testfall | Erwartetes Ergebnis |
|---|---|---|
| 1 | Navigation vorhanden (statisch) | 5 Labels + 5 Unterpunkte |
| 2 | Container-IDs | `ansicht`, `fehler`, `tabelle` u. a. vorhanden |
| 3 | Modul-Einbindung | `type="module"` + `app.js` |
| 4 | API-Wrapper | `getJson`/`postJson` exportiert |
| 5 | **Moli:** Seite lädt | 5 Navigationspunkte sichtbar |
| 6 | **Moli:** alle Punkte klickbar | Ansicht wechselt, aktiv markiert, keine Konsolenfehler |
| 7 | **Moli:** Projekt-Unterpunkte | gelistet |
| 8 | **Moli:** Serverfehler | sichtbare Fehlermeldung, keine leere Seite |

## A11 — Listenansicht mit Filtern und Klarung-Hervorhebung

- **user_story:** US-1, US-5 · **Priorität:** hoch · **Konfliktgruppe:** G9 — **nach A10** · **Abhängigkeiten:** A8, A10

**Ziel:** `liste.js` rendert Tabelle (Titel, Status, owner, zuletzt geändert) aus `/api/overview` (bzw. `/api/aufgaben`, `/api/wellen`); Dropdown-Filter Status (6 + alle) und owner (alle/mensch/ai/ohne); „Klarung"-Zeilen hervorgehoben; Leer-/Fehlerzustand; kein automatisches Ausblenden.

**Testfälle (Moli)**
| # | Szenario | Erwartetes Ergebnis |
|---|---|---|
| 1 | Spalten | Kopfzeile vollständig, Zeilenanzahl = Fixture |
| 2 | Statusfilter `Klarung` | nur Klarung-Zeilen |
| 3 | owner-Filter `mensch` | nur mensch-Zeilen |
| 4 | Kombination | Schnittmenge |
| 5 | Reset | alle Zeilen da |
| 6 | Hervorhebung | abweichende Farbe/Klasse sichtbar |
| 7 | Leerzustand | „Keine Einträge" |
| 8 | Fehlerzustand | sichtbare Meldung, keine JS-Exception |
| 9 | Aufgabenpunkt | nur Aufgaben, keine Wellen |

## A12 — Detailansicht: Markdown, Nachtrag, owner/Status-Bedienung

- **user_story:** US-2, US-5, US-7 · **Priorität:** hoch · **Konfliktgruppe:** G9 — **nach A11** · **Abhängigkeiten:** A8, A9, A10

**Ziel:** Zeilenklick → Detailansicht mit Frontmatter-Kopf und gerendertem Markdown (Minimal-Renderer, XSS-sicher via `textContent`), Formular „Nachtrag einfügen" (POST, sofortige Anzeige), owner-Umschalter, **nur** Status-Buttons `Klarung`/`Geschlossen`.

**Testfälle (Moli)**
| # | Szenario | Erwartetes Ergebnis |
|---|---|---|
| 1 | Detail öffnen | Titel, FM-Kopf, gerenderter Text |
| 2 | Nachtrag speichern | Marker sofort sichtbar |
| 3 | Persistenz | nach Reload einmalig vorhanden |
| 4 | Leerer Nachtrag | Fehlermeldung, kein Eintrag |
| 5 | owner umschalten | Anzeige wechselt, in Liste sichtbar |
| 6 | Status-Buttons | genau „Klarung" und „Geschlossen" |
| 7 | Klarung setzen | Liste zeigt `Klarung` + `mensch`, hervorgehoben |
| 8 | Geschlossen setzen | `Geschlossen`, bleibt in der Liste |
| 9 | XSS-Schutz | `<script>` als Text, keine Ausführung |
| 10 | 403-Pfad | Fehlermeldung sichtbar, Datei unverändert |

## A13 — Formulare: Aufgabe und Welle anlegen

- **user_story:** US-3, US-4 · **Priorität:** hoch · **Konfliktgruppe:** G9 — **nach A12** · **Abhängigkeiten:** A9, A10

**Ziel:** Formulare Aufgabe (Titel, Ziel, Akzeptanz mehrzeilig, Priorität, optional Welle/User Story) und Welle (Titel, Ziel, Status, owner); Erfolg zeigt Pfad + kopierbaren Kurzkontext für die KI-Übergabe; inline Validierung; Button während Request deaktiviert.

**Testfälle (Moli)**
| # | Szenario | Erwartetes Ergebnis |
|---|---|---|
| 1 | Aufgabe anlegen | Erfolg mit Pfad; Liste: Titel, `Offen`, `ai` |
| 2 | Pflichtfeld leer | Feldfehler, kein Eintrag |
| 3 | Akzeptanz mehrzeilig | 3 `- `-Einträge in der Datei |
| 4 | Kurzkontext | Titel, Pfad, Ziel sichtbar/kopierbar |
| 5 | Welle anlegen | Welle in Liste, Spalten korrekt |
| 6 | Welle ungültig | Feldfehler, kein Eintrag |
| 7 | Doppelklick | genau eine Datei |
| 8 | Wellen-Zuordnung | Zuordnung in beiden Ansichten erkennbar |

## A14 — Entscheidungen- und Projekt-Ansicht

- **user_story:** US-1 · **Priorität:** mittel · **Konfliktgruppe:** G9 — **nach A13** · **Abhängigkeiten:** A8, A10

**Ziel:** „Entscheidungen" listet Einträge aus `entscheidungen/log.md` (`## YYYY-MM-DD: Titel` → Datum + Titel, Klick → Detail). „Projekt" listet die fünf Unterpunkte und öffnet sie. **Kein neuer Server-Endpunkt** (nur `GET /api/file`).

**Testfälle (Moli)**
| # | Szenario | Erwartetes Ergebnis |
|---|---|---|
| 1 | Entscheidungen | alle Einträge mit Datum + Titel |
| 2 | Eintrag öffnen | Detail der Log-Datei |
| 3 | Projekt-Unterpunkte | 5 gelistet |
| 4 | Spec öffnen | Detail mit gerendertem Inhalt |
| 5 | Fehlende Datei | Fehlermeldung, kein leerer Screen |

## A15 — `setup.sh`/`verify.sh` um App-Verteilung erweitern

- **user_story:** US-6, US-7 · **Priorität:** mittel · **Konfliktgruppe:** G10 — parallel möglich · **Abhängigkeiten:** A1, A7, A10

**Ziel:** Neuer setup-Abschnitt „App (`app/`)" nach bestehendem Muster (`install_file`, Verzeichnisse wie `tools/` mit `cp -r` und Skip-Logik): verteilt `*.py`, `static/`, `tests/` nach `<ziel>/app/`. Ohne `--force` nie überschreiben; bestehende Abschnitte/Nummern funktional unverändert. `verify.sh` prüft zusätzlich `app/server.py`, `app/static/index.html`, `python3 -m pytest app/tests -q`. `README.md`-Tabelle um `app/` ergänzen.

**Testfälle (pytest via `subprocess`, `tmp_path`)**
| # | Testfall | Erwartetes Ergebnis |
|---|---|---|
| 1 | Erstinstallation | Exit 0; `app/server.py` u. a. vorhanden |
| 2 | Idempotenz | Datei unverändert, „übersprungen" |
| 3 | `--force` | veränderte Datei wieder Original |
| 4 | Bestandsschutz | Marker in `AGENTS.md` bleibt erhalten |
| 5 | Verify grün | Exit 0 |
| 6 | Verify rot | Exit 1, nennt `app/server.py` |
| 7 | Tests mitverteilt | `pytest tmp/app/tests -q` Exit 0 |
| 8 | Keine Regression | Abschnitte 1–8 weiterhin vorhanden |

## A16 — Colab-Startzelle `start_colab.py`

- **user_story:** US-6 · **Priorität:** hoch · **Konfliktgruppe:** G11 (README nur in Abstimmung mit A15: **A15 zuerst**) · **Abhängigkeiten:** A7

**Ziel:** Ausführbare/importierbare Startzelle: prüft/installiert `flask`, `pyyaml`; startet `server.py` als Subprozess mit `BUNDLE_ROOT=/content/pmTool/wissen`, `PORT` (Default 5000); erkennt belegten Port („läuft bereits" statt Doppelstart); ruft `google.colab.output.serve_kernel_port_as_window(port)`; ohne Colab → URL-Hinweis `http://localhost:<port>`. Kein Schreibzugriff aufs Bundle.

**Testfälle (gemockt)**
| # | Testfall | Erwartetes Ergebnis |
|---|---|---|
| 1 | Port-Freigabe | `serve_kernel_port_as_window(5000)` genau einmal |
| 2 | Subprozess-Env | `BUNDLE_ROOT == /content/pmTool/wissen`, `PORT` gesetzt |
| 3 | Ohne Colab | Exit 0, Ausgabe `http://localhost:5000` |
| 4 | Port belegt | „läuft bereits", kein `Popen` |
| 5 | Fehlende Pakete | `pip install`-Aufruf (gemockt) |
| 6 | Kein Bundle-Schreibzugriff | Tree-Hash identisch |

## A17 — End-to-End-Absicherung & Abnahmelauf

- **user_story:** US-7 (integrierend US-1…US-6) · **Priorität:** hoch · **Konfliktgruppe:** G12 · **Abhängigkeiten:** A1–A16

**Ziel:** Gesamtsuite grün, automatisierter E2E-Lauf über die JSON-API, Moli-Kernszenario auf **Test-Bundle** `/tmp/opencode/moli-bundle` (nie `/content/pmTool/wissen`).

**Testfälle**
| # | Testfall | Erwartetes Ergebnis |
|---|---|---|
| 1 | API-E2E | Overview → Nachtrag → Klarung → owner `ai` → konsistente Werte |
| 2 | Frontmatter intakt | `type`/`title` unverändert, genau 1 Nachtrag |
| 3 | Bundle unberührt | Hash von `/content/pmTool/wissen` vor/nach identisch |
| 4 | Gesamtsuite | `pytest definitions/app/tests -q` Exit 0 |
| 5 | Verify | `bash definitions/verify.sh /content` Exit 0 |
| 6 | Moli-E2E | Übersicht → Aufgabe → Nachtrag → Marker → Klarung → Liste → owner `ai`, keine Konsolenfehler |
| 7 | Reset-Fähigkeit | reproduzierbar grün |

# Reihenfolge & Abhängigkeiten

```
A1 ──┬─► A3   ├─► A4   ├─► A5   ├─► A6 (zusätzlich A2)   └─► A7 ─► A8 ─► A9
A2 ──┘                          │                              ├─► A12 (zusätzlich A10)
                                │                              └─► A14 (zusätzlich A10)
A10 ─► A11 (A8) ─► A12 ─► A13 ─► A14
A7 ─► A16        A1+A7+A10 ─► A15        alle ─► A17
```

| Takt | Backend | Frontend | Sonstiges |
|---|---|---|---|
| 1 | A1, A2 (parallel) | A10 (Gerüst, ohne Live-Test) | — |
| 2 | A3, A4, A5, A6 (parallel), A7 | — | — |
| 3 | A8 | A11 (Test nach A8) | A16, A15 (nach A10/A7) |
| 4 | A9 | A12 (Test nach A9) | — |
| 5 | — | A13, A14 | — |
| 6 | A17 | A17 (Moli) | — |

**Zwingend seriell:** `server.py` (A7→A8→A9) und `static/js/app.js` (A10→A14); A1 vor A3–A7; A2 vor A6/A8; A17 zuletzt. **Parallel möglich:** Backend-Kette ‖ Frontend-Kette (keine gemeinsamen Dateien); A15/A16 sobald Struktur steht.

**Konfliktmatrix:** `okf_bundle.py`+`conftest.py` → A1 allein · `status.py` → A2 · `nachtrag/neu_aufgabe/neu_welle/meta` → A3–A6 je exklusiv · `server.py` → A7/A8/A9 seriell · `overview.py` → A8 · `index.html`/`style.css` → A10 · `app.js` → A10–A14 seriell · `api.js` → A10 · `setup.sh`/`verify.sh` → A15 · `README.md` → A15 dann A16 · `start_colab.py` → A16 · Fixtures → A1, danach A17.

# Entscheidungen des Projektmanagers zu den Risiken

| # | Punkt | Entscheidung |
|---|---|---|
| R1 | Schreibrecht `task_status` | App darf ausschließlich `in Klärung` und `abgeschlossen` setzen (Teilmenge); alles andere 403. **Bestätigt** (siehe Entscheidungslog). |
| R2 | ID-/Slug-Konvention | ASCII-Slug aus Titel, max. 60 Zeichen, Kollision `-2`/`-3`. **Entschieden.** |
| R3 | `owner` fehlt in Bestandsdateien | Anzeige „—", Filteroption „ohne owner"; **keine** automatische Migration. |
| R4 | Overview-Umfang | Alle nicht-reservierten `.md` (`type` als `typ`), `index.md`/`log.md` ausgeschlossen. |
| R5 | Wellen-Struktur fehlt | Vom PM nachgepflegt: `wissen/wellen/index.md` angelegt, in `wissen/index.md` verlinkt. |
| R6 | Markdown-Rendering | Eigener Minimal-Renderer, `textContent`, kein CDN. |
| R7 | „zuletzt geändert" | mtime als ISO-Zeitstempel, lokal formatiert; Frontmatter-`updated` ist Ausbau. |
| R8 | Gleichzeitige Schreibzugriffe | MVP: atomares Schreiben + Re-Read, kein Locking; als bekanntes Risiko dokumentiert. |
| R9 | Testisolation | **Verbindlich:** Test-Bundle unter `/tmp/opencode/moli-bundle`; `/content/pmTool/wissen` nie beschrieben (A17 prüft per Hash). |
| R10 | `feature:`-Feld | **Optional** im MVP; Feature-Dateien erst bei Feature-Beginn. |
| R11 | Port-Wahl Colab | Default 5000, Ausweichport + klare Meldung bei Belegung. |
| R12 | `verify.sh`-Erweiterung | Neuer Abschnitt, bestehende Blöcke unverändert. |
| R13 | Datum im Marker | Serverzeit UTC, Format `YYYY-MM-DD`, als Parameter injizierbar. |
| R14 | Pakete in Startzelle | `start_colab.py` installiert `flask`/`pyyaml` bei Bedarf (keine neuen Abhängigkeiten zur Spec). |

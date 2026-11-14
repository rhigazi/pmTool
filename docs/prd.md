# PRD – OKF Projekt-Manager (SPA) für Mensch-KI-Zusammenarbeit

> **Status:** Konkretisiert — Entscheidungen getroffen (siehe Entscheidungslog `wissen/entscheidungen/log.md`)  
> **Datum:** 2026-11-14  
> **Kontext:** Single-User-Anwendung zur gemeinsamen Verwaltung eines OKF-Projekts zwischen einer Person und dem Projektmanager (OpenCode). Umsetzung primär in **Colab**.

## 1. Ziel & Vision

Eine schlanke **Single-Page-Application**, die aus **Colab heraus gestartet** wird und die Kommunikation zwischen Mensch und Projektmanager (KI) vereinfacht: Beide Seiten sehen jederzeit **alle Aspekte des Projekts** — Wellen, Aufgaben, Status, Zuständigkeit — in einer Liste und über Navigationspunkte.

**Leitprinzip: Die Wissensdatenbank (`wissen/`) bleibt Single Source of Truth.** Die App ist eine Oberfläche darauf, kein Zweitspeicher. Die bestehende Arbeitsweise aus `AGENTS.md` (Projektmanager + Subagenten) wird **nicht verändert** — die App unterstützt sie lediglich.

**Ziel der Interaktion:** Reibungslos — „Mensch erfasst Nachtrag/entscheidet → Status/Zuständigkeit sagt, wer dran ist → KI sieht Nachtrag im Bundle → KI arbeitet ab → Status wandert → Mensch sieht in der Liste, wo es steht.“

## 2. Nutzer & Nutzungskontext

- **Genau 1 Person** (Projektleitung) arbeitet mit dem Projektmanager (KI) an einem Projekt.
- **Datenbasis:** OKF-Bundle in Colab unter `/content/pmTool/wissen/` (`.md`-Dateien mit YAML-Frontmatter, `index.md`, `log.md`, `aufgaben/`, `features.md`, `entscheidungen/`, `projekt/`).
- **Kommunikationskanal mit der KI:** OpenCode-CLI-Chat (läuft **unabhängig von der App**), gemeinsamer Kanal sind die **Dateien + Status** im Bundle.
- **Arbeitsumgebung:** Colab (Umsetzung, Server, Daten) — App wird aus Colab heraus gestartet.

## 3. Kernentscheidungen (geklärt)

| # | Thema | Entscheidung |
|---|---|---|
| 1 | Workflow | Bestehender PM-/Subagenten-Workflow aus `AGENTS.md` bleibt unverändert |
| 2 | Statusmodell | Einheitlich für **alles** (Wellen, Aufgaben, Punkte): `Klarung`, `Offen`, `In Arbeit`, `Testing`, `Dokumentation`, `Geschlossen` |
| 3 | Zuständigkeit | Eigenes Feld **owner: `mensch` \| `ai`** zusätzlich zum Status — Status + Zuständigkeit steuern gemeinsam, wer als Nächstes dran ist |
| 4 | Nachträge | Block im Text mit sichtbarem Marker, z. B. `> **Nachtrag (Mensch, 2026-11-14):** …` — für die KI sofort erkennbar |
| 5 | Wellen | Eigener OKF-Punkt pro Welle (`type: Welle`), verlinkt mit zugehörigen Aufgaben/Features |
| 6 | UI-Konzept | Navigation über Punkte **+** Listenansicht mit Status und Zuständigkeit (Komplexität möglichst niedrig) |
| 7 | MVP-Scope | Liste + Status/Zuständigkeit + Nachträge einfügen |
| 8 | Start aus Colab | Lokaler Server in Colab + Browser-Tunnel |
| 9 | Datenpfad | Bundle liegt in Colab unter `/content` |
| 10 | KI-Übergabe | Dateien + Status im Bundle sind der gemeinsame Kanal (nutzt definierten Session-Start-Workflow) |

## 4. Statusmodell & Zuständigkeit (zentral)

**Statuswerte (einheitlich):**
`Klarung` → `Offen` → `In Arbeit` → `Testing` → `Dokumentation` → `Geschlossen`

**Zuständigkeit:** `owner: mensch` oder `owner: ai`

**Lesart für beide Seiten:** Status sagt, **in welcher Phase** die Sache steht; owner sagt, **wer als Nächstes antwortet/arbeitet**.

Beispiele:
- `Klarung` + `owner: mensch` → Projektmanager wartet auf Klärung durch die Person.
- `Offen` + `owner: ai` → AI kann übernehmen (bereit für Übergabe).
- `In Arbeit` + `owner: ai` → KI setzt gerade um.
- `Testing` + `owner: ai` → Subagent `tester` prüft.
- `Dokumentation` + `owner: ai` → `documenter` dokumentiert.
- `Geschlossen` → abgeschlossen, Zuständigkeit egal.
- Rücklauf bei kritischem Review/Befund → wieder `owner: mensch` (Entscheidung liegt bei Projektleitung).

## 5. UI-Konzept (niedrige Komplexität)

- **Navigation über Punkte** (Seitenmenü/Reiter): z. B. Übersicht, Wellen, Aufgaben, Entscheidungen, Projekt, Log.
- **Listenansicht** als Hauptsicht: Zeile = Element, Spalten mindestens **Titel, Status, owner, zuletzt geändert** — sofort erkennbar, was gerade läuft und wer dran ist.
- **Detailansicht:** gerendertes Markdown + Bearbeitung von **Nachträgen** (siehe 6).
- Keine komplexen Boards/Kanban im MVP — Liste + Filter nach Status/owner reichen.

## 6. Nachträge (Mensch-KI-Klarheit)

- Einfügen eines sichtbaren Blocks in die jeweilige Datei:
  ```
  > **Nachtrag (Mensch, 2026-11-14):** Konkrete Anweisung/Wunsch an die KI …
  ```
- Dadurch ist in der Datei **eindeutig erkennbar, was vom Menschen stammt** und was geändert werden soll.
- Status und `owner` werden mitgepflegt, damit beide Seiten jederzeit sehen, wer als Nächstes handelt.
- (Optionaler Ausbau) zusätzliches Frontmatter-Feld `owner` für maschinenlesbare Filterung.

## 7. Wellen (Waves)

- Eigener OKF-Punkt pro Welle, z. B. `wissen/wellen/wave-1.md` mit Frontmatter:
  ```yaml
  ---
  type: Welle
  title: Wave 1 — MVP
  status: In Arbeit
  owner: mensch
  ---
  ```
- Inhalt: Ziel, Umfang, gehörige Aufgaben/Features als OKF-Links.
- Gleiche Statuswerte wie alles andere (einheitliches Modell).
- Wird definiert/gebendet von der Projektleitung, strukturiert/bearbeitet vom Projektmanager — **ohne Änderung des festgelegten Workflows**.

## 8. Umsetzung in Colab

- **Start aus Colab:** Colab-Zelle startet einen **lokalen Python-Server** (App + API auf `wissen/`), Zugriff im Browser über **Tunnel** (z. B. `pyngrok`).
- **Daten:** direkt in Colab unter `/content/pmTool/wissen/` — App und OpenCode-CLI arbeiten auf **denselben Dateien** (eine Quelle, kein Sync).
- **Kommunikation mit der KI:** läuft weiter im **OpenCode-CLI-Chat**; die App liefert den gemeinsamen Datei-/Statuskanal.
- **Erweiterung der `definitions/`:** neue Funktionalitäten (Vorlagen, ggf. neue Punkt-Typen, App-Dateien) werden in der Single Source of Truth unter `definitions/` gepflegt und über `setup.sh` verteilt.

## 9. MVP (Scope eingefroren)

1. **Starten aus Colab:** Zelle startet Server + Tunnel → App im Browser.
2. **Navigation über Punkte** (Übersicht, Wellen, Aufgaben, …).
3. **Listenansicht** aller Elemente mit Spalten Titel / Status / owner / zuletzt geändert.
4. **Status ändern** (die sechs Werte) und **owner umschalten** (`mensch` ↔ `ai`).
5. **Nachträge einfügen** in die jeweilige Datei mit sichtbarem Mensch-Marker.
6. **Wellen als eigene OKF-Punkte** anlegen und mit Aufgaben verlinken.
7. **OKF-Konformität:** Frontmatter (`type`) erhalten, reservierte Dateien respektieren, keine Inhalte zerstören.

**Nicht im MVP (Ausbau):** Volltextsuche, Dashboard-Kennzahlen, automatische Index-/Log-Pflege, Git-Integration, direkter KI-Aufruf aus der App, Export/Import.

## 10. Erfolgskriterien

- Aus Colab gestartet, in < 2 Minuten eine Übersicht „was läuft + wer ist dran“.
- Ein Nachtrag kann in < 1 Minute eingefügt sein und ist in der Datei eindeutig als Mensch-Eingabe erkennbar.
- Der Projektmanager (KI) erkennt aus dem Bundle ohne Rückfrage, was als Nächstes zu tun ist (Status + owner + Nachtrag).
- Status/Durchsatz: weniger Rückfragen zwischen Mensch und KI wegen „was ist gerade dran“.

## 11. Verbleibende offene Punkte (für die Projektplanung)

1. Konkrete Feldnamen/Schema für `owner` und Statuswerte im YAML-Frontmatter (Konsistenz mit vorhandenen Dateien prüfen).
2. Navigationspunkte-Feinschliff (welche Seiten genau, Reihenfolge).
3. Server-Technik (Empfehlung: schlanke Python-API, z. B. Flask/FastAPI) und Tunnel-Auswahl.
4. Vorlagen für neue Punkte/Aufgaben (OKF-konformes Frontmatter).
5. Wie `aufgaben/index.md`/`features.md`/`log.md` gepflegt werden (automatisch vs. assistiert).

## 12. Nächste Schritte

- Diese PRD-Entscheidungen als User Stories + Technische Spec in `wissen/projekt/` ausformulieren (Aufgaben aus `wissen/projekt/user-stories/` und `wissen/projekt/technische-spec.md`).
- `definitions/` um die neuen Funktionalitäten/Strukturen erweitern.
- Umsetzung granular nach TDD über die Subagenten (`planner`) planen lassen.

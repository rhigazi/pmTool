# OpenCode-Definitionen (Single Source of Truth)

Dieses Verzeichnis bündelt **alle** OpenCode-Definitionen des Projekts. Damit starten ein neuer Container oder ein neues Projekt nicht bei Null.

## Inhalt

| Pfad | Inhalt |
|---|---|
| `AGENTS.md` | Projektregeln & PM-Workflow (wird von OpenCode automatisch geladen) |
| `agents/` | Subagenten: `planner`, `coder`, `reviewer`, `tester`, `documenter` |
| `opencode.jsonc` | Projekt-Konfiguration: Projektmanager-Modell `opencode-go/mimo-v2.6-pro` |
| `wissen-vorlage/` | Gerüst der OKF-Wissensdatenbank (Index, Log, Features, Aufgaben, Phasen, …) |
| `skills/` | Skill-Snapshots: `okf-knowledge-base`, `duckdb-docs` |
| `tools/` | Werkzeuge der Vorlage: `telegram_send.py` + Tests |
| `setup.sh` | Installiert alles in ein Projekt / einen Container (inkl. `tools/` und pytest) |
| `verify.sh` | Setup-Test: prüft Vollständigkeit und Funktion (nach Container-Neustart ausführen) |

## Modellzuordnung

| Rolle | Modell | Wo definiert |
|---|---|---|
| Projektmanager (Hauptagent) | `opencode-go/mimo-v2.6-pro` | `opencode.jsonc` (`model`) |
| Subagenten (planner, coder, reviewer, tester, documenter) | `opencode-go/deepseek-v4.1-flash` | `agents/*.md` (Frontmatter `model`) |

Die Subagenten erben das Modell der Session nicht mehr — die Zuordnung ist explizit. Varianten (z. B. `#high`) können bei Bedarf im jeweiligen Agent-Frontmatter ergänzt werden.

## Verknüpfung im Projekt `/app`

`/app` nutzt Symlinks, damit es nur **eine** Quelle gibt:

```
/app/AGENTS.md          → definitions/AGENTS.md
/app/.opencode/agents/  → definitions/agents/
/app/wissen/            → eigene Wissensdatenbank des Projekts (aus wissen-vorlage/ entstanden)
```

Änderungen an Regeln oder Subagenten daher immer in `definitions/` vornehmen.

## Nutzung

### Neuer Container / Container-Neustart

Das Container-Setup (`container.sh`) ruft automatisch auf:

```sh
bash /app/definitions/setup.sh /app --global --wissen
```

Damit sind Regeln, Subagenten, Skills, Werkzeuge und (falls fehlend) das Wissensdatenbank-Gerüst sofort vorhanden; `pytest` wird bei Bedarf nachinstalliert.

**Setup-Test nach dem Neustart** (ein Befehl prüft alles — Dateien, Subagenten, Laufzeit, Test-Suite, CLI):

```sh
bash /app/definitions/verify.sh /app
```

Exit 0 = Setup vollständig und funktionsfähig. Der Test kann auch gegen ein frisch installiertes Projekt laufen: `bash definitions/verify.sh <projekt>`.

### Neues Projekt

```sh
bash /app/definitions/setup.sh /pfad/zum/neuen/projekt --wissen --global
```

- `--wissen` legt `wissen/` (OKF-Gerüst) an, falls nicht vorhanden.
- `--global` installiert die Subagenten global (`~/.config/opencode/agents/`) und die Skills nach `~/.agents/skills/` — dann stehen sie in **allen** Projekten zur Verfügung.
- Ohne `--force` bleiben vorhandene Dateien unangetastet (kein Überschreiben von Projektstand).

### Nach Prozess-Änderungen

Wurde z. B. `wissen/projekt/phasen.md` im Projekt weiterentwickelt, die Vorlage aktualisieren:

```sh
cp /app/wissen/projekt/phasen.md /app/definitions/wissen-vorlage/projekt/phasen.md
```

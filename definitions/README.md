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
| `app/` | SPA-App: Flask-Server (`server.py`), Fachmodule, `static/` und Tests — wird nach `<projekt>/app/` verteilt |
| `setup.sh` | Installiert alles in ein Projekt / einen Container (inkl. `tools/`, `app/` und pytest) |
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

Damit sind Regeln, Subagenten, Skills, Werkzeuge, die App und (falls fehlend) das Wissensdatenbank-Gerüst sofort vorhanden; `pytest` wird bei Bedarf nachinstalliert.

**Setup-Test nach dem Neustart** (ein Befehl prüft alles — Dateien, Subagenten, Laufzeit, Test-Suite, CLI, App):

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

## App starten (Colab)

`setup.sh` verteilt `app/` nach `<projekt>/app/`; der Server liest das Bundle über `BUNDLE_ROOT` und lauscht auf `PORT` (Default 5000). Fehlt `<projekt>/app/` noch, einmal `bash definitions/setup.sh <projekt>` ausführen.

Zelle 1 — Abhängigkeiten und Serverstart:

```python
!python3 -m pip install --quiet flask pyyaml
!BUNDLE_ROOT=/content/pmTool/wissen PORT=5000 python3 /content/pmTool/app/server.py &
```

Zelle 2 — Port im Browser freigeben:

```python
from google.colab import output

output.serve_kernel_port_as_window(5000)
```

Bequemer ist die Startzelle `app/start_colab.py` (A16): Sie prüft bzw. installiert `flask` und `pyyaml` bei Bedarf, startet `server.py` mit `BUNDLE_ROOT=/content/pmTool/wissen` als Subprozess, meldet einen belegten Port als „läuft bereits" statt doppelt zu starten und ruft `serve_kernel_port_as_window` selbst auf:

```sh
python3 /content/pmTool/app/start_colab.py
```

# Neue Colab-Sitzung starten

Kurzanleitung, um das Projekt in einer **frischen Colab-Sitzung** wieder lauffähig
zu bekommen: Repository klonen, Server starten, Telegram konfigurieren,
OpenCode-CLI öffnen.

Alle Befehle laufen in Colab-Zellen (`!` = Shell-Befehl, `%cd` = Verzeichniswechsel,
`%run` = Skript im Kernel ausführen). Projektwurzel ist **`/content/pmTool`**.

## 1) Repository klonen

```python
!git clone https://github.com/rhigazi/pmTool
%cd /content/pmTool
```

Nur nötig, wenn `/content/pmTool` in der Sitzung noch nicht existiert.
Bereits vorhanden? Dann direkt `%cd /content/pmTool` und mit Schritt 2 weitermachen.

`start.sh` liegt als Repo-Werkzeug direkt in der Projektwurzel (neben
`definitions/`) und wird von `setup.sh` **nicht** in Zielprojekte verteilt.
Es prüft genau dieses Repository und ist für den **lokalen** Start gedacht;
in Colab übernimmt `%run definitions/app/start_colab.py` (Schritt 2).

## 2) Umgebung wiederherstellen und Server starten

Die Port-Freigabe von Colab (`serve_kernel_port_as_window`) wirkt **nur im
Notebook-Kernel**. Deshalb wird das Startskript als Kernel-Aufruf gestartet —
nicht als Shell-Befehl:

```python
%cd /content/pmTool
%run definitions/app/start_colab.py
```

Dasselbe ohne Magie (falls `%run` in der Zelle nicht möglich ist):

```python
import os, sys
os.chdir("/content/pmTool")
sys.path.insert(0, "definitions/app")
import start_colab
start_colab.main()
```

Das Skript erledigt der Reihe nach:

1. prüft `python3` (in Colab vorhanden),
2. installiert **nur bei Bedarf** `flask` und `pyyaml` (per `pip`),
3. startet `definitions/app/server.py` als Subprozess auf Port 5000
   (Bundle `wissen/` wird nur lesend verwendet),
4. gibt den Port im Kernel frei → Browserfenster mit der App.

**Warum nicht `!bash start.sh --colab` oder `!python3 …`?** Ein `!`-Befehl läuft
als Unterprozess ohne Kernel-Kanal. Dort findet `google.colab` zwar statt, der
Aufruf der Freigabe schlägt aber fehl — sichtbar wird nur
`127.0.0.1:5000`/`172.x:5000`, das im Browser nicht erreichbar ist. Das Skript
erkennt das und gibt die Handlungsanweisung aus:

```python
from google.colab import output
output.serve_kernel_port_as_window(5000)   # in laufender Sitzung nachholen
```

`start.sh` selbst bleibt für den lokalen Start zuständig:

| Aufruf | Wirkung |
|---|---|
| `bash start.sh` | lokal: Server auf `http://localhost:5000`, `BUNDLE_ROOT=$PROJEKT/wissen` (absolut gesetzt, `PROJEKT` = Projektroot) |
| `bash start.sh --colab` | startet nur den Server über `definitions/app/start_colab.py` **ohne** Port-Freigabe (Unterprozess) — in Colab stattdessen den Kernel-Aufruf oben verwenden |
| `bash start.sh --skip-verify` | ohne Setup-Prüfung (schneller) |
| `bash start.sh --dry-run` | zeigt nur, was getan würde (installiert/startet nichts; `verify.sh` wird dabei still übersprungen) |
| `bash start.sh --help` | Hilfe |

Läuft der Server bereits auf Port 5000, meldet das Skript das und startet keinen
zweiten. Beenden mit **Strg+C** (kein Traceback).

## 3) Telegram-Konfiguration (Secrets)

`config.json` ist **gitignored** und existiert in einer neuen Sitzung nicht —
die Telegram-Benachrichtigungen sind dann deaktiviert (das Startskript weist
darauf hin, legt aber **keine** Datei an).

Zuerst in Colab unter *Secrets* (Schlüsselsymbol, linke Leiste) anlegen:

- `TELEGRAM_BOT_TOKEN` — Token des Bots
- `TELEGRAM_CHAT_ID` — Ziel-Chat-ID

Dann diese Zelle ausführen:

```python
from google.colab import userdata
import json
from pathlib import Path

config = {
    "bot_token": userdata.get("TELEGRAM_BOT_TOKEN"),
    "chat_id": userdata.get("TELEGRAM_CHAT_ID"),
}

Path("/content/pmTool/config.json").write_text(json.dumps(config), encoding="utf-8")
print("config.json geschrieben; Schlüssel:", sorted(config))
```

Hinweise:

- Die Secret-Namen müssen exakt zu den Aufrufen `userdata.get(...)` passen.
- Der Token wird nie ausgegeben oder committet — nicht in Zellen `print`-en.
- Test: `!cd /content/pmTool && python3 tools/telegram_send.py "Test aus neuer Sitzung"`.

## 4) OpenCode-CLI starten

Im Terminal der Sitzung die Projektwurzel öffnen:

```bash
cd /content/pmTool
opencode
```

- Die Projektregeln stehen in `/content/pmTool/AGENTS.md`.
- Die Subagenten liegen in `.opencode/agents/` (inkl. `planner`, `coder`, `reviewer`,
  `tester`, `documenter`) und werden von OpenCode automatisch geladen.
- Sessions immer aus `/content/pmTool` heraus starten, damit relative Pfade
  (`tools/`, `wissen/`, `definitions/`) stimmen.

## 5) Erster Check

```python
!bash definitions/verify.sh .
```

Exit 0 = Setup vollständig. Befunde (`✗`) zuerst beheben; Hinweise (`!`) sind
optional (z. B. nicht installierte globale Skills → `bash definitions/setup.sh . --global`).

## Typischer Ablauf als Kurzfassung

```python
!git clone https://github.com/rhigazi/pmTool
%cd /content/pmTool
%run definitions/app/start_colab.py   # Server + Browserfenster (Kernel-Aufruf!)
# Secrets-Zelle aus Schritt 3 ausführen (falls Telegram gewünscht)
!bash definitions/verify.sh .         # Setup-Check
# neues Terminal: cd /content/pmTool && opencode
```

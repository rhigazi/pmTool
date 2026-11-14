# Neue Colab-Sitzung starten

Kurzanleitung, um das Projekt in einer **frischen Colab-Sitzung** wieder lauffähig
zu bekommen: Repository klonen, Server starten, Telegram konfigurieren,
OpenCode-CLI öffnen.

Alle Befehle laufen in Colab-Zellen (`!` = Shell-Befehl, `%cd` = Verzeichniswechsel).
Projektwurzel ist **`/content/pmTool`**.

## 1) Repository klonen

```python
!git clone https://github.com/rhigazi/pmTool
%cd /content/pmTool
```

Nur nötig, wenn `/content/pmTool` in der Sitzung noch nicht existiert.
Bereits vorhanden? Dann direkt `%cd /content/pmTool` und mit Schritt 2 weitermachen.

`start.sh` liegt als Repo-Werkzeug direkt in der Projektwurzel (neben
`definitions/`) und wird von `setup.sh` **nicht** in Zielprojekte verteilt —
es prüft genau dieses Repository und wird direkt nach `git clone` + `cd pmTool`
ausgeführt.

## 2) Umgebung wiederherstellen und Server starten

```python
!bash start.sh --colab
```

Das Skript erledigt der Reihe nach:

1. prüft `python3`,
2. prüft die Projektstruktur (`wissen/`, `definitions/`),
3. installiert **nur bei Bedarf** `flask`, `pyyaml`, `pytest`,
4. prüft die Telegram-Konfiguration (`config.json`),
5. führt `definitions/verify.sh` aus (Warnungen blockieren den Start nicht),
6. ruft `python3 definitions/app/start_colab.py` auf → Server auf Port 5000 und
   Freigabe des Ports im Colab-Browserfenster.

Alternativen:

| Aufruf | Wirkung |
|---|---|
| `bash start.sh` | lokal: Server auf `http://localhost:5000`, `BUNDLE_ROOT=./wissen` |
| `bash start.sh --skip-verify` | ohne Setup-Prüfung (schneller) |
| `bash start.sh --dry-run` | zeigt nur, was getan würde (installiert/startet nichts) |
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
# Secrets-Zelle aus Schritt 3 ausführen (falls Telegram gewünscht)
!bash start.sh --colab          # Server + Browserfenster
!bash definitions/verify.sh .   # Setup-Check
# neues Terminal: cd /content/pmTool && opencode
```

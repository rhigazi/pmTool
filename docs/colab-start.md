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
in Colab übernimmt `%run /content/pmTool/definitions/app/start_colab.py` (Schritt 2).

## 2) Umgebung wiederherstellen und Server starten

Die Port-Freigabe von Colab wirkt **nur im Notebook-Kernel**. Deshalb wird das
Startskript als Kernel-Aufruf gestartet — nicht als Shell-Befehl. Die App öffnet
sich danach in einem **neuen Browser-Tab** über den sicheren, authentifizierten
Colab-Link (`google.colab.kernel.proxyPort`). Beide Varianten funktionieren; die
erste ist ein Einzeiler mit absolutem Pfad:

```python
%run /content/pmTool/definitions/app/start_colab.py
```

Oder relativ — dann **muss** `%cd` in einer eigenen Zeile davor stehen:

```python
%cd /content/pmTool
%run definitions/app/start_colab.py
```

> **Achtung:** `%run definitions/app/start_colab.py` ohne vorheriges `%cd`
> schlägt fehl (`File not found`), weil das Notebook-Verzeichnis in einer
> frischen Sitzung `/content` ist — nicht die Projektwurzel.

Dasselbe ohne Magie (falls `%run` in der Zelle nicht möglich ist):

```python
import sys
sys.path.insert(0, "/content/pmTool/definitions/app")
import start_colab
start_colab.main()
```

Das Skript erledigt der Reihe nach:

1. prüft `python3` (in Colab vorhanden),
2. installiert **nur bei Bedarf** `flask` und `pyyaml` (per `pip`),
3. startet `definitions/app/server.py` als Subprozess auf Port 5000
   (Bundle `wissen/` wird nur lesend verwendet),
4. öffnet die App in einem **neuen Browser-Tab** — sicherer Colab-Link über
   `google.colab.kernel.proxyPort` (per `output.eval_js` + `window.open`).

Das Bundle wird aus dem Skriptpfad abgeleitet (`<Repo>/wissen`), ein gesetztes
`BUNDLE_ROOT` in der Umgebung hat Vorrang (wie bei `server.py`) — der Klon-Name
ist damit egal.

**Warum nicht `!bash start.sh --colab` oder `!python3 …`?** Ein `!`-Befehl läuft
als Unterprozess ohne Kernel-Kanal. Dort findet `google.colab` zwar statt, der
Aufruf der Freigabe schlägt aber fehl — sichtbar wird nur
`127.0.0.1:5000`/`172.x:5000`, das im Browser nicht erreichbar ist. Das Skript
erkennt das und gibt die Handlungsanweisung aus. Freigabe in laufender Sitzung
nachholen (Server läuft schon) — Nutzer-Snippet:

```python
from google.colab import output
output.serve_kernel_port_as_window(5000)   # erzeugt sicheren Link, fragt neuen Tab an
```

Alternative mit garantiertem Proxy-Link (neuer Tab):

```python
from google.colab import output
output.eval_js('(async () => window.open(await google.colab.kernel.proxyPort(5000), "_blank"))()')
```

Reihenfolge im Skript: (1) Proxy-Link in neuem Tab, (2) `serve_kernel_port_as_window`
als Fallback, (3) **Notbehelf** iframe — dann erscheint die App in der Zelle
(Meldung: „Fallback: Anzeige in der Zelle").

> **Hinweis:** `serve_kernel_port_as_window(5000)` ist in Colab als veraltet
> markiert und hat in unserer `%run`-Zelle nur `https://localhost:5000/`
> ausgegeben. Es bleibt nur als Fallback drin; der sichere Link entsteht über
> `google.colab.kernel.proxyPort`.

`start.sh` selbst bleibt für den lokalen Start zuständig:

| Aufruf | Wirkung |
|---|---|
| `bash start.sh` | lokal: Server auf `http://localhost:5000`, `BUNDLE_ROOT=$PROJEKT/wissen` (absolut gesetzt, `PROJEKT` = Projektroot) |
| `bash start.sh --colab` | startet nur den Server über `definitions/app/start_colab.py` **ohne** Port-Freigabe (Unterprozess) — in Colab stattdessen den Kernel-Aufruf oben verwenden |
| `bash start.sh --neu` | setzt `wissen/` auf die leere Vorlage zurück (mit Backup), dann Start — siehe „Neues Projekt beginnen" |
| `bash start.sh --skip-verify` | ohne Setup-Prüfung (schneller) |
| `bash start.sh --dry-run` | zeigt nur, was getan würde (installiert/löscht/startet nichts; `verify.sh` wird dabei still übersprungen) |
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

## Neues Projekt beginnen (optional)

Ein frischer Klon bringt das Projektwissen des Vorbilds mit. `start.sh` erkennt
das an pmTool-spezifischen Markerdateien (`wissen/aufgaben/a1-okf-bundle.md`,
`wissen/features/okf-projekt-manager-spa.md`) und bietet den Reset an:

```bash
bash start.sh                  # Rückfrage: „Neues leeres Projekt beginnen? [j/N]"
bash start.sh --neu            # Reset ohne Rückfrage (Backup + Vorlage), dann Start
bash start.sh --neu --dry-run  # zeigt nur den Plan — ändert nichts
```

- **Ja** = Reset über `tools/neues_projekt.py --ja` (erst Backup, dann Vorlage).
- **Nein / Strg+D** = unveränderter Normalstart; es wird nichts gelöscht.
- **Kein TTY** = nur Hinweistext, kein Reset (fail-safe).
- `--neu` ist mit `--colab` kombinierbar. In Colab ist der Kernel-Aufruf von
  `start_colab.py` (Schritt 2) der Startweg — dort den Reset wie unten in einer
  Zelle ausführen.

Den Reset ohne Start des Servers — die manuelle Variante, drei Zellen in dieser
Reihenfolge:

```python
%cd /content/pmTool
!python3 tools/neues_projekt.py       # Plan: Löschziel, Backup-Pfad, Vorlage — ändert nichts
```

```python
!cd /content/pmTool && python3 tools/neues_projekt.py --ja
```

```python
!cd /content/pmTool && bash definitions/verify.sh .
```

Danach wie gewohnt starten (Schritt 2) — die App zeigt ein leeres Projekt ohne
Aufgaben und Wellen. In einem per `setup.sh` installierten Zielprojekt liegt das
Werkzeug derzeit **nicht** (offener Punkt A26: Spiegelung nach `definitions/tools/`);
dort den Reset in der Quell-Instanz ausführen oder das Skript manuell übernehmen.

> **Achtung:** `--ja` löscht das gesamte Projekt-Wissen in `wissen/` — inklusive
> versteckter Dateien, Nachträgen und Entscheidungen. Vorher entsteht automatisch
> ein Backup `wissen-backup-YYYYMMDD-HHMMSS.tar.gz` im Repo-Root. Schlägt das
> Backup fehl, wird nichts gelöscht. Das Backup ist danach die **einzige** Kopie
> des alten Wissens: herunterladen oder an einen sicheren Ort verschieben, bevor
> die Runtime endet (Colab-Dateien sind flüchtig).

Details: Ohne `--ja` passiert nichts (Exit 0). `--backup PFAD` überschreibt das
Ziel, muss aber innerhalb des Repo-Roots liegen; ein vorhandenes Backup wird nie
überschrieben (Suffix `-2`, `-3`, …). Fehlt die Vorlage, bricht das Skript ab,
nennt die fehlende Datei und löscht nichts.

## 5) Erster Check

```python
!bash definitions/verify.sh .
```

Exit 0 = Setup vollständig. Befunde (`✗`) zuerst beheben; Hinweise (`!`) sind
optional (z. B. nicht installierte globale Skills → `bash definitions/setup.sh . --global`).

## Test-Instanz / Abnahme-Instanz

**Zweck:** den echten Nutzerpfad prüfen — frischer Clone von GitHub, echte
Packungs-Details (was nach `git clone` tatsächlich da ist), ohne den
Entwicklungs-Ordner zu kopieren und ohne dass Testdaten in dessen `wissen/`
landen. Die Test-Instanz läuft in einer eigenen Colab-Runtime (Port 5000 ist pro
Runtime nur einmal frei).

1. Frische Runtime starten (*Laufzeit → Sitzung trennen und löschen* oder neues
   Notebook).
2. **Nur von GitHub klonen** — niemals `/content/pmTool` kopieren:

   ```python
   !git clone https://github.com/rhigazi/pmTool /content/pmTool-test
   ```

3. In einem Rutsch starten (Kernel-Aufruf, absoluter Pfad):

   ```python
   %cd /content/pmTool-test
   %run /content/pmTool-test/definitions/app/start_colab.py
   ```

   Das Skript leitet sein Bundle aus dem Skriptpfad ab
   (`/content/pmTool-test/wissen`) — der Klon-Name ist egal; ein gesetztes
   `BUNDLE_ROOT` in der Umgebung hätte Vorrang (wie bei `server.py`).

4. **Smoke-Checkliste** (jeder Punkt 1× durchklicken):

   - **Liste:** Einträge mit Status und `owner` sichtbar, Filter reagieren.
   - **Detail:** Frontmatter-Kopf + gerendertes Markdown, Status-Buttons nur
     `Klarung`/`Geschlossen`, owner-Umschalter.
   - **Nachtrag:** Text einfügen → erscheint im Dokument des Eintrags.
   - **Formular:** neue **Aufgabe** und neue **Welle** anlegen.
   - **Entscheidungen/Projekt:** Log-Einträge und Projekt-Unterpunkte laden.

5. **Aktualisieren** (nach neuen Commits):

   ```python
   %cd /content/pmTool-test
   !git pull
   %run /content/pmTool-test/definitions/app/start_colab.py
   ```

   Läuft der alte Server noch, meldet das Skript „läuft bereits"; für einen
   echten Neustart die Runtime neu starten.

## Typischer Ablauf als Kurzfassung

```python
!git clone https://github.com/rhigazi/pmTool
%run /content/pmTool/definitions/app/start_colab.py   # Server + App im neuen Browser-Tab (Kernel-Aufruf, absoluter Pfad)
# Secrets-Zelle aus Schritt 3 ausführen (falls Telegram gewünscht)
!bash definitions/verify.sh .         # Setup-Check
# Optional: leeres Projekt statt mitgeliefertem Wissen
# !cd /content/pmTool && python3 tools/neues_projekt.py --ja
# neues Terminal: cd /content/pmTool && opencode
```

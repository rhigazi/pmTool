# Entscheidungslog

Alle Projektentscheidungen, neueste zuerst. Format: `## YYYY-MM-DD: Titel` mit **Entscheidung**, **Begründung** und **Auswirkung**.

## 2026-11-15: Freigabe-Gate für Aufgaben und Wellen (Standardentscheidung)

**Entscheidung:** Neue Aufgaben werden bei Wahrnehmung mit Kennung + Titel (`A<N>: Titel`) versehen und geplant — die **Umsetzung beginnt erst, wenn die Aufgabe geklärt und von der Projektleitung freigegeben** ist ([A28](/aufgaben/a28-benachrichtigung-neue-aufgabe.md)). Aufgaben werden Wellen zugeordnet; eine Welle ist standardmäßig **nicht freigegeben** — erst die Freigabe der Welle startet die Umsetzung aller Aufgaben dieser Welle ([A29](/aufgaben/a29-wellen-abarbeiten.md)). Bis die Funktion existiert, gilt das als Prozessregel: Freigabe = ausdrückliche Zustimmung der Projektleitung (App/Chat/Telegram); die Datenhaltung wird von A28/A29 spezifiziert.

**Begründung:** Nutzer-Anforderung 2026-11-15 (zwei neue Aufgaben aus der App). Standardentscheidung des PM, solange die Projektleitung nicht abweicht: die Freigabe ist ein Menschen-Recht (analog `owner`/Status-Rechte: nur die Person), die Planung darf parallel laufen (Wartezeit verkürzen).

**Auswirkung:** PM-Workflow: annehmen → ID/Titel → pushen → planen → **warten auf Freigabe** → umsetzen. A28 und A29 werden vom `planner` parallel geplant; die Umsetzung von A29 startet zusätzlich erst nach A27 (Datei-Überschneidung `detail.js`/`meta.py`/Wellen-Dateien).

## 2026-11-15: Neue Aufgaben im Moment der Annahme pushen

**Entscheidung:** Sobald der Projektmanager eine neue Aufgabe wahrgenommen und angenommen hat (Kennung + Titel gesetzt, Datei in `wissen/aufgaben/`), werden Aufgaben-Datei und Index-Eintrag sofort committed und nach GitHub gepusht — vor Planung/Beauftragung. Die Regel steht in [AGENTS.md](/../AGENTS.md) (Abschnitt „Arbeitsweise") und in `definitions/AGENTS.md` (Single Source of Truth).

**Begründung:** Anweisung der Projektleitung 2026-11-15: „Sobald wir neue Aufgaben anlegen und diese von dir wahrgenommen werden, müssen diese ins Repo gepusht werden, damit wir nichts verloren geht." Ein Container-/Sitzungs-Reset (zweimal erlebt) darf keine erkannte Aufgabe verschlingen; der Sicherungs-Push ist nicht auf grüne Tests beschränkt, wenn es um Aufgaben-Metadaten geht.

**Auswirkung:** Erweiterung des Sicherungs-Push-Regelwerks: zusätzlich zum „Sicherungs-Push nach grünen Tests" gilt „Push bei angenommenen Aufgaben" ohne Warten auf Tests. Betrifft nur Aufgaben-/Status-Metadaten und Doku — halbfertiger Produktcode wird weiterhin erst nach grünen Tests gepusht.

## 2026-11-15: Aufgaben-Kennung steht eindeutig im Titel

**Entscheidung:** `title` einer Aufgabe führt die Kennung an: `A<N>: <Titel>`. Die Regel steht in [AGENTS.md](/../AGENTS.md) (Abschnitt „Arbeitsweise") und in `definitions/AGENTS.md` (Single Source of Truth) und gilt beim Anlegen, beim Umbenennen der Datei (`a<N>-<slug>.md`) und für per App angelegte Aufgaben. Korrigiert wurden [A23](/aufgaben/a23-feature-liste.md) („Die Feature List fehlt" → „A23: Feature-Liste (Menüpunkt + Feature-Status)") und [A25](/aufgaben/a25-suche.md) („Suche" → „A25: Suche (Feldsuche in den Listen)"); alle übrigen Aufgaben-Dateien waren bereits konform.

**Begründung:** Befund der Projektleitung: „Die Kennung muss eindeutig sein und im Titel stehen". Aufgaben müssen ohne Textlesen identifizierbar sein und per Suche auffindbar — der **Titel** ist der gesuchte Anzeigeort (Liste, Detailkopf, App-Suche). Die Suche selbst funktionierte bereits über den Pfad (`aufgaben/a23-…`, Suchfeld A25), half aber nicht, wenn jemand nur den Titel sieht. Die ursprüngliche Nutzer-Formulierung bleibt als Ziel-/Anforderungstext im Abschnitt „Ziel" erhalten, sie ist die Quelle der Aufgabe.

**Auswirkung:** Einheitliche Lesbarkeit in Aufgaben-Index, Feature-Liste, App-Liste/Detail und Suche; Dateiname und Titel sind an derselben Kennung erkennbar. Neue Aufgaben (auch aus der App) werden mit `A<N>: <Titel>` angelegt.

## 2026-11-15: A25 Suche läuft parallel zu A23

**Entscheidung:** Die Suche (A25, Konfliktgruppe G11: `liste.js`, `test_suche.py`) wird **parallel** zu A23 (G10: `features.js`, `app.js`, `index.html`, `style.css`, `test_features.py`) umgesetzt. Die frühere Empfehlung „Umsetzung erst nach Abschluss von A23" ist aufgehoben.

**Begründung:** Die Dateimengen sind disjunkt (G11 vs. G10), es gibt keine gemeinsame Datei; eine Serialisierung hätte nur Zeit gekostet. PM-Entscheidung 2026-11-15.

**Auswirkung:** A25 steht im Aufgaben-Index und in [features.md](/features.md) als „in Umsetzung" neben A23. Vorbehalt: Berührt ein Strang nachträglich Dateien des anderen, wird er dahinter serialisiert. Inhaltliche PM-Festlegungen zur Suche (alle drei Listen, UND-Verknüpfung, Umlaut-/ß-Toleranz, „zuletzt geändert" nicht durchsuchbar, Reset leert die Suche, Phase 2 Volltextsuche bleibt Vormerkung) sind in [A25](/aufgaben/a25-suche.md) unter „Kontext" festgehalten.

## 2026-11-15: Colab-Port-Freigabe nur im Kernel-Kontext

**Entscheidung:** Colab-Startzellen nutzen `%run`/Import im Notebook-Kernel; `!bash`-/`!python`-Aufrufe starten nicht mehr still, sondern geben die Handlungsanweisung `HINWEIS_PORT_FREIGABE` aus. Der `__main__`-Guard von `start_colab.py` beendet im Kernel nicht per `sys.exit`.

**Begründung:** `google.colab.output.serve_kernel_port_as_window` braucht den Kernel-Kanal des Notebooks — als Unterprozess (`!bash start.sh --colab`) schlägt die Freigabe still fehl (nur 127.0.0.1-/172.x-URLs); das war der A16-Bug.

**Auswirkung:** Notebook-Zelle 6 und Doku/README nutzen `%run definitions/app/start_colab.py`; `start.sh --colab` bleibt als Unterprozess-Variante mit Hinweis bestehen (nicht empfohlen); 4 neue Tests, Gesamtsuite 765.

## 2026-11-14: MVP-Abnahme mit Einmal-Nachweis; E2E-Regression als A22 (post-MVP)

**Entscheidung:** Die MVP-Abnahme erfolgt auf Basis des dokumentierten **Einmal-Nachweises** aus dem A17-Abnahmelauf (T1/T2/T7-Kette, 23/23, 761 passed, verify.sh Exit 0, Moli 0 Konsolenfehler, Hash-Nachweis). Ein eingechecktes `test_e2e.py` existiert noch nicht; die dauerhafte E2E-Regression wird als **A22 „E2E-Regressionstest (test_e2e.py)"** post-MVP nachgezogen (Aufgaben-Datei angelegt, Priorität mittel).

**Begründung:** Der Abnahmelauf ist vollständig belegt und reproduzierbar (T7 Reset), ein eingecheckter Dauer-Test wäre für die Abnahme nice-to-have, aber kein Abnahmekriterium; keine Abhängigkeit für die Projektleitung.

**Auswirkung:** MVP ist abnahmefähig; A22 bleibt offen (Post-MVP) und überführt die Ad-hoc-Skripte `/tmp/opencode/a17_*.py` in einen dauerhaften Test.

## 2026-11-14: Nachtrag-Marker wird literal gerendert — R6-konform akzeptiert

**Entscheidung:** Dass der Marker `**Nachtrag …:**` in der Detailansicht literal (ohne Fett-Rendering) erscheint, wird akzeptiert — R6-konform (minimaler Renderer, keine Inline-Auszeichnung). Eine optionale Fett-Rendering-Erweiterung wird nur als Post-MVP-Punkt geführt.

**Begründung:** Der minimale Renderer ist eine bewusste Entscheidung (XSS-sicher, kein CDN, kein Markdown-Parser); der Nachträge-Block bleibt als Blockquote lesbar, die Funktion ist nicht beeinträchtigt.

**Auswirkung:** Kein Code-Change; Punkt steht in der Offen-Liste (Post-MVP).

## 2026-11-14: K1-Schutz zweischichtig (Modulgrenze + zentraler Handler-Schutz)

**Entscheidung:** Der Schutz vor Pfad-Leaks ist zweischichtig: (1) an der Modulgrenze — neutrale Meldungskonstanten `MELDUNG_NICHT_GEFUNDEN`/`MELDUNG_NICHT_LESBAR` in `okf_bundle`, Übersetzung in `nachtrag._lies`/`okf_bundle._lies_text`; (2) zentral im `server._domaenen_handler` über `_sichere_meldung`, der nur echte OS-Fehler mit `errno` ersetzt, Domänenmeldungen aber lesbar lässt.

**Begründung:** Ein einzelner Schutzpunkt reicht nicht — Pfade können sowohl über Modulmeldungen als auch über unerwartete OS-Fehler nach außen gelangen; Domänenmeldungen sollen für die Fehlersuche erhalten bleiben.

**Auswirkung:** Geschlossener Pfad-Leak für A7/A9 (Commit des Sicherheits-Blocks); 29 neue Tests, Gesamtsuite 676 grün; Bestätigungs-Review läuft.

## 2026-11-14: API-Fehlercodes der Schreibstrecke

**Entscheidung:** Fehlende Datei → 404, Nicht-`.md`/Verzeichnis → 400, ungültiger Rechte-Wert → 403 (Fail-Closed-Reihenfolge: Whitelist vor Pfad-Check), keine setzbaren Felder → 400 („Keine setzbaren Felder").

**Begründung:** Validierung vollständig vor dem Schreiben; neutrale Fehlermeldungen ohne Pfad-Leaks.

**Auswirkung:** `okf_bundle.pruefe_zieldatei()`/`_pruefe_schreibziel` werden in `nachtrag.anfuegen` und `meta.setzen` angewandt; `POST /api/meta` ohne setzbare Felder liefert 400 statt 200-No-Op (PM-Entscheidung K2).

## 2026-11-14: Lokal-Betrieb/Desktop-Modus — MVP/Colab zuerst (Entscheidung der Projektleitung)

**Entscheidung:** Endgültig: **Erst die Colab-Version (MVP) fertigstellen, danach erweitern.** Der Desktop-Modus (Option B: Desktop-Fenster via `pywebview` mit direktem Aufruf der Domänen-Module — neue Abhängigkeit) wird danach als eigenes Feature geplant und bleibt als **A21 „Desktop-Modus/Lokal-Betrieb"** vorgemerkt (Nummer reserviert, noch keine Aufgaben-Datei). Option A (Ein-Klick-Start mit unsichtbarem localhost-Server) ggf. als Kleinigkeit vorher; Option C (File System Access API — nur Chromium, Logik-Dopplung) nicht empfohlen.

**Begründung:** Entscheidung der Projektleitung 2026-11-14 (bestätigt die vorläufige Standardentscheidung): Machbarkeit ist geprüft — ein reines Frontend im Browser ist ohne Webserver nicht sauber möglich; der MVP-Fokus bleibt erhalten.

**Auswirkung:** MVP/Colab-Ansatz unverändert; A21 in [features.md](/features.md) vorgemerkt; die frühere „vorläufige Standardentscheidung" ist damit bestätigt.

## 2026-11-14: Moli-Integration — Moli wird installiert, Harness bleibt Fallback

**Entscheidung:** Moli wird installiert (`setup.sh --global`, Installer der Projektleitung — Commit `5bc453f`). Der Node-DOM-Harness bleibt Fallback, wo Moli nicht verfügbar ist; UI-Tests nutzen Moli künftig, wo möglich.

**Begründung:** Die Moli-Frage ist durch die Projektleitung entschieden; Moli ist die im Phasenmodell vorgesehene UI-Test-Instanz (Moli-Szenarien).

**Auswirkung:** A17 (Moli-Kernszenario) wird realisierbar; die bisherige Standardentscheidung „Harness" endet. Die Moli-Frage ist aus den offenen Punkten genommen.

## 2026-11-14: Sicherungs-Push nach grünen Tests (Reset-Schutz)

**Entscheidung:** Sobald der Tester einen Stand positiv getestet hat (alle Tests grün), werden die geänderten Dateien sofort committed und nach GitHub gepusht — Reset-Schutz.

**Begründung:** Container-/Sitzungsverlust (Colab) — ein Zwischen-Commit nach jedem grünen Tester-Stand ist jedem Datenverlust vorzuziehen. Regel von der Projektleitung gewünscht, in `AGENTS.md` + `definitions/AGENTS.md` aufgenommen (Commit `666bdba`).

**Auswirkung:** Push-Pflicht nach jedem grünen Tester-Stand, zusätzlich zu den Commits je Takt/Meilenstein.

## 2026-11-14: setup.sh --global (okf-Skill + Moli-Installer) — übernommen nach Klärung

**Entscheidung:** Die Änderung in `definitions/setup.sh` (Zweig `--global`, Sektion „8) Global: Wichtige Skills & Browser": `npx skills add … --skill okf-knowledge-base` sowie ein Moli-Installer per `curl … | sh`) war zunächst **quarantänisiert** (uncommitted, keine Nutzung; PM-Entscheidung: keine neuen Abhängigkeiten ohne Bescheid, `curl | sh` ist riskant; Rückfrage an die Projektleitung per Telegram).

**Klärungs-Nachtrag:** Geklärt 2026-11-14: stammt von der Projektleitung, übernommen (Commit `5bc453f`); Installer vor Ausführung gesichtet (sauber: HTTPS/TLS1.2, staged Install, Cleanup).

**Begründung:** Ursprünglich: unauftragte Änderung + ungeprüfter Remote-Code; nach Klärung: gewollte Projektleitungs-Änderung mit gesichtetem Installer.

**Auswirkung:** `setup.sh --global` installiert okf-Skill + Moli; Härtung (Pin/SHA256, Guard, npx-Doku) läuft als [A20](/aufgaben/a20-setup-haertung.md).

## 2026-11-14: Moli-Frage — Standardentscheidung Harness bleibt vorerst

**Entscheidung:** Bis zu abweichender Weisung der Projektleitung bleibt der Node-DOM-Harness (HTTP-Requests gegen den laufenden Server + DOM-Harness auf Basis des vorhandenen Node) der Standardweg für UI-Tests; Moli wird nicht nachinstalliert. **Hinweis:** Die Moli-Skills sind in der Umgebung jetzt verfügbar (u. a. `moli-cdp-server`); die Rückfrage an die Projektleitung (Moli installieren oder Harness-Weg beibehalten?) läuft weiter. Bei abweichender Weisung wird umgestellt und dies hier korrigiert.

**Begründung:** `moli` fehlt im PATH; die UI-Tests laufen per HTTP + Node-DOM-Harness ohne neue Abhängigkeit (Projektregel: keine neuen Abhängigkeiten ohne Bescheid). Gemäß Projektregel wird mit der dokumentierten Standardentscheidung weitergearbeitet und später korrigiert, falls die Projektleitung abweicht.

**Auswirkung:** Die Testberichte weisen die Abweichung (Harness statt Moli) weiterhin aus; die offene Klärungsfrage bleibt im Übergabeprotokoll unter „Offene Punkte" geführt.

**Nachtrag (2026-11-14):** Ersetzt durch die Entscheidung „Moli-Integration" — Moli wird installiert, der Harness bleibt Fallback. Die Moli-Frage ist damit geklärt.

## 2026-11-14: verify.sh akzeptiert definitions/app als Fallback (A19)

**Entscheidung:** `verify.sh` Abschnitt „7) App" akzeptiert künftig beide Ablageorte: `app/` im verteilten Ziel und `definitions/app/` als Fallback im Dev-Repo — analog zum Fallback in `start.sh`. Die Umsetzung erfolgt als neue Kleinaufgabe [A19](/aufgaben/a19-verify-app-fallback.md) inklusive passender Tests; fehlen beide Orte, schlägt die Prüfung weiterhin fehl.

**Begründung:** Das Dev-Repo führt die App aus `definitions/app/` (Single Source of Truth); `start.sh` hat denselben Fallback (prüft `app/`, sonst `definitions/app/`). Allein deshalb schlug `verify.sh` Abschnitt 7 im Dev-Repo fehl.

**Auswirkung:** `definitions/verify.sh` und ggf. `definitions/app/tests/test_setup_verteilung.py` werden geändert (A19); die Prüfung bleibt im verteilten Ziel unverändert gültig (R12: bestehende Abschnitte unverändert).

## 2026-11-14: API-Auslegungen Schreib-Endpunkte bestätigt (A9)

**Entscheidung:** (a) `/api/task` und `/api/welle` lehnen ein mitgesendetes `path`-Feld mit 400 ab (fail-closed gegen Pfadausbruch) — bestätigt. (b) `/api/meta` ohne `owner`/`status` ist ein No-op (200, nichts geschrieben); `{"owner": null}` gilt wie „nicht gesetzt" (das Frontend übermittelt nur gesetzte Felder); Leerstrings/Whitespace → 403 (strikte Whitelist) — bestätigt, kein zusätzlicher Guard. (c) Beim **Anlegen** einer Welle sind alle 6 UI-Status gültig (Initialwert); die Einschränkung auf `Klarung`/`Geschlossen` gilt nur für **Änderungen** über `/api/meta` — bestätigt, entsprechender Test angepasst.

**Begründung:** Klärung von Auslegungsfragen aus der Umsetzung von A9; fail-closed bleibt durchgängige Regel.

**Auswirkung:** Verhalten der Schreib-API ist damit verbindlich; Review/Testphase orientieren sich daran.

## 2026-11-14: UI-Tests ohne Moli (Node-DOM-Harness + HTTP) in dieser Umgebung

**Entscheidung:** Der Moli-Browser ist in der Arbeitsumgebung nicht installiert. Bis zur Klärung werden UI-Szenarien (A10, A11, A12, A13, A17) per HTTP-Requests gegen den laufenden Server plus einem DOM-Harness auf Basis des vorhandenen Node getestet — ohne neue Abhängigkeit. Die Abweichung wird in den Testberichten dokumentiert. Bei Klärung durch die Projektleitung (Moli installieren) können die Szenarien zusätzlich per Moli/Screenshot laufen.

**Begründung:** Projektregel „keine neuen Abhängigkeiten ohne Bescheid"; der Ersatzweg liefert belastbare Belege (Router-, Fehler- und DOM-Verhalten echt ausgeführt) ohne Installationsbedarf.

**Auswirkung:** Phasenmodell-TDD-Regel „Moli-Szenarien" wird für diese Umgebung durch den Harness ersetzt; Testberichte führen die Abweichung explizit auf.

## 2026-11-14: Regelmäßige Sicherungs-Commits (Anweisung Projektleitung)

**Entscheidung:** Der Code-/Projektstand wird in regelmäßigen Abständen in das Repository gepusht — nicht erst nach vollständig abgeschlossenen Meilensteinen. Ein Zwischen-Commit (auch bei laufenden Arbeiten) ist jedem Datenverlust vorzuziehen, da die Arbeitsumgebung (Colab-Container) ausfallen kann.

**Begründung:** Anweisung der Projektleitung: verhindern, dass bei einem Container-Ausfall der Stand verloren geht und bei Null angefangen werden muss.

**Auswirkung:** Der Projektmanager committed und pusht mindestens bei jeder großen Statusmeldung sowie nach jedem abgeschlossenen Takt — zusätzlich zu den Commits nach Aufgaben/Meilensteinen. Zwischenstände werden in der Commit-Nachricht als solche gekennzeichnet.

## 2026-11-14: Reservierte Dateien sind für die App generell gesperrt (Guard in okf_bundle)

**Entscheidung:** `index.md`, `features.md` und `log.md` sind für **alle** App-Schreibzugriffe gesperrt — auch als Ziel von Nachträgen. Die Pflege dieser KI-Dateien erfolgt ausschließlich durch Projektmanager/documenter (OpenCode-CLI). `okf_bundle.py` erhält einen zentralen Guard: `schreiben()`/`set_meta()` weisen reservierte Ziele mit eigener Exception `ReservierteDateiFehler` ab (A6 mappt sie auf HTTP 403). A3-Testfall T9 wird entsprechend von „anfügend erlaubt" auf „abgewiesen" korrigiert.

**Begründung:** Die Schreibrechte-Matrix der Spec verbietet der App die Pflege dieser Dateien; ein Guard im Fundament schützt das tiefer liegend (Defense-in-Depth) und klärt den Widerspruch mit A3-T9.

**Auswirkung:** okf_bundle-API erweitert (`ReservierteDateiFehler`), A1-Nachbesserung inkl. Review-Empfehlungen (CRLF/Ungültig-YAML-Tests, Schlüssel-Regex, `scan()`-Filter, Docstring-Hinweis), A3/A6 angepasst.

## 2026-11-14: features.md ist für die App reserviert (schreibgeschützt)

**Entscheidung:** `features.md` wird wie `index.md` und `log.md` als reserviert behandelt: Die App darf sie nicht ersetzen und führt sie nicht in der Übersicht. `okf_bundle.py` erkennt sie als reservierte Datei (`scan()`, `ist_reserviert()`).

**Begründung:** `features.md` ist laut Schreibrechte-Matrix eine KI-Datei (gepflegt von Projektmanager/documenter). Ohne Reservierung wäre sie für App-Schreibzugriffe offen und würde als normaler Punkt mit Status/owner erscheinen.

**Auswirkung:** Spec, US-7 und Aufgaben A1/A6/A8 angepasst; A1 erhält eine Mini-Nachbesserung, A6/A8 bauen bei der Umsetzung auf dem erweiterten Reserve-Begriff auf.

## 2026-11-14: owner-Vorrang und Status-Owner-Defaults im Datenmodell

**Entscheidung:** Ein explizit gesetztes Frontmatter-Feld `owner` hat immer Vorrang vor dem owner-Default aus dem Status (sonst würde eine vom Menschen umgeschaltete Zuständigkeit von der Anzeige überschrieben). Für Punkte mit `status`-Feld ohne `task_status` (Wellen) gelten die Defaults: `Klarung` → `mensch`, `Offen`/`In Arbeit`/`Testing`/`Dokumentation` → `ai`, `Geschlossen` → `None` (Anzeige „—“).

**Begründung:** Klärung von Auslegungsfragen aus der Umsetzung von A2; ohne Vorrangregel wären owner-Umschaltungen aus US-5 nicht korrekt darstellbar.

**Auswirkung:** In der Technischen Spec als owner-Default-Regel festgehalten; `status.py` und alle Konsumenten (A6/A8/A11) orientieren sich daran.

## 2026-11-14: Projekt vollständig ins GitHub-Repository umgezogen

**Entscheidung:** Das Projekt liegt vollständig in `/content/pmTool` (Repository `github.com/rhigazi/pmTool`, Branch `main`): `definitions/` (Single Source of Truth), `wissen/` (OKF-Bundle), `docs/prd.md`, dazu die installierte Projekt-Wurzel (`AGENTS.md`, `.opencode/agents/`, `opencode.jsonc`, `tools/`). Alle Pfade wurden von `/content/wissen` auf `/content/pmTool/wissen` umgestellt (Spec, User Stories, Planung, Aufgaben, PRD). Bestehende Einträge in diesem Log bleiben unverändert (Historie). Ausschlüsse: `sample_data/`, `.config/`, `config.json` (Secret), Cruft-Dateien (`.gitignore`).

**Begründung:** Projektdateien sollen nicht lose in `/content` liegen; Git ist der gemeinsame Stand (Commit nach jedem Meilenstein, Push nach `origin/main`).

**Auswirkung:** `BUNDLE_ROOT` ist `/content/pmTool/wissen`; `verify.sh` läuft gegen `/content/pmTool`; Commits erfolgen aus `/content/pmTool`.

## 2026-11-14: Schreibrecht für task_status konkretisiert (Klarung/Geschlossen)

**Entscheidung:** Die Schreibrechte-Matrix der Spec wird wie folgt ausgelegt: Die App darf `task_status` ausschließlich auf die Werte `in Klärung` (Klarung) und `abgeschlossen` (Geschlossen) setzen — genau diese Teilmenge. Jeder andere Statuswechsel (`in Planung`, `in Umsetzung`, `im Review`, `im Test`, `in Doku`, `zur Abnahme`, …) wird serverseitig mit 403 abgewiesen.

**Begründung:** Die beiden erlaubten Status sind fachlich der Projektleitung zugeordnet (Rückfrage stellen, Abnahme); die Pipeline-Steuerung bleibt wie bisher ausschließlich der KI vorbehalten.

**Auswirkung:** `meta.py`/Schreib-API implementieren die Whitelist; Testfälle prüfen 403 bei allem anderen.

## 2026-11-14: Slug-Konvention für neue Aufgaben und Wellen

**Entscheidung:** IDs neuer Punkte sind lesbare ASCII-Slugs aus dem Titel (Umlaute → ASCII, Sonderzeichen → `-`, max. 60 Zeichen), Kollisionen bekommen ein Suffix (`-2`, `-3`). Dateien werden nie überschrieben.

**Begründung:** Lesbare Pfade (auch ohne App nachvollziehbar), robust gegen Sonderzeichen, kein separates Nummernregister nötig.

**Auswirkung:** `neu_aufgabe.py`/`neu_welle.py` setzen die Regel um; Aufgaben liegen als `wissen/aufgaben/<slug>.md`, Wellen als `wissen/wellen/<slug>.md`.

## 2026-11-14: Wellen-Struktur im Bundle nachgepflegt (R5)

**Entscheidung:** Der Ordner `wissen/wellen/` wird mit `index.md` angelegt und unter „Struktur“ in `wissen/index.md` verlinkt. Die Pflege der `index.md`-Dateien übernimmt der Projektmanager/documenter wie bisher — nicht die App.

**Begründung:** US-4 verlangt, dass Wellen auch ohne App im Bundle auffindbar sind; die App darf `index.md` laut Schreibrechten nicht pflegen.

**Auswirkung:** Vorlage und Projekt-Bundle enthalten die Wellen-Struktur; `setup.sh --wissen` verteilt sie künftig.

## 2026-11-14: feature-Feld bleibt optional; Testisolation verbindlich

**Entscheidung:** Das Frontmatter-Feld `feature:` in Aufgaben ist im MVP optional (Feature-Dateien werden erst mit dem Beginn der Feature-Arbeit angelegt). Verbindlich für alle Tests: Szenarien laufen ausschließlich gegen Test-Bundle unter `/tmp/opencode/moli-bundle` — `/content/wissen` wird von pytest/Moli nie beschrieben.

**Begründung:** Verhindert inkonsistente Pflichtverweise und Datenverlust beim Testen.

**Auswirkung:** Aufgabenformat behält `feature:` als optionales Feld; A17 prüft zusätzlich die Unversehrtheit des echten Bundles per Hash.

**Entscheidung:** Die App ist primär ein Tracker zur Projektsteuerung. Das Mitpflegen von `index.md`, `features.md` und `log.md` übernimmt die **KI** (Projektmanager/documenter), nicht die Person. Ziel: Die KI bleibt jederzeit in der Lage, das Projekt im OpenCode-CLI-Dialog fortzusetzen, Probleme zu klären, Nachträge zu dokumentieren und offene Fragen/Aufgaben zu behalten, bis sie gelöst sind. Priorisierung der Aufgabenpakete obliegt dem Projektmanager, nicht der Person.

**Begründung:** Autonome Arbeitsweise der KI soll gewahrt bleiben; das Tool steuert, ergänzt und verfeinert, bearbeitet aber nicht selbst.

**Auswirkung:** Schreibrechte der App sind in der Technischen Spec als Matrix festgelegt (Nachtrag, Anlegen, owner, `Klarung`/`Geschlossen` — alles andere KI-Sache).

## 2026-11-14: Sechs UI-Status sind eine Sicht auf das bestehende task_status

**Entscheidung:** Die sechs PRD-Status (Klarung, Offen, In Arbeit, Testing, Dokumentation, Geschlossen) werden **nicht** als zweites Statusmodell in den Dateien geführt, sondern leiten sich als Anzeige-/Filterebene aus `task_status`/`phase` ab (Mapping siehe Technische Spec). Wellen und andere Punkte ohne `task_status` tragen `status` direkt.

**Begründung:** Der festgelegte Workflow (Phasenmodell) bleibt unverändert; es entsteht keine parallele Statuslogik.

**Auswirkung:** Listenansicht filtert über die sechs UI-Status; Aufgaben-Dateien behalten ihr bisheriges Frontmatter-Schema.

## 2026-11-14: Zuständigkeit als Frontmatter-Feld owner (mensch | ai)

**Entscheidung:** Jeder Punkt trägt `owner: mensch | ai` im YAML-Frontmatter. Die Person darf `owner` jederzeit umschalten; zusätzlich darf sie nur die Status `Klarung` (Rückfrage) und `Geschlossen` (Abnahme) setzen. Pipeline-Statuswechsel bleiben KI-Sache.

**Begründung:** Status + owner beantworten gemeinsam „Wo steht es“ und „Wer ist als Nächstes dran“, ohne in die Steuerung der KI einzugreifen.

**Auswirkung:** `owner` ist Pflichtfeld für neue Aufgaben/Wellen; Spalte in der Listenansicht.

## 2026-11-14: Colab-Start ohne externen Tunnel (Port-Freigabe nativ)

**Entscheidung:** Die App wird über einen schlanken Python-Server (Flask) gestartet; der Zugang erfolgt über die eingebaute Colab-Port-Freigabe (`google.colab.output.serve_kernel_port_as_window/iframe`). pyngrok/ngrok/Gradio/Streamlit werden nicht verwendet.

**Begründung:** Einfachster sicherer Weg ohne externen Dienst, ohne Token und ohne Account — Port-Freigabe ist in Colab integriert.

**Auswirkung:** Technische Spec und US-6 halten Start-Befehle fest; `definitions/app/` wird um `server.py` + statisches Frontend ergänzt.

## 2026-11-14: MVP-Umfang — Nachtrag + Aufgabe + Welle anlegen

**Entscheidung:** Der MVP kann: Nachtrag einfügen, neue Aufgabe anlegen, neue Welle anlegen (jeweils OKF-konform) — dazu Übersicht/Listen mit Status/owner. Alle OKF-Typen anlegen und KI-Übergabe-Helfer als Ausbau.

**Begründung:** Deckt den Kernablauf ab („Punkte anlegen, die die KI bearbeitet“), hält den Start klein und testbar.

**Auswirkung:** US-2, US-3, US-4 sind MVP-Scope; weitere Typen kommen in einer späteren Welle.

## 2026-11-14: Navigation mit fünf Hauptpunkten

**Entscheidung:** Fünf Navigationspunkte: Übersicht, Wellen, Aufgaben, Entscheidungen, Projekt (mit Unterpunkten Konzept, Spec, User Stories, Phasen, Log).

**Begründung:** Niedrigste mögliche Komplexität, ausreichend für die Projektsteuerung; Kern ist die Listenansicht.

**Auswirkung:** Frontend-Routing und `GET /api/overview` richten sich danach (US-1).

## 2026-11-14: Statusmodell einheitlich für Wellen, Aufgaben und Punkte

**Entscheidung:** Ein einziges Statusmodell für alle Elemente: `Klarung`, `Offen`, `In Arbeit`, `Testing`, `Dokumentation`, `Geschlossen`.

**Begründung:** Gleiche Spalten und gleiche Lesart überall, geringstmögliche Komplexität in Oberfläche und Pflege.

**Auswirkung:** App-Liste, Wissensdatenbank und Kommunikation verwenden dieselben Statuswerte; keine getrennten Statuslogiken.

## 2026-11-14: Zuständigkeit als eigenes Feld (owner: mensch | ai)

**Entscheidung:** Zusätzlich zum Status gibt es `owner` mit den Werten `mensch` oder `ai`. Status + Zuständigkeit steuern gemeinsam, wer als Nächstes dran ist (z. B. `Klarung` + `owner: mensch` = Projektmanager wartet auf Antwort der Projektleitung).

**Begründung:** Der Status allein sagt nicht, wer antworten muss; durch die Trennung ist jederzeit sichtbar, in welcher Phase eine Sache steht und wer als Nächstes handelt.

**Auswirkung:** Listenansicht der App zeigt Status und owner; beide Seiten (Mensch und Projektmanager) orientieren sich daran.

## 2026-11-14: Nachträge als sichtbarer Block im Dateitext

**Entscheidung:** Nachträge der Projektleitung werden als hervorgehobener Block in die jeweilige Datei eingefügt, z. B. `> **Nachtrag (Mensch, 2026-11-14):** …`.

**Begründung:** So ist in der Datei eindeutig erkennbar, was vom Menschen stammt und geändert werden soll — auch ohne App, rein über den OKF-Text für die KI lesbar.

**Auswirkung:** App bietet Feld zum Einfügen solcher Blöcke; OKF-Struktur und -Lesbarkeit bleiben erhalten.

## 2026-11-14: Umsetzung in Colab, App aus Colab gestartet, Bundle unter /content

**Entscheidung:** Umsetzung primär in Colab. Die SPA wird über einen lokalen Python-Server in Colab plus Browser-Tunnel gestartet. Die Wissensdatenbank liegt in Colab unter `/content/wissen/`.

**Begründung:** App und OpenCode-CLI arbeiten auf denselben Dateien (eine Quelle, kein Synchronisationsaufwand), Umsetzung bleibt in einer Umgebung.

**Auswirkung:** `definitions/` wird um Server-/App-Funktionalität erweitert; Start erfolgt über eine Colab-Zelle.

## 2026-11-14: Kommunikation Mensch/KI über Dateien + Status im Bundle

**Entscheidung:** Der OpenCode-CLI-Chat läuft unabhängig von der App; gemeinsamer Kanal sind Dateien und Status im OKF-Bundle (Session-Start liest wie definiert `wissen/index.md`).

**Begründung:** Nutzt den bereits definierten Workflow, kein zusätzliches Protokoll, klare Single Source of Truth.

**Auswirkung:** Keine direkte KI-Anbindung aus der App im MVP; Status-/Nachtrag-Pflege im Bundle genügt.

## 2026-11-14: Wellen als eigener OKF-Punkt je Welle

**Entscheidung:** Jede Welle wird als eigener Punkt angelegt (z. B. `wissen/wellen/wave-1.md` mit `type: Welle`, Status, owner, Ziel, verlinkte Aufgaben).

**Begründung:** Strukturiert, maschinenlesbar, OKF-konform und für App wie KI gleichermassen zugänglich; gleiche Statuswerte wie überall.

**Auswirkung:** Neuer Ordner `wissen/wellen/` plus Navigationspunkt in der App.

## 2026-11-14: Bestehender Arbeitsablauf bleibt unverändert

**Entscheidung:** Der in `AGENTS.md` festgelegte Arbeitsablauf (Projektmanager + Subagenten `planner`, `coder`, `reviewer`, `tester`, `documenter`) wird durch die App nicht verändert.

**Begründung:** Die App unterstützt die Kommunikation, definiert den Workflow nicht neu.

**Auswirkung:** `definitions/AGENTS.md` bleibt Maßstab; App-Erweiterungen kommen als zusätzliche Funktionalitäten in `definitions/` dazu.

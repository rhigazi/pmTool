# Entscheidungslog

Alle Projektentscheidungen, neueste zuerst. Format: `## YYYY-MM-DD: Titel` mit **Entscheidung**, **Begründung** und **Auswirkung**.

## 2026-11-16: Subagent-Modell zurück auf `deepseek-v4.1-flash` (revidiert die Beam-Entscheidung)

**Entscheidung:** Auf Anweisung der Projektleitung (2026-11-16, Menschen-Kanal: „Ab jetzt lass die neuen SubAgenten mit Modell deepseek-v4.1-flash laufen") laufen **alle neuen Subagenten-Aufträge** wieder mit `deepseek-v4.1-flash` (Projektstandard). Die bereits laufenden Stränge (A26-Bestätigungs-Review, Delta-Bestätigungs-Lauf) beenden ihren Lauf mit Beam — nur **neue** Aufträge sind betroffen. Die Beam-Entscheidung von heute Morgen ist damit für die Zukunft aufgehoben (für die Historie unverändert stehen).

**Begründung:** Ausdrückliche Weisung der Projektleitung; die Modellwahl folgt wieder dem in `AGENTS.md`/`definitions/AGENTS.md` dokumentierten Projektstandard (Subagenten `deepseek-v4.1-flash`, PM `mimo-v2.6-pro`).

**Auswirkung:** Alle ab sofort gestarteten Subagenten (`planner`/`coder`/`reviewer`/`tester`/`documenter`) tragen `model: deepseek-v4.1-flash`; Protokolle nennen das Modell weiterhin mit. Revidierbar bei abweichender Weisung.

## 2026-11-16: Welle 3 freigegeben (Menschen-Kanal über die App)

**Entscheidung:** Die Projektleitung hat **Welle 3 freigegeben** („W3 ist freigegeben", 2026-11-16, Menschen-Kanal). Die Freigabe wurde **von der Projektleitung selbst über die App gesetzt** (Änderung an `wellen/w3.md`: `freigabe: true`, gesetzt über `POST /api/freigabe` — Menschen-Kanal, im Arbeitsbaum als uncommittete Änderung vorgefunden und vom PM als Nutzer-Arbeit erkannt und gepusht). Damit ist der Gate-Zustand formal sauber: **A34** (einzige Aufgabe mit `welle: wellen/w3.md`) erfüllt das UND-Gate ausdrücklich (Aufgabe `freigabe: true` **und** Welle `freigabe: true`) — die Pakete A34-P3/P4 laufen nicht mehr nur auf Basis der Arbeitsanweisung. `wellen/w3.md` hat keine eigenen Aufgaben-Verweise im Body; weitere Aufgaben sind nicht betroffen (A35–A38/A22/A21 bleiben gesperrt ohne Weisung).

**Begründung:** Die Telegram-Erinnerung von heute Morgen („Welle 3 in der App freigeben") wurde umgehend umgesetzt; der Menschen-Kanal `POST /api/freigabe` ist der vorgesehene Weg (KI-Weg bleibt 403). Diesmal setzte die Projektleitung die Freigabe selbst in der App — der Regelfall (Präzedenz K6 war der stellvertretende Datei-Edit; künftig/App-Weg ist jetzt Realität).

**Auswirkung:** Freigabe-Gate für A34 vollständig erfüllt; A34-P3-Review (läuft) und A34-P4 sind formal gedeckt. Freigabe-`w3.md` wird mit diesem Eintrag gepusht (Sofort-Push). Status der App-Freigabe erstmals live durch die Projektleitung genutzt — A39-Test-Befunde bleiben weiterhin offen.

## 2026-11-16: Subagenten laufen mit Modell Beam; Session-Fortsetzung nach der Abend-Pause

**Entscheidung:** Auf Anweisung der Projektleitung (2026-11-16, Menschen-Kanal) laufen **alle Subagenten** (`planner`/`coder`/`reviewer`/`tester`/`documenter`) mit dem Modell **Beam** (`opencode-go/beam-free`) statt `deepseek-v4.1-flash`; der Projektmanager bleibt `mimo-v2.6-pro`. Die Arbeitsreihenfolge knüpft am Übergabeprotokoll 2026-11-15 an (kein Neustart): A39 mit Vorrang (wartet auf Test-Befunde der Projektleitung), dann WIP A34-P3 abschließen (nur Mutantenproben + Urteil, Diff-Sichtung/78+222 grün sind bestätigt) → Takt 8, A34-P4 + Doku-Runde, kombinierter Testlauf, README final. Nebenbefund der Session-Start-Prüfung: die in A34-P4 als PM-Aufgabe vermerkte Umnummerierung der A33-Vorschlagsliste (A34→A35–A38) ist **bereits erledigt** (A33 führt durchgängig A35–A38; Alt-Verweise nur als historische Notiz in a34/a28) — A34-P4 reduziert sich auf Doku/Ergebnisprotokoll. Zusätzlich wurde der Skill `okf-knowledge-base` (Repo `inkeep/open-knowledge-skills`) auf Anweisung der Projektleitung nachinstalliert (`npx skills add …`, identisch zur `--global`-Sektion von `definitions/setup.sh`; Security-Check Gen Safe / Socket 0 / Snyk Low Risk; Ablage `~/.agents/skills/`, kein Repo-Eingriff).

**Begründung:** Ausdrückliche Weisung der Projektleitung zu Subagent-Modell und Skill-Installation; die Rollen-/Workflow-Regeln bleiben unverändert. Die Umnummerierungs-Feststellung verhindert Doppelarbeit (Stand-Abgleich gegen `wissen/aufgaben/a33-…`); der Skill war bereits in `setup.sh --global` vorgesehen (2026-11-14 geklärt und übernommen).

**Auswirkung:** Alle Subagenten-Aufträge ab 2026-11-16 tragen `model: opencode-go/beam-free`; Protokolle nennen das Modell. Revidierbar, falls die Projektleitung abweicht. OKF-Pflege nutzt künftig den geladenen `okf-knowledge-base`-Skill.

## 2026-11-15: Arbeitsanweisung „Offene Pakete" als Freigabe; Welle 2 freigegeben

**Entscheidung:** Die Arbeitsanweisung der Projektleitung (2026-11-15, „Offene Pakete abschließen: A28-Welle B → A29-Rücklauf → A33-B1/B4/B7/B9 + Nachträge → A34-Paket 3+4") gilt für **genau diese Pakete** als Menschen-Kanal-Freigabe — Aufgaben-Gate und Wellen-Gate (UND-Regel) sind damit erfüllt (A28 hängt an `welle: wellen/w2.md`, A34 an `wellen/w3.md`); revidierbar. Zusätzlich hat die Projektleitung **Welle 2 ausdrücklich freigegeben** („Welle 2 ist freigegeben", Menschen-Kanal): `wellen/w2.md` trägt seitdem `freigabe: true`, gesetzt stellvertretend über den Menschen-Kanal `freigabe.setzen(..., herkunft=MENSCH)` (dieselbe Stelle wie `POST /api/freigabe`; Präzedenz K6 — künftig via Endpunkt/App). `wellen/w3.md` bleibt formal ohne `freigabe`-Feld; die Pakete A34-P3/P4 laufen auf Basis der Arbeitsanweisung, die formale Wellen-Freigabe bleibt der Projektleitung vorbehalten (Telegram-Erinnerung gesendet). Keine weitere Aufgabe wird beauftragt (A35–A38, A22, A21 bleiben gesperrt).

**Begründung:** Fail-closed darf eine ausdrückliche Arbeitsanweisung nicht blockieren; der Zweck des Gates (menschlicher Auslöser vor jeder Umsetzung) ist durch die Paketliste der Projektleitung erfüllt. Die KI setzt `freigabe` weiterhin nie aus eigenem Antrieb — hier wurde ein Menschen-Befehl dokumentiert übertragen (K6-Präzedenz).

**Auswirkung:** Umsetzung der genannten Pakete startet in der festgelegten Reihenfolge (A28-Welle B zuerst, je Paket Review + Testphase + Commit); A39-Befunde haben jederzeit Vorrang. Subagenten laufen mit `deepseek-v4.1-flash`.

## 2026-11-15: Neues-Projekt-Flow — start.sh --neu + Erststart-Hinweis

**Entscheidung:** Nach einem Repo-Pull (neuer Container) enthält `wissen/` die pmTool-Projektdaten (Feststellung der Projektleitung). Der neue Flow lautet: `start.sh` **erkennt** vorbefüllte Projektdaten und schlägt **interaktiv** den Reset auf die saubere Vorlage vor (Ja/Nein-Rückfrage, **Nein = unveränderter Normalstart**); zusätzlich gibt es das Flag **`--neu`** für den direkten Reset (Backup + Vorlage + Start). Die Reset-Logik läuft ausschließlich über `tools/neues_projekt.py` (A24) — keine zweite Lösch-Implementierung in `start.sh`. Variante aus vier Optionen von der Projektleitung gewählt (2026-11-15).

**Begründung:** Der manuelle Reset-Schritt wird nach einem Pull nicht gefunden (Nutzer-Feststellung); ein interaktiver Hinweis ist sicher (kein Datenverlust ohne Bestätigung) und komfortabel. `--neu` deckt den bewussten Neustart ab.

**Auswirkung:** [A32](/aufgaben/a32-neues-projekt-flow.md) angelegt (angenommen, ID + Titel, Sofort-Push); betroffen: `start.sh`, `test_start_skript.py`, README, `docs/colab-start.md`. Reihenfolge: parallel zu A30/A31 umsetzbar (keine Datei-Überschneidung mit der UI-Strecke).

## 2026-11-15: A28-Review — Nachbesserung zweigeteilt (W1–W3 + K1–K7)

**Entscheidung:** Das A28-Review lief **NACHBESSERUNG** (W1 `naechste_kennung` ignoriert `a<N>.md` ohne Slug — echter AK-2-Fehler inkl. vergebener Doppelkennung; W2 Testlücke: KI-Weg bei `wert=false` nicht gepinnt (Mutante überlebt); W3 `freigabe` fehlt in der Spec-Datenmodelltabelle). PM-Beschlüsse: **W1–W3 werden behoben**; **K1:** den `neu`-Fixture-Default in `test_welle_spalte.py` **entfernen** (A31 bleibt grün — fehlendes `neu` gilt als `false` — und bleibt scharf für „Marke standardmäßig an"; die Marke decken A28-T23–T25); **K2:** `test_arbeitsstand.py` T12 wieder auf **exakte** Schlüsselmenge (inkl. A28-Felder); **K3** → [A37](/aufgaben/a37-dom-harness-konsolidierung.md) (Harness-Lücke `createTextNode` beheben, Produktivcode-Weg rückgängig machen); **K4:** Plan-Liste wird vom `documenter` korrigiert; **K5:** Modultest „leerer Bestand → A1"; **K6:** Wortlaut geklärt (Freigaben stellvertretend für die Projektleitung als Datei-Edit — Menschen-Kanal, dokumentiert; der Endpunkt wird ab der nächsten Freigabe genutzt); **K7:** Doppel-Param entfernen. **Rücklauf zweigeteilt wegen Datei-Konflikte:** Welle A (W2/W3/K5/K7) sofort (disjunkt zu laufender Arbeit), Welle B (W1 `overview.py`, K1 `test_welle_spalte.py`, K2) erst nach Rückkehr von A34-P1+2 und B8. Danach Kurz-Bestätigungs-Review.

**Begründung:** W1 ist ein realer Logikfehler (falsche `naechste_kennung` genau im Fall inkonsistenter Dateien); W2 pinnt eine Sicherheitszusage (Mutantenschutz); die Zweiteilung verhindert Moving-Target-Konflikte mit A34 (`overview.py`) und B8 (`test_welle_spalte.py`).

**Auswirkung:** A28 → in Nachbesserung (Phase 4); Welle A startet sofort, Welle B nach A34/B8; danach Bestätigungs-Review. A29-Architektur (ein Fundament, ein Endpunkt, fail-closed) wurde vom Review ausdrücklich als tragend bestätigt.

## 2026-11-15: A26-Review — Nachbesserung (W1/W2 Dev-Selbstlauf) und korrigierter Zählumfang

**Entscheidung:** Das A26-Review lief **NACHBESSERUNG NÖTIG** (2 wesentlich + 5 klein). PM-Beschlüsse: **W1:** `setup.sh` erkennt Selbstkopien (realpath-Vergleich → „übersprungen (Quelle = Ziel)") — `bash definitions/setup.sh . --force` im Dev-Repo muss sauber durchlaufen (Exit 0); Regressionsfall „Dev-Layout" wird Test-Pflicht. **W2:** Die dokumentierte Auffrischung wird korrigiert: im Dev-Repo überspringt `setup.sh` (bei `TARGET` = Elternverzeichnis von `SRC`) die Abschnitte 4b/5/10 bzw. die README-Anweisung nennt einen expliziten Spiegel-Kopierschritt statt `setup.sh . --force` — Ziel: nach der dokumentierten Auffrischung bleibt die Root-Suite grün (kein zweites `app/`). **K3** (Testlücken: verify.sh im Dev-Repo, `--force` für die neuen Verteilziele, Dev-Selbstlauf) wird im selben Rücklauf mitgehärtet; **K4:** Namensregel „Testdatei-Basisnamen repo-weit eindeutig" in den `conftest.py`-Docstring; **K1/K2/K5** gehen an den `documenter` (Doku-Runde). **K5-Zählumfang wird korrigiert:** „Gesamtsuite" = **Root-Suite** (`pytest -q` im Repo) = App-Suite + `definitions/tools/tests` (Quelle); der verteilte Spiegel `tools/tests` zählt **nicht** (wird vom Root per `collect_ignore` übersprungen). Damit ist die Gesamtsuite zuletzt **1118** (Stand A26); die frühere Definition „App + tools/tests (69)" ist überholt und wird in README/Features/Übergabeprotokoll nachgezogen.

**Begründung:** W1/W2 hängen zusammen (der naive W1-Fix macht W2 sichtbar) und betreffen die in der Doku versprochene Dauerhaftigkeit der Root-Suite-Lösung; der Zählumfang muss zur realen Root-Suite passen, sonst sind Standangaben nicht reproduzierbar.

**Auswirkung:** A26 → in Nachbesserung (Phase 4); Rücklauf nach Tester-Rückkehr (Moving-Target-Schutz für `setup.sh`), danach Bestätigungs-Review + Testnachlauf. Dokumentations-Nachläufe (K1/K2/K5) in der nächsten Doku-Runde.

## 2026-11-15: A32-Review — Nachbesserung mit PM-Entscheidungen zu W1 und K1–K8

**Entscheidung:** Das A32-Review lief **NACHBESSERUNG NÖTIG** (1 wesentlich + 8 klein). PM-Beschlüsse für den Rücklauf: **W1 (wesentlich):** Marker-Erkennung wird am **Reset-Ziel** ausgerichtet (`$PROJEKT/wissen`, nicht `BUNDLE_ROOT`); weicht `BUNDLE_ROOT` ab, wird im Hinweis ausdrücklich darauf hingewiesen („Reset wirkt auf `<Projekt>/wissen`") — plus Test mit überschriebenem `BUNDLE_ROOT`, der die Semantik festnagelt. **K1:** der funktional tote Fallback `definitions/tools/neues_projekt.py` wird **entfernt** (klare Fail-loud-Meldung „Werkzeug fehlt: `tools/neues_projekt.py`" statt irreführender Vorlagen-Fehlermeldung). **K2/K4/K8:** Einzeiler (Werkzeug im interaktiven Hinweis nennen, Rot-Stand-Zahl 12/10 präzisieren, Kopfkommentar `BUNDLE_ROOT` korrigieren). **K3:** `--neu` darf auch bei **fehlendem** `wissen/` arbeiten — die Strukturprüfung wird bei `--neu` auf `definitions/` reduziert, das Werkzeug baut das Bundle aus der Vorlage (PM-Entscheidung: „Neues Projekt" muss den einzigen Fall ohne Bundle bedienen können). **K5:** Randfälle als parametrisierte Tests (leere Eingabe, `y`/`YES`/Groß-Klein, `BUNDLE_ROOT`-Override, `--neu` ohne `wissen/`). **K7:** Port-Hinweis/-Prüfung **vor** den Reset ziehen (bei belegtem Port: Hinweis/Abbruch vor der Rückfrage; günstigste Variante). **K6:** Status/Phase wurden regelkonform vom **PM** gesetzt (nicht vom Coder); das Ergebnisprotokoll wird in der Doku-Runde ergänzt.

**Begründung:** W1 betrifft die Zustimmungsgrundlage des Löschens („fremdes Bundle als Auslöser") — das muss vor dem nächsten Takt sauber sein; die übrigen Punkte sind klein und gehen gebündelt im selben Rücklauf mit.

**Auswirkung:** A32 → in Nachbesserung (Phase 4); Rücklauf an den `coder` startet, sobald die A32-Testphase beendet ist (Moving-Target-Schutz für `start.sh`). Danach erneutes Kurz-Review + Testnachlauf.

## 2026-11-15: Feature-Strecke zuerst, dann gemeinsame Testpause und README-Abschluss

**Entscheidung:** Vorgehen laut Vorgabe der Projektleitung (2026-11-15): (1) **Alle ausstehenden Features fertig machen** (A28–A38 inkl. A33-Batches, Review/Testphase je Aufgabe). (2) Dann **bewusste Pause + gemeinsame, ausgiebige Test- und Abstimmungsrunde** mit der Projektleitung — Ziel: feststellen, was für sauberes Zusammenarbeiten noch fehlt (Lückenliste). (3) Danach **`README.md` im Repo final aktualisieren** (Abschlussstand, Nutzung, Abläufe). Kein neuer Feature-Takt nach der Runde ohne Weisung. Festgehalten als [A39](/aufgaben/a39-testrunde-readme-abschluss.md) (angenommen, Sofort-Push).

**Begründung:** Die Projektleitung möchte nach der Feature-Strecke gemeinsam Qualität und Zusammenarbeits-Lücken bewerten, statt weiter in Features zu laufen; die README soll erst am Ende den echten Abschlussstand dokumentieren (Zwischenstände laufen weiter klein mit).

**Auswirkung:** A39 ist der Abschluss-Meilenstein und Blocker für neue Feature-Takte; die Lückenliste wird die Folgeaufgaben liefern (dort greifen wieder ID+Titel+Sofort-Push).

## 2026-11-15: A33-Plan bestätigt — Batches, Nummernvergabe A35–A38, A5-B2 entschieden

**Entscheidung:** (1) Der A33-Plan (28 Befunde → 18 in 9 Batches B1–B9, 22 Tests) wird bestätigt; die 5 offenen Fragen sind entschieden: B9 durch den `coder`; B1 nur `lexists` + R8-Vermerk (`O_EXCL` post-MVP); B4/B5/B6 warten auf A28-P0, B1–B3 laufen (B1 zusätzlich erst nach A26-Review/-Testphase — Moving-Target-Schutz, die lesen die Werkzeug-Dateien). (2) **A5-B2 entfällt als Code-Punkt:** `FALLBACK_KUERZEL` bleibt bewusst robust (bestätigte PM-Entscheidung aus dem A5-Ergebnisprotokoll); die Asymmetrie zu A4 wird in B9 dokumentiert. (3) Die ausgegliederten großen Befunde erhalten die bestätigten Nummern **A35** (Status-Mapping server-seitig, A12-1), **A36** (`schreibgeschuetzt`-Signal), **A37** (DOM-Harness-Konsolidierung, A14-6), **A38** (Log-Anker, A14-9) — die ursprünglichen Planner-Vorschläge A34–A37 kollidierten mit dem zwischenzeitlich angelegten A34 (Unter-Aufgaben) und wurden verschoben. Die vier Aufgaben sind als Dateien angelegt und gepusht (Vormerkung, Umsetzung nach A29/A33).

**Begründung:** Nichts verliert sich (Sofort-Push-Regel); die Nummernvergabe ist eindeutig; B1–B3 sind datei-disjunkt zu A28/A29 und laufen sofort; A33 bleibt klein und parallelisierbar.

**Auswirkung:** Coder-Takt B2+B3 startet sofort; B1 bei A26-Rückkehr; B4–B6 nach A28-P0; B7–B9 nach A29. A35–A38 in der Warteschlange.

## 2026-11-15: A28 und A29 durch die Projektleitung freigegeben

**Entscheidung:** Die Projektleitung hat A28 („Benachrichtigung bei neuer Aufgabe") und A29 („Wellen abarbeiten") am 2026-11-15 **ausdrücklich freigegeben** („A29,A28 sind freigegeben", Menschen-Kanal). Die Freigaben sind im Frontmatter der Aufgaben-Dateien vermerkt (`aktuell`); sobald das A28-Paket-0-Fundament (`freigabe`-Feld) existiert, werden sie als `freigabe: true` nachgetragen. Die Umsetzung startet in der festgelegten Reihenfolge **A27 (läuft) → A30 → A31 → A28 → A29** (Datei-Konflikte `liste.js`/`detail.js`/`meta.py`/`overview.py`; G15–G23). **A31 ist noch nicht freigegeben** — fail-closed: Umsetzung erst nach ausdrücklicher Freigabe; Rückfrage an die Projektleitung läuft.

**Begründung:** Freigabe-Gate (Standardentscheidung 2026-11-15): Umsetzung beginnt erst nach geklärt + freigegeben. Die Reihenfolge minimiert Datei-Konflikte bei maximaler Parallelität der Review-/Teststränge.

**Auswirkung:** Coder-Takte A30/A31/A28/A29 nacheinander (jeweils Review + Testphase); A29 startet zusätzlich erst nach A28 Paket 0 + 2 (grün/committed) laut Plan.

## 2026-11-15: H1-Schluss (A23) und fester Zählumfang der Gesamtsuite

**Entscheidung:** (1) **H1 (A23-Testzahl 92 vs. 93) wird geschlossen** — die Planzahl war falsch: 71 `def test_`-Zeilen inkl. des Fixtures `test_bundle` + 22 parametrisierte Fälle ⇒ 70 echte Tests + 22 = **92** = pytest-Collect; kein Test fehlt, die Abdeckung (T1–T23) ist vollständig. Planzahl auf 92 korrigiert; die kosmetische Fixture-Umbenennung geht in den Aufräum-Takt. (2) **Der Zählumfang „Gesamtsuite" wird festgelegt:** App-Suite (`definitions/app/tests`) + `tools/tests`; `definitions/tools/tests` wird separat ausgewiesen. Der Stand **1015 war nicht reproduzierbar** und wird auf **1011** korrigiert (Basis `07ad675`: 942 + 69). Stand 2026-11-15 (Arbeitsbaum): 995/996 — der eine „failed" ist fremde halbfertige A27-Arbeit (`test_welle_zuordnung.py` noch rot), kein A25/A23-Regress.

**Begründung:** Tester-Bericht 2026-11-15 (A25-Testphase S1–S6 + H1 + Kontrolllauf). Ohne festen Zählumfang sind Standangaben nicht reproduzierbar; die bekannte Flaky-Zone im Parallelbetrieb verlangt klar bezifferte Basis-Stände.

**Auswirkung:** A23 ist reif für Abschluss. Standangaben in `features.md`/`README`/`Übergabeprotokoll` werden in der Doku-Runde auf 1011-Basis nachgezogen (Auftrag an den `documenter`).

## 2026-11-15: A30 als nächste Aufgabe — Freigabe durch Priorisierung der Projektleitung

**Entscheidung:** Die Projektleitung hat die neue Aufgabe „Was passiert gerade" (angenommen als [A30](/aufgaben/a30-was-passiert-gerade.md)) als „nächste Aufgabe" bezeichnet. Das gilt als **Priorisierung und Freigabe** über den Menschen-Kanal (Standardentscheidung: ausdrückliche Zustimmung über Chat/Telegram/App genügt) — Planung startet sofort, Umsetzung nach A27 (Datei-Überschneidung `liste.js`). Wird die Freigabe widerrufen, stoppt die Umsetzung (revidierbar).

**Begründung:** Klarer Handlungsauftrag der Projektleitung („hier die nächste Aufgabe"); die A28-Freigabe-Regel soll Wartezeiten verhindern, nicht blockieren. Die Datensemantik von `freigabe` (eigenes Feld, fail-closed) wird erst mit A28/A29 produktiv — bis dahin gilt der Menschen-Kanal.

**Auswirkung:** A30 geht in die Planung und wird nach A27 umgesetzt (Reihenfolge im Frontmatter `aktuell` gepflegt). Die Freigabe-Interpretation ist im Log offen dokumentiert.

## 2026-11-15: Freigabe-Datenhaltung fail-closed (A28/A29-Planung bestätigt)

**Entscheidung:** Die im Planungsstand von [A28](/aufgaben/a28-benachrichtigung-neue-aufgabe.md)/[A29](/aufgaben/a29-wellen-abarbeiten.md) getroffenen Festlegungen werden bestätigt: `freigabe` ist ein boolesches Frontmatter-Feld, fehlend/≠`true` = **nicht freigegeben** (fail-closed); bei Neuanlage immer `freigabe: false`. Die Freigabe ist ein **Menschen-Recht** — der KI-Schreibweg liefert technisch 403 und schreibt nichts (auch nicht bei `false`); dokumentiert als Modul-/API-Konvention + Projektregel, da eine lokale Single-User-App keine Authentifizierung kennt. Wahrnehmungssignal: abgeleitetes `neu`-Flag (Titel `^A<N>:` **und** Dateiname `^a<N>(-|.)`); kein Push/Watcher/Telegram aus der App (verworfen — Prüfpflicht des PM bleibt, die App liefert das deterministische Signal). Wellen-Gate: `wirksam = Aufgabe freigegeben AND (keine Welle OR Welle freigegeben)`; Entzug sperrt nur weitere Beauftragungen, keine laufende Umsetzung.

**Begründung:** Fail-closed ist die sichere Voreinstellung (nichts beginnt ohne ausdrückliche Freigabe); die Rechteklasse ist analog zu `owner`/Status-Klarung/Geschlossen als Menschen-Recht konsistent; externe Benachrichtigungsdienste widersprechen der Abhängigkeits-Regel.

**Auswirkung:** Umsetzung in A28 Paket 0 (Fundament) → A29; `phasen.md` erhält Phase „3b. Freigabe" + Wartestatus `geplant`; `technische-spec.md` Rechtezeile + Endpunkt `POST /api/freigabe`.

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

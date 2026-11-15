---
type: Task
title: "A33: Kleinbefunde-/Aufräum-Takt (gebündelt)"
description: Gebündelte Behebung der offenen Kleinbefunde aus Reviews und Post-MVP (A24-K1–K3,
  A23-Fixture, A4-1/2, A5-B3/B4, A6-1/2, A7-2, A9-K3/K4, A13-3, A14-5/6/7/9, A16-1/4, N5/N8,
  A20-Pin-Pflege) in eigenen Batches mit je eigenem Commit.
task_status: in Planung
phase: 2 Planung
priority: mittel
assigned_to: coder
owner: ai
aktuell: "PM: B2+B3 umgesetzt (gruen, App-Suite 1107) — B1 nach A26-Ruecklauf, B4–B6 nach A28-P0, B7–B9 nach A29"
---

# Ziel

Über die Reviews und Post-MVP-Takte haben sich **28 kleine, unkritische Befunde** gesammelt (Übergabeprotokoll „Offene Punkte", Reviews A23/A24/A25). Sie werden **gebündelt** in einem Aufräum-Takt abgearbeitet — je Batch ein eigener Commit, Tests vorher rot/nachher grün, keine Verhaltensänderungen über die Befunde hinaus.

Das Ergebnis der Prüfung gegen den aktuellen Code-Stand (2026-11-15, nach A26/A27):

- **9 Batches (B1–B9)** mit zusammen **18 Befunden** — dateiweise getrennt, sofort oder nach A28-P0/A29 lauffähig (B1–B3 laufen parallel zur A28-Strecke).
- **4 eigene Aufgaben (A35–A38)** für die zu großen Befunde: A12-1 (Status-Mapping-Spiegel), A12-Schreib-UI-Grenze, A14-6 (Harness-Konsolidierung), A14-9 (Log-Anker).
- **6 Befunde entfallen** mit Begründung (A4-1, A14-7, A16-4, N5, N8, A20-Pin) — erledigt, durch Tests abgedeckt oder reine Betriebshinweise; nichts wird still gestrichen.
- **1 sicherheitsrelevanter Fix** ist A24-K2 (baumelnder Symlink auf dem automatischen Backup-Namen) — deshalb steht B1 vorn.

# Akzeptanzkriterien

1. **Vollständigkeit ohne stilles Streichen:** Jeder der 28 Befunde aus dem Katalog hat genau einen Status — **Batch (B1–B9)**, **eigene Aufgabe (A35–A38)** oder **entfällt** — mit Begründung und Beleg gegen den geprüften Code-Stand (2026-11-15, nach A26/A27). Kein Befund verschwindet ohne Eintrag im Prüfergebnis.
2. **Batch-Schnitt und Commits:** Neun Batches (B1–B9), dateiweise disjunkt zueinander und zu den laufenden Aufgaben (A28/A29), je Batch **ein eigener Commit**, isoliert rückrollbar. Werkzeug-Batches ändern **nur** `definitions/tools/…` (Single Source seit A26) und verteilen danach den Spiegel nach `tools/…`; beide Dateien sind anschließend byte-identisch.
3. **TDD-Beleg:** Je Batch T1–T22 wie unten; jeder Test läuft **vor** der Änderung rot (Ausnahmen sind ausdrücklich als Bestands-/Mutationstests markiert: K1, K3, A24-H1, A6-2 — Beleg über Mutation bzw. dokumentierte Prüfung). Nach der Änderung grün, Baselines unverändert grün.
4. **Keine Streuverluste:** Keine Verhaltensänderung über den jeweiligen Befund hinaus, keine neuen Abhängigkeiten, kein neuer Endpunkt, `index.html` unverändert. Bestehende Testdateien werden nur dort angepasst, wo der Befund es verlangt (namentlich genannt).
5. **Prüfstand:** App-Suite, `tools/tests` und `definitions/tools/tests` grün; `bash definitions/verify.sh .` → Exit 0. Belege (Testzahlen, Rot/Grün) im `# Ergebnisse`-Abschnitt je Batch.
6. **Doku nachgezogen:** Die Doku-Batches ändern ausschließlich `wissen/projekt/…` und die betroffene Aufgaben-Datei; `features.md`, `log.md` und Aufgaben-Status pflegt der PM/`documenter` (kein Coder-Schreibzugriff).
7. **Große Befunde ausgegliedert:** A12-1, A12-Schreib-UI-Grenze, A14-6 und A14-9 werden **nicht** in A33 umgesetzt, sondern als eigene Aufgaben mit Nummer, Scope, Abhängigkeit und Aufwand vorgeschlagen (A35–A38, siehe Kontext).
8. **Parallelität dokumentiert:** Für jeden Batch steht, ob er sofort parallel zu A28 läuft, erst nach A28 Paket 0 oder erst nach A29 — mit Datei-Schnittmengen-Begründung.

# Befund-Katalog (Ausgangsbestand)

- **A24-Review (2026-11-15):** K1 zweite Backup-Barriere ohne Test, K2 baumelnder Symlink auf automatischem Backup-Namen, K3 Ausweichen `-2`/`-3` nicht deterministisch getestet; H1 verify-Meldungstest prüft Wortlaut statt Eigenschaft, H2 Testlücken a–e einzeln dokumentieren, H3 Rollback-Meldung ohne Wiederherstellungsschritt.
- **A23:** H1-Nachtrag: Fixture `test_bundle` umbenennen (kosmetisch).
- **Post-MVP-Liste (Übergabeprotokoll):** A12-1 Mapping-Spiegel, A12-Schreib-UI-Grenze (`schreibgeschuetzt`-Signal — prüfen ob aufwändig → ggf. eigene Aufgabe), A13-3 Linktext-Kosmetik, A4-1 `#`-Maskierung in `ziel`, A4-2 `welle`-Feld in Spec/phasen.md, A5-B3 `description`-Feld bei Wellen, A5-B4 Slug-Logik-Duplikat, A6-1 H-Belege je H-Punkt, A6-2 T2 Body-Hash optional, A7-2 Startfehler absoluter Pfad, A9-K3 403-Notiz/Spec-Abgleich, A9-K4 TOCTOU (R8, dokumentiert — vermutlich nur Vermerk), A14-5 `istDatei`/Meldungen nach `api.js`, A14-6 DOM-Harness-Fork `MINI_DOM` konsolidieren, A14-7 Request-Sequenz-Guard, A14-9 Anker je Log-Eintrag, A16-1 R11-Zitat/Ausweichport, A16-4 Env-Weitergabe, N5 Cache-Fixture ins Definitions-Repo, N8 T7-Betriebshinweis, A20-Pin-Pflege (Hinweis).

# Prüfergebnis (gegen Code-Stand 2026-11-15, nach A26/A27)

| Befund | Prüfung am Code | Status | Aufwand |
|---|---|---|---|
| **A24-K1** | Barriere in `backup_erstellen` vorhanden, aber nur indirekt über `_pruefe_backup_ziel` getestet — direkter Aufruf fehlt | **B1** (Test) | 0,5 h |
| **A24-K2** | **Offen:** `_backup_name` nutzt `exists()` → baumelnder Symlink gilt als frei; der automatische Zweig prüft kein `is_symlink`; `tarfile.open` folgt dem Link (Schreiben außerhalb des Ziels möglich) | **B1** (Fix + Test) | 1 h |
| **A24-K3** | Test `test_zweites_backup_ueberschreibt_das_erste_nicht` hängt am Sekundenstempel; `_backup_name(zeitpunkt=…)` wird nicht genutzt | **B1** (deterministischer Test) | 0,5 h |
| **A24-H1** | Test prüft Wortlaut („aus der geprüften Vorlage") + eine Negativformulierung, nicht die Eigenschaft „keine unbelegte Verify-Behauptung" | **B1** (Testrefactor) | 0,5 h |
| **A24-H2** | a–e nur als „u. a." im A24-Ergebnis; die Reviewer-Details a–e stehen nicht im Bundle | **B9** (Doku) | 0,5 h |
| **A24-H3** | Meldung „Altbestand unter … gesichert." nennt keinen Wiederherstellungsschritt | **B1** (Fix + Test) | 0,5 h |
| **A23-H1** | Fixture `test_bundle` in `test_projekt.py` und `test_features.py` (wird von pytest **nicht** als Test gesammelt — rein kosmetisch) | **B2** (Rename) | 0,25 h |
| **A12-1** | `TASK_STATUS_UI`/`OWNER_DEFAULTS` in `detail.js` spiegeln `status.py`; Drift möglich | **eigene Aufgabe A35** | 4–6 h |
| **A12-Schreib-UI** | Kein `schreibgeschuetzt`-Signal; die UI bietet Schreibaktionen auf reservierten Dateien an (Server antwortet 403) | **eigene Aufgabe A36** | 3–4 h |
| **A13-3** | `neu_aufgabe._verweis_zeile` nutzt den Dateistamm (`w2`), keinen Wellen-Titel | **B4** (Fix + Test) | 0,5 h |
| **A4-1** | YAML quotet `#`-Werte automatisch (`'# foo'`, `'foo # bar'` — verifiziert); ein führendes `#` im Body ist Markdown-Absicht | **entfällt** (kein Fehler) | – |
| **A4-2** | `welle` fehlt im Aufgaben-Format (`phasen.md`) und in der Read-Modell-Tabelle (`technische-spec.md`) | **B9** (Doku) | 0,5 h |
| **A5-B3** | `neu_welle._inhalt` schreibt kein `description` (Aufgaben tun es) | **B3** (Fix + Test) | 0,5 h |
| **A5-B4** | Slug-Logik in `neu_aufgabe.slug_aus_titel` und `neu_welle.kuerzel` dupliziert; leichter Unicode-Unterschied (`encode ascii` vs. Combining-Filter) | **B7** (Refactor + Test) | 2–3 h |
| **A6-1** | Doku-Eintrag vom 2026-11-14 vorhanden; H1/H5/H7-Definitionen fehlen im Bundle (1:1-Zuordnung nicht belegbar) | **B9** (Vermerk) | 0,25 h |
| **A6-2** | T2 (`owner → mensch`) prüft keinen Body-Hash | **B6** (Test) | 0,25 h |
| **A7-2** | `StartFehler` nennt den absoluten Pfad (`BUNDLE_ROOT ist kein Verzeichnis: /…`); Test prüft nur `"BUNDLE_ROOT" in err` | **B5** (Fix + Test) | 0,5 h |
| **A9-K3** | 403-Semantik im A9-Ergebnis präzisiert; die Spec nennt „bekannt, aber verboten → 403" nicht | **B9** (Doku) | 0,5 h |
| **A9-K4** | R8/TOCTOU im A9-Ergebnis dokumentiert; Spec/Entscheidungslog nicht | **B9** (Doku) | 0,25 h |
| **A14-5** | `istDatei` identisch in `detail.js` und `features.js`; Meldungen sind bewusst kontextspezifisch | **B8** (nur Prädikat) | 1 h |
| **A14-6** | Vier Harness-Kopien (`test_detail`, `test_suche`, `test_features`, `test_welle_zuordnung`); A30 legt `dom_helfer.py` nur für neue Tests an | **eigene Aufgabe A37** | 5–8 h |
| **A14-7** | Durch exakte `aufrufe`-Assertions (A25-T16, A27-T38) und Doppelklick-/Parallel-Tests (A12-2) abgedeckt | **entfällt** (abgedeckt) | – |
| **A14-9** | Log-Einträge verlinken alle auf dieselbe Detailseite; kein Anker je Eintrag | **eigene Aufgabe A38** | 2–3 h |
| **A16-1** | R11 in `planung.md` („Ausweichport") widerspricht dem Verhalten (`start_colab`/`server`: klare Meldung, kein Ausweichport) | **B9** (Doku) | 0,5 h |
| **A16-4** | `_starte_server` übergibt `{**os.environ, BUNDLE_ROOT, PORT}` | **entfällt** (erledigt) | – |
| **N5** | Tests/Fixtures nutzen `tmp_path`; `test_verteilung` prüft, dass keine Cache-Artefakte verteilt werden (A26/R12) | **entfällt** (erledigt) | – |
| **N8** | Betriebshinweis (Suite wächst automatisch mit neuen Testdateien) — kein Code | **entfällt** (Hinweis) | – |
| **A20-Pin** | Betriebshinweis (Moli-URL + SHA256 gemeinsam ändern) — kein Code | **entfällt** (Hinweis) | – |

**Zusatz (nicht im Katalog, in A5 offen): A5-B2 ENTSCIEDEN (PM, 2026-11-15):** `FALLBACK_KUERZEL` bleibt bewusst robust (Fallback statt `EingabeFehler` bei leerem Wellen-Slug — bestätigte PM-Entscheidung aus dem A5-Ergebnisprotokoll). Die Asymmetrie zu A4 wird in **B9** als bewusste Entscheidung in der Spec/`phasen.md` dokumentiert; kein Code-Punkt.

# Testfälle (TDD)

Reihenfolge = Red-Green-Takt: erst Test schreiben, rot laufen lassen, dann das Minimum implementieren. Jede Testnummer ist ein eigener pytest-Fall; Ausnahmen (Bestands-/Mutationstest) sind markiert. Neue Tests liegen in den jeweils genannten Dateien; **keine** neuen Harness-Kopien (A30-`dom_helfer.py` wird genutzt, wo UI nötig wäre — in A33 nicht nötig).

**B1 — A24-Werkzeug-Härtung (K1, K2, K3, H1, H3) · Dateien: `definitions/tools/neues_projekt.py`, `definitions/tools/tests/test_neues_projekt.py` (+ Verteilung)**

- **T1 (K1) Zweite Barriere direkt:** `backup_erstellen(wissen, ziel)` mit vorhandenem `ziel` (reguläre Datei, Inhalt `b"alt"`) → `BackupFehler`, Dateiinhalt byte-gleich, `wissen/` unverändert. *Bestandstest (grün); Rot-Beleg über Mutation: Barriere lokal entfernen → Test rot, nicht committen.*
- **T2 (K2) Baumelnder Symlink auf automatischem Namen:** Im Projekt-Root liegt `wissen-backup-<jetzt>.tar.gz` als Symlink auf ein nicht existierendes Ziel; `main(["--ja"])` → Exit 0, Backup entsteht unter `…-2.tar.gz`, der Symlink bleibt unverändert, das Linkziel wird **nicht** angelegt, `wissen/` entspricht der Vorlage. *Rot vor dem Fix (heute wird durch den Link geschrieben bzw. das Ziel angelegt).*
- **T3 (K2) Barriere in `backup_erstellen`:** `backup_erstellen(wissen, dangling_symlink)` → `BackupFehler`, Symlink unverändert, Linkziel fehlt, `wissen/` unverändert. *Rot vor dem Fix.*
- **T4 (K3) Determinismus:** `_backup_name(root, zeitpunkt=datetime(2026,1,1,12,0,0))` mit vorhandenen `…-20260101-120000.tar.gz` und `…-2.tar.gz` → `…-3.tar.gz`; mit fehlender `-2`, vorhandener `-3` → `-2`; mit baumelndem Symlink auf dem Basisnamen → `-2` (via `lexists`). *Teil 1/2 Bestandstest; Teil 3 rot vor dem Fix.*
- **T5 (H1) Eigenschaft statt Wortlaut:** Nach `--ja` enthält die Ausgabe **keine** unbelegte Verify-Behauptung (`re.search(r"verify[^.\n]*(grün|bestanden|erfolgreich|ok)", out, re.I) is None`) und nennt die Quelle als „geprüfte Vorlage"; der Hinweis „Setup prüfen: bash definitions/verify.sh" bleibt erlaubt. *Bestandstest; ersetzt die Wortlaut-Assertion.*
- **T6 (H3) Wiederherstellungsschritt:** Fehlgeschlagener Rollback (Seam `_ersetze` scheitert beim Tausch und beim Rücktausch) → stderr nennt den `Altbestand`-Pfad **und** einen konkreten Wiederherstellungsschritt (`Wiederherstellen` + `mv`/Ziel `wissen`); Altbaum bleibt vollständig. *Rot vor dem Fix (Meldung ohne Schritt).*

**B2 — A23-H1 Fixture-Rename · Dateien: `definitions/app/tests/test_projekt.py`, `test_features.py`**

- **T7 (A23-H1) Kosmetik ohne Verhaltensänderung:** `@pytest.fixture def test_bundle` existiert in beiden Dateien nicht mehr; die Fixture heißt `szenarien_bundle` (bzw. `bundle_voll`), alle Verwendungen (`app_server`) sind umgestellt, Suite und Sammelbild unverändert (`pytest --collect-only` gleiche Testzahl). *Dokumentierte Prüfung (kein Rot möglich — die Fixture wird heute nicht als Test gesammelt).*

**B3 — A5-B3 Wellen-`description` · Dateien: `definitions/app/neu_welle.py`, `tests/test_neu_welle.py`**

- **T8 (A5-B3) Feld vorhanden:** `neu_welle.anlegen` mit `ziel: "Erste Zeile\nzweite"` → Frontmatter `description == "Erste Zeile"` (≤ 160 Zeichen, Umlaute erhalten), `title`/`status`/`owner` unverändert, Body weiterhin `# Ziel` + `# Aufgaben`. *Rot vor dem Fix (Feld fehlt).*
- **T9 (A5-B3) Kürzung/Randfall:** `ziel` mit 200 Zeichen → `description` endet auf `…` und ist ≤ 160; leeres `ziel` bleibt `EingabeFehler` (unverändert); bestehende Wellen-Tests grün. *Rot vor dem Fix (Feld fehlt).*

**B4 — A13-3 Wellen-Linktext · Dateien: `definitions/app/neu_aufgabe.py`, `tests/test_neu_aufgabe.py` · nach A28 Paket 0**

- **T10 (A13-3) Titel als Linktext:** Welle `wellen/w2.md` mit `title: "W2"`; `anlegen` mit `welle: "wellen/w2.md"` → Kontext-Zeile `- Welle: [W2](wellen/w2.md)`; `user_story`-Linktext bleibt unverändert der Dateistamm. *Rot vor dem Fix (`[w2]`).*
- **T11 (A13-3) Fallback/fail-safe:** `welle` fehlt als Datei, hat kein Frontmatter oder ist kein String → Linktext bleibt der Dateistamm (`[w2]`), **kein** Fehler, Aufgabe wird angelegt; `welle` leer → keine Zeile (wie bisher). *Rot vor dem Fix nur für den Titel-Fall; Fallback ist Bestandsschutz.*

**B5 — A7-2 Startfehler ohne Pfad · Dateien: `definitions/app/server.py`, `tests/test_server.py` · nach A28 Paket 0**

- **T12 (A7-2) Kein Pfad-Leak:** `BUNDLE_ROOT` zeigt auf eine nicht existierende Datei/Verzeichnis (tmp-Pfad) → `main()` Exit 1, stderr enthält `BUNDLE_ROOT` und den Grund, aber **nicht** `str(tmp_path)` (kein absoluter Pfad). *Rot vor dem Fix.*
- **T13 (A7-2) Verhalten unverändert:** leeres/fehlendes `BUNDLE_ROOT` → Exit 1 mit bestehender Meldung; gültige Wurzel startet weiterhin (Start-Test mit Monkeypatch); keine Änderung an HTTP-Fehlern. *Bestandstest.*

**B6 — A6-2 T2 Body-Hash · Dateien: `tests/test_meta.py` · nach A28 Paket 0**

- **T14 (A6-2) Body byte-identisch:** A6-T2 (`meta.setzen(owner="mensch")`) zusätzlich mit Body-SHA256 vor/nach; Frontmatter-Keys unverändert. *Bestandstest (Invariante gilt bereits); Rot-Beleg optional über Mutation (`set_meta` schreibt Body um) — nicht committen.*

**B7 — A5-B4 Slug-Konsolidierung · Dateien: `definitions/app/slug.py` (neu), `neu_aufgabe.py`, `neu_welle.py`, `tests/test_neu_aufgabe.py`, `tests/test_neu_welle.py` · nach A29**

- **T15 (A5-B4) Verhaltensgleiche Extraktion:** Neue Matrix (Umlaute/ß/Akzente/Sonderzeichen/Leerzeichen/61+ Zeichen/leer) über `slug.slug_aus_titel` → identische Ergebnisse wie bisher für **beide** Aufrufer; `neu_aufgabe` wirft bei leerem Slug weiter `EingabeFehler`, `neu_welle` fällt weiter auf `welle` zurück; bestehende Tests grün. *Rot vor dem Fix (`import slug` schlägt fehl).*

**B8 — A14-5 `istDatei` konsolidieren · Dateien: `definitions/app/static/js/api.js`, `detail.js`, `features.js` · nach A29**
  - **Nachtrag A27-F1 (tester, 2026-11-15, PM eingeordnet):** Deep-Link `#/aufgaben` ohne vorherige Übersicht zeigt im Wellen-Filter nur „Alle"/„ohne Welle"/referenzierte Pfade statt aller Wellen (AK-8 im Sonderfall nicht wörtlich erfüllt; Ursache = dokumentierte Abweichung „Optionen aus geladenen Listen", die die A25-Request-Zusicherungen schützt). Lösung im B8-Takt: Wellen-Titel-Cache lazy über `GET /api/wellen` nachladen (erst bei erster Filter-Interaktion — die A25-Assertions prüfen nur die Requests der `ladeUebersicht`/`ladeAufgaben`-Aufrufe) **oder** bewusst dokumentierte Grenze belassen — Umsetzer entscheidet mit B8, Testfall ergänzen.
  - **Nachtrag A27-K2 (reviewer, 2026-11-15):** Options-Cache `bekannteWellen` wird nur bei `basis === "uebersicht"` erneuert — eine in der Sitzung neu angelegte Welle fehlt im Filter der Aufgabenliste. Gratis-Fix in `ermittleWellen` (auch für `basis === "wellen"` `bekannteWellen = wellenAusBestand(daten)`) — mit B8/`liste.js`-Takt.
  - **Nachtrag A27-K1 (reviewer, 2026-11-15, PM eingeordnet — NACH A28-P0 wegen `meta.py`/G13):** `meta.py:_wellen_pfad` gibt den Eingabe-String zurück statt des `unquote`-aufgelösten Pfads (`POST {"welle":"wellen/%77%31.md"}` → 200 mit kodiertem Pfad, Wellen-Join findet die Aufgabe nicht). Fix: `unquote(text) != text` → `EingabeFehler` oder aufgelösten Pfad zurückgeben. Mit B6-Takt (nach A28-P0).
  - **Nachtrag A30-R1 (reviewer, 2026-11-15):** Testlücke in `test_arbeitsstand.py` T5 — die Nicht-String-Fälle (`aktuell: 42|true|[]|{}`) laufen am Typ-Gate vorbei und decken `_text` nicht ab (Mutante `str(wert)` blieb grün, Laufzeitverhalten korrekt). Fix: T5 um `{"type": "Task", "aktuell": <nicht-string>}` ergänzen (parametrisierter Fall). Reiner Test-Zusatz — mit dem B4–B6-Takt (nach A28-P0) oder jederzeit einzeln.
  - **Nachtrag A32-H1/H2/H3/H6 (Bestätigungs-Review, 2026-11-15, PM eingeordnet — `start.sh`-Polish, jederzeit lauffähig):** H1 Doppelmeldung am belegten Port (Schritt 5 + 7) → bei `PORT_BELEGT=1` in `starte_server` ohne Textzeile `return 0`; H2 `--neu` bei belegtem Port endet still mit Exit 0 → Meldung „Server zuerst beenden, dann `--neu`" (oder rc ≠ 0); H3 `warnung_reset_ziel` vergleicht Strings statt normalisierte Pfade (Trailing-Slash → Fehlwarnung) → `cd … && pwd -P`; H6 K7-Test ohne explizite Assertion „kein Serverstart" → Assertion ergänzen. H4 (Commit-Zuordnung A26-Doku) und H5 (K5-Randfälle sind Regressionsklammern, keine Rot-Probe) sind Vermerke ohne Code-Bedarf.

- **T16 (A14-5) Ein Prädikat:** `api.js` exportiert `istDateiAntwort(daten)` (gleiche Semantik: Objekt, kein Array, `markdown` ist String); `detail.js`/`features.js` importieren es, keine eigene `function istDatei` mehr; bestehende Detail-/Feature-Tests grün; Meldungen bleiben kontextspezifisch (bewusste Abgrenzung, im Ergebnis begründet). *Rot vor dem Fix (Duplikate vorhanden).*

**B9 — Doku-Sammelbatch (A4-2, A6-1, A9-K3, A9-K4, A16-1, A24-H2) · Dateien: `wissen/projekt/phasen.md`, `technische-spec.md`, `planung.md`, `wissen/aufgaben/a24-neues-projekt.md` · nach A29**

- **T17 (A4-2)** `phasen.md` Aufgaben-Format enthält `welle` (optional, Pfad `wellen/<x>.md`) und verweist auf `freigabe`/`aktuell`; `technische-spec.md` Read-Modell nennt `welle`. *Dokumentierte Prüfung: gezielte Suche/Grep, Review.*
- **T18 (A9-K3)** Spec ergänzt: bekannte, aber für die App verbotene Workflow-Werte → **403**; unbekannte/ungültige Werte und Payload-Fehler → **400**. *Dokumentierte Prüfung.*
- **T19 (A9-K4)** Spec/Entscheidungslog ergänzt R8: atomares Schreiben, kein Locking im MVP, TOCTOU (KI + App) bekanntes Risiko. *Dokumentierte Prüfung.*
- **T20 (A16-1)** R11 in `planung.md` beschreibt das tatsächliche Verhalten (Default 5000, **kein** automatischer Ausweichport, klare Meldung bei Belegung) — oder der Ausweichport wird als eigener Post-MVP-Punkt vorgemerkt; Code unverändert. *Dokumentierte Prüfung.*
- **T21 (A24-H2)** A24-Ergebnis enthält eine a–e-Tabelle mit Testnamen oder den Vermerk „a–e im Review-Text, nicht im Bundle rekonstruierbar"; keine erfundene Zuordnung. *Dokumentierte Prüfung.*
- **T22 (A6-1)** A24/A6-Vermerk: H1/H5/H7-Belege im Doku-Eintrag vom 2026-11-14; H-Definitionen fehlen im Bundle → offener Doku-Punkt an den PM (kein Code). *Dokumentierte Prüfung.*

# Kontext

- **Auftrag/Stand:** Sammel-Aufgabe vom PM (2026-11-15). Geprüft gegen den Arbeitsbaum nach A26 (`d9eb05c`, Werkzeug-Spiegel) und A27 (`a4906d7`); A28–A32 laufen bzw. sind geplant. Die Befunde sind **unkritisch** — kein Review-Blocker; A24-K2 ist die einzige sicherheitsrelevante Lücke (Symlink auf automatischem Backup-Namen).
- **Batches, Dateien und Reihenfolge (je ein Commit):**
  - **B1 „A24-Werkzeug-Härtung"** (K1/K2/K3/H1/H3): `definitions/tools/neues_projekt.py`, `definitions/tools/tests/test_neues_projekt.py`, danach Verteilung → `tools/…`. **Sofort parallel zu A28/A29 möglich** (keine Schnittmenge mit App- oder Wissensdateien; `setup.sh` wird nur aufgerufen, nicht geändert). **Aufwand 2–3 h.**
  - **B2 „A23-Fixture-Rename"** (A23-H1): `definitions/app/tests/test_projekt.py`, `test_features.py`. **Sofort parallel** (A28/A29 fassen diese Dateien nicht an; A23 ist in Doku). **0,25 h.**
  - **B3 „Wellen-`description`"** (A5-B3): `neu_welle.py`, `test_neu_welle.py`. **Sofort parallel**, muss aber **vor A29** committed sein (A29 ergänzt `freigabe: false` in derselben Datei). **0,5 h.**
  - **B4 „Wellen-Linktext"** (A13-3): `neu_aufgabe.py`, `test_neu_aufgabe.py`. **Erst nach A28 Paket 0** (dort wird `freigabe: false` in `neu_aufgabe.py` ergänzt). **0,5 h.**
  - **B5 „Startfehler ohne Pfad"** (A7-2): `server.py`, `test_server.py`. **Erst nach A28 Paket 0** (`server.py` erhält `/api/freigabe`). **0,5 h.**
  - **B6 „A6-T2 Body-Hash"** (A6-2): `tests/test_meta.py`. **Erst nach A28 Paket 0** (dort kommt der `freigabe`-Guard-Test hinzu). **0,25 h.**
  - **B7 „Slug-Konsolidierung"** (A5-B4): `slug.py` (neu), `neu_aufgabe.py`, `neu_welle.py`, beide Testdateien. **Erst nach A29** (beide Aufrufer sind dann frei). **2–3 h.**
  - **B8 „`istDatei` konsolidieren"** (A14-5): `api.js`, `detail.js`, `features.js`. **Erst nach A29** (UI-Kette endet dort). **1 h.**
  - **B9 „Doku-Sammel"** (A4-2, A6-1, A9-K3, A9-K4, A16-1, A24-H2): `phasen.md`, `technische-spec.md`, `planung.md`, `a24-neues-projekt.md`. **Erst nach A29** (A28/A29/A30/A31 ändern `phasen.md`/Spec in ihren Doku-Paketen); alternativ übernimmt der PM den Batch nach dem letzten Doku-Paket. **1,5 h.**
- **Eigene Aufgaben (Vorschlag, nicht Teil von A33):**
  - **A35 „Status-Mapping server-seitig (A12-1)"** — `overview.details` liefert `ui_status`/`hinweis`/`owner_default` aus `status.py` (wie A30s `arbeitsstatus`), `detail.js` nutzt sie und der JS-Spiegel `TASK_STATUS_UI`/`OWNER_DEFAULTS` entfällt; Tests: Mapping-Matrix über die API + UI-Regression. **Abhängigkeit: nach A29** (`detail.js`, `overview.py`). Aufwand 4–6 h.
  - **A36 „`schreibgeschuetzt`-Signal (A12-Schreib-UI-Grenze)"** — API markiert reservierte Dateien (`/api/file`/Liste), `detail.js` blendet Schreib-UI aus; Server-403 bleibt zweite Barriere. **Nach A35.** 3–4 h.
  - **A37 „DOM-Harness-Konsolidierung (A14-6)"** — `tests/dom_helfer.py` (aus A30) als einzige Quelle; die vier Altkopien + A28/A29/A30/A31-Testdateien umstellen; kein Verhaltenswechsel. **Nach A29** (alle Testdateien stabil). 5–8 h.
  - **A38 „Log-Anker (A14-9)"** — `#/detail/entscheidungen/log.md#<anker>` + IDs im Markdown-Renderer; `projekt.js`/`detail.js`. **Nach A29.** 2–3 h.
  - Nummern A35–A38 sind vom PM bestätigt und als Aufgaben angelegt (A34 ist vergeben: „Unter-Aufgaben erstellen"); Umsetzung nach A29/A33.
- **Parallelitäts-Matrix (Kurz):** B1/B2/B3 = **frei** (parallel zu A28 und A29, sofern B3 vor A29 committed ist); B4/B5/B6 = **nach A28-P0**; B7/B8/B9 = **nach A29**. A28-Dateien: `freigabe.py`, `meta.py`, `server.py`, `overview.py`, `neu_aufgabe.py`, `liste.js`, `detail.js`, `test_meta.py`, `test_api_schreiben.py`, `test_neu_aufgabe.py`, `test_freigabe_ui.py`, `test_neue_aufgabe_signal.py`, `AGENTS.md`, `phasen.md`, `technische-spec.md`. A29 zusätzlich: `neu_welle.py`, `test_neu_welle.py`, `test_freigabe_ui.py`, `phasen.md`, `technische-spec.md`.
- **Werkzeug-Spiegel (A26-Regel):** Quelle ist `definitions/tools/neues_projekt.py`; `tools/neues_projekt.py` ist die verteilte Kopie (heute byte-identisch). Nach jeder Änderung: Tests in `definitions/tools/tests/` **und** `tools/tests/` grün, `diff` leer; `bash definitions/setup.sh` nur ausführen, wenn er den Spiegel aktualisiert (sonst `cp` mit anschließendem `test_verteilung.py`).
- **Risiken/Grenzen:** (a) B1-K2 ist die einzige sicherheitsrelevante Änderung — Rest-TOCTOU zwischen `lexists` und `tarfile.open` bleibt als R8-Risiko dokumentiert (optional `O_EXCL`-Öffnen; nicht zwingend); (b) B7 kann für exotische Zeichen (z. B. `ø`) Slug-Ergebnisse leicht ändern — Matrix-Test und bewusste Entscheidung für die `neu_aufgabe`-Variante; (c) B8 lässt kontextspezifische Meldungen absichtlich stehen (kein Zusammenlegen); (d) B9 ist Doku und damit nicht pytest-belegbar — Review-Prüfschritte T17–T22; (e) A14-9/A12-1/A14-6 sind bewusst **nicht** im Takt (eigene Aufgaben), damit A33 klein und parallelisierbar bleibt; (f) A5-B2 ist entschieden (Fallback bleibt robust, PM 2026-11-15) — Dokumentation der Asymmetrie in B9.
- **PM-Entscheidungen (2026-11-15):**
  1. **B9 durch den `coder`** (A33 hat einen Commit je Batch; PM hakt danach `features.md`/Log ab) — bestätigt.
  2. **A35–A38 sind angelegt und gepusht** (A34 war zwischenzeitlich vergeben: „Unter-Aufgaben"); Umsetzung nach A29/A33.
  3. **A5-B2 entfällt als Code-Punkt:** `FALLBACK_KUERZEL` bleibt bewusst robust (PM-Entscheidung aus dem A5-Ergebnisprotokoll); die Asymmetrie zu A4 (`EingabeFehler`) wird in B9 als bewusste Entscheidung dokumentiert.
  4. **B1 nur `lexists` + R8-Vermerk** (Standard bestätigt); `O_EXCL`-Härtung bleibt Post-MVP.
  5. **B4/B5/B6 warten auf A28-P0, B1–B3 laufen** (Standard bestätigt). PM-Zusatz: **B1 startet zusätzlich erst nach Rückkehr von A26-Review/-Testphase** (die lesen genau die Werkzeug-Dateien — Moving-Target-Schutz).

# Betroffene Dateien

- `definitions/tools/neues_projekt.py` — `_backup_name`/`_pruefe_backup_ziel`/`backup_erstellen` mit `os.path.lexists` (baumelnde Symlinks), Rollback-Meldung mit Wiederherstellungsschritt (B1; K2/K3/H3).
- `definitions/tools/tests/test_neues_projekt.py` — T1–T6 (direkte Barriere, Symlink-Fälle, deterministische Namenswahl, Eigenschafts-Test Meldung) (B1).
- `tools/neues_projekt.py` **und** `tools/tests/test_neues_projekt.py` — verteilter Spiegel, nach B1 byte-identisch (A26-Regel).
- `definitions/app/tests/test_projekt.py` **und** `definitions/app/tests/test_features.py` — Fixture `test_bundle` → `szenarien_bundle` umbenennen, `app_server`-Verwendung anpassen (B2).
- `definitions/app/neu_welle.py` — `description` im Frontmatter aus der ersten Ziel-Zeile (max. 160, `…`) (B3; A5-B3).
- `definitions/app/tests/test_neu_welle.py` — T8/T9 (Feld, Kürzung, Randfall) (B3).
- `definitions/app/neu_aufgabe.py` — `_verweis_zeile` löst den Wellen-Titel tolerant auf (Fallback Dateistamm) (B4; A13-3).
- `definitions/app/tests/test_neu_aufgabe.py` — T10/T11 (Titel-Linktext, Fallback), nach A28-P0 (B4).
- `definitions/app/server.py` — `StartFehler` ohne absoluten Pfad (B5; A7-2).
- `definitions/app/tests/test_server.py` — T12/T13 (kein Pfad-Leak, Verhalten unverändert), nach A28-P0 (B5).
- `definitions/app/tests/test_meta.py` — T14 (A6-T2 Body-Hash), nach A28-P0 (B6).
- `definitions/app/slug.py` (**neu**) — gemeinsame Slug-Funktion (`slug_aus_titel`) (B7; A5-B4).
- `definitions/app/neu_aufgabe.py` **und** `definitions/app/neu_welle.py` — auf `slug.py` umstellen, öffentliche Namen/Semantik erhalten (B7, nach A29).
- `definitions/app/tests/test_neu_aufgabe.py` **und** `test_neu_welle.py` — T15 (Verhaltensgleichheit) (B7).
- `definitions/app/static/js/api.js` — Export `istDateiAntwort` (B8; A14-5).
- `definitions/app/static/js/detail.js` **und** `features.js` — Import statt lokaler `istDatei`; Meldungen bleiben kontextspezifisch (B8, nach A29).
- `wissen/projekt/phasen.md` — `welle` im Aufgaben-Format (B9; A4-2), erst nach A29 (A28/A30 ergänzen dort `freigabe`/`aktuell`).
- `wissen/projekt/technische-spec.md` — `welle` im Read-Modell (A4-2), 403-Semantik (A9-K3), R8/TOCTOU (A9-K4) (B9).
- `wissen/projekt/planung.md` — R11-Wortlaut an das Verhalten angleichen (A16-1) (B9).
- `wissen/aufgaben/a24-neues-projekt.md` — a–e-Zuordnung/„nicht rekonstruierbar" (A24-H2) (B9).
- **Nicht geändert:** `definitions/app/static/index.html`, `style.css`, `app.js`, `meta.py`, `okf_bundle.py`, `status.py`, `overview.py`, `neu_aufgabe.py` (außer B4/B7), `features.js` (außer B8), `liste.js`, `detail.js` (außer B8), `wissen/features.md`, `wissen/log.md`, `wissen/aufgaben/index.md` (PM/`documenter`).

# Ergebnisse

Noch keine Einträge. Der `documenter` pflegt hier je Übergabe Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege.

---
type: Task
title: "A5: Welle anlegen neu_welle.py"
description: Neue Wellen-Datei in wellen/ mit type Welle, validiertem Status/owner, Ziel-Abschnitt und leerer Aufgaben-Linkliste anlegen.
task_status: in Doku
phase: 7 Dokumentation
priority: hoch
assigned_to: coder
user_story: /projekt/user-stories/us-4.md
owner: ai
---

# Ziel

`definitions/app/neu_welle.py` implementiert `anlegen({titel, ziel, status, owner})` → `wellen/<kuerzel>.md` mit `type: Welle`, `title`, `status` (nur die 6 UI-Werte), `owner` und dem Body `# Ziel` + `# Aufgaben` (Linkliste, leer startend). Der Ordner `wellen/` wird bei Erstanlage erzeugt.

# Akzeptanzkriterien

- Der Ordner `wellen/` wird bei Erstanlage angelegt.
- Status und owner werden validiert; bei Verstoß `EingabeFehler` ohne Datei.
- Bei Namenskollision entsteht ein Suffix, die bestehende Datei bleibt unverändert.
- Die neue Welle erscheint in `GET /api/wellen` (Integrationstest).

# Testfälle (TDD)

- **T1 Happy Path:** `wellen/<kuerzel>.md` existiert.
- **T2 Frontmatter:** `type: Welle`, `title`, `status`, `owner`.
- **T3 Ordner-Erstanlage:** Ordner und Datei entstehen.
- **T4 Ungültiger Status:** `EingabeFehler`, keine Datei.
- **T5 Ungültiger owner:** `EingabeFehler`.
- **T6 Leerer Titel:** `EingabeFehler`.
- **T6b Leeres Ziel:** `ziel` ∈ {"", "   ", `None`, 42} → `EingabeFehler`, Dateianzahl unverändert (`ziel` ist Pflichtfeld, konsistent zu A4).
- **T7 Kollision:** `…-2.md`, erste Datei unverändert.
- **T8 Body:** `# Ziel` und `# Aufgaben` vorhanden.
- **T9 Kürzel:** `Wave 1 — MVP` → `wave-1-mvp.md`.

# Kontext

- **Abhängigkeiten:** A1 — **parallel zu A4**.
- **Konfliktgruppe G5:** `neu_welle.py` exklusiv.
- **Nachfolger:** A9 (`POST /api/welle`) und A13 (Formular) nutzen dieses Modul.
- **Entscheidungen:** R2 (Slug-Konvention analog Aufgaben), R5 (Wellen-Struktur: `wissen/wellen/index.md` existiert bereits und ist im Root-Index verlinkt).
- **Verweise:** Struktur neuer Punkte in [Technischer Spec](/projekt/technische-spec.md); Statuswerte in [Phasenmodell](/projekt/phasen.md).

# Betroffene Dateien

- `definitions/app/neu_welle.py`
- `definitions/app/tests/test_neu_welle.py`

# Ergebnisse

Je Eintrag Datum, Rolle (coder/reviewer/tester), Ergebnis, Befunde, offene Punkte und Belege. Neueste Einträge unten.

## 2026-11-14 — coder (Zwischenstand zum Halt, inkl. Sammel-Nachbesserung)

- **Ergebnis:** Umsetzung abgeschlossen (48 Tests); `ziel` ist Pflicht (PM-Entscheidung, siehe Testfall T6b). Sammel-Nachbesserung „zentrale Exceptions": Import-Umstellung auf den zentralen `EingabeFehler` aus `okf_bundle`, Geschwister-Import in `neu_welle.py` aufgelöst. (Quelle: Übergabeprotokoll, Abschnitte „Aufgabenstatus" und „Session-Rückmeldungen zum Halt".)
- **Belege:** 102 Tests im Sammel-Lauf; Gesamtsuite 549 grün (Endstand zum Halt).
- **Offene Punkte:** Review, Testphase, Doku.

## 2026-11-14 — tester (Gebündelte Testphase)

- **Ergebnis:** **Testphase BESTANDEN** (DoD-Beleg): 49 Tests grün, keine offenen Testbefunde. Gesamtlauf: 549 passed (Start = Ende, kein Zuwachs), 0 rot, 0 geskippt.
- **Offene Punkte:** Review ausstehend.

## 2026-11-14 — reviewer (Review-Runde 2)

- **Ergebnis:** **Freigegeben** — keine kritischen Befunde; Sicherheit sauber. Die Nachbesserung [B1] wurde umgesetzt (Commit `d651ec6`: reservierte Wellen-Kürzel erhalten Suffix statt 403, 6 Regressionstests, 55 grün); Bestätigungs-Review ausstehend.
- **Befunde:** [B1] wesentlich (behoben, Commit `d651ec6`): `_freier_pfad` ohne Reserviert-Skip → 403 statt `-2`-Suffix. Klein offen: [B2] `FALLBACK_KUERZEL` vs. `EingabeFehler` inkonsistent zu A4; [B3] `description`-Feld fehlt bei Wellen; [B4] Slug-Logik dupliziert zu `neu_aufgabe`.
- **Offene Punkte:** B2/B3/B4 (Aufräum-Takt, siehe [features.md](/features.md)); Review-Bestätigung; Doku.

## 2026-11-14 — reviewer (Bestätigungs-Review, Runde 2)

- **Ergebnis:** **Review-frei** — [B1] (reservierte Kürzel erhalten Suffix statt 403, Commit `d651ec6`) ist behoben und durch echte, nicht abgeschwächte Regressionstests belegt.
- **Befunde:** **PM-Entscheidung A5-2:** Das `FALLBACK_KUERZEL`-Verhalten bleibt bewusst bestehen — es ist ein robuster Fallback für die Kürzelbildung; die Abweichung zu A4 (`EingabeFehler`) ist damit begründet und kein Fehler. (Wie beauftragt im Ergebnisprotokoll dokumentiert.)
- **Offene Punkte:** [B3] `description`-Feld bei Wellen, [B4] Slug-Logik-Duplikat (Aufräum-Takt); Doku/Abschluss.

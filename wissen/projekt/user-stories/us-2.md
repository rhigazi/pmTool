---
type: User Story
title: US-2: Nachträge mit sichtbarem Mensch-Marker einfügen
description: Aus der App heraus lassen sich Nachträge in eine beliebige OKF-Datei einfügen, die eindeutig als Mensch-Erkennbar sind.
story_status: offen
priority: hoch
---

# Story
Als Projektleitung möchte ich in eine beliebige Datei des Projekts einen Nachtrag einfügen, der eindeutig als von mir erstellt erkennbar ist, damit die KI genau weiß, was ich anders haben möchte und keine Information verloren geht.

# Akzeptanzkriterien
- In der Detailansicht jeder OKF-Datei gibt es ein Eingabefeld „Nachtrag einfügen“.
- Der Nachtrag wird am Dateiende in einem eigenen Abschnitt `# Nachträge` angefügt (Abschnitt wird angelegt, falls nicht vorhanden) im Format:
  `> **Nachtrag (Mensch, YYYY-MM-DD):** <Text>`
- Bestehender Dateiinhalt bleibt unverändert erhalten (Anfügen, nie Überschreiben); mehrere Nachträge werden untereinander gesammelt.
- Reservierte Dateien (`index.md`, `features.md`, `log.md`) können **nicht** Ziel von Nachträgen sein — sie werden ausschließlich von der KI gepflegt (Guard in `okf_bundle`).
- Der Marker macht den Ursprung (Mensch) und das Datum für Leser ohne App offensichtlich — auch im reinen Markdown-Text.
- Der KI-Workflow bleibt unverändert: `index.md`, `features.md` und `log.md` werden durch das Einfügen von Nachträgen **nicht** automatisch mitgepflegt (Pflicht der KI-Rollen, siehe Technische Spec).
- Eine erfolgreiche Eingabe zeigt den gespeicherten Stand unmittelbar in der Detailansicht.

# Technische Hinweise
Schreibrechte der App siehe Technische Spec (Abschnitt Schreibrechte). OKF-Konformität (Frontmatter, Links, reservierte Dateien) muss erhalten bleiben.

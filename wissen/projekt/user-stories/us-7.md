---
type: User Story
title: US-7: OKF-Konformität und Schutz der Wissensdatenbank
description: Die App beschädigt weder Struktur noch Inhalte des OKF-Bundles; reservierte Dateien und Frontmatter bleiben intakt.
story_status: offen
priority: hoch
---

# Story
Als Projektleitung möchte ich, dass die Wissensdatenbank durch die App nie beschädigt wird, damit KI und andere OKF-Consumer die Dateien weiterhin korrekt lesen und der Projektfortschritt nicht verloren geht.

# Akzeptanzkriterien
- Schreibvorgänge erhalten bestehendes YAML-Frontmatter (inkl. `type`) und den bestehenden Text; nur erlaubte Operationen (Nachtrag anfügen, neue Datei anlegen, `owner`/definierte Status setzen) werden ausgeführt.
- Reservierte Dateien (`index.md`, `log.md`, `features.md`) werden durch die App nicht automatisch überschrieben; Log-Einträge der App (falls vorgesehen) werden nur angehängt, nie ersetzt.
- Abgelehnte Operationen (ungültiger Pfad, leere Eingabe, fehlendes Frontmatter, unerlaubtes Ziel) liefern einen klaren Fehler an die Oberfläche, ohne dass Dateien beschädigt oder unvollständig angelegt werden.
- Pfade werden gegen Ausbrüche aus dem Bundle-Root abgesichert (kein Zugriff außerhalb von `/content/pmTool/wissen/`).
- Unit-Tests (pytest) decken: Nachtrag-Anfügen, Anlegen von Aufgabe/Welle, `owner`-Update, Mapping-Status, Pfad-Abweisung, Frontmatter-Erhalt.
- Ein UI-Szenario über den Moli-Browser prüft die Kernpfade: Übersicht laden → Nachtrag einfügen → sichtbarer Marker → Status/owner in der Liste korrekt.

# Technische Hinweise
Test-First: Testfälle werden vor der Implementierung festgelegt (Red-Green-Refactor, siehe TDD-Regeln im Phasenmodell). Pfad-/Schema-Validierung beschrieben in der Technischen Spec.

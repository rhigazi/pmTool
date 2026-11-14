---
type: User Story
title: US-6: App aus Colab starten
description: Eine Colab-Zelle startet den lokalen Server und stellt die App im Browser-Fenster bereit — ohne externe Tunnel-Dienste.
story_status: offen
priority: hoch
---

# Story
Als Projektleitung möchte ich die App mit einer einzigen Colab-Zelle starten und direkt im Browser nutzen, damit die Umsetzung vollständig in Colab erfolgt und kein externer Dienst (Tunnel/Token) nötig ist.

# Akzeptanzkriterien
- Eine Colab-Zelle startet den Server im Hintergrund und öffnet die App über die eingebaute Colab-Port-Freigabe (`google.colab.output.serve_kernel_port_as_window` bzw. `_as_iframe`) im Browser.
- Die App greift auf die Wissensdatenbank unter `/content/pmTool/wissen/` zu (kein Kopieren/Kein Zweitbestand).
- Ein Neustart der Zelle lässt die Daten unangetastet (Dateien bleiben erhalten); ein zweiter Start parallel zum laufenden Server wird sauber behandelt (Port-Handling/Klare Meldung).
- Fehlende Abhängigkeiten werden in der Zelle automatisch installiert (`pip install` der benötigten Pakete).
- Der OpenCode-CLI-Chat arbeitet unabhängig davon weiter auf denselben Dateien.
- Fällt die Port-Freigabe aus (Browser-/Colab-Einschränkung), zeigt die Zelle eine verständliche Meldung mit Alternative (z. B. URL-/Port-Hinweis).

# Technische Hinweise
Technik-Entscheidung: schlanker Python-Server (Flask) ohne pyngrok/ngrok, da Colab den Port nativ im Browser freigeben kann. Details und Start-Befehle siehe Technische Spec.

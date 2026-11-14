# User Stories

Vom Projektmanager aus den Anforderungen abgeleitet. Je Story eine Datei (`type: User Story`), Format siehe [/projekt/phasen.md](/projekt/phasen.md). Aufgaben verweisen über das Feld `user_story` auf ihre Story; der `planner` plant ausschließlich aus User Stories und [Technischer Spec](/projekt/technische-spec.md).

# Offene User Stories

* [US-1: Tracker-Übersicht mit Status und Zuständigkeit](us-1.md) - Listenansicht über fünf Navigationspunkte: Titel, Status (6 UI-Werte), owner, zuletzt geändert; Filter; offene Rückfragen sichtbar
* [US-2: Nachträge mit sichtbarem Mensch-Marker einfügen](us-2.md) - Anfügen als `> **Nachtrag (Mensch, YYYY-MM-DD):** …` in beliebige OKF-Dateien, ohne Inhalte zu überschreiben
* [US-3: Neue Aufgabe anlegen und an die KI übergeben](us-3.md) - Formular → `wissen/aufgaben/<id>.md` im Phasen-Format, `owner: ai`, sofort in der Liste sichtbar
* [US-4: Wellen anlegen und mit Aufgaben verknüpfen](us-4.md) - `wissen/wellen/<kuerzel>.md` mit `type: Welle`, gemeinsames Statusmodell, Verlinkung zu Aufgaben
* [US-5: Status und owner verwalten (Klärung und Abnahme)](us-5.md) - owner umschaltbar; Mensch darf `Klarung`/`Geschlossen` setzen; Pipeline-Status bleibt KI-Sache
* [US-6: App aus Colab starten](us-6.md) - eine Zelle startet Flask-Server + eingebaute Colab-Port-Freigabe, ohne pyngrok; Daten unter `/content/pmTool/wissen/`
* [US-7: OKF-Konformität und Schutz der Wissensdatenbank](us-7.md) - Frontmatter/Struktur bleiben intakt, Pfadschutz, Reserve-Dateien geschützt, pytest + Moli-Szenario

# Umgesetzte User Stories

*Noch keine.*

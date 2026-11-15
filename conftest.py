"""Root-Testkonfiguration des Entwicklungs-Repos (Aufgabe A26).

Quelle der Werkzeuge ist ``definitions/tools/`` (Single Source of Truth);
``tools/`` ist die von ``definitions/setup.sh`` installierte Kopie. Beide Bäume
enthalten dieselben Testdateien (``test_telegram_send.py``,
``test_neues_projekt.py``, ``test_verteilung.py``). Würde die Root-Suite beide
Bäume kollektieren, bräche pytest wegen doppelter Modul-Basisnamen ab
("import file mismatch" — jedes Testmodul wird über seinen Basisnamen importiert).

Deshalb kollektiert die Root-Suite nur die Quelle ``definitions/tools/tests/``;
der installierte Spiegel ``tools/tests/`` wird ignoriert. Jede Testdatei läuft
damit genau einmal, und es werden keine Tests still übersprungen (die Drift-
Prüfung ``definitions/tools/tests/test_verteilung.py`` wacht darüber, dass
Spiegel und Quelle inhaltsgleich bleiben).

Explizit genannte Pfade (z. B. ``pytest tools/tests/`` in
``definitions/verify.sh``) kollektiert pytest weiterhin — ``collect_ignore``
greift nur beim Rekursieren, nicht bei direkt übergebenen Pfaden. Ein frisch
installiertes Zielprojekt hat diese Datei nicht; dort ist ``tools/tests/``
ohne Konflikt der einzige Testbaum.

Quelle und Spiegel gleichzeitig explizit zu übergeben (``pytest definitions/tools/tests
tools/tests``) bleibt ein Fehler — Root-Suite und ``verify.sh`` tun das nicht.
"""

collect_ignore = ["tools/tests"]

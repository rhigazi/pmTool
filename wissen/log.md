# Update-Log Wissensdatenbank

<!-- Einträge neueste zuerst; Format: ## YYYY-MM-DD (ISO-Datum), darunter Stichpunkte mit **Update**/**Creation**/**Deprecation** -->

## 2026-11-14

* **Update** Projekt ins GitHub-Repository `/content/pmTool` umgezogen (`definitions/`, `wissen/`, `docs/prd.md`, Projekt-Wurzel via `setup.sh`); Pfade `/content/wissen` → `/content/pmTool/wissen` in Spec, User Stories, Planung, Aufgaben und PRD angepasst; `.gitignore` angelegt; Entscheidungslog-Eintrag ergänzt.
* **Creation** 17 Aufgaben A1–A17 aus dem freigegebenen TDD-Plan als OKF-Aufgaben-Dateien angelegt (`wissen/aufgaben/`), Index unter „Offene Aufgaben“ ergänzt — Phase 3 Aufgabenanlage.
* **Creation** User Stories US-1 bis US-7 angelegt (`wissen/projekt/user-stories/`), Index aktualisiert — Konzeptionsphase des Projekts „OKF Projekt-Manager (SPA)“.
* **Update** Technische Spec ausformuliert (`wissen/projekt/technische-spec.md`): Architektur (Flask + Colab-Port-Freigabe), Frontmatter-Erweiterung `owner`/`status`, Mapping `task_status` → UI-Status, Schreibrechte-Matrix, JSON-API, Start-/Testbefehle.
* **Update** Entscheidungslog um fünf Einträge erweitert (App als Tracker/KI-Pflege, UI-Status als Sicht, owner-Feld, Colab-Start ohne Tunnel, MVP-Umfang + Navigation).
* **Creation** PRD für OKF-Projekt-Manager-SPA angelegt (`prd.md`): Ziel, Statusmodell, Zuständigkeit, Nachträge, Wellen, Colab-Umsetzung, MVP-Scope.
* **Creation** Entscheidungslog mit sieben Konzeptentscheidungen befüllt (`wissen/entscheidungen/log.md`).

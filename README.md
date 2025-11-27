# ki_fallstudie

KI-Nutzung:
- Ideenfindung
- Hilfe beim Aufsetzen des Projekts (Einrichtung venv, Ordnerstruktur)
- Inspiration für Klassenstruktur
- Umgang mit pathlib
- Unterstützung bei Fehlerbehandlung

# Project Management Tool (CLI)

Python-basiertes Kommandozeilen-Tool zur Verwaltung von Projekten, Aufgaben und Teammitgliedern (Lokaler Datenhaltung via JSON).

## Features

Das Tool deckt den kompletten Workflow kleiner Teams ab:

* **Projektverwaltung:** Anlegen von Projekten mit Start-, Fälligkeitsdatum und Prioritäten.
* **Team-Management:** Verwalten von Mitarbeitern inkl. Rollen und Eintrittsdatum.
* **Aufgaben-Tracking:** Erstellen von Tasks mit Prioritäten (Niedrig, Mittel, Hoch).
* **Zuweisungen:** Flexible Zuordnung:
    * Mitarbeiter -> Projekt
    * Aufgabe -> Mitarbeiter (innerhalb eines Projekts)
* **Filter & Suche:** Filtern von Projekten nach Priorität, Startdatum oder Fälligkeit.

## Installation & Setup

Es sind keine externen Bibliotheken notwendig, nur eine aktuelle Python-Version (3.x).

1.  **Repository klonen oder herunterladen.**
2.  **Daten-Struktur prüfen:**
    Das Skript erwartet einen `data`-Ordner im Hauptverzeichnis. Falls dieser fehlt, leg ihn bitte an:
    ```bash
    mkdir data
    ```
    Hinweis: Die JSON-Dateien (`projekte.json`, etc.) werden beim ersten Start automatisch erstellt, falls sie nicht existieren.

3.  **Starten:**
    Führe das Skript über die `main.py` aus:
    ```bash
    python main.py
    ```
## Nutzung
 erst wenn cli.py final fertig ist

## Projektstruktur

* `main.py` - Einstiegspunkt.
* `cli.py` - Behandelt das Menü und User-Input.
* `src/`
    * `dateiverwaltung.py` - Lese-/Schreiboperationen (JSON).
    * `item.py` - Basisklasse für Projekte und Aufgaben.
    * `projekt.py` - Hauptlogik für Projekt-Verknüpfungen.
    * `filter.py` - Logik für die Sortierfunktionen.

## Roadmap / Bekannte To-Dos

* Funktion zum Löschen von Einträgen hinzufügen.
* Status für Aufgaben einführen (z. B. "In Bearbeitung", "Erledigt").
* Datenintegrität sicherstellen (z. B. keine doppelten Einträge).

---
*Erstellt für die Übungsaufgabe KI Fallstudie 2 (Gruppe).*
*AI: Formatierung von der Projektstruktur und die 'bash-Funktion' im README.
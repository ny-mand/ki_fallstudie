# ki_fallstudie

KI-Nutzung:
In diesem Projekt wurde Künstliche Intelligenz (z.B. ChatGPT/GitHub Copilot) als **Navigator** und Ideengeber eingesetzt.

**Konkrete Nutzungsbereiche:**
* **Ideenfindung:** Brainstorming zu Features und Aufbau.
* **Setup:** Hilfe beim Aufsetzen des Projekts (Einrichtung venv, Ordnerstruktur).
* **Architektur:** Inspiration für die Klassenstruktur (Basisklasse `Item`).
* **Implementation:** Umgang mit Modulen wie `pathlib` und `json`.
* **Qualitätssicherung:** Unterstützung bei Fehlerbehandlung (Exception Handling).
* **Refactoring:** Automatische Neuformatierung und Vervollständigung von repetitivem Code (Copilot).

# Project Management Tool (CLI)

Python-basiertes Kommandozeilen-Tool zur Verwaltung von Projekten, Aufgaben und Teammitgliedern (Lokaler Datenhaltung via JSON).

## Features

Das Tool deckt den kompletten Workflow kleiner Teams ab:

* **Projektverwaltung:** Anlegen von Projekten mit Startdatum, Fälligkeitsdatum und Prioritäten.
* **Team-Management:** Verwalten von Mitarbeitern inkl. Berufsbezeichnung und Eintrittsdatum.
* **Aufgaben-Tracking:** Erstellen von Tasks mit Prioritäten (Niedrig, Mittel, Hoch).
* **Zuweisungen (Many-to-Many):** Flexible Zuordnung:
    * Mitarbeiter ↔ Projekt
    * Aufgabe ↔ Mitarbeiter (innerhalb eines Projekts)
* **Filter & Suche:** Filtern von Projekten nach Priorität, Startdatum oder Fälligkeit.
* **Löschfunktionen:** Entfernen von Projekten, Aufgaben oder Teammitgliedern.

## Installation & Setup

Es sind keine externen Bibliotheken notwendig, nur eine aktuelle Python-Version (3.x).

1.  **Repository klonen oder herunterladen.**
2.  **Daten-Struktur prüfen:**
    Es sind **keine externen Bibliotheken** notwendig. Das Projekt nutzt nur Python-Standardbibliotheken (wie `json`, `pathlib`, `datetime`).

1.  **Repository klonen oder herunterladen.**
2.  **Ordnerstruktur prüfen:**
    Das Skript erwartet einen `data`-Ordner im Hauptverzeichnis. Falls dieser fehlt, lege ihn bitte an:
    ```bash
    mkdir data
    ```
    *(Hinweis: Die JSON-Dateien wie `projekte.json` werden beim ersten Programmstart automatisch generiert, falls sie nicht existieren.)*

3.  **Starten:**
    Führe das Skript über die Kommandozeile aus:
    ```bash
    python main.py
    ```
    
Achtung: Achte darauf, dass in deinen Daten keine Umlaute (ä, ö, ü) verwendet werden, da dies zu Problemen bei der JSON-Verarbeitung führen kann.
## Nutzung
Hier ein typischer Ablauf, um das Tool kennenzulernen:

1.  **Projekt anlegen:**
    * Wähle im Menü `Neu erstellen (4)` -> `Projekt erstellen (1)`.
    * Gib Name (z.B. "Website Relaunch"), Datum und Priorität ein.
2.  **Team aufbauen:**
    * Wähle `Neu erstellen (4)` -> `Neues Teammitglied (2)`.
    * Erstelle einen Mitarbeiter (z.B. "Alice").
3.  **Zuweisung:**
    * Gehe zu `Zuweisungen verwalten (5)`.
    * Wähle `Teammitglied zu Projekt zuweisen (3)`.
    * Verbinde "Alice" mit "Website Relaunch".
4.  **Analyse:**
    * Nutze `Filter (6)` -> `Nach Priorität (4)`, um zu sehen, welche Projekte am wichtigsten sind.

## Projektstruktur

Der Code ist modular aufgebaut (`src/`) und trennt Logik von Benutzeroberfläche:

* `main.py`: Der Einstiegspunkt des Programms.
* `cli.py`: Behandelt das Hauptmenü und sämtliche User-Inputs (Controller).
* `src/`
    * `item.py`: **Basisklasse** (Parent) für Projekte und Aufgaben (Vererbung).
    * `projekt.py`: Hauptlogik für Projekte und die Verwaltung der Zuweisungen.
    * `aufgabe.py`: Logik für Aufgaben-Objekte.
    * `teammitglied.py`: Verwaltung der Team-Daten.
    * `dateiverwaltung.py`: Kapselt Lese-/Schreiboperationen (JSON) und Fehlerbehandlung.
    * `filter.py`: Enthält die Logik für Sortier- und Filterfunktionen (z.B. mittels Lambda).
    * `utils.py`: Hilfsfunktionen für Input-Validierung und Datumsformatierung.
* `data/`: Speicherort für die JSON-Dateien (wird automatisch generiert).

## Roadmap / Bekannte To-Dos

Das Projekt ist funktionsfähig, folgende Erweiterungen sind geplant:

- [ ] **Status-Tracking:** Status für Aufgaben einführen (z. B. "In Bearbeitung", "Erledigt").
- [ ] **Datenintegrität:** Erweiterte Prüfungen sicherstellen (z. B. keine doppelten Einträge bei gleicher ID).
- [ ] **ID-Logik:** Die implementierten IDs stärker in die User-Interaktion einbinden (aktuell läuft viel über Namen).
- [ ] **Erweiterte Löschlogik:** Kaskadierendes Löschen (z.B. Aufgaben löschen, wenn Projekt gelöscht wird).

---
*Erstellt für die Übungsaufgabe KI Fallstudie 2 (Gruppe).*
*AI: Formatierung von der Projektstruktur und die 'bash-Funktion' im README.
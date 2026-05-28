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
2.  **Ordnerstruktur prüfen:**
Das Skript erwartet einen `data`-Ordner im Hauptverzeichnis. Falls dieser fehlt, lege ihn und die Dateien `projekte.json`, `teammitglieder.json` und `aufgaben.json` bitte an:
    ```bash
    mkdir data
    ```

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

Der Code ist modular aufgebaut (`src/`) und trennt Logik von Daten:

* `src/`
  * `main.py`: Der Einstiegspunkt des Programms.
  * `cli.py`: Behandelt das Hauptmenü und sämtliche User-Inputs (Controller).
  * `item.py`: **Basisklasse** (Parent) für Projekte und Aufgaben (Vererbung).
  * `projekt.py`: Hauptlogik für Projekte und die Verwaltung der Zuweisungen.
  * `aufgabe.py`: Logik für Aufgaben-Objekte.
  * `teammitglied.py`: Verwaltung der Team-Daten.
  * `dateiverwaltung.py`: Kapselt Lese-/Schreiboperationen (JSON) und Fehlerbehandlung.
  * `filter.py`: Enthält die Logik für Sortier- und Filterfunktionen (z.B. mittels Lambda).
  * `utils.py`: Hilfsfunktionen für Input-Validierung und Datumsformatierung.
* `data/`: Speicherort für die JSON-Dateien.

### Fensterstruktur und verwendete Widgets
Die Benutzeroberfläche wurde nach dem Prinzip der *Separation of Concerns* entwickelt. Die Kern-Logikklassen blieben unberührt, während die GUI als reine Präsentationsschicht darübergelegt wurde.
* **Fensterstruktur:** Die Anwendung öffnet sich in einem zentralen Hauptfenster (`Tk`), das über ein strukturiertes Grid-Layout (`grid`) und Sub-Frames (`Frame`) in logische Arbeitsbereiche (Projekte, Team, Zuweisungen) unterteilt ist.
* **Verwendete Widgets:**
  * `ttk.Entry` & `tk.StringVar`: Zur dynamischen, asynchronen Eingabe und Übermittlung von Textdaten.
  * `ttk.Radiobutton` / `ttk.Combobox`: Für die standardisierte Auswahl vordefinierter Werte wie Prioritäten (Niedrig, Mittel, Hoch).
  * `ttk.Button`: Verknüpft mit ereignisgesteuerten Callbacks (Event-Handlern) zur Ausführung von Logik-Aktionen.
  * `tk.Listbox` / `ttk.Treeview`: Zur übersichtlichen, tabellarischen Darstellung der geladenen Daten.
  
## Bedienung (Benutzerdokumentation)

Die Interaktion mit dem Programm erfolgt intuitiv über die grafische Oberfläche des Hauptfensters.

### 1. Welche Felder gibt es?
* **Projektname / Aufgabenname / Name des Teammitglieds:** Freitextfelder (`Entry`) zur Eingabe der jeweiligen Bezeichnungen oder Namen.
* **Startdatum / Fälligkeitsdatum:** Textfelder zur zeitlichen Eingabe. Diese erwarten zwingend das Format `TT.MM.JJJJ`.
* **Priorität:** Radiobuttons zur exakten Festlegung der Dringlichkeitsstufe (Niedrig, Mittel, Hoch).
* **Auswahllisten (Listboxen / Dropdowns):** Zur Selektion bereits angelegter Elemente, um beispielsweise Verknüpfungen oder Löschungen vorzunehmen.

### 2. Welche Buttons führen welche Aktionen aus?
* **[Projekt erstellen] / [Task hinzufügen] / [Mitglied anlegen]:** Liest die Werte aus den jeweiligen Eingabefeldern aus, erzeugt die entsprechenden Objekte im Hintergrund und speichert diese persistent in den JSON-Dateien ab. Die Listenansichten aktualisieren sich sofort.
* **[Zuweisung vornehmen]:** Verknüpft ein in der Liste ausgewähltes Teammitglied mit einem ausgewählten Projekt oder einer Aufgabe.
* **[Filter anwenden]:** Sortiert oder filtert die angezeigten Projekte in Echtzeit nach der ausgewählten Priorität oder dem Datum.
* **[Löschen]:** Entfernt das aktuell in der Liste markierte Element unwiderruflich aus dem Datensatz.

### 3. Was passiert bei ungültigen Eingaben?
* Wenn Pflichtfelder (wie der Name) leer gelassen werden oder ein falsches Datumsformat eingegeben wird, bricht der Event-Handler die Verarbeitung sofort ab, um Datenfehler zu verhindern.
* Das Programm wirft keine Terminal-Fehler mehr, sondern fängt die Ausnahmen ab und öffnet ein natives, visuelles GUI-Dialogfenster (`messagebox.showerror`). Dem Benutzer wird darin eine präzise Fehlermeldung (z. B. *"Eingabefehler: Das Datum muss im Format TT.MM.JJJJ eingegeben werden!"*) angezeigt, damit er die Eingabe korrigieren kann.
## Roadmap / Bekannte To-Dos

Das Projekt ist funktionsfähig, folgende Erweiterungen sind geplant:

- [ ] **Status-Tracking:** Status für Aufgaben einführen (z. B. "In Bearbeitung", "Erledigt").
- [ ] **Datenintegrität:** Erweiterte Prüfungen sicherstellen (z. B. keine doppelten Einträge bei gleicher ID).
- [ ] **ID-Logik:** Die implementierten IDs stärker in die User-Interaktion einbinden (aktuell läuft viel über Namen).
- [ ] **Erweiterte Löschlogik:** Kaskadierendes Löschen (z.B. Aufgaben löschen, wenn Projekt gelöscht wird).

---
*Erstellt für die Übungsaufgabe KI Fallstudie 2 (Gruppe).*
*AI: Formatierung von der Projektstruktur und die 'bash-Funktion' im README.


from src.dateiverwaltung import *
from pathlib import Path


def filter_projects():
    file_path = Path(__file__).resolve().parent.parent / 'data' / 'projekte.json'
    all_projects = read(file_path)

    print("--- Projekte filtern ---")
    print("1: Nach bestimmter Priorität filtern")
    print("2: Nach Startdatum filtern (zeigt Projekte ab diesem Datum)")
    print("3: Nach Fälligkeitsdatum (nächstes zuerst)")
    print("4: Nach Priorität (Wichtigstes zuerst)")

    choice_filter = input("Bitte wähle eine Option (1, 2, 3 oder 4): ").strip()

    found_projects = []

    if choice_filter == "1":
        prio_input = input("Priorität wählen - niedrig (1), mittel (2), hoch (3): ").strip().lower()

        if prio_input == "1" or prio_input == "niedrig":
            target_priority = "niedrig"
        elif prio_input == "2" or prio_input == "mittel":
            target_priority = "mittel"
        elif prio_input == "3" or prio_input == "hoch":
            target_priority = "hoch"
        else:
            print("Ungültige Priorität.")
            return

        for project in all_projects:
            if project.get('priority') == target_priority:
                found_projects.append(project)

    elif choice_filter == "2":
        target_date = input("Startdatum eingeben (YYYY-MM-DD): ").strip()

        for project in all_projects:
            if project['date_start'] and project['date_start'] >= target_date:
                found_projects.append(project)

    elif choice_filter == "3":
        all_projects.sort(key=lambda p: p['date_due'])

        for project in all_projects:
                found_projects.append(project)

        print("Sortiert nach Fälligkeitsdatum (aufsteigend).")

    elif choice_filter == "4":
        #AI Mapping-Tabelle erstellt mit "prio"

        prio_map = {
            "hoch": 3,
            "mittel": 2,
            "niedrig": 1
        }
        #AI hilfe bei korrektem einsatz von lambda
        all_projects.sort(key=lambda p: prio_map.get(p.get('priority', '').lower(), 0), reverse=True)

        for project in all_projects:
                found_projects.append(project)

        print("Sortiert nach Priorität (hoch -> niedrig).")

    else:
        print("Ungültige Auswahl. Bitte 1, 2, 3 oder 4 wählen.")
        return

    print(f"--- {len(found_projects)} Projekte gefunden ---")
    for project in found_projects:
        print("-" * 20)
        print(
                f"Projekt-ID:   {project['project_id']}\n"
                f"Name:         {project['name']}\n"
                f"Startdatum:   {project['date_start']}\n"
                f"Priorität:    {project['priority']}\n"
                f"Beschreibung: {project['description']}"
            )
        print("-" * 20)
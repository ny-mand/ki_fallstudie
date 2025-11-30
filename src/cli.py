from pathlib import Path
from src.dateiverwaltung import *
from src.filter import filter_projects
from src.teammitglied import TeamMember
from src.aufgabe import Task
from src.projekt import Project
from src.utils import *



def show_menu():
    print("--- Hauptmenü ---")
    print("Projekte anzeigen (1)")
    print("Teammitglieder anzeigen (2)")
    print("Aufgaben anzeigen (3)")
    print("Neu erstellen: (4)")
    print("Zuweisungen verwalten: (5)")
    print("Filter: (6)")
    print("Löschen: (7)")
    print("Beenden (0)")


def run():
    print("Willkommen im Projektmanagement-Tool")
    while True:
        show_menu()
        user_input = get_non_empty_input("Wähle eine Option: ")
        if user_input == "0":
            print("-" *20, "\nProgramm beendet.")
            break
        elif user_input == "1":
            show_projects()
        elif user_input == "2":
            show_team_members()
        elif user_input == "3":
            show_tasks()
        elif user_input == "4":
            create()
        elif user_input == "5":
            assign()
        elif user_input == "6":
            filter_projects()
        elif user_input == "7":
            delete()
        else:
            print("Ungültige Eingabe. Bitte versuche es erneut.")

# mithilfe von AI an Änderungen in Daten angepasst und Lesbarkeit verbessert
def show_projects():
    data = read(Path(__file__).resolve().parent.parent / 'data' / 'projekte.json')
    if not data:
        print("Keine Projekte gefunden.")
        return
    for projekt in data:
        print("-" * 20)
        print(
            f"Projekt-ID: {projekt['project_id']}\n"
            f"Projektname: {projekt['name']}\n"
            f"Beschreibung: {projekt['description']}\n"
            f"Startdatum: {format_to_german_date(projekt['date_start'])}\n"
            f"Enddatum: {format_to_german_date(projekt['date_due'])}\n"
            f"Priorität: {projekt['priority']}\n"
        )
        # nächster Block AI
        working_by_person = projekt.get('working_by_person', {})
        if isinstance(working_by_person, dict) and working_by_person:
            print("Teammitglieder und Aufgaben:")
            for person, task_name in working_by_person.items():
                if isinstance(task_name, list):
                    tasks_str = ", ".join(str(t) for t in task_name)
                else:
                    tasks_str = str(task_name)
                print(f"  - {person}: {tasks_str}")
        else:
            print("Keine Teamzuweisungen vorhanden.")
        print("-" * 20)


def show_team_members():
    data = read(Path(__file__).resolve().parent.parent / 'data' / 'teammitglieder.json')
    if not data:
        print("Keine Teammitglieder gefunden.")
        return
    for member in data:
        print("-" * 20)
        print(
            f"Name: {member['name']}\n"
            f"Berufsbezeichnung: {member['job_title']}\n"
            f"Aktiv seit: {format_to_german_date(member['active_since'])}"
        )
        print("-" * 20)


def show_tasks():
    data = read(Path(__file__).resolve().parent.parent / 'data' / 'aufgaben.json')
    if not data:
        print("Keine Aufgaben gefunden.")
        return
    for task in data:
        print("-" * 20)
        print(
            f"Aufgaben-ID: {task['task_id']}\n"
            f"Aufgabe: {task['name']}\n"
            f"Beschreibung: {task['description']}\n"
            f"Priorität: {task['priority']}\n"
            f"Fälligkeitsdatum: {format_to_german_date(task['date_due'])}\n"
            f"Erstellt am: {format_to_german_date(task['date_created'])}"
        )
        print("-" * 20)


def create():
    print("--- Erstellen Menü ---")
    choice = get_non_empty_input("Projekt erstellen (1)\nNeues Teammitglied (2)\nAufgabe erstellen (3)\nZurück zum Hauptmenü (0)\nWähle eine Option: ")
    if choice == "1":
        project_created_name = Project.create_project()
        add_member_choice = input("Möchtest du ein Teammitglied zum Projekt hinzufügen? (j/n): ").strip().lower()
        if add_member_choice == "j":
            members_to_add = None
            while members_to_add is None:
                members_to_add_input = get_non_empty_input("Wie viele Teammitglieder möchtest du hinzufügen? ")
                try:
                    members_to_add = int(members_to_add_input)
                    if members_to_add < 1:
                        print("Bitte gib eine Zahl größer 0 ein.")
                        members_to_add = None
                except ValueError:
                    print("Ungültige Eingabe. Bitte gib eine Zahl ein.")
            for i in range(members_to_add):
                member_to_add = get_non_empty_input("Gib den Namen des Teammitglieds ein: ")
                Project.assign_member_to_project(project_created_name, member_to_add)
            print("Mitglieder zum Projekt hinzugefügt.")

    elif choice == "2":
        TeamMember.add_member()

    elif choice == "3":
        Task.create_task()

    elif choice == "0":
        return

    else:
        print("Ungültige Eingabe. Bitte versuche es erneut.")
        create()


def delete():
    print("--- Löschen Menü ---")
    choice = get_non_empty_input(
        "Projekt löschen (1)\n"
        "Aufgabe löschen (2)\n"
        "Teammitglied löschen (3)\n"
        "Zurück zum Hauptmenü (0)\n"
        "Wähle eine Option: "
    )

    if choice == "1":
        delete_item("projekt")
    elif choice == "2":
        delete_item("aufgabe")
    elif choice == "3":
        delete_item("teammitglied")
    elif choice == "0":
        return
    else:
        print("Ungültige Eingabe.")

# AI assisted
def assign():
    print("--- Zuweisungen verwalten ---")
    choice = get_non_empty_input("Aufgabe zuweisen (1)\nAufgabe entfernen (2)\nTeammitglied zu Projekt zuweisen (3)\n"
        "Teammitglied aus Projekt entfernen (4)\nZurück zum Hauptmenü (0)\nWähle eine Option: ")
    if choice == "1":
        project_name = get_non_empty_input("In welchem Projekt möchtest du eine Aufgabe zuweisen? ")
        if not Project.project_exists(project_name):
            print(f"Das Projekt '{project_name}' existiert nicht.")
            return
        member_name = get_non_empty_input("Gib den Namen des Teammitglieds ein: ")
        task_name = get_non_empty_input("Gib den Namen der Aufgabe ein: ")
        Project.assign_task_to_member(project_name, member_name, task_name)

    elif choice == "3":
        project_name = get_non_empty_input("Zu welchem Projekt möchtest du Mitglieder hinzufügen? ")
        if not Project.project_exists(project_name):
            print(f"Das Projekt '{project_name}' existiert nicht.")
            return
        members_to_add = None
        while members_to_add is None:
            members_to_add_input = get_non_empty_input("Wie viele Teammitglieder möchtest du hinzufügen? ")
            try:
                members_to_add = int(members_to_add_input)
                if members_to_add < 1:
                    print("Bitte gib eine Zahl größer 0 ein.")
                    members_to_add = None
            except ValueError:
                print("Ungültige Eingabe. Bitte gib eine Zahl ein.")

        for i in range(members_to_add):
            member_to_add = get_non_empty_input("Gib den Namen des Teammitglieds ein: ")
            Project.assign_member_to_project(project_name, member_to_add)
        if members_to_add > 1:
            print("Mitglieder zum Projekt hinzugefügt.")
        else:
            print("Mitglied zum Projekt hinzugefügt.")

    elif choice == "2":
        project_name = get_non_empty_input("Aus welchem Projekt möchtest du eine Aufgabe entfernen? ")
        if not Project.project_exists(project_name):
            print(f"Das Projekt '{project_name}' existiert nicht.")
            return
        member_name = get_non_empty_input("Von welchem Mitglied? ")
        task_name = get_non_empty_input("Welche Aufgabe? ")
        Project.remove_task_from_member(project_name, member_name, task_name)

    elif choice == "4":
        project_name = get_non_empty_input("Aus welchem Projekt? ")
        if not Project.project_exists(project_name):
            print(f"Das Projekt '{project_name}' existiert nicht.")
            return
        member_name = get_non_empty_input("Welches Mitglied entfernen? ")
        Project.remove_member_from_project(project_name, member_name)

    elif choice == "0":
        return

    else:
        print("Ungültige Eingabe.")


# AI assisted
def delete_item(item_type):
    # Bestimme Datei und relevante Felder basierend auf Typ
    if item_type == "projekt":
        file_path = Path(__file__).resolve().parent.parent / 'data' / 'projekte.json'
        name_field = "name"
        id_field = "project_id"
        exists_func = Project.project_exists
    elif item_type == "aufgabe":
        file_path = Path(__file__).resolve().parent.parent / 'data' / 'aufgaben.json'
        name_field = "name"
        id_field = "task_id"
        exists_func = Task.task_exists
    elif item_type == "teammitglied":
        file_path = Path(__file__).resolve().parent.parent / 'data' / 'teammitglieder.json'
        name_field = "name"
        id_field = "member_id"
        exists_func = TeamMember.member_exists
    else:
        print("Ungültiger Typ.")
        return

    # Lade Daten
    data = read(file_path)
    if not data:
        if item_type == "projekt":
            print(f"Keine Projekte gefunden.")
        if item_type == "aufgabe":
            print(f"Keine Aufgaben gefunden.")
        if item_type == "teammitglied":
            print(f"Keine Teammitglieder gefunden.")
        return

    # Frage nach Namen
    name = get_non_empty_input(f"Gib den Namen des zu löschenden {item_type}s ein: ") if item_type in ["projekt", "teammitglied"] else get_non_empty_input("Gib den Namen der zu löschenden Aufgabe ein: ")

    # Prüfe Existenz
    if not exists_func(name):
        print(f"{item_type.capitalize()} '{name}' existiert nicht.")
        return

    # Bestätigung einholen
    confirm = get_non_empty_input(f"Möchtest du '{name}' wirklich löschen? (j/n): ").lower()
    if confirm != "j":
        print("Löschvorgang abgebrochen.")
        return

    # Filtere Eintrag heraus (case-insensitive)
    original_length = len(data)
    data = [item for item in data if item[name_field].lower() != name.lower()]

    # Prüfe, ob etwas gelöscht wurde
    if len(data) == original_length:
        print(f"Fehler beim Löschen von '{name}'.")
        return

    # Speichere aktualisierte Daten
    write(file_path, data)
    print(f"{item_type.capitalize()} '{name}' erfolgreich gelöscht.")



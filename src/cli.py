from pathlib import Path
from src.dateiverwaltung import read
from src.teammitglied import TeamMember
from src.aufgabe import Task
from src.projekt import Project



def show_menu():
    print("--- Hauptmenü ---")
    print("Projekte anzeigen (1)")
    print("Teammitglieder anzeigen (2)")
    print("Aufgaben anzeigen (3)")
    print("Neu erstellen: (4)")
    print("Zuweisen: (5)")
    print("Beenden (0)")


def run():
    print("Willkommen im Projektmanagement-Tool")
    while True:
        show_menu()
        user_input = input("Wähle eine Option: ").strip().lower()
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
        else:
            print("Ungültige Eingabe. Bitte versuche es erneut.")


def show_projects():
    data = read(Path(__file__).resolve().parent.parent / 'data' / 'projekte.json')
    for projekt in data:
        print("-" * 20)
        print(
            f"Projekt-ID: {projekt['project_id']}\n"
            f"Projektname: {projekt['name']}\n"
            f"Beschreibung: {projekt['description']}\n"
            f"Startdatum: {projekt['date_start']}\n"
            f"Enddatum: {projekt['date_due']}\n"
            f"Priorität: {projekt['priority']}\n"
        )
        # nächster Block AI
        working_by_person = projekt.get('working_by_person', {})
        if isinstance(working_by_person, dict) and working_by_person:
            print("Teammitglieder und Aufgaben:")
            for person, task_name in working_by_person.items():
                print(f"  - {person}: {task_name}")
        else:
            print("Keine Teamzuweisungen vorhanden.")
        print("-" * 20)


def show_team_members():
    data = read(Path(__file__).resolve().parent.parent / 'data' / 'teammitglieder.json')
    for member in data:
        print("-" * 20)
        print(
            f"Name: {member['name']}\n"
            f"Berufsbezeichnung: {member['job_title']}\n"
            f"Aktiv seit: {member['active_since']}"
        )
        print("-" * 20)


def show_tasks():
    data = read(Path(__file__).resolve().parent.parent / 'data' / 'aufgaben.json')
    for task in data:
        print("-" * 20)
        print(
            f"Aufgaben-ID: {task['task_id']}\n"
            f"Aufgabe: {task['name']}\n"
            f"Beschreibung: {task['description']}\n"
            f"Priorität: {task['priority']}\n"
            f"Fälligkeitsdatum: {task['date_due']}\n"
            f"Erstellt am: {task['date_created']}"
        )
        print("-" * 20)


def create():
    print("--- Erstellen Menü ---")
    choice = input("Projekt erstellen (1)\nNeues Teammitglied (2)\nAufgabe erstellen (3)\nZurück zum Hauptmenü (0)\nWähle eine Option: ")
    if choice == "1":
        Project.create_project()
        print("Projekt erstellen")
    elif choice == "2":
        TeamMember.add_member()
        print("Teammitglied erstellen")
    elif choice == "3":
        Task.create_task()
        print("Aufgabe erstellen")
    elif choice == "0":
        return
    else:
        print("Ungültige Eingabe. Bitte versuche es erneut.")
        create()


def assign():
    print("--- Zuweisen Menü ---")
    choice = input("Aufgabe zuweisen (1)\nTeammitglied zu Projekt zuweisen (2)")
    if choice == "1":
        #TODO assign_task()
        print("Aufgabe zuweisen")
    elif choice == "2":
        #TODO assign_member_to_project()
        print("Teammitglied zu Projekt zuweisen")

from pathlib import Path
from src.dateiverwaltung import read
from src.filter import filter_projects
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
    print("Filter: (6)")
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
        elif user_input == "6":
            filter_projects()
        else:
            print("Ungültige Eingabe. Bitte versuche es erneut.")

# mithilfe von AI an Änderungen in Daten angepasst und Lesbarkeit verbessert
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
        project_created_name = Project.create_project()
        add_member_choice = input("Möchtest du ein Teammitglied zum Projekt hinzufügen? (j/n): ").strip().lower()
        if add_member_choice == "j":
            members_to_add = input("Wie viele Teammitglieder möchtest du hinzufügen? ")
            for i in range(int(members_to_add)):
                member_to_add = input("Gib den Namen des Teammitglieds ein: ")
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


def assign():
    print("--- Zuweisen Menü ---")
    choice = input("Aufgabe zuweisen (1)\nTeammitglied zu Projekt zuweisen (2)")
    if choice == "1":
        project_name = input("In welchem Projekt möchtest du eine Aufgabe zuweisen? ")
        member_name = input("Gib den Namen des Teammitglieds ein: ")
        task_name = input("Gib den Namen der Aufgabe ein: ")
        Project.assign_task_to_member(project_name, member_name, task_name)

    elif choice == "2":
        project_name = input("Zu welchem Projekt möchtest du Mitglieder hinzufügen? ")
        members_to_add = input("Wie viele Teammitglieder möchtest du hinzufügen? ")
        for i in range(int(members_to_add)):
            member_to_add = input("Gib den Namen des Teammitglieds ein: ")
            Project.assign_member_to_project(project_name, member_to_add)

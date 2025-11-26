import datetime as dt
from src.item import Item
from src.dateiverwaltung import *
from src.teammitglied import TeamMember
from src.aufgabe import Task


class Project(Item):
    def __init__(self, name, description, date_start, date_due, priority):
        super().__init__(name, description)
        self.date_start = date_start
        self.date_due = date_due
        self.priority = priority
        self.working_by_person = []
        self.working_by_task = []

    def get_name(self):
        return self.name
    def get_description(self):
        return self.description
    def get_date_start(self):
        return self.date_start
    def get_date_end(self):
        return self.date_due
    def get_priority(self):
        return self.priority

    def is_running(self):
        current_date = dt.datetime.now()
        if self.date_start <= current_date:
            return True
        elif current_date >= self.date_due:
            return "Overdue"
        else:
            return False

    @staticmethod
    def project_exists(project_name):
        data = read((Path(__file__).resolve().parent.parent / 'data' / 'projekte.json'))
        for project in data:
            if project['name'].lower() == project_name.lower():
                return True
        else:
            return False

    @staticmethod
    def create_project():
        data = read((Path(__file__).resolve().parent.parent / 'data' / 'projekte.json'))
        if data:
            new_id = data[-1]['project_id'] + 1
        else:
            new_id = 1

        name_input = input("Gib den Namen des Projekts ein: ")
        description_input = input("Gib eine Beschreibung des Projekts ein: ")
        date_start_input = input("Gib das Startdatum des Projekts ein (YYYY-MM-DD): ")
        date_due_input = input("Gib das Fälligkeitsdatum des Projekts ein (YYYY-MM-DD): ")
        priority_input = input("Gib die Priorität des Projekts ein (niedrig (1), mittel (2), hoch (3)): ")
        priority = "niedrig" if priority_input == "1" else "mittel" if priority_input == "2" else "hoch"
        working_by_person = {}
        working_by_task = {}

        new_project = {
            "project_id": new_id,
            "name": name_input,
            "description": description_input,
            "date_start": date_start_input,
            "date_due": date_due_input,
            "priority": priority,
            "working_by_person": working_by_person,
            "working_by_task": working_by_task
        }
        data.append(new_project)
        write((Path(__file__).resolve().parent.parent / 'data' / 'projekte.json'), data)
        print("Neues Projekt hinzugefügt:", name_input)
        return name_input

    @staticmethod #AI assisted
    def assign_member_to_project(project_name, member, task=None):
        data = read(Path(__file__).resolve().parent.parent / 'data' / 'projekte.json')
        changed = False

        if not Project.project_exists(project_name):
            print(f'Projekt existiert nicht. Bitte erstelle es zuerst.')
            return
        if not TeamMember.member_exists(member):
            print(f"Teammitglied existiert nicht. Bitte füge es zuerst hinzu.")
            return
        if input("Möchtest du eine Aufgabe zuweisen? (j/n): ").strip().lower() == "j":
            task_name_input = input("Gib den Namen der Aufgabe ein: ").strip()
            if not Task.task_exists(task_name_input):
                print(f"Aufgabe existiert nicht. Bitte erstelle sie zuerst.")
                return
            task = task_name_input

        for project in data:
            if project["name"] == project_name:
                # Sicherstellen, dass die Mappings initialisiert sind
                project.setdefault("working_by_person", {})
                project.setdefault("working_by_task", {})
                if member not in project["working_by_person"]:
                    if task:
                        project["working_by_person"][member] = [task]
                        if task in project["working_by_task"]:
                            if member not in project["working_by_task"][task]:
                                project["working_by_task"][task].append(member)
                        else:
                            project["working_by_task"][task] = [member]
                    else:
                        project["working_by_person"][member] = []
                else:
                    print(f"Mitglied {member} ist bereits dem Projekt {project_name} zugewiesen.")
                    return
                changed = True
                break

        if changed:
            write(Path(__file__).resolve().parent.parent / 'data' / 'projekte.json', data)
            print(f'{member} dem Projekt "{project_name}" zugewiesen.')

    @staticmethod #AI assisted
    def assign_task_to_member(project_name, member, task):
        data = read(Path(__file__).resolve().parent.parent / 'data' / 'projekte.json')
        changed = False

        if not Project.project_exists(project_name):
            print(f'Projekt existiert nicht. Bitte erstelle es zuerst.')
            return
        if not TeamMember.member_exists(member):
            print(f"Teammitglied existiert nicht. Bitte füge es zuerst hinzu.")
            return
        if not Task.task_exists(task):
            print(f"Aufgabe existiert nicht. Bitte erstelle sie zuerst.")
            return

        for project in data:
            if project["name"] == project_name:
                # Sicherstellen, dass die Mappings initialisiert sind
                project.setdefault("working_by_person", {})
                project.setdefault("working_by_task", {})
            if member not in project["working_by_person"]:
                print(f"{member} ist nicht dem Projekt zugewiesen. Aufgabe kann nicht zugeteilt werden.")
                return
            if task in project["working_by_person"][member]:
                print(f"{member} ist bereits der Aufgabe '{task}' zugewiesen.")
                return

            project["working_by_person"][member].append(task)
            if task in project["working_by_task"]:
                if member not in project["working_by_task"][task]:
                    project["working_by_task"][task].append(member)
            else:
                project["working_by_task"][task] = [member]

            changed = True
            break

        if changed:
            write(Path(__file__).resolve().parent.parent / 'data' / 'projekte.json', data)
            print(f"Aufgabe '{task}' erfolgreich an {member} im Projekt '{project_name}' zugewiesen.")
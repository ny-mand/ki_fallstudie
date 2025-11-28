from src.item import Item
from src.dateiverwaltung import *
from src.teammitglied import TeamMember
from src.aufgabe import Task
from src.utils import *


class Project(Item):
    def __init__(self, project_id, name, description, date_start, date_due, priority):
        super().__init__(name, description)
        self.project_id = project_id
        self.date_start = date_start
        self.date_due = date_due
        self.priority = priority
        # Dictionary: Mitglied -> Liste von Aufgaben
        self.working_by_person = {}
        # Dictionary: Aufgabe -> Liste von Mitgliedern
        self.working_by_task = {}

    @staticmethod
    def project_exists(project_name):
        # Projektdaten aus JSON laden
        data = read((Path(__file__).resolve().parent.parent / 'data' / 'projekte.json'))
        # Prüfe ob Projektname vorhanden ist (case-insensitive)
        for project in data:
            if project['name'].lower() == project_name.lower():
                return True
        return False

    @staticmethod
    def validate_existence(project_name, member, task):
        # Prüfe nacheinander, ob Projekt, Mitglied und Aufgabe existieren
        if not Project.project_exists(project_name):
            print(f'Projekt existiert nicht. Bitte erstelle es zuerst.')
            return False
        if not TeamMember.member_exists(member):
            print(f"Teammitglied existiert nicht. Bitte füge es zuerst hinzu.")
            return False
        if task == "": # Falls keine Aufgabe angegeben wurde, überspringe die Prüfung
            return True
        if not Task.task_exists(task):
            print(f"Aufgabe existiert nicht. Bitte erstelle sie zuerst.")
            return False
        return True

    @staticmethod
    def create_project():
        data = read((Path(__file__).resolve().parent.parent / 'data' / 'projekte.json'))
        # Generiere neue ID basierend auf letzter ID oder starte bei 1
        if data:
            new_id = data[-1]['project_id'] + 1
        else:
            new_id = 1

        # Benutzereingaben sammeln
        name_input = get_non_empty_input("Gib den Namen des Projekts ein: ")
        if Project.project_exists(name_input):
            print(f"Ein Projekt mit dem Namen '{name_input}' existiert bereits.")
            return

        description_input = get_non_empty_input("Gib eine Beschreibung des Projekts ein: ")
        date_start_input = get_non_empty_input("Gib das Startdatum des Projekts ein (YYYY-MM-DD): ")
        # Validierung des Datumsformats
        while not validate_date_format(date_start_input):
            print("Ungültiges Datumsformat. Bitte benutze YYYY-MM-DD.")
            date_start_input = get_non_empty_input("Gib das Startdatum des Projekts ein (YYYY-MM-DD): ")

        date_due_input = get_non_empty_input("Gib das Fälligkeitsdatum des Projekts ein (YYYY-MM-DD): ")
        # Validierung des Datumsformats
        while not validate_date_format(date_due_input):
            print("Ungültiges Datumsformat. Bitte benutze YYYY-MM-DD.")
            date_due_input = get_non_empty_input("Gib das Fälligkeitsdatum des Projekts ein (YYYY-MM-DD): ")

        priority_input = get_non_empty_input("Gib die Priorität des Projekts ein (niedrig (1), mittel (2), hoch (3)): ")
        while not priority_input in ["1", "2", "3"]: # Validierung der Prioritätseingabe
            print("Ungültige Eingabe. Bitte gib 1, 2 oder 3 ein.")
            priority_input = get_non_empty_input("Gib die Priorität des Projekts ein (niedrig (1), mittel (2), hoch (3)): ").strip()

        # Konvertiere Zahl in Prioritätstext
        priority = "niedrig" if priority_input == "1" else "mittel" if priority_input == "2" else "hoch"
        # Initialisiere leere Zuordnungen
        working_by_person = {}
        working_by_task = {}

        # Erstelle Projekt-Dictionary
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
        # Speichere neues Projekt
        data.append(new_project)
        write((Path(__file__).resolve().parent.parent / 'data' / 'projekte.json'), data)
        print("Neues Projekt hinzugefügt:", name_input)
        return name_input

    @staticmethod #AI assisted
    def assign_member_to_project(project_name, member, task=None):
        data = read(Path(__file__).resolve().parent.parent / 'data' / 'projekte.json')
        changed = False

        # Optional: Frage nach Aufgabenzuweisung
        if input("Möchtest du eine Aufgabe zuweisen? (j/n): ").strip().lower() == "j":
            task = get_non_empty_input("Gib den Namen der Aufgabe ein: ")

        # Validiere, dass Projekt, Mitglied und Aufgabe existieren
        if not Project.validate_existence(project_name, member, task):
            return

        # Suche Projekt und weise Mitglied zu
        for project in data:
            if project["name"] == project_name:
                # Stelle sicher, dass Mappings existieren
                project.setdefault("working_by_person", {})
                project.setdefault("working_by_task", {})
                # Prüfe, ob Mitglied bereits zugewiesen
                if member not in project["working_by_person"]:
                    if task:
                        # Füge Mitglied mit Aufgabe hinzu
                        project["working_by_person"][member] = [task]
                        # Bidirektionale Zuordnung: Aufgabe → Mitglied
                        if task in project["working_by_task"]:
                            if member not in project["working_by_task"][task]:
                                project["working_by_task"][task].append(member)
                        else:
                            project["working_by_task"][task] = [member]
                    else:
                        # Füge Mitglied ohne Aufgabe hinzu
                        project["working_by_person"][member] = []
                else:
                    print(f"Mitglied {member} ist bereits dem Projekt {project_name} zugewiesen.")
                    return
                changed = True
                break

        # Speichere Änderungen, falls erfolgt
        if changed:
            write(Path(__file__).resolve().parent.parent / 'data' / 'projekte.json', data)
            print(f'{member} dem Projekt "{project_name}" zugewiesen.')

    @staticmethod #AI assisted
    def assign_task_to_member(project_name, member, task):
        data = read(Path(__file__).resolve().parent.parent / 'data' / 'projekte.json')
        changed = False

        # Validiere Existenz
        if not Project.validate_existence(project_name, member, task):
            return

        for project in data:
            if project["name"] == project_name:
                # Stelle sicher, dass Mappings existieren
                project.setdefault("working_by_person", {})
                project.setdefault("working_by_task", {})
            # Prüfe, ob Mitglied dem Projekt zugewiesen ist
            if member not in project["working_by_person"]:
                print(f"{member} ist nicht dem Projekt zugewiesen. Aufgabe kann nicht zugeteilt werden.")
                return
            # Prüfe ob Aufgabe bereits zugewiesen
            if task in project["working_by_person"][member]:
                print(f"{member} ist bereits der Aufgabe '{task}' zugewiesen.")
                return

            # Füge Aufgabe zum Mitglied hinzu
            project["working_by_person"][member].append(task)
            # Bidirektionale Zuordnung: Aufgabe → Mitglied
            if task in project["working_by_task"]:
                if member not in project["working_by_task"][task]:
                    project["working_by_task"][task].append(member)
            else:
                project["working_by_task"][task] = [member]

            changed = True
            break

        # Speichere Änderungen
        if changed:
            write(Path(__file__).resolve().parent.parent / 'data' / 'projekte.json', data)
            print(f"Aufgabe '{task}' erfolgreich an {member} im Projekt '{project_name}' zugewiesen.")
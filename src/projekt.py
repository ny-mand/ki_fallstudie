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
        if task == "" or task is None: # Falls keine Aufgabe angegeben wurde, überspringe die Prüfung
            return True
        if not Task.task_exists(task):
            print(f"Aufgabe existiert nicht. Bitte erstelle sie zuerst.")
            return False
        return True

    @staticmethod
    def create_project(name, description, date_start, date_due, priority):
        data = read((Path(__file__).resolve().parent.parent / 'data' / 'projekte.json'))
        # Generiere neue ID basierend auf letzter ID oder starte bei 1
        if data:
            new_id = data[-1]['project_id'] + 1
        else:
            new_id = 1

        if Project.project_exists(name):
            print(f"Ein Projekt mit dem Namen '{name}' existiert bereits.")
            return

        # Validierung des Datumsformats
        while not validate_date_format(date_start): # TODO mit Fehlermeldung anders umgehen
            print("Ungültiges Datumsformat. Bitte benutze YYYY-MM-DD.")

        # Validierung des Datumsformats
        while not validate_date_format(date_due): # TODO s.o.
            print("Ungültiges Datumsformat. Bitte benutze YYYY-MM-DD.")

        while date_start > date_due:
            print("Das Fälligkeitsdatum muss nach dem Startdatum liegen.")

        while not priority in ["1", "2", "3"]: # Validierung der Prioritätseingabe
            print("Ungültige Eingabe. Bitte gib 1, 2 oder 3 ein.") # TODO s.o.

        # Konvertiere Zahl in Prioritätstext
        priority = "niedrig" if priority == "1" else "mittel" if priority == "2" else "hoch"
        # Initialisiere leere Zuordnungen
        working_by_person = {}
        working_by_task = {}

        # Erstelle Projekt-Dictionary
        new_project = {
            "project_id": new_id,
            "name": name,
            "description": description,
            "date_start": date_start,
            "date_due": date_due,
            "priority": priority,
            "working_by_person": working_by_person,
            "working_by_task": working_by_task
        }
        # Speichere neues Projekt
        data.append(new_project)
        write((Path(__file__).resolve().parent.parent / 'data' / 'projekte.json'), data)
        print("Neues Projekt hinzugefügt:", name)
        return name

    @staticmethod #AI assisted
    def assign_member_to_project(project_name, member, task=None):
        data = read(Path(__file__).resolve().parent.parent / 'data' / 'projekte.json')
        changed = False

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
                #AI fix für den Fall, dass nur ein String statt einer Liste gespeichert ist
                if isinstance(project["working_by_person"][member], str):
                    project["working_by_person"][member] = [project["working_by_person"][member]]
                elif not isinstance(project["working_by_person"][member], list):
                    project["working_by_person"][member] = []
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


    # AI assisted
    @staticmethod
    def remove_member_from_project(project_name, member_name):
        if not Project.project_exists(project_name):
            print(f"Das Projekt '{project_name}' existiert nicht.")
            return False

        if not TeamMember.member_exists(member_name):
            print(f"Das Teammitglied '{member_name}' existiert nicht.")
            return False

        projects_path = Path(__file__).resolve().parent.parent / 'data' / 'projekte.json'
        projects_data = read(projects_path)

        member_found = False
        for project in projects_data:
            if project['name'].lower() == project_name.lower():
                # Entferne aus working_by_person
                working_by_person = project.get('working_by_person', {})
                if member_name in working_by_person:
                    del working_by_person[member_name]
                    member_found = True

                # Entferne aus working_by_task
                working_by_task = project.get('working_by_task', {})
                for task_name, members in list(working_by_task.items()):
                    if member_name in members:
                        members.remove(member_name)
                        if not members:  # Wenn keine Mitglieder mehr, entferne Aufgabe
                            del working_by_task[task_name]

                project['working_by_person'] = working_by_person
                project['working_by_task'] = working_by_task
                break

        if not member_found:
            print(f"'{member_name}' ist nicht Teil des Projekts '{project_name}'.")
            return False

        write(projects_path, projects_data)
        print(f"'{member_name}' wurde aus Projekt '{project_name}' entfernt.")
        return True

    @staticmethod
    def remove_task_from_member(project_name, member_name, task_name):
        if not Project.project_exists(project_name):
            print(f"Das Projekt '{project_name}' existiert nicht.")
            return False

        projects_path = Path(__file__).resolve().parent.parent / 'data' / 'projekte.json'
        projects_data = read(projects_path)

        task_removed = False
        for project in projects_data:
            if project['name'].lower() == project_name.lower():
                working_by_person = project.get('working_by_person', {})
                working_by_task = project.get('working_by_task', {})

                # Entferne aus working_by_person
                if member_name in working_by_person:
                    tasks = working_by_person[member_name]
                    if isinstance(tasks, list):
                        if task_name in tasks:
                            tasks.remove(task_name)
                            task_removed = True
                            if not tasks:  # Wenn keine Aufgaben mehr, entferne Mitglied
                                del working_by_person[member_name]
                            else:
                                working_by_person[member_name] = tasks
                    elif tasks == task_name:  # Einzelner String
                        del working_by_person[member_name]
                        task_removed = True

                # Entferne aus working_by_task
                if task_name in working_by_task:
                    members = working_by_task[task_name]
                    if member_name in members:
                        members.remove(member_name)
                        task_removed = True
                        if not members:  # Wenn keine Mitglieder mehr
                            del working_by_task[task_name]

                project['working_by_person'] = working_by_person
                project['working_by_task'] = working_by_task
                break

        if not task_removed:
            print(f"Aufgabe '{task_name}' ist '{member_name}' nicht zugewiesen.")
            return False

        write(projects_path, projects_data)
        print(f"Aufgabe '{task_name}' wurde von '{member_name}' entfernt.")
        return True

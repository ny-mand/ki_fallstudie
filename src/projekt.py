import datetime as dt
from src.item import Item
from src.dateiverwaltung import *

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
        working_by_person = []
        working_by_task = []

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

    @staticmethod
    def assign_member_to_project(project_name, member):
        pass

    @staticmethod
    def assign_task_to_member(member, task):
        pass
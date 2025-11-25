import datetime as dt
from src.item import Item
from src.dateiverwaltung import *

class Task(Item):
    def __init__(self, name, description, date_due, priority, status, *allocated_to):
        super().__init__(name, description)
        self.date_due = date_due
        self.allocated_to = allocated_to
        self.priority = priority
        self.status = status

    def get_name(self):
        return self.name
    def get_description(self):
        return self.description
    def get_date_due(self):
        return self.date_due
    def get_allocated_to(self):
        return self.allocated_to
    def get_priority(self):
        return self.priority

    def is_allocated(self):
        if self.allocated_to:
            return True
        else:
            return False

    def set_priority(self, priority):
        self.priority = priority

    @staticmethod
    def create_task(date_created = dt.datetime.now().date().isoformat()):
        data = read((Path(__file__).resolve().parent.parent / 'data' / 'aufgaben.json'))
        if data:
            new_id = data[-1]['task_id'] + 1
        else:
            new_id = 1

        name_input = input("Gib den Namen der Aufgabe ein: ")
        description_input = input("Gib eine Beschreibung der Aufgabe ein: ")
        priority_input = input("Gib die Priorität der Aufgabe ein (niedrig (1), mittel (2), hoch (3)): ")
        priority = "niedrig" if priority_input == "1" else "mittel" if priority_input == "2" else "hoch"
        date_due_input = input("Gib das Fälligkeitsdatum der Aufgabe ein (YYYY-MM-DD): ")

        new_task = {
            "task_id": new_id,
            "name": name_input,
            "description": description_input,
            "priority": priority,
            "date_due": date_due_input,
            "date_created": date_created,
        }
        data.append(new_task)
        write((Path(__file__).resolve().parent.parent / 'data' / 'aufgaben.json'), data)
        print("Neue Aufgabe hinzugefügt:", name_input)
import datetime as dt
from src.item import Item
from src.dateiverwaltung import *

class Task(Item):
    def __init__(self, task_id, name, description, date_due, priority, date_created = dt.datetime.now().date().isoformat()):
        super().__init__(name, description)
        self.task_id = task_id
        self.priority = priority
        self.date_due = date_due
        self.date_created = date_created


    @staticmethod
    def task_exists(task_name):
        # Aufgabendaten aus JSON laden
        data = read((Path(__file__).resolve().parent.parent / 'data' / 'aufgaben.json'))
        # Prüfe, ob Aufgabenname vorhanden ist (case-insensitive)
        for task in data:
            if task['name'].lower() == task_name.lower():
                return True
        else:
            return False

    @staticmethod
    def create_task(date_created = dt.datetime.now().date().isoformat()):
        data = read((Path(__file__).resolve().parent.parent / 'data' / 'aufgaben.json'))
        # Generiere neue ID basierend auf letzter ID oder starte bei 1
        if data:
            new_id = data[-1]['task_id'] + 1
        else:
            new_id = 1

        # Benutzereingaben sammeln
        name_input = input("Gib den Namen der Aufgabe ein: ")
        description_input = input("Gib eine Beschreibung der Aufgabe ein: ")
        priority_input = input("Gib die Priorität der Aufgabe ein (niedrig (1), mittel (2), hoch (3)): ")
        # Konvertiere Zahl in Prioritätstext
        priority = "niedrig" if priority_input == "1" else "mittel" if priority_input == "2" else "hoch"
        date_due_input = input("Gib das Fälligkeitsdatum der Aufgabe ein (YYYY-MM-DD): ")

        # Erstelle Aufgaben-Dictionary
        new_task = {
            "task_id": new_id,
            "name": name_input,
            "description": description_input,
            "priority": priority,
            "date_due": date_due_input,
            "date_created": date_created,
        }
        # Speichere neue Aufgabe
        data.append(new_task)
        write((Path(__file__).resolve().parent.parent / 'data' / 'aufgaben.json'), data)
        print("Neue Aufgabe hinzugefügt:", name_input)
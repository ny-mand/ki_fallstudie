import datetime as dt
from src.item import Item
from src.dateiverwaltung import *
from src.utils import *

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
        if task_name is None: # Fehler, die mit None zusammenhängen abfangen
            return False
        # Prüfe, ob Aufgabenname vorhanden ist (case-insensitive)
        for task in data:
            if task['name'].lower() == task_name.lower():
                return True
        return False

    @staticmethod
    def create_task(name, description, priority, date_due, date_created = dt.datetime.now().date().isoformat()):
        data = read((Path(__file__).resolve().parent.parent / 'data' / 'aufgaben.json'))
        # Generiere neue ID basierend auf letzter ID oder starte bei 1
        if data:
            new_id = data[-1]['task_id'] + 1
        else:
            new_id = 1

        # Benutzereingaben sammeln
        if Task.task_exists(name):
            print(f"Eine Aufgabe mit dem Namen '{name}' existiert bereits.")
            return

        while not priority in ["1", "2", "3"]:  # Validierung der Prioritätseingabe TODO mit dropdown austauschen
            print("Ungültige Eingabe. Bitte gib 1, 2 oder 3 ein.")
        # Konvertiere Zahl in Prioritätstext
        priority = "niedrig" if priority == "1" else "mittel" if priority == "2" else "hoch"

        # Validierung des Datumsformats
        while not validate_date_format(date_due):
            print("Ungültiges Datumsformat. Bitte benutze YYYY-MM-DD.")
        # Erstelle Aufgaben-Dictionary
        new_task = {
            "task_id": new_id,
            "name": name,
            "description": description,
            "priority": priority,
            "date_due": date_due,
            "date_created": date_created,
        }
        # Speichere neue Aufgabe
        data.append(new_task)
        write((Path(__file__).resolve().parent.parent / 'data' / 'aufgaben.json'), data)
        print("Neue Aufgabe hinzugefügt:", name)
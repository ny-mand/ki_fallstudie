import datetime as dt
from src.dateiverwaltung import *
from src.utils import *

class TeamMember:
    def __init__(self, name, job_title, active_since):
        self.name = name
        self.job_title = job_title
        self.active_since = active_since

    @staticmethod
    def member_exists(name):
        # Teammitglieder aus JSON laden
        data = read((Path(__file__).resolve().parent.parent / 'data' / 'teammitglieder.json'))
        # Prüfe, ob Name vorhanden ist (case-insensitive)
        for member in data:
            if member['name'].lower() == name.lower():
                return True
        return False

    @staticmethod
    def add_member(name, job_title, active_since = dt.datetime.now().date().isoformat()):
        data = read((Path(__file__).resolve().parent.parent / 'data' / 'teammitglieder.json'))
        # Generiere neue ID basierend auf letzter ID oder starte bei 1
        if data:
            new_id = data[-1]['member_id'] + 1
        else:
            new_id = 1

        # Benutzereingaben sammeln
        if TeamMember.member_exists(name):
            print(f"Ein Teammitglied mit dem Namen '{name}' existiert bereits.")
            return

        # Validierung des Datumsformats, falls eingegeben
        while not validate_date_format(active_since):
            print("Ungültiges Datumsformat. Bitte benutze YYYY-MM-DD.") # TODO anders handlen

        # Erstelle Teammitglied-Dictionary
        new_member = {
            "member_id": new_id,
            "name": name,
            "job_title": job_title,
            "active_since": active_since
        }
        # Speichere neues Teammitglied
        data.append(new_member)
        write((Path(__file__).resolve().parent.parent / 'data' / 'teammitglieder.json'), data)
        print("Neues Teammitglied hinzugefügt:", name)

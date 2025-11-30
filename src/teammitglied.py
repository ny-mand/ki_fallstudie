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
    def add_member(active_since = dt.datetime.now().date().isoformat()):
        data = read((Path(__file__).resolve().parent.parent / 'data' / 'teammitglieder.json'))
        # Generiere neue ID basierend auf letzter ID oder starte bei 1
        if data:
            new_id = data[-1]['member_id'] + 1
        else:
            new_id = 1

        # Benutzereingaben sammeln
        name_input = get_non_empty_input("Gib den Namen des Teammitglieds ein: ")
        if TeamMember.member_exists(name_input):
            print(f"Ein Teammitglied mit dem Namen '{name_input}' existiert bereits.")
            return

        job_title_input = get_non_empty_input("Gib die Berufsbezeichnung des Teammitglieds ein: ")
        active_since_input = input("Gib das Eintrittsdatum ein (YYYY-MM-DD) oder leer lassen: ").strip()
        # Validierung des Datumsformats, falls eingegeben
        while active_since_input != "" and not validate_date_format(active_since_input):
            print("Ungültiges Datumsformat. Bitte benutze YYYY-MM-DD.")
            active_since_input = input("Gib das Eintrittsdatum ein (YYYY-MM-DD) oder leer lassen: ").strip()
        # Erstelle Teammitglied-Dictionary
        new_member = {
            "member_id": new_id,
            "name": name_input,
            "job_title": job_title_input,
            "active_since": active_since_input if active_since_input != "" else active_since  # Verwende aktuelles Datum, falls leer
        }
        # Speichere neues Teammitglied
        data.append(new_member)
        write((Path(__file__).resolve().parent.parent / 'data' / 'teammitglieder.json'), data)
        print("Neues Teammitglied hinzugefügt:", name_input)

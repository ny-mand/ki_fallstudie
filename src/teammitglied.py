import datetime as dt
from src.dateiverwaltung import *

class TeamMember:
    def __init__(self, member_id, name, job_title, active_since):
        self.member_id = member_id
        self.name = name
        self.job_title = job_title
        self.active_since = active_since

    @staticmethod
    def member_exists(name):
        data = read((Path(__file__).resolve().parent.parent / 'data' / 'teammitglieder.json'))
        for member in data:
            if member['name'].lower() == name.lower():
                return True
        else:
            return False

    @staticmethod
    def add_member(active_since = dt.datetime.now().date().isoformat()):
        data = read((Path(__file__).resolve().parent.parent / 'data' / 'teammitglieder.json'))
        if data:
            new_id = data[-1]['member_id'] + 1
        else:
            new_id = 1

        name_input = input("Gib den Namen des Teammitglieds ein: ")
        job_title_input = input("Gib die Berufsbezeichnung des Teammitglieds ein: ")
        active_since_input = input("Gib das Eintrittsdatum ein (YYYY-MM-DD) oder leer lassen: ").strip()
        new_member = {
            "member_id": new_id,
            "name": name_input,
            "job_title": job_title_input,
            "active_since": active_since_input if active_since_input != "" else active_since
        }
        data.append(new_member)
        write((Path(__file__).resolve().parent.parent / 'data' / 'teammitglieder.json'), data)
        print("Neues Teammitglied hinzugefügt:", name_input)


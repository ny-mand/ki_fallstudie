import datetime as dt
from pathlib import Path
from src.dateiverwaltung import *

class TeamMember:
    def __init__(self, member_id, name, job_title, active_since, *allocated_tasks):
        self.member_id = member_id
        self.name = name
        self.job_title = job_title
        self.active_since = active_since
        self.allocated_tasks = allocated_tasks

    def get_member_id(self):
        return self.member_id
    def get_name(self):
        return self.name
    def get_job_title(self):
        return self.job_title
    def get_active_since(self):
        return self.active_since

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


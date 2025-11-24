import datetime as dt
from src.item import Item

class Project(Item):
    def __init__(self, name, description, member_list, task_list, date_start, date_due, priority, date_created=dt.datetime.now()):
        super().__init__(name, description)
        self.date_created = date_created
        self.member_list = member_list
        self.task_list = task_list
        self.date_start = date_start
        self.date_due = date_due
        self.priority = priority

    def get_name(self):
        return self.name
    def get_description(self):
        return self.description
    def get_member_list(self):
        return self.member_list
    def get_task_list(self):
        return self.task_list
    def get_date_start(self):
        return self.date_start
    def get_date_end(self):
        return self.date_due
    def get_priority(self):
        return self.priority
    def get_date_created(self):
        return self.date_created

    def is_running(self):
        current_date = dt.datetime.now()
        if self.date_start <= current_date:
            return True
        elif current_date >= self.date_due:
            return "Overdue"
        else:
            return False



    #def create_project(self):
    #    return Project(

project_1 = Project("Projekt Alpha", "2024-01-15")

print(project_1.get_name())
#from src.item import Item
from src.aufgabe import Task

class Person:
    def __init__(self, name):
        self.name = name

class TeamMember(Person):
    def __init__(self, name, *allocated_tasks, job_title):
        super().__init__(name)
        self.allocated_tasks = allocated_tasks
        self.job_title = job_title
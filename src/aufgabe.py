import datetime as dt
from src.item import Item

class Task(Item):
    def __init__(self, name, description, date_due, priority, *allocated_to):
        super().__init__(name, description)
        self.date_due = date_due
        self.allocated_to = allocated_to
        self.priority = priority

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
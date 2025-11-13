class Projekt_Base:
    def __init__(self, name, date_created):
        self.name = name
        self.date_created = date_created

    def get_name(self):
        return self.name
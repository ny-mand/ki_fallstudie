import datetime as dt

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def get_name(self):
        return self.name
    def get_description(self):
        return self.description

    @staticmethod
    def create_item():
        return Item(input("Gib den Namen deines Items ein."), input("Gib eine Beschreibung ein."))

test = Item.create_item()
print(test.get_name())
print(test.get_description())
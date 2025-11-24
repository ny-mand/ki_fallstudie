from src.dateiverwaltung import Manager

class CLI:
    def __init__(self):
        self.manager = Manager()

    def show_menu(self):
        print("Willkommen im Projektmanagement-Tool")
        print("--- Hauptmenü ---")
        print("Projekte anzeigen (1)")
        print("Teammitglieder anzeigen (2)")
        print("Aufgaben anzeigen (3)")
        print("Neu erstellen: (4)")
        print("Beenden (0)")
        self.test()

    def run(self):
        while True:
            self.show_menu()
            user_input = input("Wähle eine Option: ")
            if user_input == "0":
                print("-" *20, "\nProgramm beendet.")
                break
            elif user_input == "1":
                print("Projekte anzeigen ausgewählt.")
            elif user_input == "2":
                print("Teammitglieder anzeigen ausgewählt.")
    @staticmethod
    def test():
        print("CLI Test erfolgreich!")

    def show_projects



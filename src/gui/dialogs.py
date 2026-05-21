from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename

def dialog_quit():
    if askokcancel("Sicher?", "Möchtest du WIRKLICH BEENDEN?"):
        quit()

def dialog_delete():
    if askokcancel("Löschen?", "Möchtest du das ausgewählte Item wirklich löschen?"):
        return True
    else:
        print("Vorgang abgebrochen")

def dialog_confirm():
    if askokcancel("Bestätigen?", "Möchtest du das Item wirklich erstellen?"):
        return True
    else:
        print("Vorgang abgebrochen")

def dialog_no_project():
    pass

def dialog_file():
    if askopenfilename():
        print("Datei geöffnet")
    else:
        print("Vorgang abgebrochen")

def dialog_creation_error(message="Eine Eingabe ist ungültig!"): # ggf. zu general error dialog umbauen
    showwarning("Fehler", message=message)
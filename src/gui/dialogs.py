from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename

def dialog_quit():
    if askokcancel("Are you sure?", "Do your REALLY want to QUIT?"):
        quit()

def dialog_no_project():
    pass

def dialog_file():
    if askopenfilename():
        print("Datei geöffnet")
    else:
        print("Vorgang abgebrochen")
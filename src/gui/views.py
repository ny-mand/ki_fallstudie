from tkinter import *
from src.gui.design_elements import *

def create_test_screen(parent):
    """Erstellt den Test-Screen Frame"""
    frm_test_screen = Frame(parent)
    
    Label(frm_test_screen, text="test label").pack()
    Button(frm_test_screen, text="Zurück", command=lambda: parent.event_generate("<<ShowMainScreen>>")).pack()
    scrollbar = Scrollbar(frm_test_screen)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox = Listbox(frm_test_screen, yscrollcommand=scrollbar.set, height=5)
    listbox.pack(side=LEFT, fill=BOTH, expand=True)
    for values in range(100):
        listbox.insert(END, values)
    scrollbar.config(command=listbox.yview)


    return frm_test_screen

def mainscreen(parent):
    pass

def project_screen(parent):
    pass

def member_screen(parent):
    pass

def task_screen(parent):
    pass
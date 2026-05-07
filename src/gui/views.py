from tkinter import *
from pathlib import Path
from src.gui.design_elements import *
from src.dateiverwaltung import read

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
    frame = ModernCard(parent)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)

    # Head
    head = ModernCard(frame)
    head.columnconfigure(0, weight=4)
    head.columnconfigure(1, weight=1)
    head.grid(row=0, column=0, sticky="ew")

    header = HeaderLabel(head, text="Projekte")
    header.grid(row=0, column=1, sticky="w")

    back_button = ModernButton(head, text="<-")
    back_button.grid(row=0, column=0, sticky="w")

    # Buttons
    controls = ModernCard(frame)
    controls.columnconfigure(0, weight=1)
    controls.columnconfigure(1, weight=1)
    controls.columnconfigure(2, weight=1)
    controls.grid(row=1, column=0, sticky="ew")

    filter = ModernButton(controls, text="Filtern")
    filter.grid(row=0, column=0, sticky="ew", padx=10)
    create = ModernButton(controls, text="Erstellen")
    create.grid(row=0, column=1, sticky="ew", padx=10)
    delete = ModernButton(controls, text="Löschen")
    delete.grid(row=0, column=2, sticky="ew", padx=10)

    # List
    proj_list = ModernCard(frame)
    proj_list.grid(row=2, column=0, sticky="nsew")

    proj_listbox = Listbox(proj_list)
    #proj_listbox.pack(fill=BOTH, expand=True)
    proj_listbox.grid(sticky="nsew")

    
    # Projekte aus projekte.json laden
    file_path = Path(__file__).resolve().parent.parent / 'data' / 'projekte.json'
    projects = read(file_path)
    for project in projects:
        proj_listbox.insert(END, project['name'])

    return frame

def member_screen(parent):
    pass

def task_screen(parent):
    pass
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
    frame.rowconfigure(2, weight=1)

    # Head
    head = ModernCard(frame)
    head.columnconfigure(0, weight=0)
    head.columnconfigure(1, weight=1)
    head.grid(row=0, column=0, sticky="ew", pady=(0, 12))

    back_button = ModernButton(head, text="◀", font=("Segoe UI", 13, "bold"), padx=14, pady=8)
    back_button.grid(row=0, column=0, sticky="w")

    header = HeaderLabel(head, text="Projekte")
    header.grid(row=0, column=1, sticky="w", padx=(50, 0))

    # Buttons
    controls = ModernCard(frame)
    controls.columnconfigure(0, weight=1)
    controls.columnconfigure(1, weight=1)
    controls.columnconfigure(2, weight=1)
    controls.grid(row=1, column=0, sticky="ew", pady=(0, 12))

    filter = ModernButton(controls, text="Filtern")
    filter.grid(row=0, column=0, sticky="ew", padx=(80, 80))
    create = ModernButton(controls, text="Erstellen")
    create.grid(row=0, column=1, sticky="ew", padx=7)
    delete = ModernButton(controls, text="Löschen")
    delete.grid(row=0, column=2, sticky="ew", padx=(80, 80))

    # List
    proj_list = ModernCard(frame)
    proj_list.grid(row=2, column=0, sticky="nsew")
    proj_list.columnconfigure(0, weight=1)
    proj_list.rowconfigure(0, weight=1)

    # Projekte aus projekte.json laden
    file_path = Path(__file__).resolve().parent.parent.parent / 'data' / 'projekte.json'
    projects = read(file_path)

    # Treeview für Projektübersicht
    proj_treeview = ModernTreeview(proj_list, columns=("id", "name", "description", "priority", "due_date"))
    proj_treeview.grid(row=0, column=0, sticky="nsew")
    
    # Header-Zeile konfigurieren
    proj_treeview.tree.heading("#0", text="")
    proj_treeview.tree.column("#0", width=0, stretch=False)
    
    proj_treeview.heading("id", text="ID")
    proj_treeview.column("id", width=50, anchor="center", stretch=False)
    
    proj_treeview.heading("name", text="Name")
    proj_treeview.column("name", width=150, anchor="w")
    
    proj_treeview.heading("description", text="Beschreibung")
    proj_treeview.column("description", width=300, anchor="w")
    
    proj_treeview.heading("priority", text="Priorität")
    proj_treeview.column("priority", width=120, anchor="center", stretch=False)
    
    proj_treeview.heading("due_date", text="Fällig")
    proj_treeview.column("due_date", width=200, anchor="center", stretch=False)
    
    # Projekte einfügen
    for project in projects:
        proj_treeview.insert(
            "",
            "end",
            values=(
                project.get("project_id", ""),
                project.get("name", ""),
                project.get("description", ""),
                project.get("priority", ""),
                project.get("date_due", "")
            )
        )

    return frame

def member_screen(parent):
    pass

def task_screen(parent):
    pass
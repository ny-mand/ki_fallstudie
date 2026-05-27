from tkinter import *
from pathlib import Path
from src.gui.design_elements import *
from src.dateiverwaltung import read
from src.logic import *
from src.projekt import Project
from tkinter import ttk  # Wird für das Dropdown-Menü (Combobox) benötigt
from src.dateiverwaltung import read
from src.utils import validate_date_format, format_to_german_date

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

def mainscreen(parent, project_screen=None):
    frame = ModernCard(parent, padx=75, pady=75)
    frame.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Konfiguriere die Spalten und Zeilen
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(0, weight=0)  # Header - feste Größe
    frame.rowconfigure(1, weight=1)  # Button-Zeile 1
    frame.rowconfigure(2, weight=1)  # Button-Zeile 2
    frame.rowconfigure(3, weight=1)  # Button-Zeile 3

    header_label = HeaderLabel(frame, text="Projektmanagement - Hauptmenü")
    header_label.grid(row=0, columnspan=2, sticky="ew", pady=(0, 40))

    # Erste Reihe
    projects_button = ModernButton(frame, text="Projekte anzeigen", command=lambda: project_screen.tkraise() if project_screen else None, padx=35, pady=22, font=("Segoe UI", 12, "bold"))
    projects_button.grid(row=1, column=0, sticky="nsew", padx=(0, 36), pady=(0, 36))

    create_project_button = ModernButton(frame, text="Projekt erstellen", padx=35, pady=22, font=("Segoe UI", 12, "bold"))
    create_project_button.grid(row=1, column=1, sticky="nsew", padx=(36, 0), pady=(0, 36))

    # Zweite Reihe
    member_button = ModernButton(frame, text="Member anzeigen", padx=35, pady=22, font=("Segoe UI", 12, "bold"))
    member_button.grid(row=2, column=0, sticky="nsew", padx=(0, 36), pady=(0, 36))

    add_member_button = ModernButton(frame, text="Member hinzufügen", padx=35, pady=22, font=("Segoe UI", 12, "bold"))
    add_member_button.grid(row=2, column=1, sticky="nsew", padx=(36, 0), pady=(0, 36))

    # Dritte Reihe
    tasks_button = ModernButton(frame, text="Aufgaben anzeigen", padx=35, pady=22, font=("Segoe UI", 12, "bold"))
    tasks_button.grid(row=3, column=0, sticky="nsew", padx=(0, 36), pady=0)

    add_task_button = ModernButton(frame, text="Aufgabe hinzufügen", padx=35, pady=22, font=("Segoe UI", 12, "bold"))
    add_task_button.grid(row=3, column=1, sticky="nsew", padx=(36, 0), pady=0)

    return frame

def project_screen(parent, back_screen):
    frame = ModernCard(parent)
    frame.grid(row=0, column=0, sticky="nsew")
    # frame.place(x=0, y=0, relwidth=1, relheight=1)
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)

    file_path = Path(__file__).resolve().parent.parent.parent / 'data' / 'projekte.json'

    # Head
    head = ModernCard(frame)
    head.columnconfigure(0, weight=0)
    head.columnconfigure(1, weight=1)
    head.grid(row=0, column=0, sticky="ew", pady=(0, 12))

    back_button = ModernButton(head, text="◀", command=lambda: raise_screen(back_screen), font=("Segoe UI", 13, "bold"), padx=14, pady=8)
    back_button.grid(row=0, column=0, sticky="w")

    header = HeaderLabel(head, text="Projekte")
    header.grid(row=0, column=1, sticky="w", padx=(50, 0))

    # Buttons
    controls = ModernCard(frame)
    controls.columnconfigure(0, weight=1)
    controls.columnconfigure(1, weight=1)
    controls.columnconfigure(2, weight=1)
    controls.grid(row=1, column=0, sticky="ew", pady=(0, 12))

    # List
    proj_list = ModernCard(frame)
    proj_list.grid(row=2, column=0, sticky="nsew")
    proj_list.columnconfigure(0, weight=1)
    proj_list.rowconfigure(0, weight=1)

    # Projekte aus projekte.json laden
    projects = read(file_path)

    # TODO in logic verschieben?
    def refresh_projects(data_to_show=None):
        proj_treeview.tree.delete(*proj_treeview.tree.get_children())
        # Wenn keine gefilterten Daten übergeben wurden, lade alle Projekte neu
        display_list = data_to_show if data_to_show is not None else read(file_path)
        for project in display_list:
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

    def delete_selected_project():
        selected_name = proj_treeview.get_selected_name()
        if not selected_name:
            return
        delete_item("projekt", selected_name)
        refresh_projects()

    def create_new_project():
        Project.create_project()
        refresh_projects()

    def delete_selected_project():
        selected_name = proj_treeview.get_selected_name()
        if not selected_name:
            return
        delete_item("projekt", selected_name)
        refresh_projects()

    def create_new_project():
        Project.create_project() #TODO austauschen mit raise_screen(create_project_screen)
        refresh_projects()

    def open_filter_window():
        filter_popup = Toplevel(parent)
        filter_popup.title("Projekte filtern & sortieren")
        filter_popup.geometry("460x260")
        filter_popup.configure(bg="#2d2d2d")
        filter_popup.resizable(False, False)

        Label(filter_popup, text="Filter / Sortierung wählen:", bg="#2d2d2d", fg="white",
              font=("Segoe UI", 10, "bold")).pack(pady=(15, 5))

        choice_var = StringVar()
        filter_choice = ttk.Combobox(filter_popup, textvariable=choice_var, state="readonly", width=42)
        filter_choice["values"] = [
            "Alle Projekte anzeigen",
            "Nach bestimmter Priorität filtern",
            "Nach Startdatum filtern (ab Datum)",
            "Nach Fälligkeitsdatum sortieren (aufsteigend)",
            "Nach Priorität sortieren (hoch -> niedrig)"
        ]
        filter_choice.pack(pady=5)
        filter_choice.current(0)

        # Bereich für dynamische Eingabefelder (je nach Filter-Modus)
        param_frame = Frame(filter_popup, bg="#2d2d2d")
        param_frame.pack(pady=10, fill="x")

        param_label = Label(param_frame, text="Wert:", bg="#2d2d2d", fg="white")
        param_entry = Entry(param_frame, width=20, bg="#1e1e1e", fg="white", insertbackground="white", bd=1,
                            relief="flat")
        param_prio = ttk.Combobox(param_frame, values=["niedrig", "mittel", "hoch"], state="readonly", width=15)

        # Steuert, welche Felder sichtbar sind
        def on_choice_changed(event):
            param_label.pack_forget()
            param_entry.pack_forget()
            param_prio.pack_forget()

            mode = choice_var.get()
            if mode == "Nach bestimmter Priorität filtern":
                param_label.config(text="Priorität wählen:")
                param_label.pack(side="left", padx=(60, 5))
                param_prio.pack(side="left", padx=5)
                param_prio.current(0)
            elif mode == "Nach Startdatum filtern (ab Datum)":
                param_label.config(text="Datum (YYYY-MM-DD):")
                param_label.pack(side="left", padx=(60, 5))
                param_entry.pack(side="left", padx=5)
                param_entry.delete(0, END)

        filter_choice.bind("<<ComboboxSelected>>", on_choice_changed)

        # Verarbeitet die Auswahl analog src/filter.py
        def apply_and_close():
            all_projects = read(file_path)
            mode = choice_var.get()
            filtered_result = []

            if mode == "Alle Projekte anzeigen":
                filtered_result = all_projects

            elif mode == "Nach bestimmter Priorität filtern":
                target_prio = param_prio.get()
                filtered_result = [p for p in all_projects if p.get('priority', '').lower() == target_prio.lower()]

            elif mode == "Nach Startdatum filtern (ab Datum)":
                target_date = param_entry.get().strip()
                # Gruppen-Validierungsfunktion aus utils.py
                if not validate_date_format(target_date):
                    from tkinter import messagebox
                    messagebox.showerror("Fehler", "Ungültiges Datumsformat! Bitte YYYY-MM-DD nutzen.",
                                         parent=filter_popup)
                    return
                filtered_result = [p for p in all_projects if
                                   p.get('date_start') and p.get('date_start') >= target_date]

            elif mode == "Nach Fälligkeitsdatum sortieren (aufsteigend)":
                all_projects.sort(key=lambda p: p.get('date_due', ''))
                filtered_result = all_projects

            elif mode == "Nach Priorität sortieren (hoch -> niedrig)":
                prio_map = {"hoch": 3, "mittel": 2, "niedrig": 1}
                all_projects.sort(key=lambda p: prio_map.get(p.get('priority', '').lower(), 0), reverse=True)
                filtered_result = all_projects

            # Aktualisiert das Hauptfenster mit den gefilterten Daten
            refresh_projects(filtered_result)
            filter_popup.destroy()

        apply_btn = ModernButton(filter_popup, text="Anwenden", command=apply_and_close)
        apply_btn.pack(pady=15)


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


    filter = ModernButton(controls, text="Filtern", command=open_filter_window)
    filter.grid(row=0, column=0, sticky="ew", padx=(80, 80))

    create = ModernButton(controls, text="Erstellen", command=create_new_project)
    create.grid(row=0, column=1, sticky="ew", padx=7)

    delete = ModernButton(
        controls,
        text="Löschen",
        command=delete_selected_project
    )
    delete.grid(row=0, column=2, sticky="ew", padx=(80, 80))

    return frame




def member_screen(parent):
    frame = ModernCard(parent)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(1, weight=0)
    frame.rowconfigure(2, weight=1)

    file_path = Path(__file__).resolve().parent.parent.parent / "data" / "teammitglieder.json"

    # Head
    head = ModernCard(frame)
    head.columnconfigure(0, weight=0)
    head.columnconfigure(1, weight=1)
    head.grid(row=0, column=0, sticky="ew", pady=(0, 12))

    back_button = ModernButton(head, text="◀", font=("Segoe UI", 13, "bold"), padx=14, pady=8)
    back_button.grid(row=0, column=0, sticky="w")

    header = HeaderLabel(head, text="Teammitglieder")
    header.grid(row=0, column=1, sticky="w", padx=(50, 0))

    # Buttons
    controls = ModernCard(frame)
    controls.columnconfigure(0, weight=1)
    controls.columnconfigure(1, weight=1)
    controls.columnconfigure(2, weight=1)
    controls.grid(row=1, column=0, sticky="ew", pady=(0, 12))

    # List
    member_list = ModernCard(frame)
    member_list.grid(row=2, column=0, sticky="nsew")
    member_list.columnconfigure(0, weight=1)
    member_list.rowconfigure(0, weight=1)

    def refresh_members(data_to_show=None):
        member_treeview.tree.delete(*member_treeview.tree.get_children())
        display_list = data_to_show if data_to_show is not None else read(file_path)

        for member in display_list:
            member_treeview.insert(
                "",
                "end",
                values=(
                    member.get("member_id", ""),
                    member.get("name", ""),
                    member.get("job_title", ""),
                    member.get("active_since", "")
                )
            )

    def delete_selected_team_member():
        selected_name = member_treeview.get_selected_name()
        if not selected_name:
            return
        delete_item("teammitglied", selected_name)
        refresh_members()

    def create_new_team_member():
        # TODO austauschen mit raise_screen(create_member_screen)
        pass

    def assign_selected_task_to_member():
        selected_name = member_treeview.get_selected_name()
        if not selected_name:
            return
        assign("assign task", task_name=selected_name)

    def unassign_selected_task_from_member():
        selected_name = member_treeview.get_selected_name()
        if not selected_name:
            return
        assign("unassign task", task_name=selected_name)

    member_treeview = ModernTreeview(
        member_list,
        columns=("id", "name", "job_title", "active_since")
    )
    member_treeview.grid(row=0, column=0, sticky="nsew")

    member_treeview.tree.heading("#0", text="")
    member_treeview.tree.column("#0", width=0, stretch=False)

    member_treeview.heading("id", text="ID")
    member_treeview.column("id", width=60, anchor="center", stretch=False)

    member_treeview.heading("name", text="Name")
    member_treeview.column("name", width=180, anchor="w")

    member_treeview.heading("job_title", text="Jobtitel")
    member_treeview.column("job_title", width=220, anchor="w")

    member_treeview.heading("active_since", text="Aktiv seit")
    member_treeview.column("active_since", width=160, anchor="center", stretch=False)

    refresh_members()

    assign_button = ModernButton(controls, text="Zuweisen", command=assign_selected_task_to_member)
    assign_button.grid(row=0, column=0, sticky="ew", padx=(80, 7))

    create_button = ModernButton(controls, text="Erstellen", command=create_new_team_member)
    create_button.grid(row=0, column=1, sticky="ew", padx=7)

    delete_button = ModernButton(controls, text="Löschen", command=delete_selected_team_member)
    delete_button.grid(row=0, column=2, sticky="ew", padx=(7, 80))

    return frame
    # nutzt TeamMember.add_member() zum erstellen -> TODO def create_new_team_member() wie in project_screen
    # nutzt delete_item("teammitglied", selected_name) zum löschen -> TODO def delete_selected_team_member()
    # nutzt assign("assign task", task_name=selected_name)
    # nutzt assign("unassign task", task_name=selected_name)

def task_screen(parent):
    pass
    # nutzt Task.create_task() zum erstellen -> TODO def create_new_task() wie in project_screen
    # nutzt delete_item("aufgabe", selected_name) zum löschen -> TODO def delete_selected_task()
    # nutzt assign("assign member", member_name=selected_name)
    # nutzt assign("unassign member", member_name=selected_name)

def create_project_screen(parent):
    pass
    # Formular um Nutzereingaben für Projekterstellung zu sammeln
    # create_new_project() am besten erst bei click von Bestätigen Button callen (Klassenfunktionen haben teils return, könnte sonst Probleme verursachen)
    # name, description, date_start (YYYY-MM-DD), date_due (YYYY-MM-DD), priority (niedrig (1), mittel (2), hoch (3)) # TODO priority in dropdown umbauen
    # erwartetes Verhalten: Formular ausfüllen, bestätigen / abbrechen Button, bei Fehleingabe dialog mit entsprechendem Fehler (per argument übergeben), nur fehlerhaftes Feld wird geleert, Rest bleibt bestehen bis Erstellen erfolgreich

def create_member_screen(parent):
    frame = ModernCard(parent)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=0)
    frame.rowconfigure(1, weight=1)

    # Head
    head = ModernCard(frame)
    head.columnconfigure(0, weight=0)
    head.columnconfigure(1, weight=1)
    head.grid(row=0, column=0, sticky="ew", pady=(0, 12))

    back_button = ModernButton(head, text="◀", font=("Segoe UI", 13, "bold"), padx=14, pady=8)
    back_button.grid(row=0, column=0, sticky="w")

    header = HeaderLabel(head, text="Teammitglied erstellen")
    header.grid(row=0, column=1, sticky="w", padx=(50, 0))

    # Formular
    form_card = ModernCard(frame)
    form_card.grid(row=1, column=0, sticky="n", padx=80, pady=20)
    form_card.columnconfigure(0, weight=0)
    form_card.columnconfigure(1, weight=1)

    name_label = TextLabel(form_card, text="Name:")
    name_label.grid(row=0, column=0, sticky="w", padx=(0, 12), pady=8)
    name_entry = ModernEntry(form_card)
    name_entry.grid(row=0, column=1, sticky="ew", pady=8)

    job_title_label = TextLabel(form_card, text="Jobtitel:")
    job_title_label.grid(row=1, column=0, sticky="w", padx=(0, 12), pady=8)
    job_title_entry = ModernEntry(form_card)
    job_title_entry.grid(row=1, column=1, sticky="ew", pady=8)

    active_since_label = TextLabel(form_card, text="Aktiv seit:")
    active_since_label.grid(row=2, column=0, sticky="w", padx=(0, 12), pady=8)
    active_since_entry = ModernEntry(form_card)
    active_since_entry.grid(row=2, column=1, sticky="ew", pady=8)

    hint_label = TextLabel(form_card, text="Format: YYYY-MM-DD", muted=True)
    hint_label.grid(row=3, column=1, sticky="w", pady=(0, 12))

    button_frame = ModernCard(form_card)
    button_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(12, 0))
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)

    def clear_entry(widget):
        widget.entry.delete(0, END)

    def submit_member():
        name = name_entry.get().strip()
        job_title = job_title_entry.get().strip()
        active_since = active_since_entry.get().strip()

        if not name:
            dialog_creation_error("Bitte einen Namen eingeben.")
            clear_entry(name_entry)
            return

        if TeamMember.member_exists(name):
            dialog_creation_error("Ein Teammitglied mit diesem Namen existiert bereits.")
            clear_entry(name_entry)
            return

        if not job_title:
            dialog_creation_error("Bitte einen Jobtitel eingeben.")
            clear_entry(job_title_entry)
            return

        if not active_since:
            dialog_creation_error("Bitte ein Datum eingeben.")
            clear_entry(active_since_entry)
            return

        if not validate_date_format(active_since):
            dialog_creation_error("Ungültiges Datumsformat. Bitte YYYY-MM-DD nutzen.")
            clear_entry(active_since_entry)
            return

        if not dialog_confirm():
            return

        TeamMember.add_member(name, job_title, active_since)

        clear_entry(name_entry)
        clear_entry(job_title_entry)
        clear_entry(active_since_entry)

    def cancel_creation():
        clear_entry(name_entry)
        clear_entry(job_title_entry)
        clear_entry(active_since_entry)
        # TODO austauschen mit raise_screen(member_screen)

    create_button = ModernButton(button_frame, text="Bestätigen", command=submit_member)
    create_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))

    cancel_button = ModernButton(button_frame, text="Abbrechen", command=cancel_creation)
    cancel_button.grid(row=0, column=1, sticky="ew", padx=(8, 0))

    return frame
    # siehe create_project_screen()
    # name, job_title, active_since = YYYY-MM-DD (hat now by default)

def create_task_screen(parent):
    pass
    # siehe create_project_screen()
    # name, description, priority (niedrig (1), mittel (2), hoch (3)), date_due # TODO priority in dropdown umbauen

def filter_settings_screen(parent):
    pass
    # öffnet separates Fenster um Filtereinstellungen anzupassen
    # sollten nach Möglichkeit gespeichert werden und auf die Projektliste angewendet werden, ohne eine weitere Liste zu erstellen

def choose_item_screen(parent):
    pass
    # öffnet separates Fenster mit Projektliste, um auszuwählen, wo Task / Member hinzugefügt werden soll
    # ggf. auch für Teammitglied, um Tasks zuzuweisen
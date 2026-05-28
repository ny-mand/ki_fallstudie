from tkinter import *
from pathlib import Path
from src.gui.design_elements import *
from src.dateiverwaltung import read
from src.logic import *
from src.projekt import Project
from tkinter import ttk  # Wird für Treeview und das Dropdown-Menü (Combobox) benötigt
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

def mainscreen(parent, show_projects=None, show_members=None, show_tasks=None, show_create_project=None, show_create_member=None, show_create_task=None):
    GAP = 80  # Abstand zwischen und um die Buttons — anpassen wie gewünscht

    frame = ModernCard(parent, padx=GAP, pady=GAP)  # Außenabstand = GAP
    frame.place(x=0, y=0, relwidth=1, relheight=1)

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(0, weight=0)
    frame.rowconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)
    frame.rowconfigure(3, weight=1)

    header_label = HeaderLabel(frame, text="Projektmanagement - Hauptmenü")
    header_label.grid(row=0, columnspan=2, sticky="ew", pady=(0, GAP))

    HALF = GAP // 2  # Halber Abstand für die Mitte zwischen den Buttons

    # Erste Reihe
    projects_button = ModernButton(frame, text="Projekte anzeigen", command=lambda: show_projects() if show_projects else None, padx=20, pady=12, font=("Segoe UI", 14, "bold"))
    projects_button.grid(row=1, column=0, sticky="nsew", padx=(0, HALF), pady=(0, GAP))

    create_project_button = ModernButton(frame, text="Projekt erstellen", command=lambda: show_create_project() if show_create_project else None, padx=20, pady=12, font=("Segoe UI", 14, "bold"))
    create_project_button.grid(row=1, column=1, sticky="nsew", padx=(HALF, 0), pady=(0, GAP))

    # Zweite Reihe
    member_button = ModernButton(frame, text="Teammitglieder anzeigen", command=lambda: show_members() if show_members else None, padx=20, pady=12, font=("Segoe UI", 14, "bold"))
    member_button.grid(row=2, column=0, sticky="nsew", padx=(0, HALF), pady=(0, GAP))

    add_member_button = ModernButton(frame, text="Teammitglied hinzufügen", command=lambda: show_create_member() if show_create_member else None, padx=20, pady=12, font=("Segoe UI", 14, "bold"))
    add_member_button.grid(row=2, column=1, sticky="nsew", padx=(HALF, 0), pady=(0, GAP))

    # Dritte Reihe
    tasks_button = ModernButton(frame, text="Aufgaben anzeigen", command=lambda: show_tasks() if show_tasks else None, padx=20, pady=12, font=("Segoe UI", 14, "bold"))
    tasks_button.grid(row=3, column=0, sticky="nsew", padx=(0, HALF), pady=0)

    add_task_button = ModernButton(frame, text="Aufgabe hinzufügen", command=lambda: show_create_task() if show_create_task else None, padx=20, pady=12, font=("Segoe UI", 14, "bold"))
    add_task_button.grid(row=3, column=1, sticky="nsew", padx=(HALF, 0), pady=0)

    return frame

def project_screen(parent, back_command=None, create_command=None):
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

    back_button = ModernButton(head, text="◀", command=lambda: back_command() if back_command else None, font=("Segoe UI", 13, "bold"), padx=14, pady=8)
    back_button.grid(row=0, column=0, sticky="w")

    header = HeaderLabel(head, text="Projekte")
    header.grid(row=0, column=1, sticky="w", padx=(50, 0))

    # Buttons
    controls = ModernCard(frame)
    controls.columnconfigure(0, weight=1, uniform="project_actions")
    controls.columnconfigure(1, weight=1, uniform="project_actions")
    controls.columnconfigure(2, weight=1, uniform="project_actions")
    controls.grid(row=1, column=0, sticky="ew", pady=(0, 12))

    # List
    proj_list = ModernCard(frame)
    proj_list.grid(row=2, column=0, sticky="nsew")
    proj_list.columnconfigure(0, weight=1)
    proj_list.rowconfigure(0, weight=1)

    # Projekte aus projekte.json laden
    projects = read(file_path)

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

    frame.refresh_projects = refresh_projects

    def delete_selected_project():
        selected_name = proj_treeview.get_selected_name()
        if not selected_name:
            return
        delete_item("projekt", selected_name)
        refresh_projects()

    def delete_selected_project():
        selected_name = proj_treeview.get_selected_name()
        if not selected_name:
            return
        delete_item("projekt", selected_name)
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
    filter.grid(row=0, column=0, sticky="ew", padx=12)

    create = ModernButton(controls, text="Erstellen", command=lambda: create_command() if create_command else None)
    create.grid(row=0, column=1, sticky="ew", padx=12)

    delete = ModernButton(
        controls,
        text="Löschen",
        command=delete_selected_project
    )
    delete.grid(row=0, column=2, sticky="ew", padx=12)

    return frame

def member_screen(parent, back_command=None, create_command=None, assign_command=None):
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

    back_button = ModernButton(head, text="◀", command=lambda: back_command() if back_command else None, font=("Segoe UI", 13, "bold"), padx=14, pady=8)
    back_button.grid(row=0, column=0, sticky="w")

    header = HeaderLabel(head, text="Teammitglieder")
    header.grid(row=0, column=1, sticky="w", padx=(50, 0))

    # Buttons
    controls = ModernCard(frame)
    controls.columnconfigure(0, weight=1, uniform="member_actions")
    controls.columnconfigure(1, weight=1, uniform="member_actions")
    controls.columnconfigure(2, weight=1, uniform="member_actions")
    controls.columnconfigure(3, weight=1, uniform="member_actions")
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

    frame.refresh_members = refresh_members

    def delete_selected_team_member():
        selected_name = member_treeview.get_selected_name()
        if not selected_name:
            return
        delete_item("teammitglied", selected_name)
        refresh_members()

    def assign_selected_member_to_project():
        selected_name = member_treeview.get_selected_name()
        if not selected_name:
            dialog_creation_error("Bitte zuerst ein Teammitglied auswählen.")
            return
        if assign_command:
            assign_command(selected_name, mode=assignment_mode["value"])

    assignment_mode = {"value": "assign"}

    def update_assignment_controls():
        is_assign_mode = assignment_mode["value"] == "assign"
        assign_button.config(text="Zuweisen" if is_assign_mode else "Entfernen")
        mode_button.config(text="Modus umschalten")

    def toggle_assignment_mode():
        assignment_mode["value"] = "unassign" if assignment_mode["value"] == "assign" else "assign"
        update_assignment_controls()

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

    mode_button = ModernButton(controls, text="Modus umschalten", command=toggle_assignment_mode, padx=18, pady=10)
    mode_button.grid(row=0, column=0, sticky="ew", padx=12)

    assign_button = ModernButton(controls, text="Zuweisen", command=assign_selected_member_to_project)
    assign_button.grid(row=0, column=1, sticky="ew", padx=12)

    create_button = ModernButton(controls, text="Erstellen", command=lambda: create_command() if create_command else None)
    create_button.grid(row=0, column=2, sticky="ew", padx=12)

    delete_button = ModernButton(controls, text="Löschen", command=delete_selected_team_member)
    delete_button.grid(row=0, column=3, sticky="ew", padx=12)

    update_assignment_controls()

    return frame
    # nutzt TeamMember.add_member() zum erstellen -> TODO def create_new_team_member() wie in project_screen
    # nutzt delete_item("teammitglied", selected_name) zum löschen -> TODO def delete_selected_team_member()
    # nutzt assign("assign task", task_name=selected_name)
    # nutzt assign("unassign task", task_name=selected_name)

def task_screen(parent, back_command=None, create_command=None, assign_command=None):
    frame = ModernCard(parent)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(1, weight=0)
    frame.rowconfigure(2, weight=1)

    file_path = Path(__file__).resolve().parent.parent.parent / "data" / "aufgaben.json"

    # Head
    head = ModernCard(frame)
    head.columnconfigure(0, weight=0)
    head.columnconfigure(1, weight=1)
    head.grid(row=0, column=0, sticky="ew", pady=(0, 12))

    back_button = ModernButton(head, text="◀", command=lambda: back_command() if back_command else None, font=("Segoe UI", 13, "bold"), padx=14, pady=8)
    back_button.grid(row=0, column=0, sticky="w")

    header = HeaderLabel(head, text="Aufgaben")
    header.grid(row=0, column=1, sticky="w", padx=(50, 0))

    # Buttons
    controls = ModernCard(frame)
    controls.columnconfigure(0, weight=1, uniform="task_actions")
    controls.columnconfigure(1, weight=1, uniform="task_actions")
    controls.columnconfigure(2, weight=1, uniform="task_actions")
    controls.columnconfigure(3, weight=1, uniform="task_actions")
    controls.grid(row=1, column=0, sticky="ew", pady=(0, 12))

    # List
    task_list = ModernCard(frame)
    task_list.grid(row=2, column=0, sticky="nsew")
    task_list.columnconfigure(0, weight=1)
    task_list.rowconfigure(0, weight=1)

    def refresh_tasks(data_to_show=None):
        task_treeview.tree.delete(*task_treeview.tree.get_children())
        display_list = data_to_show if data_to_show is not None else read(file_path)

        for task in display_list:
            task_treeview.insert(
                "",
                "end",
                values=(
                    task.get("task_id", ""),
                    task.get("name", ""),
                    task.get("description", ""),
                    task.get("priority", ""),
                    task.get("date_due", "")
                )
            )

    frame.refresh_tasks = refresh_tasks

    def delete_selected_task():
        selected_name = task_treeview.get_selected_name()
        if not selected_name:
            return
        delete_item("aufgabe", selected_name)
        refresh_tasks()

    def assign_selected_task_to_member():
        selected_name = task_treeview.get_selected_name()
        if not selected_name:
            dialog_creation_error("Bitte zuerst eine Aufgabe auswählen.")
            return
        if assign_command:
            assign_command(selected_name, mode=assignment_mode["value"])

    assignment_mode = {"value": "assign"}

    def update_assignment_controls():
        is_assign_mode = assignment_mode["value"] == "assign"
        assign_button.config(text="Zuweisen" if is_assign_mode else "Entfernen")
        mode_button.config(text="Modus umschalten")

    def toggle_assignment_mode():
        assignment_mode["value"] = "unassign" if assignment_mode["value"] == "assign" else "assign"
        update_assignment_controls()

    task_treeview = ModernTreeview(
        task_list,
        columns=("id", "name", "description", "priority", "date_due")
    )
    task_treeview.grid(row=0, column=0, sticky="nsew")

    task_treeview.tree.heading("#0", text="")
    task_treeview.tree.column("#0", width=0, stretch=False)

    task_treeview.heading("id", text="ID")
    task_treeview.column("id", width=60, anchor="center", stretch=False)

    task_treeview.heading("name", text="Name")
    task_treeview.column("name", width=180, anchor="w")

    task_treeview.heading("description", text="Beschreibung")
    task_treeview.column("description", width=320, anchor="w")

    task_treeview.heading("priority", text="Priorität")
    task_treeview.column("priority", width=120, anchor="center", stretch=False)

    task_treeview.heading("date_due", text="Fällig")
    task_treeview.column("date_due", width=160, anchor="center", stretch=False)

    refresh_tasks()

    mode_button = ModernButton(controls, text="Modus umschalten", command=toggle_assignment_mode, padx=18, pady=10)
    mode_button.grid(row=0, column=0, sticky="ew", padx=12)

    assign_button = ModernButton(controls, text="Zuweisen", command=assign_selected_task_to_member)
    assign_button.grid(row=0, column=1, sticky="ew", padx=12)

    create_button = ModernButton(controls, text="Erstellen", command=lambda: create_command() if create_command else None)
    create_button.grid(row=0, column=2, sticky="ew", padx=12)

    delete_button = ModernButton(controls, text="Löschen", command=delete_selected_task)
    delete_button.grid(row=0, column=3, sticky="ew", padx=12)

    update_assignment_controls()

    return frame
    # nutzt Task.create_task() zum erstellen -> TODO def create_new_task() wie in project_screen
    # nutzt delete_item("aufgabe", selected_name) zum löschen -> TODO def delete_selected_task()
    # nutzt assign("assign member", member_name=selected_name)
    # nutzt assign("unassign member", member_name=selected_name)

def create_project_screen(parent, back_command=None):
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

    back_button = ModernButton(head, text="◀", command=lambda: back_command() if back_command else None, font=("Segoe UI", 13, "bold"), padx=14, pady=8)
    back_button.grid(row=0, column=0, sticky="w")

    header = HeaderLabel(head, text="Projekt erstellen")
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

    description_label = TextLabel(form_card, text="Beschreibung:")
    description_label.grid(row=1, column=0, sticky="w", padx=(0, 12), pady=8)
    description_entry = ModernEntry(form_card)
    description_entry.grid(row=1, column=1, sticky="ew", pady=8)

    date_start_label = TextLabel(form_card, text="Startdatum:")
    date_start_label.grid(row=2, column=0, sticky="w", padx=(0, 12), pady=8)
    date_start_entry = ModernEntry(form_card)
    date_start_entry.grid(row=2, column=1, sticky="ew", pady=8)

    date_due_label = TextLabel(form_card, text="Fällig bis:")
    date_due_label.grid(row=3, column=0, sticky="w", padx=(0, 12), pady=8)
    date_due_entry = ModernEntry(form_card)
    date_due_entry.grid(row=3, column=1, sticky="ew", pady=8)

    priority_label = TextLabel(form_card, text="Priorität:")
    priority_label.grid(row=4, column=0, sticky="w", padx=(0, 12), pady=8)

    priority_var = StringVar()
    priority_dropdown = ttk.Combobox(
        form_card,
        textvariable=priority_var,
        state="readonly",
        width=27,
        values=["niedrig", "mittel", "hoch"]
    )
    priority_dropdown.grid(row=4, column=1, sticky="ew", pady=8)
    priority_dropdown.current(0)

    hint_label = TextLabel(form_card, text="Datumsformat: YYYY-MM-DD", muted=True)
    hint_label.grid(row=5, column=1, sticky="w", pady=(0, 12))

    button_frame = ModernCard(form_card)
    button_frame.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(12, 0))
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)

    def clear_entry(widget):
        widget.entry.delete(0, END)

    def submit_project():
        name = name_entry.get().strip()
        description = description_entry.get().strip()
        date_start = date_start_entry.get().strip()
        date_due = date_due_entry.get().strip()
        priority_text = priority_var.get().strip()

        if not name:
            dialog_creation_error("Bitte einen Projektnamen eingeben.")
            clear_entry(name_entry)
            return

        if Project.project_exists(name):
            dialog_creation_error("Ein Projekt mit diesem Namen existiert bereits.")
            clear_entry(name_entry)
            return

        if not description:
            dialog_creation_error("Bitte eine Beschreibung eingeben.")
            clear_entry(description_entry)
            return

        if not date_start:
            dialog_creation_error("Bitte ein Startdatum eingeben.")
            clear_entry(date_start_entry)
            return

        if not validate_date_format(date_start):
            dialog_creation_error("Ungültiges Startdatum. Bitte YYYY-MM-DD nutzen.")
            clear_entry(date_start_entry)
            return

        if not date_due:
            dialog_creation_error("Bitte ein Fälligkeitsdatum eingeben.")
            clear_entry(date_due_entry)
            return

        if not validate_date_format(date_due):
            dialog_creation_error("Ungültiges Fälligkeitsdatum. Bitte YYYY-MM-DD nutzen.")
            clear_entry(date_due_entry)
            return

        if date_start > date_due:
            dialog_creation_error("Das Fälligkeitsdatum muss nach dem Startdatum liegen.")
            clear_entry(date_due_entry)
            return

        priority_map = {
            "niedrig": "1",
            "mittel": "2",
            "hoch": "3"
        }
        priority_value = priority_map.get(priority_text)

        if not priority_value:
            dialog_creation_error("Bitte eine gültige Priorität auswählen.")
            return

        if not dialog_confirm():
            return

        Project.create_project(name, description, date_start, date_due, priority_value)

        clear_entry(name_entry)
        clear_entry(description_entry)
        clear_entry(date_start_entry)
        clear_entry(date_due_entry)
        priority_dropdown.current(0)

    def cancel_creation():
        clear_entry(name_entry)
        clear_entry(description_entry)
        clear_entry(date_start_entry)
        clear_entry(date_due_entry)
        priority_dropdown.current(0)
        if back_command:
            back_command()

    create_button = ModernButton(button_frame, text="Bestätigen", command=submit_project)
    create_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))

    cancel_button = ModernButton(button_frame, text="Abbrechen", command=cancel_creation)
    cancel_button.grid(row=0, column=1, sticky="ew", padx=(8, 0))

    return frame
    # Formular um Nutzereingaben für Projekterstellung zu sammeln
    # create_new_project() am besten erst bei click von Bestätigen Button callen (Klassenfunktionen haben teils return, könnte sonst Probleme verursachen)
    # name, description, date_start (YYYY-MM-DD), date_due (YYYY-MM-DD), priority (niedrig (1), mittel (2), hoch (3)) # TODO priority in dropdown umbauen
    # erwartetes Verhalten: Formular ausfüllen, bestätigen / abbrechen Button, bei Fehleingabe dialog mit entsprechendem Fehler (per argument übergeben), nur fehlerhaftes Feld wird geleert, Rest bleibt bestehen bis Erstellen erfolgreich

def create_member_screen(parent, back_command=None):
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

    back_button = ModernButton(head, text="◀", command=lambda: back_command() if back_command else None, font=("Segoe UI", 13, "bold"), padx=14, pady=8)
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
        if back_command:
            back_command()

    create_button = ModernButton(button_frame, text="Bestätigen", command=submit_member)
    create_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))

    cancel_button = ModernButton(button_frame, text="Abbrechen", command=cancel_creation)
    cancel_button.grid(row=0, column=1, sticky="ew", padx=(8, 0))

    return frame
    # siehe create_project_screen()
    # name, job_title, active_since = YYYY-MM-DD (hat now by default)

def create_task_screen(parent, back_command=None):
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

    back_button = ModernButton(head, text="◀", command=lambda: back_command() if back_command else None, font=("Segoe UI", 13, "bold"), padx=14, pady=8)
    back_button.grid(row=0, column=0, sticky="w")

    header = HeaderLabel(head, text="Aufgabe erstellen")
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

    description_label = TextLabel(form_card, text="Beschreibung:")
    description_label.grid(row=1, column=0, sticky="w", padx=(0, 12), pady=8)
    description_entry = ModernEntry(form_card)
    description_entry.grid(row=1, column=1, sticky="ew", pady=8)

    priority_label = TextLabel(form_card, text="Priorität:")
    priority_label.grid(row=2, column=0, sticky="w", padx=(0, 12), pady=8)

    priority_var = StringVar()
    priority_dropdown = ttk.Combobox(
        form_card,
        textvariable=priority_var,
        state="readonly",
        width=27,
        values=["niedrig", "mittel", "hoch"]
    )
    priority_dropdown.grid(row=2, column=1, sticky="ew", pady=8)
    priority_dropdown.current(0)

    date_due_label = TextLabel(form_card, text="Fällig bis:")
    date_due_label.grid(row=3, column=0, sticky="w", padx=(0, 12), pady=8)
    date_due_entry = ModernEntry(form_card)
    date_due_entry.grid(row=3, column=1, sticky="ew", pady=8)

    hint_label = TextLabel(form_card, text="Datumsformat: YYYY-MM-DD", muted=True)
    hint_label.grid(row=4, column=1, sticky="w", pady=(0, 12))

    button_frame = ModernCard(form_card)
    button_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(12, 0))
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)

    def clear_entry(widget):
        widget.entry.delete(0, END)

    def submit_task():
        name = name_entry.get().strip()
        description = description_entry.get().strip()
        priority_text = priority_var.get().strip()
        date_due = date_due_entry.get().strip()

        if not name:
            dialog_creation_error("Bitte einen Aufgabennamen eingeben.")
            clear_entry(name_entry)
            return

        if Task.task_exists(name):
            dialog_creation_error("Eine Aufgabe mit diesem Namen existiert bereits.")
            clear_entry(name_entry)
            return

        if not description:
            dialog_creation_error("Bitte eine Beschreibung eingeben.")
            clear_entry(description_entry)
            return

        if not priority_text:
            dialog_creation_error("Bitte eine Priorität auswählen.")
            return

        if not date_due:
            dialog_creation_error("Bitte ein Fälligkeitsdatum eingeben.")
            clear_entry(date_due_entry)
            return

        if not validate_date_format(date_due):
            dialog_creation_error("Ungültiges Datumsformat. Bitte YYYY-MM-DD nutzen.")
            clear_entry(date_due_entry)
            return

        priority_map = {
            "niedrig": "1",
            "mittel": "2",
            "hoch": "3"
        }
        priority_value = priority_map.get(priority_text)

        if not priority_value:
            dialog_creation_error("Ungültige Priorität ausgewählt.")
            return

        if not dialog_confirm():
            return

        Task.create_task(name, description, priority_value, date_due)

        clear_entry(name_entry)
        clear_entry(description_entry)
        clear_entry(date_due_entry)
        priority_dropdown.current(0)

    def cancel_creation():
        clear_entry(name_entry)
        clear_entry(description_entry)
        clear_entry(date_due_entry)
        priority_dropdown.current(0)
        if back_command:
            back_command()

    create_button = ModernButton(button_frame, text="Bestätigen", command=submit_task)
    create_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))

    cancel_button = ModernButton(button_frame, text="Abbrechen", command=cancel_creation)
    cancel_button.grid(row=0, column=1, sticky="ew", padx=(8, 0))

    return frame
    # siehe create_project_screen()
    # name, description, priority (niedrig (1), mittel (2), hoch (3)), date_due # TODO priority in dropdown umbauen

def filter_settings_screen(parent):
    pass
    # öffnet separates Fenster um Filtereinstellungen anzupassen
    # sollten nach Möglichkeit gespeichert werden und auf die Projektliste angewendet werden, ohne eine weitere Liste zu erstellen


def resolve_project_for_member(member_name):
    projects_path = Path(__file__).resolve().parent.parent.parent / "data" / "projekte.json"
    projects = read(projects_path)
    matching_projects = []

    for project in projects:
        working_by_person = project.get("working_by_person", {})
        if member_name in working_by_person:
            matching_projects.append(project.get("name", ""))

    if len(matching_projects) == 1:
        return matching_projects[0]

    return None

def create_member_assignment_starter(
    choose_project_screen_frame,
    show_screen,
    assign_func,
    refresh_members,
    refresh_projects,
):
    def start_member_assignment(member_name, mode="assign"):
        member_name = member_name.strip()
        if not member_name:
            dialog_creation_error("Bitte zuerst ein Teammitglied auswählen.")
            return

        is_assign_mode = mode != "unassign"
        action_choice = "assign member" if is_assign_mode else "unassign member"
        screen_instruction = (
            "Wähle das Projekt aus, dem das Teammitglied zugewiesen werden soll."
            if is_assign_mode
            else "Wähle das Projekt aus, aus dem das Teammitglied entfernt werden soll."
        )

        if hasattr(choose_project_screen_frame, "set_instruction_text"):
            choose_project_screen_frame.set_instruction_text(screen_instruction)

        def confirm_project(project_name):
            project_name = project_name.strip()
            if not project_name:
                dialog_creation_error("Bitte zuerst ein Projekt auswählen.")
                return

            assign_func(action_choice, project_name=project_name, member_name=member_name)
            refresh_members()
            refresh_projects()
            show_screen("member")

        choose_project_screen_frame.set_confirm_command(confirm_project)
        show_screen("choose_project_member")

    return start_member_assignment


def create_task_assignment_starter(
    choose_member_screen_frame,
    show_screen,
    assign_func,
    refresh_tasks,
    refresh_members,
    refresh_projects,
):
    def start_task_assignment(task_name, mode="assign"):
        task_name = task_name.strip()
        if not task_name:
            dialog_creation_error("Bitte zuerst eine Aufgabe auswählen.")
            return

        is_assign_mode = mode != "unassign"
        action_choice = "assign task" if is_assign_mode else "unassign task"
        screen_instruction = (
            "Wähle das Teammitglied aus, dem die Aufgabe zugewiesen werden soll."
            if is_assign_mode
            else "Wähle das Teammitglied aus, von dem die Aufgabe entfernt werden soll."
        )

        if hasattr(choose_member_screen_frame, "set_instruction_text"):
            choose_member_screen_frame.set_instruction_text(screen_instruction)

        def confirm_member(member_name):
            member_name = member_name.strip()
            if not member_name:
                dialog_creation_error("Bitte zuerst ein Teammitglied auswählen.")
                return

            project_name = resolve_project_for_member(member_name)
            if not project_name:
                dialog_creation_error(
                    "Das Teammitglied ist keinem eindeutigen Projekt zugeordnet. Bitte Mitglied zuerst genau einem Projekt zuweisen."
                )
                return

            assign_func(
                action_choice,
                project_name=project_name,
                member_name=member_name,
                task_name=task_name,
            )
            refresh_tasks()
            refresh_members()
            refresh_projects()
            show_screen("task")

        choose_member_screen_frame.set_confirm_command(confirm_member)
        show_screen("choose_member_task")

    return start_task_assignment

def choose_project_screen(parent, back_command=None, confirm_command=None):
    frame = ModernCard(parent)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)

    file_path = Path(__file__).resolve().parent.parent.parent / "data" / "projekte.json"

    selected_project_var = StringVar(value="")

    # Head
    head = ModernCard(frame)
    head.columnconfigure(0, weight=0)
    head.columnconfigure(1, weight=1)
    head.grid(row=0, column=0, sticky="ew", pady=(0, 12))

    callbacks = {
        "back": back_command,
        "confirm": confirm_command,
    }

    back_button = ModernButton(head, text="◀", command=lambda: callbacks["back"]() if callbacks["back"] else None, font=("Segoe UI", 13, "bold"), padx=14, pady=8)
    back_button.grid(row=0, column=0, sticky="w")

    header = HeaderLabel(head, text="Projekt auswählen")
    header.grid(row=0, column=1, sticky="w", padx=(50, 0))

    # Content
    content = ModernCard(frame)
    content.grid(row=1, column=0, sticky="nsew")
    content.columnconfigure(0, weight=1)
    content.rowconfigure(1, weight=1)
    content.rowconfigure(2, weight=0)

    info_label = TextLabel(
        content,
        text="Wähle das Projekt aus, in dem das Item zugewiesen oder entfernt werden soll."
    )
    info_label.grid(row=0, column=0, sticky="w", pady=(0, 12))

    proj_treeview = ModernTreeview(
        content,
        columns=("id", "name", "description", "priority", "due_date")
    )
    proj_treeview.grid(row=1, column=0, sticky="nsew")

    proj_treeview.tree.heading("#0", text="")
    proj_treeview.tree.column("#0", width=0, stretch=False)

    proj_treeview.heading("id", text="ID")
    proj_treeview.column("id", width=60, anchor="center", stretch=False)

    proj_treeview.heading("name", text="Name")
    proj_treeview.column("name", width=180, anchor="w")

    proj_treeview.heading("description", text="Beschreibung")
    proj_treeview.column("description", width=320, anchor="w")

    proj_treeview.heading("priority", text="Priorität")
    proj_treeview.column("priority", width=120, anchor="center", stretch=False)

    proj_treeview.heading("due_date", text="Fällig")
    proj_treeview.column("due_date", width=160, anchor="center", stretch=False)

    def refresh_projects():
        proj_treeview.tree.delete(*proj_treeview.tree.get_children())
        projects = read(file_path)

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

    def on_select(event=None):
        selected_name = proj_treeview.get_selected_name()
        if not selected_name:
            selected_project_var.set("")
            selected_label.config(text="Aktuell ausgewählt: Kein Projekt")
            return

        selected_project_var.set(selected_name)
        selected_label.config(text=f"Aktuell ausgewählt: {selected_name}")

    def confirm_selection():
        selected_name = selected_project_var.get().strip()
        if not selected_name:
            dialog_creation_error("Bitte zuerst ein Projekt auswählen.")
            return

        if callbacks["confirm"]:
            callbacks["confirm"](selected_name)

    bottom_area = ModernCard(content)
    bottom_area.grid(row=2, column=0, sticky="ew", pady=(12, 0))
    bottom_area.columnconfigure(0, weight=1)
    bottom_area.columnconfigure(1, weight=0)

    selected_label = TextLabel(bottom_area, text="Aktuell ausgewählt: Kein Projekt", muted=True)
    selected_label.grid(row=0, column=0, sticky="w")

    confirm_button = ModernButton(bottom_area, text="Bestätigen", command=confirm_selection)
    confirm_button.grid(row=0, column=1, sticky="e")

    proj_treeview.tree.bind("<<TreeviewSelect>>", on_select)

    refresh_projects()

    frame.set_confirm_command = lambda command: callbacks.__setitem__("confirm", command)
    frame.set_back_command = lambda command: callbacks.__setitem__("back", command)
    frame.set_instruction_text = lambda text: info_label.config(text=text)

    return frame
    # öffnet separates Fenster mit Projektliste, um auszuwählen, wo Task / Member hinzugefügt werden soll
    # ggf. auch für Teammitglied, um Tasks zuzuweisen

def choose_member_screen(parent, back_command=None, confirm_command=None):
    frame = ModernCard(parent)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)

    file_path = Path(__file__).resolve().parent.parent.parent / "data" / "teammitglieder.json"

    selected_member_var = StringVar(value="")

    # Head
    head = ModernCard(frame)
    head.columnconfigure(0, weight=0)
    head.columnconfigure(1, weight=1)
    head.grid(row=0, column=0, sticky="ew", pady=(0, 12))

    callbacks = {
        "back": back_command,
        "confirm": confirm_command,
    }

    back_button = ModernButton(head, text="◀", command=lambda: callbacks["back"]() if callbacks["back"] else None, font=("Segoe UI", 13, "bold"), padx=14, pady=8)
    back_button.grid(row=0, column=0, sticky="w")

    header = HeaderLabel(head, text="Teammitglied auswählen")
    header.grid(row=0, column=1, sticky="w", padx=(50, 0))

    # Content
    content = ModernCard(frame)
    content.grid(row=1, column=0, sticky="nsew")
    content.columnconfigure(0, weight=1)
    content.rowconfigure(1, weight=1)
    content.rowconfigure(2, weight=0)

    info_label = TextLabel(
        content,
        text="Wähle das Teammitglied aus, dem die Aufgabe zugewiesen werden soll."
    )
    info_label.grid(row=0, column=0, sticky="w", pady=(0, 12))

    member_treeview = ModernTreeview(
        content,
        columns=("id", "name", "job_title", "active_since")
    )
    member_treeview.grid(row=1, column=0, sticky="nsew")

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

    def refresh_members():
        member_treeview.tree.delete(*member_treeview.tree.get_children())
        members = read(file_path)

        for member in members:
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

    def on_select(event=None):
        selected_name = member_treeview.get_selected_name()
        if not selected_name:
            selected_member_var.set("")
            selected_label.config(text="Aktuell ausgewählt: Kein Teammitglied")
            return

        selected_member_var.set(selected_name)
        selected_label.config(text=f"Aktuell ausgewählt: {selected_name}")

    def confirm_selection():
        selected_name = selected_member_var.get().strip()
        if not selected_name:
            dialog_creation_error("Bitte zuerst ein Teammitglied auswählen.")
            return

        if callbacks["confirm"]:
            callbacks["confirm"](selected_name)

    bottom_area = ModernCard(content)
    bottom_area.grid(row=2, column=0, sticky="ew", pady=(12, 0))
    bottom_area.columnconfigure(0, weight=1)
    bottom_area.columnconfigure(1, weight=0)

    selected_label = TextLabel(bottom_area, text="Aktuell ausgewählt: Kein Teammitglied", muted=True)
    selected_label.grid(row=0, column=0, sticky="w")

    confirm_button = ModernButton(bottom_area, text="Bestätigen", command=confirm_selection)
    confirm_button.grid(row=0, column=1, sticky="e")

    member_treeview.tree.bind("<<TreeviewSelect>>", on_select)

    refresh_members()

    frame.set_confirm_command = lambda command: callbacks.__setitem__("confirm", command)
    frame.set_back_command = lambda command: callbacks.__setitem__("back", command)
    frame.set_instruction_text = lambda text: info_label.config(text=text)

    return frame


def choose_item_screen(parent, back_command=None):
    return choose_project_screen(parent, back_command=back_command)
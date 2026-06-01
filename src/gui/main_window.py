from tkinter import *
import ctypes


# Use package-qualified imports so modules are found when the project
# root is on sys.path (running `src/main.py` directly).
from src.gui.views import *
from src.gui.design_elements import ModernButton as mButton
from src.gui.design_elements import ModernEntry as mEntry
from src.gui.design_elements import ModernCard as mFrame
from src.gui.design_elements import HeaderLabel as hLabel
from src.gui.design_elements import TextLabel as tLabel
from src.gui.design_elements import apply_scrollbar_style
from src.gui.dialogs import *
from src.logic import *

# Dieser Teil korrigiert die Unschärfe auf Windows
try:
    # Für Windows 8.1 und neuer
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        # Für ältere Windows-Versionen
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        # Falls es auf Linux/Mac läuft, passiert einfach nichts
        pass

root = Tk()
root.geometry("1800x1200")
root.title("Projekt-Management-Tool")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
apply_scrollbar_style()
menu = Menu(root)
root.config(menu=menu)

def run_gui():
    root.mainloop()

# Menu
filemenu = Menu(menu)
helpmenu = Menu(menu)
menu.add_cascade(label="Datei", menu=filemenu)
menu.add_cascade(label="Hilfe", menu=helpmenu)

filemenu.add_command(label="Datei öffnen", command=dialog_file) # nur Demo, da Hauptprogramm anpassen zu viel Aufwand
filemenu.add_separator()
filemenu.add_command(label="Beenden", command=dialog_quit)

helpmenu.add_command(label="Readme öffnen", command=open_readme)

screens = {}

def show_screen(name):
    refresh_method = getattr(screens[name], "refresh_tasks", None)
    if callable(refresh_method):
        refresh_method()

    refresh_method = getattr(screens[name], "refresh_members", None)
    if callable(refresh_method):
        refresh_method()

    refresh_method = getattr(screens[name], "refresh_projects", None)
    if callable(refresh_method):
        refresh_method()

    refresh_method = getattr(screens[name], "refresh_project_details", None)
    if callable(refresh_method):
        refresh_method()

    raise_screen(screens[name])

frm_mainscreen = mainscreen(
    root,
    show_projects=lambda: show_screen("project"),
    show_members=lambda: show_screen("member"),
    show_tasks=lambda: show_screen("task"),
    show_create_project=lambda: show_screen("create_project"),
    show_create_member=lambda: show_screen("create_member"),
    show_create_task=lambda: show_screen("create_task"),
)

def open_project_detail(project_name):
    frm_project_detail_screen.set_project(project_name)
    show_screen("project_detail")


frm_project_detail_screen = project_detail_screen(root, back_command=lambda: show_screen("project"))
frm_project_screen = project_screen(
    root,
    back_command=lambda: show_screen("main"),
    create_command=lambda: show_screen("create_project"),
    detail_command=open_project_detail,
)
frm_choose_project_member_screen = choose_project_screen(
    root,
    back_command=lambda: show_screen("member"),
    confirm_command=None,
)
frm_choose_member_task_screen = choose_member_screen(
    root,
    back_command=lambda: show_screen("task"),
    confirm_command=None,
)

frm_member_screen = member_screen(
    root,
    back_command=lambda: show_screen("main"),
    create_command=lambda: show_screen("create_member"),
    assign_command=create_member_assignment_starter(
        choose_project_screen_frame=frm_choose_project_member_screen,
        show_screen=show_screen,
        assign_func=assign,
        refresh_members=lambda: screens["member"].refresh_members(),
        refresh_projects=lambda: screens["project"].refresh_projects(),
    ),
)
frm_task_screen = task_screen(
    root,
    back_command=lambda: show_screen("main"),
    create_command=lambda: show_screen("create_task"),
    assign_command=create_task_assignment_starter(
        choose_project_screen_frame=frm_choose_project_member_screen,
        choose_member_screen_frame=frm_choose_member_task_screen,
        show_screen=show_screen,
        assign_func=assign,
        refresh_tasks=lambda: screens["task"].refresh_tasks(),
        refresh_members=lambda: screens["member"].refresh_members(),
        refresh_projects=lambda: screens["project"].refresh_projects(),
    ),
)

frm_create_project_screen = create_project_screen(root, back_command=lambda: show_screen("project"))
frm_create_member_screen = create_member_screen(root, back_command=lambda: show_screen("member"))
frm_create_task_screen = create_task_screen(root, back_command=lambda: show_screen("task"))

screens["main"] = frm_mainscreen
screens["project"] = frm_project_screen
screens["member"] = frm_member_screen
screens["task"] = frm_task_screen
screens["create_project"] = frm_create_project_screen
screens["create_member"] = frm_create_member_screen
screens["create_task"] = frm_create_task_screen
screens["choose_project_member"] = frm_choose_project_member_screen
screens["choose_member_task"] = frm_choose_member_task_screen
screens["project_detail"] = frm_project_detail_screen

# Initial den Main-Screen zeigen
raise_screen(frm_mainscreen)
from pathlib import Path
from src.dateiverwaltung import *
from src.filter import filter_projects
from src.teammitglied import TeamMember
from src.aufgabe import Task
from src.projekt import Project
from src.utils import *
from src.gui.dialogs import *
import os
import platform
import subprocess

def raise_screen(screen):
    """Zeigt einen Screen und versteckt andere"""
    screen.tkraise()

def open_readme():
    """Öffnet die Readme.md um die Funktionen nachschlagen zu können"""
    # Ermittelt das Verzeichnis, in dem dieses Skript liegt
    # Pfad der aktuellen Datei (ki_fallstudie/src/gui/dein_skript.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Zwei Ebenen nach oben gehen, um in root zu landen
    project_root = os.path.dirname(os.path.dirname(current_dir))
    dateipfad = os.path.join(project_root, "README.md")

    if os.path.exists(dateipfad):
        if platform.system() == "Windows":
            os.startfile(dateipfad)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", dateipfad])
        else:
            subprocess.Popen(["xdg-open", dateipfad])
    else:
        print(f"Fehler: Datei nicht gefunden unter {dateipfad}")

def assign(choice, project_name=None, member_name=None, task_name=None):
    if choice == "assign task":
        if not Project.project_exists(project_name):
            print(f"Das Projekt '{project_name}' existiert nicht.")
            return
        Project.assign_task_to_member(project_name, member_name, task_name)

    elif choice == "unassign task":
        if not Project.project_exists(project_name):
            print(f"Das Projekt '{project_name}' existiert nicht.")
            return
        Project.remove_task_from_member(project_name, member_name, task_name)

    elif choice == "assign member":
        project_name = get_non_empty_input("Zu welchem Projekt möchtest du Mitglieder hinzufügen? ")
        if not Project.project_exists(project_name):
            print(f"Das Projekt '{project_name}' existiert nicht.")
            return
        Project.assign_member_to_project(project_name, member_name)

    elif choice == "unassign member":
        if not Project.project_exists(project_name):
            print(f"Das Projekt '{project_name}' existiert nicht.")
            return
        Project.remove_member_from_project(project_name, member_name)

# AI assisted
def delete_item(item_type, name):
    # Bestimme Datei und relevante Felder basierend auf Typ
    if item_type == "projekt":
        file_path = Path(__file__).resolve().parent.parent / 'data' / 'projekte.json'
        name_field = "name"
        exists_func = Project.project_exists
    elif item_type == "aufgabe":
        file_path = Path(__file__).resolve().parent.parent / 'data' / 'aufgaben.json'
        name_field = "name"
        exists_func = Task.task_exists
    elif item_type == "teammitglied":
        file_path = Path(__file__).resolve().parent.parent / 'data' / 'teammitglieder.json'
        name_field = "name"
        exists_func = TeamMember.member_exists
    else:
        print("Ungültiger Typ.")
        return

    # Lade Daten
    data = read(file_path)
    if not data:
        if item_type == "projekt":
            print(f"Keine Projekte gefunden.")
        if item_type == "aufgabe":
            print(f"Keine Aufgaben gefunden.")
        if item_type == "teammitglied":
            print(f"Keine Teammitglieder gefunden.")
        return

    # Prüfe Existenz
    if not exists_func(name):
        print(f"{item_type.capitalize()} '{name}' existiert nicht.")
        return

    # Bestätigung einholen
    if not dialog_delete():
        return

    # Filtere Eintrag heraus (case-insensitive)
    original_length = len(data)
    data = [item for item in data if item[name_field].lower() != name.lower()]

    # Prüfe, ob etwas gelöscht wurde
    if len(data) == original_length:
        print(f"Fehler beim Löschen von '{name}'.")
        return

    # Speichere aktualisierte Daten
    write(file_path, data)
    print(f"{item_type.capitalize()} '{name}' erfolgreich gelöscht.")
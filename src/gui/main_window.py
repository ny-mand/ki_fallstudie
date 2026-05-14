from tkinter import *
import ctypes
import os
import platform
import subprocess

# Use package-qualified imports so modules are found when the project
# root is on sys.path (running `src/main.py` directly).
from src.gui.views import *
from src.gui.design_elements import ModernButton as mButton
from src.gui.design_elements import ModernEntry as mEntry
from src.gui.design_elements import ModernCard as mFrame
from src.gui.design_elements import HeaderLabel as hLabel
from src.gui.design_elements import TextLabel as tLabel
from src.gui.dialogs import *

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
root.geometry("800x600")
root.title("Projekt-Management-Tool")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
menu = Menu(root)
root.config(menu=menu)

def run_gui():
    root.mainloop()

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

# Menu
filemenu = Menu(menu)
helpmenu = Menu(menu)
menu.add_cascade(label="Datei", menu=filemenu)
menu.add_cascade(label="Hilfe", menu=helpmenu)

filemenu.add_command(label="Datei öffnen", command=dialog_file) # nur Demo, da Hauptprogramm anpassen zu viel Aufwand
filemenu.add_separator()
filemenu.add_command(label="Beenden", command=dialog_quit)

helpmenu.add_command(label="Readme öffnen", command=open_readme)

frm_mainscreen = mainscreen(root)
frm_project_screen = project_screen(root)

# Initial den Main-Screen zeigen
raise_screen(frm_mainscreen)
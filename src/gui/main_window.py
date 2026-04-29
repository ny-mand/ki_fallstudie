from tkinter import *
import ctypes

# Use package-qualified imports so modules are found when the project
# root is on sys.path (running `src/main.py` directly).
from src.gui.views import create_test_screen
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
menu = Menu(root)
root.config(menu=menu)

def run_gui():
    root.mainloop()

def raise_screen(screen):
    """Zeigt einen Screen und versteckt andere"""
    screen.tkraise()

def open_readme():
    """Öffnet die Readme.md um die Funktionen nachschlagen zu können"""
    pass

# Menu
filemenu = Menu(menu)
helpmenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
menu.add_cascade(label="Help", menu=helpmenu)

filemenu.add_command(label="Quit", command=dialog_quit)

helpmenu.add_command(label="Open Readme", command=open_readme)

# Frames übereinander stapeIn
frm_main_screen = mFrame(root)
frm_main_screen.place(relwidth=1, relheight=1)

frm_test_screen = create_test_screen(root)
frm_test_screen.place(relwidth=1, relheight=1)

# Widgets im Main-Screen
hLabel(frm_main_screen, text="Hauptscreen").pack(pady=10)
mButton(frm_main_screen, text="Zum Test-Screen", command=lambda: raise_screen(frm_test_screen)).pack()
tLabel(frm_main_screen, text="kleiner text").pack()
mEntry(frm_main_screen).pack()


# Initial den Main-Screen zeigen
raise_screen(frm_main_screen)
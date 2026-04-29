from tkinter import *
import ctypes
from views import create_test_screen
from design_elements import ModernButton as mButton
from design_elements import ModernEntry as mEntry
from design_elements import ModernCard as mFrame
from design_elements import HeaderLabel as hLabel
from design_elements import TextLabel as tLabel

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

def raise_screen(screen):
    """Zeigt einen Screen und versteckt andere"""
    screen.tkraise()

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

# Menu
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)

# Initial den Main-Screen zeigen
raise_screen(frm_main_screen)

if __name__ == "__main__":
    root.mainloop()
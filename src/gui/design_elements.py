from tkinter import *
from tkinter import ttk

COLORS = {
    "bg_dark": "#1e1e1e",
    "bg_light": "#2d2d2d",
    "accent": "#0078d4",
    "text": "#fffef5",
    "hover": "#333333",
    "border": "#404040"
}

FONT_MAIN = ("Segoe UI", 10, "bold")
FONT_BOLD = ("Impact", 11)

def apply_scrollbar_style():
    style = ttk.Style()
    # Wir nutzen das 'alt' theme als Basis, da es am anpassungsfähigsten ist
    style.theme_use('alt')
    
    style.configure("Modern.Vertical.TScrollbar",
                    gripcount=0,
                    background=COLORS["bg_light"],
                    darkcolor=COLORS["bg_light"],
                    lightcolor=COLORS["bg_light"],
                    troughcolor=COLORS["bg_dark"],
                    bordercolor=COLORS["border"],
                    arrowsize=12)
    
    # Hover-Effekt für die Scrollbar
    style.map("Modern.Vertical.TScrollbar",
              background=[('active', COLORS["accent"]), ('disabled', COLORS["bg_light"])])

class ModernButton(Button):
    def __init__(self, master, text, command=None, **kwargs):
        # Standard-Design-Definitionen
        self.default_bg = "#2e9acc"  # Schönes Grün
        self.hover_bg = "#207ba9"    # Dunkleres Grün für Hover
        self.fg_color = "white"
        self.font = FONT_MAIN

        super().__init__(
            master, 
            text=text, 
            command=command,
            bg=self.default_bg,
            fg=self.fg_color,
            font=self.font,
            bd=0,                   # Entfernt den hässlichen Rahmen
            padx=20,
            pady=10,
            activebackground=self.hover_bg,
            activeforeground="white",
            cursor="hand2",         # Zeigt den Mauszeiger-Finger
            **kwargs
        )

        # Bindings für Hover-Effekte
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, event):
        self.config(bg=self.hover_bg)

    def _on_leave(self, event):
        self.config(bg=self.default_bg)

class ModernEntry(Frame):
    def __init__(self, master, placeholder="", **kwargs):
        super().__init__(master, bg=COLORS["border"], padx=1, pady=1) # Rahmen-Effekt
        
        self.entry = Entry(
            self, 
            bg=COLORS["bg_light"], 
            fg=COLORS["text"],
            insertbackground="white", # Cursor-Farbe
            font=FONT_MAIN,
            bd=0,
            highlightthickness=0,
            **kwargs
        )
        self.entry.pack(padx=8, pady=5, fill="x")
        
    def get(self):
        return self.entry.get()
    
class ModernCard(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master, 
            bg=COLORS["bg_light"], 
            padx=15, 
            pady=15, 
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            **kwargs
        )

class HeaderLabel(Label):
    def __init__(self, master, text, **kwargs):
        super().__init__(
            master,
            text=text,
            font=("Segoe UI", 18, "bold"),
            fg=COLORS["text"],
            bg=master.cget("bg"),
            pady=10,
            **kwargs
        )

class TextLabel(Label):
    def __init__(self, master, text, muted=False, **kwargs):
        # Wenn muted=True, wird die Schrift grau statt weiß
        color = "#aaaaaa" if muted else COLORS["text"]
        
        super().__init__(
            master,
            text=text,
            font=("Segoe UI", 11),
            fg=color,
            bg=master.cget("bg"),
            **kwargs
        )

class ModernListbox(Listbox):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            bg=COLORS["bg_light"],
            fg=COLORS["text"],
            font=FONT_MAIN,
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["accent"], # Farbe des Rahmens bei Fokus
            selectbackground=COLORS["accent"],
            selectforeground="white",
            activestyle="none", # Entfernt Unterstrich beim aktiven Item
            **kwargs
        )

class ScrollingListFrame(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=COLORS["bg_dark"])
        
        # Scrollbar erstellen (mit neuem Style)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", style="Modern.Vertical.TScrollbar")
        self.scrollbar.pack(side="right", fill="y")

        # Listbox erstellen
        self.listbox = ModernListbox(self, yscrollcommand=self.scrollbar.set, **kwargs)
        self.listbox.pack(side="left", fill="both", expand=True)

        # Scrollbar mit Listbox verknüpfen
        self.scrollbar.config(command=self.listbox.yview)

    # Hilfsmethoden, um direkt auf die Listbox zuzugreifen
    def insert(self, index, item):
        self.listbox.insert(index, item)
        
    def get_selected(self):
        selection = self.listbox.curselection()
        return self.listbox.get(selection[0]) if selection else None
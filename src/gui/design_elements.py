from tkinter import *

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
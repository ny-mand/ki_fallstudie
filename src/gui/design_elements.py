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
    
    # Treeview Styling
    style.configure("Modern.Treeview",
                    background=COLORS["bg_light"],
                    foreground=COLORS["text"],
                    fieldbackground=COLORS["bg_light"],
                    font=FONT_MAIN,
                    rowheight=56,
                    borderwidth=0,
                    relief="flat")
    
    style.configure("Modern.Treeview.Heading",
                    background=COLORS["bg_dark"],
                    foreground=COLORS["text"],
                    font=("Segoe UI", 10, "bold"),
                    borderwidth=0)
    
    style.map("Modern.Treeview",
              background=[('selected', COLORS["accent"])],
              foreground=[('selected', 'white')])
    
    style.map("Modern.Treeview.Heading",
              background=[('active', COLORS["hover"])])

class ModernButton(Button): # per **kwargs gut anpassbar, bedarf andere Elemente nach gleichem Prinzip anpassen
    def __init__(self, master, text, command=None, **kwargs):
        # Standard-Design-Definitionen
        self.default_bg = "#2e9acc"  # Schönes Blau
        self.hover_bg = "#207ba9"    # Dunkleres Blau für Hover
        self.fg_color = "white"
        self.font = kwargs.pop("font", FONT_MAIN)
        bg = kwargs.pop("bg", self.default_bg)
        fg = kwargs.pop("fg", self.fg_color)
        bd = kwargs.pop("bd", 0)
        padx = kwargs.pop("padx", 20)
        pady = kwargs.pop("pady", 10)
        activebackground = kwargs.pop("activebackground", self.hover_bg)
        activeforeground = kwargs.pop("activeforeground", "white")
        cursor = kwargs.pop("cursor", "hand2")

        super().__init__(
            master, 
            text=text, 
            command=command,
            bg=bg,
            fg=fg,
            font=self.font,
            bd=bd,                   # Entfernt den hässlichen Rahmen
            padx=padx,
            pady=pady,
            activebackground=activebackground,
            activeforeground=activeforeground,
            cursor=cursor,         # Zeigt den Mauszeiger-Finger
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
        padx = kwargs.pop("padx", 15)
        pady = kwargs.pop("pady", 15)
        
        super().__init__(
            master, 
            bg=COLORS["bg_light"], 
            padx=padx, 
            pady=pady, 
            highlightbackground=COLORS["border"],
            highlightthickness=0,
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
            highlightthickness=0,
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

class ModernTreeview(Frame):
    """Styled Treeview mit Scrollbar für Tabellendarstellung"""
    def __init__(self, master, columns=None, **kwargs):
        super().__init__(master, bg=master.cget("bg"))
        
        # Scrollbars
        self.vsb = ttk.Scrollbar(self, orient="vertical", style="Modern.Vertical.TScrollbar")
        
        # Treeview erstellen
        self.tree = ttk.Treeview(
            self,
            columns=columns or [],
            style="Modern.Treeview",
            yscrollcommand=self.vsb.set,
            **kwargs
        )
        
        # Layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.vsb.grid(row=0, column=1, sticky="ns")
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Scrollbars verknüpfen
        self.vsb.config(command=self.tree.yview)
    
    def heading(self, col, **kwargs):
        """Spalte konfigurieren"""
        self.tree.heading(col, **kwargs)
    
    def column(self, col, **kwargs):
        """Spaltenbreite/Ausrichtung setzen"""
        # stretch=True ermöglicht, dass sich Spalten an Fensterbreite anpassen
        if 'stretch' not in kwargs:
            kwargs['stretch'] = True
        self.tree.column(col, **kwargs)
    
    def insert(self, parent, index, iid=None, **kwargs):
        """Zeile einfügen"""
        return self.tree.insert(parent, index, iid=iid, **kwargs)
    
    def item(self, item, **kwargs):
        """Item-Daten abrufen/setzen"""
        return self.tree.item(item, **kwargs)

    def selection(self):
        """Gibt die aktuell ausgewählten Treeview-Items zurück."""
        return self.tree.selection()

    def get_selected_values(self):
        """Gibt die Werte der ersten ausgewählten Zeile zurück."""
        selection = self.selection()
        if not selection:
            return None
        return self.tree.item(selection[0], "values")

    def get_selected_name(self):
        """Gibt den Projektnamen aus der ersten ausgewählten Zeile zurück."""
        values = self.get_selected_values()
        return values[1] if values and len(values) > 1 else None
    
# TODO ttk.combobox als dropdown menu hinzufügen
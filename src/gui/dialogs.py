from tkinter import *
from tkinter.messagebox import *

def dialog_quit():
    if askokcancel("Are you sure?", "Do your REALLY want to QUIT?"):
        quit()
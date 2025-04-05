import tkinter as tk
from interface_langs import interface_langs

current_lang = None  

def init_lang_var():
    global current_lang
    if current_lang is None:
        current_lang = tk.StringVar(value="en")
    return current_lang

def get_lang():
    if current_lang is None:
        return interface_langs["ru"]
    return interface_langs[current_lang.get()]

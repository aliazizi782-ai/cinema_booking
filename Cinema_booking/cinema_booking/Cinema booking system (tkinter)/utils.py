from tkinter import Entry
from tkinter import ttk

import hashlib

def hash_password(string:str,salt:str):
    password=hashlib.sha256((string+salt).encode())
    password=password.hexdigest()
    return password

def clear_entries(entries_list):
    for entry in entries_list:
        if isinstance(entry, ttk.Combobox):
            entry.set("")
        elif isinstance(entry, Entry):
            entry.delete(0, "end")

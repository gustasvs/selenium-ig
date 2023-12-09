import tkinter as tk
from tkinter import ttk  
from tkinter import simpledialog

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from helpers.settings import *
from selenium.webdriver.firefox.service import Service
from helpers.functions import append_account
import time
import pickle
import os

def ask_filename():
    def on_ok():
        nonlocal filename
        input_text = entry.get().strip()
        if input_text:
            filename = input_text
            root.destroy()

    filename = None
    root = tk.Tk()
    root.title("Tēmas izvēle")

    # Styling
    root.configure(bg='lightgray')
    ttk.Style().configure('TButton', padding=6, relief='flat', background='#ccc')

    # Layout
    label = ttk.Label(root, text="Ievadi profila tēmu:")
    label.pack(padx=10, pady=10)

    entry = ttk.Entry(root)
    entry.pack(padx=10, pady=10)
    entry.focus()

    ok_button = ttk.Button(root, text="OK", command=on_ok)
    ok_button.pack(pady=(0, 10))

    root.mainloop()
    return filename

def get_next_available_filename(filename, directory='tmp_data'):
    index = 1
    new_filename = f"{filename}{index}"
    while os.path.exists(os.path.join(directory, f'{new_filename}.pkl')):
        index += 1
        new_filename = f"{filename}{index}"
    return new_filename

theme = ask_filename()

append_account(f"tmp_data/themes", theme)

theme_name_full = get_next_available_filename(theme)

driver = webdriver.Firefox(service=Service(webdriver_ff_pth))

driver.get("https://www.instagram.com/")

time.sleep(40)

with open(f'tmp_data/{theme_name_full}.pkl', 'wb') as file:
    pickle.dump(driver.get_cookies(), file)

driver.quit();
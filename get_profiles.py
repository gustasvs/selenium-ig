from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from helpers.settings import *
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from helpers.functions import wait, append_account, load_seen_profiles
import pickle
from tqdm import tqdm

import tkinter as tk
from tkinter import ttk  
from tkinter import simpledialog


def ask_filename():
    def on_ok():
        nonlocal filename
        nonlocal link
        input_text = entry.get().strip()
        link_text = entry_link.get().strip()
        if input_text != "" and link_text != "":
            filename = input_text
            link = link_text
            root.destroy()

    filename = None
    link = None

    root = tk.Tk()
    root.title("Tēmas izvēle")

    # Styling
    root.configure(bg=background_color)
    ttk.Style().configure('TButton', padding=6, relief='flat', background=button_color)

    # Layout
    label = ttk.Label(root, text="Tēma:", background=text_widget_bg, foreground=text_color)
    label.pack(padx=10, pady=10)

    entry = ttk.Entry(root)
    entry.pack(padx=10, pady=10)
    entry.focus()

    label_link = ttk.Label(root, text="Profils kura followerus skatīties:", background=text_widget_bg, foreground=text_color)
    label_link.pack(padx=10, pady=10)

    entry_link = ttk.Entry(root)
    entry_link.pack(padx=10, pady=10)
    entry_link.focus()

    ok_button = ttk.Button(root, text="OK", command=on_ok)
    ok_button.pack(pady=(0, 10))

    root.mainloop()
    return filename, link

theme, from_where_to_get_accounts = ask_filename()

process_progress = 100
progress_increment = 3  
seen_profiles = load_seen_profiles(account_list_pth)
good_profiles = []

with tqdm(total=process_progress) as pbar:

    driver = webdriver.Firefox(service=Service(webdriver_ff_pth))
    driver.get('https://www.instagram.com/')
    wait(0, "Starting Instagram", 5, pbar)
    
    with open('tmp_data/cookies.pkl', 'rb') as file:
        cookies = pickle.load(file) 
        for cookie in cookies:
            driver.add_cookie(cookie)
    wait(0, "Loading cookies", 3, pbar)

    driver.get('https://www.instagram.com/accounts/login')
    wait(1)
    driver.find_element(by=By.XPATH, value="//button[text()='Not Now']").click()
    wait(1, "Skipping save login", 2, pbar)
    driver.get(f'https://www.instagram.com/{from_where_to_get_accounts}/followers/')
    wait(5, "Getting followers", 5, pbar)
    container = driver.find_element(By.CLASS_NAME, "_aano")
    # innermost_divs = driver.find_elements(By.CSS_SELECTOR, '._aano > div > div')
    wait(1, "Finding follower container", 5, pbar)

    last_height = driver.execute_script("return arguments[0].scrollHeight", container)

    # while len(good_profiles) < accounts_to_follow:
    while True:
        try:
            innermost_divs = container.find_elements(By.XPATH, './/div')
            for div in innermost_divs:
                spans = div.find_elements(By.XPATH, './/span')
                account_name = ""
                followers = -1
                following = -1
                try:
                    span = spans[0]
                    if (span.text in seen_profiles): continue
                    seen_profiles[span.text] = True
                    tqdm.write(span.text)
                    append_account(account_list_pth + f"\\{theme}_accounts", span.text)
                except Exception as e:
                    # tqdm.write(str(e))
                    pass                
        except NoSuchElementException:
            pass
        except StaleElementReferenceException:
            pass 
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", container)
        wait(3)
        new_height = driver.execute_script("return arguments[0].scrollHeight", container)
        if new_height == last_height: 
            tqdm.write(f"Ran out of {from_where_to_get_accounts} followers - quitting!")
            break 
        last_height = new_height

# tqdm.write(good_profiles);
print(good_profiles)

wait(10)
driver.quit()

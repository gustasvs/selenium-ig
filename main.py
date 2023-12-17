from tkinter import *
from threading import Thread, Semaphore, Lock
from helpers.settings import *
from tqdm import tqdm
from helpers.functions import (
    follower_difference,
    wait,
    get_next_available_filename,
    get_unchecked_accounts,
    mark_account
)
import os
from tqdm import tqdm
import sys
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import pickle

class TextRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, str):
        self.widget.config(state=NORMAL) 
        self.widget.insert(END, str)
        self.widget.see(END)
        self.widget.config(state=DISABLED) 

    def flush(self):
        pass

class TqdmTextRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, s):
        self.widget.config(state=NORMAL)
        self.widget.insert(END, s)
        self.widget.see(END)
        self.widget.config(state=DISABLED)

    def flush(self):
        pass


root = Tk()
root.geometry("782x484")
root.title("Sekošana profiliem kādai notiektai tēmai")

root.configure(background=background_color)

followed_accounts = 0
checked_accounts = 0

def custom_tqdm_write(message):
    tqdm.write(message)  # Normal tqdm output to console
    output.config(state=NORMAL)
    output.insert(END, message + "\n")  # Insert the message into the Tkinter Text widget
    output.config(state=DISABLED)

def fetch_profile_data(cookies_name, account, pbar, semaphore, theme):
    try:
        with semaphore:
            driver = webdriver.Firefox(service=Service(webdriver_ff_pth))
            
            try:
                driver.get(f'https://www.instagram.com/{account}/')
                wait(0, "Starting Instagram")
                
                with open(f'tmp_data/{cookies_name}.pkl', 'rb') as file:
                    cookies = pickle.load(file) 
                    for cookie in cookies:
                        driver.add_cookie(cookie)
                wait(0, "Loading cookies")

                driver.get('https://www.instagram.com/accounts/login')
                wait(1)
                driver.find_element(by=By.XPATH, value="//button[text()='Not Now']").click()
                wait(1, "Skipping save login")
                driver.get(f'https://www.instagram.com/{account}/')
                wait(7, "Getting followers")
                # for public accounts
                # followers = driver.find_element(By.XPATH, f"//a[contains(@href, '/{account}/followers/')]/span").get_attribute("title")
                # following = driver.find_element(By.XPATH, f"//a[contains(@href, '/{account}/following/')]/span/span").text
                # for private accounts
                try:
                    followers = driver.find_element(By.XPATH, "//li[contains(., 'followers') and .//span]/span/span").text
                    following = driver.find_element(By.XPATH, "//li[contains(., 'following') and .//span]/span/span").text
                except Exception as e:
                    raise Exception("account is NOT private")
                custom_tqdm_write(f"{account} is following {follower_difference(followers, following)} more people than he has followers")
                
                # no need for this check 
                # private_account = driver.find_element(By.XPATH, "//h2[text()='This Account is Private']") or False
                if (follower_difference(followers, following) > 0):
                    wait(1, f"Acquiring follower nr {followed_accounts + 1}", 1, pbar)
                    follow_button = driver.find_element(By.XPATH, "//button[.//div/div[text()='Follow']]")
                    mark_account(account_list_pth + f"\\{theme}_accounts", account, True)
                else :
                    custom_tqdm_write("Doesnt fall into criteria... :(")
                # container = driver.find_element(By.CLASS_NAME, "_aano")
            except Exception as e:
                wait(0, f"Error while following: {e}")
                pass
            finally:
                global checked_accounts
                checked_accounts += 1
                mark_account(account_list_pth + f"\\{theme}_accounts", account, False)
                pbar.set_description(f"Checked_accounts: {checked_accounts}")
                driver.quit()
    except Exception as e:
        print(e)
        driver.quit()

def iterate_theme_accounts(theme, count, following_speed):
    profiles_iterated = 1
    print(theme, count, following_speed)
    while profiles_iterated <= int(count):
        cookies_name = f"{theme}{profiles_iterated}"
        print(f"cookies_name: {cookies_name}")
        if not os.path.exists(os.path.join("tmp_data", f"{cookies_name}.pkl")):
            return "Visi profili no kuriem sekot izskatiti";
        # followed_accounts = 0
        accounts = get_unchecked_accounts(account_list_pth + f"\\{theme}_accounts")
        semaphore = Semaphore(following_speed)
        threads = []
        with tqdm(
            total=default_accounts_to_follow,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
            # file=tqdm_out_redirector,
        ) as pbar:
            for account in accounts:
                thread = Thread(
                    target=fetch_profile_data,
                    args=(cookies_name, account, pbar, semaphore, theme),
                )
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()
        profiles_iterated += 1


def Take_input():
    try:
        INPUT = theme_input.get("1.0", "end-1c")
        if not INPUT:
            # raise ValueError("Nav ievadīta tēma")
            INPUT = "dogs"
            print("Izmantojam default temu: dogs")
        INPUT_COUNT = accounts_to_follow.get("1.0", "end-1c")
        INPUT_FOLLOWING_SPEED = following_speed_input.get("1.0", "end-1c")
        if not INPUT_FOLLOWING_SPEED:
            print(f"Nav ievadīts cik profilus reizē apskatīt, \
                  izmantota noklusējuma vērtība - {default_following_speed}")
            INPUT_FOLLOWING_SPEED = default_following_speed
        else:
            try:
                INPUT_FOLLOWING_SPEED = int(INPUT_FOLLOWING_SPEED)
            except:
                raise ValueError("Profulu skaitam jābūt skaitlim")
        if not INPUT_COUNT.isdigit() or int(INPUT_COUNT) <= 0:
            print(f"Nav izmantots cik accountiem piesakot, \
                  noklusejuma vertiba: {default_accounts_to_follow}")
            INPUT_COUNT = default_accounts_to_follow
            # raise ValueError("Nav ievadīts profilu skaits no kuriem tik sekots.")

        response = iterate_theme_accounts(INPUT, INPUT_COUNT, int(INPUT_FOLLOWING_SPEED))
        print("Darbība pabeigta: ", response)
    except Exception as e:
        output.config(state=NORMAL)
        output.tag_config("error", foreground="red") 
        output.insert(END, f"Error: {str(e)}\n", "error") 
        output.config(state=DISABLED)


l_1 = Label(root, text="Tēma (dogs, cats, boxing ...)", bg=background_color, fg=text_color)
theme_input = Text(root, height=2, width=35, bg=text_widget_bg, fg=text_color)
l_2 = Label(root, text=f"Cik profiliem piesekot\n( noklusējumā - {default_accounts_to_follow} )", 
            bg=background_color, 
            fg=text_color)
l_3 = Label(root, text=f"Sekošanas ātrums\n( noklusējumā - {default_following_speed} )", bg=background_color, fg=text_color)

following_speed_input = Text(root, height=2, width=35, bg=text_widget_bg, fg=text_color)
accounts_to_follow = Text(root, height=2, width=35, bg=text_widget_bg, fg=text_color)

start_button = Button(
    root,
    height=3,
    width=35,
    text="Sākt",
    # bg=button_color,
    bg="green",
    fg=text_color,
    command=lambda: Take_input(),
)

output = Text(root, height=16, width=25, bg=text_widget_bg, fg=text_color, state=DISABLED)
sys.stdout = TextRedirector(output)
tqdm_output = Text(root, height=8, width=95, bg=text_widget_bg, fg=text_color, state=DISABLED)
tqdm_out_redirector = TqdmTextRedirector(tqdm_output)

spacer_frame1 = Frame(root, bg=background_color, width=5)  # horizontal spacing
spacer_frame2 = Frame(root, bg=background_color, height=15)  # vertical spacing

l_1.grid(row=0, column=0, padx=5, pady=5)
theme_input.grid(row=0, column=1, padx=5, pady=15)
l_2.grid(row=1, column=0, padx=5, pady=5)
accounts_to_follow.grid(row=1, column=1, padx=5, pady=15)
l_3.grid(row=2, column=0, padx=5, pady=5)
following_speed_input.grid(row=2, column=1, padx=5, pady=15) 
spacer_frame1.grid(row=0, column=2, rowspan=3)
start_button.grid(row=3, column=0, columnspan=2, padx=5, pady=15)
spacer_frame2.grid(row=4, column=0, columnspan=3)
output.grid(row=0, column=3, rowspan=4, padx=10) 
tqdm_output.grid(row = 5, column=0, columnspan=5, padx=5, pady=5)

mainloop()

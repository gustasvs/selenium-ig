from tkinter import *
from iterate_profiles import fetch_profile_data
from threading import Thread, Semaphore
from helpers.settings import *
from tqdm import tqdm
from helpers.functions import follower_difference, wait, get_next_available_filename, get_unchecked_accounts
import os
from tqdm import tqdm
import sys
class TextRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, str):
        self.widget.insert(END, str)
        self.widget.see(END)  # Scrolls to the bottom

    def flush(self):
        pass

followed_accounts = 0
checked_accounts = 0
accounts = get_unchecked_accounts(account_list_pth) 

root = Tk()
root.geometry("782x484")
root.title("Sekošana profiliem kādai notiektai tēmai")

def iterate_theme_accounts(theme, count):
	semaphore = Semaphore(following_speed)
	threads = []
	profiles_iterated = 1
	while profiles_iterated < int(count):
		cookies_name = f'{theme}{profiles_iterated}'
		if not os.path.exists(os.path.join('tmp_data', f'{cookies_name}.pkl')):
			return f"iterated {profiles_iterated - 1} accounts"
		with tqdm(total=accounts_to_follow, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]") as pbar:
			
			for account in accounts:
				thread = Thread(target=fetch_profile_data, args=(cookies_name, account, pbar, semaphore))
				thread.start()
				threads.append(thread)
			
			for thread in threads:
				thread.join()
		profiles_iterated += 1

def Take_input():
	INPUT = inputtxt.get("1.0", "end-1c")
	INPUT_COUNT = inputtxt_count.get("1.0", "end-1c")
	print(INPUT)
	response = iterate_theme_accounts(INPUT, INPUT_COUNT)
	print(response)

l = Label(text = "Tēma (dogs, cats, boxing ...)")
inputtxt = Text(root, 
                height = 5,
				width = 35,
				bg = "light blue")
l_2 = Label(text = "Cik profiliem veikt darbību\n (ievadi 999 ja visiem)")
inputtxt_count = Text(root, 
                height = 5,
				width = 35,
				bg = "light blue")

start_button = Button(root, height = 3,
				width = 25, 
				text ="Sākt",
				bg = "light green",
				command = lambda:Take_input())

output = Text(root, height=10, width=50)
sys.stdout = TextRedirector(output)
l.pack()
inputtxt.pack()
l_2.pack()
inputtxt_count.pack()
start_button.pack()
output.pack()

mainloop()

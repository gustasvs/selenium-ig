from tqdm import tqdm
import time
from selenium.webdriver.common.by import By

def get_user_data(driver, data_type):
    last_found_text = -1
    elements = driver.find_elements(By.XPATH, f"//span[text()='{data_type}']")
    for el in elements:
        try:
            sibling_span = el.find_element(By.XPATH, "../preceding-sibling::div/span")
            last_found_text = sibling_span.text
            print(last_found_text);
        except Exception as e:
            tqdm.write(f"Unable to retrieve count for {data_type}: {e}")
    return last_found_text


def follower_difference(followers, following):
    if (followers == -1 or following == -1):
        return False 
    following = following.replace(',', '') 
    followers = followers.replace(',', '')
    # if int(following) - int(followers) < 0:
    #     return False
    return (int(following) - int(followers))

def wait(seconds_to_wait=None, message=None, progress_amount=None, progress_bar=None):    
    if progress_bar is not None and progress_amount is not None:
        progress_bar.update(progress_amount)

    if message is not None:
        tqdm.write(f"{message} done!")
    
    if (seconds_to_wait is not None):
        time.sleep(seconds_to_wait)
        # print(f"{message} done!")


def mark_account(file_path, account, is_followed):
    """Marks a account as checked in the file."""
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip() == account:
                followed_status = "[followed]" if is_followed else "[checked]"
                file.write(f"{line.strip()} {followed_status}\n")
            else:
                file.write(line)

def get_unchecked_accounts(file_path):
    """Returns a list of unchecked accounts from the file."""
    unchecked_accounts = []
    with open(file_path, 'r') as file:
        for line in file:
            account = line.strip()
            if '[checked]' not in account and '[followed]' not in account:
                unchecked_accounts.append(account)
    return unchecked_accounts
    
def append_account(file_path, account):
    """Appends a new account to the file."""
    with open(file_path, 'a+') as file:
        file.write(f"{account}\n")

def load_seen_profiles(file_path):
    """Loads seen profiles from the file, removing '[checked]' and '[followed]'"""
    seen_profiles = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                name = line.strip().replace(' [checked]', '').replace(' [followed]', '')
                seen_profiles[name] = True
    except: pass
    return seen_profiles
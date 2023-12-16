from threading import Thread, Semaphore
from selenium import webdriver
import queue
from selenium import webdriver
from helpers.settings import *
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from helpers.functions import follower_difference, wait, mark_account, get_unchecked_accounts
import pickle
from tqdm import tqdm


followed_accounts = 0
checked_accounts = 0
accounts = get_unchecked_accounts(account_list_pth) 
# ['a_ko_teiks_e']
    # accounts = ['doggohugzz', 'a_ko_teiks_e', 'hhzzener']
    # , 'a', 'b', 'c', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd']
    

def fetch_profile_data(cookies_name, account, pbar, semaphore):
    with semaphore:
        driver = webdriver.Firefox(service=Service(webdriver_ff_pth))
        
        try:
            driver.get(f'https://www.instagram.com/{account}/')
            wait(0, "Starting Instagram")
            
            with open(f'tmp_data/{cookies_name}', 'rb') as file:
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
            tqdm.write(f"{account} is following {follower_difference(followers, following)} more people than he has followers")
            
            # no need for this check 
            # private_account = driver.find_element(By.XPATH, "//h2[text()='This Account is Private']") or False
            if (follower_difference(followers, following) > 0):
                global followed_accounts
                followed_accounts += 1
                wait(1, f"Acquiring follower nr {followed_accounts + 1}", 1, pbar)
                follow_button = driver.find_element(By.XPATH, "//button[.//div/div[text()='Follow']]")
                mark_account(account_list_pth, account, True)
            else :
                tqdm.write("Doesnt fall into criteria... :(")
            # container = driver.find_element(By.CLASS_NAME, "_aano")
        except Exception as e:
            wait(0, f"Error while following: {e}")
            pass
        finally:
            global checked_accounts
            checked_accounts += 1
            mark_account(account_list_pth, account, False)
            pbar.set_description(f"Checked_accounts: {checked_accounts}")
            driver.quit()

def main():
    semaphore = Semaphore(following_speed)
    threads = []

    with tqdm(total=accounts_to_follow, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]") as pbar:
        
        for account in accounts:
            thread = Thread(target=fetch_profile_data, args=("cookies.pkl", account, pbar, semaphore))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    main()

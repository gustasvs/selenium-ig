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
    driver.get(f'https://www.instagram.com/{account}/followers/')
    wait(5, "Getting followers", 5, pbar)
    container = driver.find_element(By.CLASS_NAME, "_aano")
    # innermost_divs = driver.find_elements(By.CSS_SELECTOR, '._aano > div > div')
    wait(1, "Finding follower container", 5, pbar)

    last_height = driver.execute_script("return arguments[0].scrollHeight", container)

    while len(good_profiles) < accounts_to_follow:
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
                    append_account(account_list_pth, span.text)
                    # account_name = span.text
                
                    # img_element = div.find_element(By.XPATH, f'.//img[@alt="{span.text}\'s profile picture"]')
                    # tqdm.write("found image")
                    # action = ActionChains(driver)
                    # # open image
                    # driver.execute_script("var event = new MouseEvent('mouseover', { 'view': window, 'bubbles': true, 'cancelable': true }); arguments[0].dispatchEvent(event);", img_element)
                    # wait(5)
                    # tqdm.write("finding specific follower count...")
                    
                    # following_elements = driver.find_elements(By.XPATH, "//span[text()='following']")
                    # for el in following_elements:
                    #     try:
                    #         sibling_span = el.find_element(By.XPATH, "../preceding-sibling::div/span")
                    #         following = sibling_span.text
                    #     except Exception as e:
                    #         tqdm.write("Nevareja iegut skaitu: ", e)
                    # follower_elements = driver.find_elements(By.XPATH, "//span[text()='followers']")
                    # for el in follower_elements:
                    #     try:
                    #         sibling_span = el.find_element(By.XPATH, "../preceding-sibling::div/span")
                    #         followers = sibling_span.text
                    #     except Exception as e:
                    #         tqdm.write("Nevareja iegut skaitu: ", e)
                    # tqdm.write(f"user {account_name} is following {follower_difference(followers, following)} more people than he has followers", end = ": ")
                    # if (follower_difference(followers, following)):
                    #     wait(1, f"Acquiring follower nr {len(good_profiles) + 1}", 80 / accounts_to_follow, pbar)
                    #     good_profiles.append(account_name)
                    #     tqdm.write("Can follow!!!")
                    #     if (len(good_profiles) > accounts_to_follow):
                    #         break
                    # else :
                    #     tqdm.write("Doesnt fall into criteria... :(")

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
            tqdm.write(f"Ran out of {account} followers - quitting!")
            break 
        last_height = new_height

# tqdm.write(good_profiles);
print(good_profiles)

wait(10)
driver.quit()

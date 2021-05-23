import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

main_hashtag = "dog"

INSTA_URL = "https://www.instagram.com/explore/tags/"


def insta_login():
    INSTA_LOGIN_IMFOMATION = [

    ]
    insta_login_inputs = WebDriverWait(browser, 2).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "_2hvTZ"))
    )
    for idx, login_input in enumerate(insta_login_inputs):
        login_input.send_keys(INSTA_LOGIN_IMFOMATION[idx])
    insta_login_inputs[1].send_keys(Keys.ENTER)
    time.sleep(3)
    browser.get(INSTA_URL + main_hashtag)


browser = webdriver.Chrome(ChromeDriverManager().install())

browser.get(INSTA_URL + main_hashtag)

if main_hashtag not in browser.current_url:
    insta_login()

insta_search_input = browser.find_element_by_class_name("x3qfX")
insta_search_input.send_keys(f"#{main_hashtag}")

results = WebDriverWait(browser, 2).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "-qQT3"))
)

number = 0

for result in results:
    hashtag = result.text.split()[0].lstrip('#')
    if hashtag != main_hashtag:
        browser.execute_script(
            f"window.open('https://www.instagram.com/explore/tags/{hashtag}')"
        )
        number += 1
        if number == 10:
            break

for window in browser.window_handles:
    browser.switch_to.window(window)
    hashtage_name = browser.find_element_by_tag_name("h1").text.lstrip("#")
    print(hashtage_name)
    time.sleep(1)

"""
hashtag = browser.current_url.split("/")[-1]
insta_search_input.send_keys(hashtag)
 """
time.sleep(3)
browser.quit()

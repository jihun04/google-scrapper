import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(ChromeDriverManager().install())


def wait_for(locator):
    return WebDriverWait(browser, 5).until(
        EC.presence_of_element_located(locator)
    )


def wait_for_all(locator):
    return WebDriverWait(browser, 5).until(
        EC.presence_of_all_elements_located(locator)
    )


main_hashtag = "dog"

INSTA_URL = "https://www.instagram.com/explore/tags/"

INSTA_LOGIN_IMFOMATION = [

]

browser.get("https://www.instagram.com/accounts/login/")

insta_login_inputs = wait_for_all((By.CLASS_NAME, "_2hvTZ"))

for idx, login_input in enumerate(insta_login_inputs):
    login_input.send_keys(INSTA_LOGIN_IMFOMATION[idx])

insta_login_inputs[1].send_keys(Keys.ENTER)
time.sleep(3)

browser.get(INSTA_URL + main_hashtag)

insta_search_input = browser.find_element_by_class_name("x3qfX")
insta_search_input.send_keys(f"#{main_hashtag}")

results = wait_for_all((By.CLASS_NAME, "-qQT3"))

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

counted_hastags = []
used_hastags = []

for window in browser.window_handles:
    browser.switch_to.window(window)

    hashtag_name = wait_for((By.TAG_NAME, "h1"))
    post_count = wait_for((By.CLASS_NAME, "g47SY"))
    if post_count:
        post_count = int(post_count.text.replace(",", ""))
    if hashtag_name:
        hashtag_name = hashtag_name.text[1:]
    if hashtag_name and post_count:
        if hashtag_name not in used_hastags:
            counted_hastags.append((hashtag_name, post_count))
            used_hastags.append(hashtag_name)

    time.sleep(1)

"""
hashtag = browser.current_url.split("/")[-1]
insta_search_input.send_keys(hashtag)
 """
time.sleep(3)
browser.quit()

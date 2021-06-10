import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

initial_hashtag = "dog"
max_hashtags = 20
INSTA_LOGIN_IMFOMATION = [
]
browser = webdriver.Chrome(ChromeDriverManager().install())
counted_hastags = []
used_hashtags = []


def wait_for_all(locator):
    return WebDriverWait(browser, 5).until(
        EC.presence_of_all_elements_located(locator)
    )


def insta_login():
    browser.get("https://www.instagram.com/accounts/login/")
    insta_login_inputs = wait_for_all((By.CLASS_NAME, "_2hvTZ"))
    for idx, login_input in enumerate(insta_login_inputs):
        login_input.send_keys(INSTA_LOGIN_IMFOMATION[idx])
    insta_login_inputs[1].send_keys(Keys.ENTER)


def extract_data(target_hashtag):
    try:
        insta_search_input = WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "x3qfX"))
        )
        insta_search_input.send_keys(f"#{target_hashtag}")
        results = wait_for_all((By.CLASS_NAME, "-qQT3"))
        for result in results:
            result_text = result.text.split()
            hashtag_name = result_text[0][1:]
            post_count = result_text[1]
            if hashtag_name not in used_hashtags:
                if hashtag_name and post_count:
                    post_count = int(post_count.replace(",", ""))
                    counted_hastags.append((hashtag_name, post_count))
                    used_hashtags.append(hashtag_name)
            if len(used_hashtags) == max_hashtags:
                break
        if len(used_hashtags) < max_hashtags:
            extract_data(used_hashtags[-1])
    except Exception:
        pass


def get_related(target_hashtag):
    insta_login()
    time.sleep(3)
    browser.get(f"https://www.instagram.com/explore/tags/{target_hashtag}")
    extract_data(target_hashtag)
    print(counted_hastags)


get_related(initial_hashtag)

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

main_hashtag = "dog"

INSTA_URL = "https://www.instagram.com/explore/tags/"

INSTA_LOGIN_IMFOMATION = [

]

browser = webdriver.Chrome(ChromeDriverManager().install())

browser.get(INSTA_URL + main_hashtag)

insta_login_inputs = WebDriverWait(browser, 2).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "_2hvTZ"))
)

for idx, login_input in enumerate(insta_login_inputs):
    login_input.send_keys(INSTA_LOGIN_IMFOMATION[idx])

insta_login_inputs[1].send_keys(Keys.ENTER)

not_now_btn = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "HoLwm"))
)

not_now_btn.click()

insta_search_input = browser.find_element_by_class_name("x3qfX")
insta_search_input.send_keys(f"#{main_hashtag}")

results = WebDriverWait(browser, 2).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "-qQT3"))
)

for result in results:
    result_text = result.text.split()
    print(f"{result_text[0]}: {result_text[1] + result_text[2]}")

# hashtag = browser.current_url.split("/")[-1]
# insta_search_input.send_keys(hashtag)


time.sleep(3)

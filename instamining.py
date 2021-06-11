import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class Instaminer():
    def __init__(self, insta_username, insta_password, initial_hashtag, max_hashtags):
        options = Options()
        options.add_argument("--headless")
        self.insta_login_information = [insta_username, insta_password]
        self.login_url = "https://www.instagram.com/accounts/login/"
        self.initial_hashtag = initial_hashtag
        self.max_hashtags = max_hashtags
        self.browser = webdriver.Chrome(
            ChromeDriverManager().install(), options=options)
        self.counted_hashtags = []
        self.used_hashtags = []

    def wait_for_all(self, locator):
        return WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located(locator)
        )

    def insta_login(self):
        self.browser.get(self.login_url)
        insta_login_inputs = self.wait_for_all((By.CLASS_NAME, "_2hvTZ"))
        for idx, login_input in enumerate(insta_login_inputs):
            login_input.send_keys(self.insta_login_information[idx])
        insta_login_inputs[1].send_keys(Keys.ENTER)

    def extract_data(self, target_hashtag):
        try:
            insta_search_input = WebDriverWait(self.browser, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, "x3qfX"))
            )
            insta_search_input.send_keys(f"#{target_hashtag}")
            results = self.wait_for_all((By.CLASS_NAME, "-qQT3"))
            for result in results:
                result_text = result.text.split()
                hashtag_name = result_text[0][1:]
                post_count = result_text[1]
                if hashtag_name not in self.used_hashtags:
                    if hashtag_name and post_count:
                        post_count = int(post_count.replace(",", ""))
                        self.counted_hashtags.append(
                            (hashtag_name, post_count))
                        self.used_hashtags.append(hashtag_name)
                if len(self.used_hashtags) == self.max_hashtags:
                    break
            if len(self.used_hashtags) < self.max_hashtags:
                self.extract_data(self.used_hashtags[-1])
        except Exception:
            pass

    def save_file(self):
        file = open(f"{self.initial_hashtag}-report.csv", "w")
        writer = csv.writer(file)
        writer.writerow(["Hashtag", "Post Count"])
        for hashtag in self.counted_hashtags:
            writer.writerow(hashtag)

    def get_related(self, target_hashtag):
        self.insta_login()
        WebDriverWait(self.browser, 10).until(
            EC.url_changes(self.login_url)
        )
        self.browser.get(
            f"https://www.instagram.com/explore/tags/{target_hashtag}")
        self.extract_data(target_hashtag)
        self.save_file()
        self.browser.quit()
        print(len(self.used_hashtags))

    def start(self):
        self.get_related(self.initial_hashtag)


Instaminer("", input("What is your password?"), "", 20).start()

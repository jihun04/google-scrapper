from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import os


class GoogleKeywordScreenshooter():
    def __init__(self, keyword, screenshots_dir, max_page=99):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.keyword = keyword
        self.screenshots_dir = screenshots_dir
        self.max_page = max_page

    def start(self):
        self.browser.get("https://google.com")
        search_bar = self.browser.find_element_by_class_name("gLFyf")
        search_bar.send_keys(self.keyword)
        search_bar.send_keys(Keys.ENTER)

        def get_result():
            try:
                print("Waiting..")
                shitty_element = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "g-blk"))
                )
                self.browser.execute_script(
                    """
                    const shitty=arguments[0];
                    shitty.parentNode.removeChild(shitty);
                    """,
                    shitty_element
                )
            except Exception:
                pass
            if not os.path.isdir(self.screenshots_dir):
                os.mkdir(self.screenshots_dir)
            search_results = self.browser.find_elements_by_class_name("g")
            current_page = int(self.browser.find_element_by_class_name(
                "YyVfkd").text)
            for index, search_result in enumerate(search_results):
                try:
                    search_result.screenshot(
                        f"{self.screenshots_dir}/{self.keyword}|{current_page}-{index}.png"
                    )
                except Exception:
                    pass
            print(
                f"Finished page: {current_page} - Found {len(search_results)} results")
            try:
                next_page = self.browser.find_element_by_id("pnnext")
                if current_page <= self.max_page:
                    next_page.click()
                    get_result()
            except:
                pass

        get_result()
        print(f"Fininshed {self.keyword}!")

    def run(self):
        self.start()
        self.browser.quit()

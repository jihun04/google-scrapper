from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from math import ceil


class ResponsiveTester():
    def __init__(self, urls):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.maximize_window()
        self.urls = urls
        self.sizes = [480, 960, 1360, 1920]

    def screenshots(self, url):
        file_name = url.replace("www.", "", 1).split("//")[1].split(".")[0]
        if not os.path.isdir(file_name):
            os.mkdir(file_name)
        self.browser.get(url)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "html"))
        )
        browser_outer_height = self.browser.get_window_size().get("height")
        browser_inner_height = self.browser.execute_script(
            "return window.innerHeight")
        for size in self.sizes:
            self.browser.set_window_size(size, browser_outer_height)
            scroll_size = self.browser.execute_script(
                "return document.body.scrollHeight")
            total_sections = ceil(scroll_size / browser_inner_height)
            for section in range(total_sections):
                self.browser.execute_script(
                    f"window.scroll(0, {browser_inner_height*section})")
                time.sleep(0.7)
                self.browser.save_screenshot(
                    f"{file_name}/{size}x{section+1}.png")

    def start(self):
        for url in self.urls:
            self.screenshots(url)

    def finish(self):
        self.browser.quit()

    def run(self):
        self.start()
        self.finish()

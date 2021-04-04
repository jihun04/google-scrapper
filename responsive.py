import time
from math import ceil
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(ChromeDriverManager().install())

browser.get("https://nomadcoders.co")

sizes = [480, 960, 1360, 1920]
browser_height = browser.get_window_size().get("height")

for size in sizes:
    browser.set_window_size(size, browser_height)
    time.sleep(2)
    scroll_size = browser.execute_script("return document.body.scrollHeight")
    total_sections = ceil(scroll_size / browser_height)
    for section in range(total_sections):
        browser.execute_script(
            f"window.scroll(0, {browser_height*section})")
        time.sleep(2)

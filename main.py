from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import csv

KEYWORD = "buy domain"

browser = webdriver.Chrome(ChromeDriverManager().install())

browser.get("https://google.com")

search_bar = browser.find_element_by_class_name("gLFyf")

search_bar.send_keys(KEYWORD)
search_bar.send_keys(Keys.ENTER)

shitty_element = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "mnr-c"))
)

print(shitty_element)

""" search_results = browser.find_elements_by_class_name("g")
file = open("titles.csv", mode="w")
writer = csv.writer(file)
for index, search_result in enumerate(search_results):
    class_name = search_result.get_attribute("class")
    if "kno-kp mnr-c g-blk" not in class_name:
        search_result.screenshot(f"screenshots/{KEYWORD}x{index}.png")
        title = search_result.find_element_by_tag_name("h3")
        if title:
            writer.writerow([title.text])
 """
browser.quit()

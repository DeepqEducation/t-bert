import time
import os
from pprint import pprint
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import subprocess
from PIL import Image 

chrome_options = Options()
chrome_options.add_argument('--headless')
prefs = {'download.default_directory' : './PDF'}
chrome_options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome('./chromedriver', options=chrome_options)
# driver = webdriver.Chrome('./chromedriver')

base_url = "https://www.airitilibrary.com/Publication/alPublicationJournal?PublicationID=P20121018003"
urls = []
for year in range(2010, 2021):
    urls.append(base_url+ f"&IssueYear={year}")


def solve_captcha(driver, sample_id):
    img_element = driver.find_element_by_xpath("//img[@alt='Captcha Image']")
    img_element.screenshot(f"train_{sample_id}.png")
    p = subprocess.Popen(["display", f"train_{sample_id}.png"])
    time.sleep(2)
    p.kill()
    
    answer = input("type in your answer: ")
    with open(f"label_{sample_id}", "w") as f:
        f.write(answer)

    refresh_btn = driver.find_element_by_xpath("/html/body/div[9]/div[2]/p/a")
    refresh_btn.click()

driver.get(urls[0])

sample_id = 0
while os.path.exists(f"train_{sample_id}.png"):
    sample_id += 1

print(f"start sample id: {sample_id}")


download_btns = driver.find_elements_by_class_name("toRight")
for download_btn in download_btns:
    print(f"sample id: {sample_id}")
    download_btn.click()

    while True:
        solve_captcha(driver, sample_id)
        sample_id += 1
    time.sleep(2)
        



driver.quit()
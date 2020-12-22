from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
from tqdm import tqdm


chrome_options = Options()
chrome_options.add_argument('headless')
driver = webdriver.Chrome('./chromedriver', options=chrome_options)

url = "https://news.pts.org.tw/subcategory/177"
driver.get(url)

get_more_btn = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "a.category_more-sm"))
)
# get_more_btn = driver.find_element_by_css_selector("a.category_more-sm")
max_page = int(get_more_btn.get_attribute("data-maxpage"))

try:
    for i in tqdm(range(max_page), desc="reading pages..."):
        sleep(2.5)
        get_more_btn.click()
        # print(f"reading page {i+1}/{max_page}")
        
except:
    print("some error happened, didn't read all pages.")
    pass

sleep(2.5)
with open("pts.html", "w") as f:
    f.write(driver.page_source)

driver.quit()
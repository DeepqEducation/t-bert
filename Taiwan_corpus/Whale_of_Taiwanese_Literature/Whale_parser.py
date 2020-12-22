import re
import cv2
import time
import pathlib
import argparse
import subprocess
import numpy as np
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

def solve_captcha(captcha_filename):
    """We first split the number from the image.
       For each subimage, we compare it to our standard sample, 
       count the exact match pixels to decide what the number is 
       in subimage"""
    img = cv2.imread(captcha_filename)
    x, y = 5, 6
    w, h = 12, 16
    
    # cut the image into 5 subimage
    crop_imgs = []
    for i in range(5):
        crop_imgs.append(img[y:y+h, x+12*i:x+w+12*i])

    ans = []
    for num_img in crop_imgs:
        distance = []
        for i in range(10):
            distance.append(np.sum(num_img != sample_img[i]))
        ans.append(str(np.argmin(distance)))
    ans_string = "".join(ans)
    print(f"answer: {ans_string}")
    return ans_string

def solve_and_sumit_captcha(img_element):
    captcha_filename = "captcha.png"
    img_element.screenshot(captcha_filename)

    # Using the following code to see captcha image
    # p = subprocess.Popen(["display", captcha_filename])
    # time.sleep(2)
    # p.kill()

    answer = solve_captcha(captcha_filename)
    input_element = driver.find_element_by_class_name("TxtValidate")
    sumit_btn = driver.find_element_by_tag_name("button")
    input_element.send_keys(answer)
    sumit_btn.click()

def is_correct(driver):
    """If we meet reCaptcha, see it as Incorrect too"""
    try:
        alert = driver.switch_to.alert
        alert.accept()

        print("Incorrect!")
        return False
    except Exception as e:
        print("Correct!")
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--resume", action="store_true", default=False, 
        help="resume from specific year-page written in current_year_page.log")
    args = parser.parse_args()

    # For solving Captcha
    sample_img = []
    for i in range(10):
        sample_img.append(cv2.imread(f"standard_sample/sample_{i}.png"))
        

    base_url = "https://www.airitilibrary.com/Publication/alPublicationJournal?PublicationID=P20121018003"
    urls = []
    # year 2010 to 2020
    start_year = 2010
    start_page = 1
    if args.resume:
        with open("current_year_page.log") as f:
            print("resume year, page specified in current_year_page.log")
            start_year, start_page = f.read().split()
            start_year = int(start_year)
            start_page = int(start_page)
    for year in range(start_year, 2021):
        urls.append(base_url+ f"&IssueYear={year}")
    urls[0] += f"&page={start_page}"
    

    print(f"start url= {urls[0]}")
    print(f"start year, page: {start_year}, {start_page}")
    

    for url in urls:

        year = re.search(r"Year=(\d*)", url).group(1)
        target_folder = f'./PDF/{year}'
        pathlib.Path(target_folder).mkdir(parents=True, exist_ok=True) 

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        prefs = {'download.default_directory' : target_folder}
        chrome_options.add_experimental_option('prefs', prefs)

        driver = webdriver.Chrome('./chromedriver', options=chrome_options)
        # driver = webdriver.Chrome('./chromedriver')

        driver.get(url)
        print("loading the page...")
        time.sleep(8)

        conjection = False
        download_btn_error = False
        while True:
            # log
            current_page = driver.find_element_by_class_name("current").text
            with open(f"current_year_page.log", "w") as f:
                f.write(year+" "+current_page)
            article_id = (int(current_page)-1)*10+1

            # click download button and solve captcha
            download_btns = driver.find_elements_by_class_name("toRight")
            for download_btn in download_btns:
                print(f"article id: {article_id}")
                try:
                    download_btn.click()
                except:
                    download_btn_error = True
                    print("download button error, refresh the page...")
                    break

                img_element = driver.find_element_by_xpath("//img[@alt='Captcha Image']")
                solve_and_sumit_captcha(img_element)
                

                if not is_correct(driver):
                    conjection = True
                    print("Encounter reCaptcha, wait 20 mins and reconnect...")
                    break
                    
                time.sleep(8)
                article_id += 1

            if download_btn_error:
                driver.refresh()
                download_btn_error = False
                time.sleep(10)
                continue
            
            # Download too frequent, wait 20 mins to reconnect
            if conjection:
                time.sleep(1200)
                driver.refresh()
                conjection = True
                time.sleep(10)
                continue

            next_page_btn = driver.find_elements_by_css_selector(".pageNumber a")[-1]
            btn_text = next_page_btn.text
            # print(btn_text)
            if btn_text != "": # encounter the end page of the year
                break
            next_page_btn.click()
            time.sleep(10)
        
        driver.quit()


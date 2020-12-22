import scrapy
import time
from selenium import webdriver
from scrapy_splash import SplashRequest
from selenium.webdriver.chrome.options import Options

class PeopleSpider(scrapy.Spider):
    name = "people_taigi_news"
    
    def start_requests(self):
        chrome_options = Options() 
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome('./chromedriver', options=chrome_options)

        url = "https://www.peoplenews.tw/list/%E5%8F%B0%E8%AA%9E%E4%B8%96%E7%95%8C"
        driver.get(url)

        time.sleep(5)
        while True:
            try:
                time.sleep(0.5)
                urls_in_current_page = driver.find_elements_by_css_selector("#area_list a")
                for url in urls_in_current_page:
                    url = url.get_attribute("href")
                    # yield scrapy.Request(url=url, callback=self.parse)
                    yield SplashRequest(url, self.parse,
                        args={
                            'wait': 1,
                        }
                    )
                next_btn = driver.find_element_by_class_name("page-link.next")
                next_btn.click()
            except:
                break 

        driver.quit()   

    def parse(self, response):
        HLtext = ""
        POJtext = ""
        contents = response.css('p.news_font2')
        HL = True
        for content in contents:
            check = content.css("strong span::text").get()
            if check != None and check[:3] == "台灣字":
                HL = False
                continue
            text = content.css("::text").get()
            if text == None:
                continue
            if HL:
                HLtext += text.strip()
            else:
                POJtext += text.strip() 
        yield{
            'time': response.css('span.date::text').get(),
            'title': response.css('.news_title::text').get(),
            'HLcontent': HLtext,
            'POJcontent': POJtext,
        }

            

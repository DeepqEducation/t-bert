import scrapy
import os

class PTSSpider(scrapy.Spider):
    name = "pts_taigi_news"

    
    def start_requests(self):
        cwd = os.getcwd()
        url = f"file://{cwd}/pts.html"
        yield scrapy.Request(url=url, callback=self.parse_url_in_html)
    
    def parse_url_in_html(self, response):
        urls = []
        urls += response.css(".xs-m-lr-5 .text-title2 a::attr(href)").getall()
        urls += response.css(".sm-list a::attr(href)").getall()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        text = ""
        contents = response.css('.article_content::text').getall()

        for content in contents:
            text += content.strip()
        yield{
            'time': response.css('.maintype-wapper h2::text').get(),
            'title': response.css('.article-title::text').get(),
            'content': text,
        }

            

# Data Source(漢羅、全羅)
[民報 台語世界](https://www.peoplenews.tw/list/%E5%8F%B0%E8%AA%9E%E4%B8%96%E7%95%8C)

# Prerequisite
Python >= 3.6 \
[docker](https://docs.docker.com/engine/install/ubuntu/) \
[Chrome](https://www.google.com/chrome/) \
Download suitable [chromedriver](https://chromedriver.chromium.org/) to the current directory.

## Python package
[Scrapy](https://docs.scrapy.org/en/latest/intro/install.html) \
[Selenium](https://selenium-python.readthedocs.io/installation.html) \
[scrapy-splash](https://github.com/scrapy-plugins/scrapy-splash)

You can install all dependencies by: \
`pip install -r requirements.txt`

# Usage 
## Step 1. Turn on splash docker for crawling website

```bash=
sudo docker pull scrapinghub/splash
sudo docker run -p 8050:8050 scrapinghub/splash
```
## Step 2. Start crawling
Turn on another terminal, and change into this directory. \
Parse the news and output the json file.
```bash=
scrapy crawl people_taigi_news -o people_taigi_news.json
```
This program parse all articles on the website to produce `people_taigi_news.json` \
After this step, you can shut down the docker started in **Step 1**.
## Step 3. Generate one line per article format
```bash=
python gen_people_one_article_per_line.py
```
This program read `paople_taigi_news.json` to produce `pts_one_article_per_line.txt`
# Data Source(全漢)
[公視新聞網 台語新聞](https://news.pts.org.tw/subcategory/177)

# Prerequisite
Python >= 3.6 \
[Chrome](https://www.google.com/chrome/) \
Download suitable [chromedriver](https://chromedriver.chromium.org/) to the current directory.

### Python package
[Scrapy](https://docs.scrapy.org/en/latest/intro/install.html) \
[Selenium](https://selenium-python.readthedocs.io/installation.html) \
[tqdm](https://github.com/tqdm/tqdm)

You can install all dependencies by: \
`pip install -r requirements.txt`

# Usage 
You can directly run `./get_pts_one_article_per_line.sh` or 
do the following 3 steps to get `pts_one_article_per_line.txt`

## Step 1. Get all ariticle links in PTS website
```bash=
python get_pts_urls.py
```
This program will turn up a browser, connect to the PTS website, continually click "載入更多" to get all article link, 
and save the final html file. \
The output is `pts.html` that contains all article links.\
(PTS website has 2 different format when using different browser window size. I use the smaller one)

## Step 2. Parse the news to generate the json file
```bash=
scrapy crawl pts_taigi_news -o pts_taigi_news.json
```
This program read `pts.html` and parse all articles to produce `pts_taigi_news.json`

## Step 3. Generate one article per line format
```bash=
python gen_pts_one_article_per_line.py
```
This program read `pts_taigi_news.json` to produce `pts_one_article_per_line.txt`
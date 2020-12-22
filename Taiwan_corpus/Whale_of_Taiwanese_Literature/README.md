This repository parse 海翁文學雜誌 (since 2010/05) from 華藝線上圖書館
https://www.airitilibrary.com/Publication/alPublicationJournal?PublicationID=P20121018003

# Prerequisite
Python >= 3.6 \
[Chrome](https://www.google.com/chrome/) \
Download suitable [chromedriver](https://chromedriver.chromium.org/) to the current directory.

## Python package
[Selenium](https://selenium-python.readthedocs.io/installation.html) \
[pdftotext](https://github.com/jalan/pdftotext)

You can install all of it by: \
`pip install -r requirements.txt`


# Usage 
## Step 1. Parse Content from library
First, you need to have a NTU VPN and connect to it

`python Whale_parser.py`

``` 
-r, --resume 
    resume from specific year-page written in current_year_page.log
```
This program will parse all pdf and store it into `PDF` folder. \
Because parse this website for a period of time will encounter advanced ReCaptcha,
you may want to stop program for a moment and use `-r` flag to resume from specific year-page written in `current_year_page.log`.


## Step 2. Convert all pdf to one article per line format
```python convert_all_pdf_to_one_file.py``` \
will produce `whale_articles_one_article_per_line.txt` which contains all aricles in folder `PDF`.

# Debug
## For each pdf, convert it to a independent file
```python convert_all_pdf_to_plain_text.py``` \
It will help you to discover what converted files look like.


## Explain `Whale_parser.py`
Here we explain design reasoning used in `Whale_parser.py`.
#### Solve captcha
When encounter captcha, we first save it to captcha.png, and split image to 5 digit.
There are 10 standard samples represents 0 to 9 in folder `standard_sample`.
For each digit, we compare it to our standard sample to decide the final answer with the most same pixel.

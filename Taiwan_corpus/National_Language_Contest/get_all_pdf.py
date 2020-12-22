import re
import requests
import openpyxl
from pathlib import Path

workbook = openpyxl.load_workbook('contest.xlsx')
worksheet = workbook['台語朗讀']


Path("contest_articles_pdf").mkdir(exist_ok=True)

i = 2
while worksheet[f'B{i}'].value != None:
    value = worksheet[f'B{i}'].value
    url, article_name = re.findall(r'"(.*?)"', value)
    url = url if url.startswith('http') else ('http://' + url)

    print(i, url, article_name)
    r = requests.get(url)
    if r.status_code != 404:
        with open(f"contest_articles_pdf/{article_name}.pdf", "wb") as f:
            f.write(r.content)    
    
    i += 1

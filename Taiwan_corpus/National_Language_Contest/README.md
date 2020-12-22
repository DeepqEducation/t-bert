Data Source(全漢):
http://ip194097.ntcu.edu.tw/longthok/longthok.asp

Download the table as .xlsx, the result file is equal to `contest.xlsx` in this directory.

## Prerequisite
[openpyxl](https://openpyxl.readthedocs.io/en/stable/) \
[pdftotext](https://github.com/jalan/pdftotext)

You can install all dependencies by: \
`pip install -r requirements.txt`

# Usage 

## Step 1. Download all pdf from the link in contest.xlsx

```bash=
python get_all_pdf.py
```
will get all pdf files in the folder `contest_articles_pdf`

## Step 2. Convert all pdf to one article per line format
```bash=
python convert_all_pdf_to_one_file.py
```
will produce `contest_one_article_per_line.txt` which contains all aricles in folder `contest_articles_pdf`.

# Debug 
## For each pdf, convert it to a independent file
```bash=
python convert_all_pdf_to_plain_text.py
```
It will help you to discover what converted files look like.



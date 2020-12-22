Data source link(全羅):
https://github.com/Taiwanese-Corpus/Khin-hoan_2010_pojbh

# Prerequisite
Python >= 3.6 


# Usage 
## Step 1. Download data from data source link
```bash=
git clone https://github.com/Taiwanese-Corpus/Khin-hoan_2010_pojbh
```
## Step 2. Generate one line per article format
```bash=
python gen_pojbh_one_article_per_line.py
```
This program will read `Khin-hoan_2010_pojbh/pojbh.json` and produce `pojbh_one_article_per_line.txt`

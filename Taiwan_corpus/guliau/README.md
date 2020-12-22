Data Source Link(漢羅、全羅):
https://github.com/Taiwanese-Corpus/Ungian_2005_guliau-supin

# Prerequisite
Python >= 3.4

# Usage 
## Step 1. Get data from data source link
```bash=
git clone https://github.com/Taiwanese-Corpus/Ungian_2005_guliau-supin
```

## Step 2. Generate one line per article format
```bash=
python gen_ungian_one_article_per_line.py
```
It will parse the data from `Ungian_2005_guliau-supin/轉換後資料`, and combine it into `guliau_one_article_per_line.txt`.

Note that I skip `Ungian_2005_guliau-supin/轉換後資料/HL/散文/陳雷/tbts-53-死人犯.txt` in the program.

Because there are many weird characters in it, results in useless subword when generate vocabulary.




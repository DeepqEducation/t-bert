Data Source Link(全漢): \
https://github.com/Taiwanese-Corpus/icorpus_ka1_han3-ji7 \
https://github.com/sih4sing5hong5/icorpus

# Prerequisite
Python >= 3.4
### Python package 
yaml

You can install yaml package by 
```bash=
pip install yaml
```

# Usage 
## Step 1. Get data from data source link
```bash=
git clone https://github.com/Taiwanese-Corpus/icorpus_ka1_han3-ji7

git clone https://github.com/sih4sing5hong5/icorpus
```

## Step 2. Generate one line per article format
```bash=
python gen_icorpus_one_article_per_line.py
```
It will parse `icorpus_ka1_han3-ji7/語料/自動標人工改漢字.txt` and seperate articles according to the sentences numbers in `icorpus/icorpus.yaml` \
There are 5 articles has different sentence number, I correct it manually in the `gen_icorpus_one_article_per_line.py`.


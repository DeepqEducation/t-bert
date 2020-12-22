This repository provide a script to generate Traidional Chinese Wikipedia training corpus

# Prerequisite 
[OpenCC](https://github.com/BYVoid/OpenCC)

You can install opencc on ubuntu by:
```bash=
sudo apt-get install opencc
```
# Usage 
`./get_zhtw_wiki.sh`

When this program is done, you will get `origin_wikicorpus_zh_one_article_per_line.txt` in folder `final`

#### Process steps written in `get_zhtw_wiki.sh`
Here explains what we do to preprocess zhtw wikipedia written in `get_zhtw_wiki.sh`

* Step 1. Download [zhtw wikipedia dump](https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2).

* Step 2. Extract articles from wikipedia dump using [WikiExtractor](https://github.com/attardi/wikiextractor).

* Step 3. combine all article into one file with one article per line format.

* Step 4. Translate all sentences from mixed Chinese characters to Traditional Chinese characters by using Opencc.
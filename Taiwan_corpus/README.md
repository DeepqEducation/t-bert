此repository包含：
* 產生T-BERT所需資料
* deepq.ai檔案結構
  
# T-BERT Data
如何產生T-BERT使用的文本資料

T-BERT 最終需要的檔案格式為：一篇文章一行，每篇文章用一個空行隔開，所有資料集都在同一個檔案下
```bash=
This is article 1, and all contents in article 1 should be in this line.

This is article 2. This article should be seperated by a blank line.

article 3 blah blah blah...
```
[T-BERT Data](wikicorpus_zh_one_article_per_line.txt)

## 準備Data步驟
### Step 1. 準備每個資料集的資料
Repository的每個子目錄底下，依照各個repository的操作步驟，得到各個資料集的彙整檔案，
各個資料集的彙整檔案格式一樣是採取一篇文章一行、每篇文章用空行隔開的格式。\
各資料集最終檔案命名為：`<資料集名稱>_one_article_per_line.txt` \
舉例來說：在pts_crawler資料夾底下，解釋的是如何產生最終檔案`pts_one_article_per_line.txt` 


#### 以下為T-BERT全部所使用到的資料
分為國語、台語、客語，
下列提供各資料集的`Code資料夾名稱`，以及最後`彙整檔案的名稱` \
各資料集的one_article_per_line可到此[t-bert.deepq.ai](https://t-bert.deepq.ai/download/All_one_article_per_line/)下載 \
繁體中文 : `zhtw` \
台語 : `taigi` \
客語 : `hakka` \

### 繁體中文 (zhtw)
* 自由時報: 
  - Code資料夾名稱：未上傳
  - 彙整檔案名稱：`ltn_one_aritcle_per_line.txt`

* Wikipedia: 
  - Code資料夾名稱：`Traditional_Chinese_Wikipedia`
  - 彙整檔案名稱：`wikicorpus_zh_one_article_per_line_origin.txt`
### 台語 (taigi)
* 公視 台語新聞(全漢): 
  - Code資料夾名稱：`pts_crawler`
  - 彙整檔案名稱：`pts_one_article_per_line.txt`
* 民報 台語世界(漢羅、全羅): 
  - Code資料夾名稱：`people_crawler`
  - 彙整檔案名稱：`people_one_article_per_line.txt`
* 全國語文競賽(全漢): 
  - Code資料夾名稱：`National_Language_Contest`
  - 彙整檔案名稱：`contest.txt`
* 海翁文學雜誌(全漢、漢羅、全羅)： 
  - Code資料夾名稱：`Whale_of_Taiwanese_Literature`
  - 彙整檔案名稱：`whale_one_article_per_line.txt`
* 台灣白話字文獻館(全羅): 
  - Code資料夾名稱：`pojbh`
  - 彙整檔案名稱：`pojbh_one_article_per_line.txt`
* 台語文語料庫蒐集及語料庫為本台語書面語音節詞頻統計(漢羅、全羅): 
  - Code資料夾名稱：`guliau`
  - 彙整檔案名稱：`guliau_one_article_per_line.txt`
* 臺華平行新聞語料庫(全漢): 
  - Code資料夾名稱：`icorpus`
  - 彙整檔案名稱：`icorpus_one_article_per_line.txt`
### 客家語 (hakka)
* 臺華平行新聞語料庫: 
  - Code資料夾名稱：未上傳
  - 彙整檔案名稱：`hakka_one_article_per_line.txt`

### Step 2. 串接所有彙整檔案
各個資料夾產生彙整資料，並將所有`<資料集名稱>_one_article_per_line.txt`移到到同一資料夾底下，將所有的彙整資料串接在一起即可，用以產生最終T-BERT訓練文本。
全部資料集的資料夾名稱為`All_one_article_per_line`
檔案結構如下:
```bash
Taiwan_corpus/
├── All_one_article_per_line/
│   ├── contest_one_article_per_line.txt
│   ├── guliau_one_article_per_line.txt
│   ├── hakka_data_one_article_per_line.txt
│   ├── icorpus_one_article_per_line.txt
│   ├── ltn_one_article_per_line.txt
│   ├── people_one_article_per_line.txt
│   ├── pojbh_one_article_per_line.txt
│   ├── pts_one_article_per_line.txt
│   ├── whale_one_article_per_line.txt
│   └── origin_wikicorpus_zh_one_article_per_line.txt
└── combine_all_articles.py
```
使用此目錄底下的`combine_all_articles.py`進行串接，將所要合併的`<資料集名稱>_one_article_per_line.txt`放在某一目錄底下，
執行: \
`python combine_all_articles.py -i <input_folder> -o <output_filename>` 

在本專案中，可至`Taiwan_corpus`目錄底下執行: \
`python combine_all_articles.py -i All_one_article_per_line -o wikicorpus_zh_one_article_per_line.txt` \
產生T-BERT所使用的文本檔案`wikicorpus_zh_one_article_per_line.txt`

**注意**：檔案名稱必須為`wikicorpus_zh_one_article_per_line.txt`

T-BERT使用的`wikicorpus_zh_one_article_per_line.txt`檔案可至[t-bert.deepq.ai](https://t-bert.deepq.ai/download/Final_Pretraining_Data/)下載 




# `Taiwanese_corpus`
[t-bert.deepq.ai](https://t-bert.deepq.ai/download/)

| 目錄名稱 | 用途 |
| ----|----|
| All_one_article_per_line | 所有資料集的最終彙整檔案，依語言分類 |
| Final_Pretraining_Data | 最終用於T-BERT使用的所有彙整檔案 |
| Fine-tuning task | 產生下游任務的資料及code |
| huggingface_tbert_base | T-BERT base預訓練10k步，並且相容於HuggingFace |
| text_data | 所有資料集的最終彙整檔案以及包含未轉換的json、pdf檔，依資料集分類 |



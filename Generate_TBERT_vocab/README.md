This repository explains how to generate T-BERT vocabulary 

# Prerequisite
### Python package
nltk \
numpy \
six \
tensorflow 1.15

Install all dependencies by: \
`pip install -r requirements.txt`

# Vocabulary
The final vocabulary we use to train T-BERT is the same as `example_tbert_vocab.txt`.

# Usage
First, for each lanuage, you need to make a folder for it. \
Then put all your `<資料集名稱>_one_article_per_line.txt` in the folders they belong to. \
In T-BERT, create 3 folders named `zhtw`, `taigi`, `hakka`. \
Download `zhtw`, `taigi`, `hakka` use for T-BERT on [t-bert.deepq.ai](https://t-bert.deepq.ai/download/All_one_article_per_line/) \
The following data and directory structure to generate T-BERT vocabulary. 
```bash=
Generate_TBERT_vocab/
├── zhtw
│   ├── ltn_one_article_per_line.txt
│   └── origin_wikicorpus_zh_one_article_per_line.txt
├── taigi
│   ├── contest_one_article_per_line.txt
│   ├── guliau_one_article_per_line.txt
│   ├── hakka_data_one_article_per_line.txt
│   ├── icorpus_one_article_per_line.txt
│   ├── people_one_article_per_line.txt
│   ├── pojbh_one_article_per_line.txt
│   ├── pts_one_article_per_line.txt
│   └── whale_one_article_per_line.txt
├── hakka
│   └── hakka_data_one_article_per_line.txt
├── bert-vocab-builder
│   ├── README.md
│   ├── subword_builder.py
│   ├── text_encoder.py
│   └── tokenizer.py
├── clean_chinese_in_vocab.py
├── combine_all_articles.py
├── gen_taiwan_vocab.sh
├── get_bpe_train_ranking.py
├── README.md
├── example_tbert_vocab.txt
├── tokenization.py
└── tokenize_sents.py
```

Run `./gen_taiwan_vocab.sh` \
This script will generate `tbert_vocab.txt` which will be used for training T-BERT. \
It will take some time to process.

### Generating script `gen_taiwan_vocab.sh` explanation:
Here explains what we do to generate T-BERT vocabulary written in `gen_taiwan_vocab.sh` \
In `gen_taiwan_vocab.sh`, First need to specify which language we want to process. \
Use `zhtw`, `taigi`, `hakka`
#### Step 1. Combine all articles into one file for each language
For each language, combine all articles into `<language>_one_article_per_line.txt` by using `combine_all_articles.py`. \
After this step,  get 3 files named `zhtw_one_article_per_line.txt`, `taigi_one_article_per_line.txt`, `hakka_one_article_per_line.txt`.

#### Step 2. For each language, tokenize `<language>_one_article_per_line.txt`into sentences
Add space around every chinese character and punctuation, 
then split sentences using period `.` and `。` by using `tokenize_sents.py` \
The processed file is named `<language>.train`. \
Similar to last step, you will get 3 files named `zhtw.train`, `taigi.train`, `hakka.train`

#### Step 3. Sampling sentences from different language sentences
This step will produce one file named `bpe.train.factor=<sampling_ratio>` consists of different language sentences. \
The sampling method is mentioned in section 3.2 in [XLM paper](https://arxiv.org/abs/1901.07291) \
Use the script `get_bpe_train_ranking.py` provided by aconneau (one of XLM authors) in [XLM issue #102](https://github.com/facebookresearch/XLM/issues/102) to sample the sentences from different language. \

In order to use the script, first need to make a `lg2count.txt` tsv file, which first column is language (e.g., "zhtw", or "taigi") and second column is the number of lines. I use `wc -l` to count the number of lines. \
Then use the following command the run the script:
```bash=
lgs="zhtw-taigi-hakka"
python get_bpe_train_ranking.py --S 0.3 --scale 1e2 --lgs $lgs
```
It will read `lg2count.txt` and `{zhtw, taigi, hakka}.train` files, and produce one file named `bpe.train.factor=0.3`

Use `--debug` to see the sampling ratio and number of sentences sampled from each language, and it do **NOT** run the sampling processing.
Assume have the following `lg2count.txt`
```bash=
zhtw	54007957
taigi	1485661
hakka	226992
```
```bash=
lgs="zhtw-taigi-hakka"
python get_bpe_train_ranking.py --S 0.3 --scale 1e2 --lgs $lgs --debug
```
The output is:
```bash=
zhtw - before resampling: 96.93 - after resampling: 65.19
taigi - before resampling: 2.67 - after resampling: 22.18
hakka - before resampling: 0.41 - after resampling: 12.63
zhtw : 117204614
shuf -r -n 117204614 zhtw.train >> bpe.train.factor=0.3
taigi : 39882585
shuf -r -n 39882585 taigi.train >> bpe.train.factor=0.3
hakka : 22699200
shuf -r -n 22699200 hakka.train >> bpe.train.factor=0.3
```
##### Sampling script explanation
`get_bpe_train_ranking.py` use the following exponential smooth formula to decide sampling probability: \
Assume  have language $\{L_i\}$ for $i=1...k$. Let $n_i$ be the number of lines of language $L_i$ \
in T-BERT, $k=3$. \
The probability $p_i$ to sample sentences from language $L_i$ with sampling factor $S$ is:
$$p_i = \frac{n_i^S}{\sum_{j=1}^{k}n_j^S}$$

With $S < 1$, which means we upsample the low resource languages. Here we use $S=0.3$. \
There is also a `scale` parameter to control how many times of total sentences we want to upsample.
This parameter is aimed to control the minimum number of sentences of each language.
If scale = 1e2, it means we sample 100 times original number of sentences.


#### Step 4. Generate T-BERT Vocab
Based on this [bert-vocab-builder repository](https://github.com/kwonmha/bert-vocab-builder). \
The [bert-vocab-builder repository](https://github.com/kwonmha/bert-vocab-builder) uses [tensor2tensor library script](https://github.com/tensorflow/tensor2tensor/blob/master/tensor2tensor/data_generators/text_encoder_build_subword.py) and modify it to suit for BERT tokenizer. \
Use `min_count=5` and `num_iterations=4` to control our vocabulary size is around 10k:
```bash=
python bert-vocab-builder/subword_builder.py \
--corpus_filepattern=bpe.train.factor0.3 \
--output_filename=tbert_uncleaned_vocab.txt \
--min_count=5 \
--num_iterations=4 
```

Further add `[unused]` subwords like the original BERT vocabulary, and remove all `#<Chinese charactor>` (e.g., ##好, ##你), because it is never used in BERT tokenizer.
```bash=
python clean_chinese_in_vocab.py -i tbert_uncleaned_vocab.txt -o tbert_vocab.txt
```
Finally, you will get T-BERT vocabulary `tbert_vocab.txt` use for training T-BERT.



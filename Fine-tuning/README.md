使用HuggingFace BERT Model來Fine-tune國語新聞及台語新聞

## 資料集概述
句子分類(sentence classification)任務，與[GLUE](https://gluebenchmark.com/)當中的`sst-2`任務相似。
### 自由時報國語新聞 dataset 
此資料集是[自由時報](https://www.ltn.com.tw/)2017年的新聞及分類， \
有8類新聞：生活、娛樂、社會、運動、政治、國際、地方、財經 \
#### 資料集下載
[ltn_data](https://t-bert.deepq.ai/download/Fine_tuning%20task/ltn_data)
`original`是自由時報原始的文章以及分類標籤，`train_dev`以及`test`資料夾是藉由執行以下指令得到
```bash=
python gen_ltn_train_dev_test_data.py 
```
讀取original中的檔案，將檔案以8：1：1切成train:val:test \
格式為tsv，第1個column的header為`sentence`，內容是新聞文章， \
第2個column的header為label，內容為新聞分類對應到的編號

### 台華平行新聞語料庫 dataset
此資料集是從[台華平行新聞語料庫](https://github.com/sih4sing5hong5/icorpus)得來，
或者可看[網頁版內容](http://icorpus.iis.sinica.edu.tw/)。 \
格式如下：

| 標題 | 內容 |
| ----|----|
| 新聞類別 | 國際 |
| 繁體中文 | 美國國會宣佈歐巴馬當選第四十四任總統 |
| 臺語羅馬字 | Bi2-kok kok-hoe7 soan-pou3 Obama tong3-soan2 te7-si3-chap-si3-jim7 chong2-thong2 |

本專案使用臺語的羅馬字版本。\
新聞總共有14類： 社會、生活、地方、政治、國際、教育、藝文、環境、健康、運動、旅遊、科技、影劇、財經，共3266篇文章
#### 資料集下載
[taigi_POJ_data](https://t-bert.deepq.ai/download/Fine_tuning%20task/taigi_POJ_data)


## Fine-tuning
下載上述兩個dataset，執行`script`資料夾底下的script來執行fine-tuninig。\
script的命名規則為`<資料集名稱>_<Model名稱>_{training, eval}.sh` \
請在當前`Fine-tuning`資料夾執行`sbatch <script>`的動作

### Step 1. 將Model下載到當前目錄，更改script內的路徑，環境名稱
`taigi_POJ_Tbert_base_training.sh`
* sbatch log檔名稱: \
`<資料集名稱>_<句子長度>_<Model名稱>_<learning_rate>_{training, eval}_log_<job_id>`

* 更改`account`, `partition`等資訊

* 更改`conda activate <環境名稱>`，國網中心的miniconda環境名稱，該環境需要[安裝Huggingface transformer](https://huggingface.co/transformers/installation.html)，以及apex用以`mixed precision training`

`run_ltn.py`的參數，可參考huggingface上面的[example](https://github.com/huggingface/transformers/tree/master/examples/text-classification)。
如下：
* `WORKDIR`為到當前`Fine_tuning`資料夾的路徑
* `DATADIR`為到各資料集`train_dev`的路徑
* `MODEL_DIR`為到Model資料夾的路徑
* `TASK_NAME` 為`tagi`跟`ltn`

更改後執行 `sbatch script/<script名稱>` \
如 ： `sbatch script/taigi_POJ_Tbert_base_training.sh`
有tensorboard將會存至`runs`資料夾
### Step 2. Evaluation
產生儲存每個checkpoint的Model資料夾\
`taigi_POJ_512_Tbert_base_5000_results` \
資料夾第一層會為最終Model，如下：
```bash=
taigi_POJ_512_Tbert_base_5000_results/
├── checkpoint-1000
│   ├── config.json
│   ├── optimizer.pt
│   ├── pytorch_model.bin
│   ├── scheduler.pt
│   └── training_args.bin
├── checkpoint-1200
│   ├── config.json
│   ├── optimizer.pt
│   ├── pytorch_model.bin
│   ├── scheduler.pt
│   └── training_args.bin
├── config.json
├── eval_results_taigi.txt
├── pytorch_model.bin
├── special_tokens_map.json
├── tokenizer_config.json
├── training_args.bin
└── vocab.txt
```
**注意** ： 
每個checkpoint資料夾底下缺少`vocab.txt`跟`tokenizer_config.json`，必須手動複製到每個checkpoint資料夾

執行`sbatch script/taigi_POJ_Tbert_base_eval.sh`，該script會對資料集的`train_dev`內的`dev.tsv`做一次evalution，
把所有結果存在`taigi_POJ_512_Tbert_base_5000_val_results.txt`。\
並資料集的`test`內的`dev.tsv`做一次evalution，把結果存在`taigi_POJ_512_Tbert_base_5000_test_results.txt`

該目錄下有範例檔案

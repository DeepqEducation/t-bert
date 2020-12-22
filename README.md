# T-BERT
本專案是基於[BERT for Pytorch](https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/LanguageModeling/BERT)進行延伸開發，包含訓練T-BERT模型之script以及步驟，並且使用國網中心High Performance Computing (HPC)進行多節點高速運算，提供Pytorch的T-BERT模型以及使用方式


## T-BERT下載
* [T-BERT-Base, Cased](https://t-bert.deepq.ai/download/huggingface_tbert_base/): 12-layer, 768-hidden, 12-heads , 90k vocabulary.

## 快速使用T-BERT
##### T-BERT相容於[Huggingface Transformers](https://github.com/huggingface/transformers),可使用[Huggingface Transformers](https://github.com/huggingface/transformers)進行下游任務的訓練
下載[T-BERT-Base, Cased](https://t-bert.deepq.ai/download/huggingface_tbert_base/)至`huggingface_tbert_base`目錄

```
from transformers import BertTokenizer, BertModel

tokenizer = BertTokenizer.from_pretrained("huggingface_tbert_base")
model = BertModel.from_pretrained("huggingface_tbert_base")
```

# Train T-BERT
## 訓練環境：
國網中心 高速計算服務（TWCC HPC）

## Step 1. 準備資料
Pre-training資料的格式必須為一篇文章一行，範例為:
`bert/data/formatted_one_article_per_line/wikicorpus_zh_one_article_per_line.txt` 
#### Pre-training資料下載
[t-bert.deepq.ai](https://t-bert.deepq.ai/download/Final_Pretraining_Data/)
#### 使用自己的Pre-training資料
依照[Taiwan_corpus](Taiwan_corpus)步驟產生檔名為`wikicorpus_zh_one_article_per_line.txt`的Pre-training資料,並將`wikicorpus_zh_one_article_per_line.txt`移至`bert/data/formatted_one_article_per_line` 

**注意**：最後檔案名稱一定要取成`wikicorpus_zh_one_article_per_line.txt`



## Step 2. 產生Vocabulary
#### Vocabulary資料下載
[tbert_vocab.txt](bert/vocab/tbert_vocab.txt)
#### 使用自己的Pre-training資料產生Vocabulary
依照[Generate_TBERT_vocab](Generate_TBERT_vocab),並且使用`<資料及名稱>_one_article_per_line.txt`檔案產生T-BERT所需要的vocabulary。 

## Step 3. 下載此專案並且設定環境
#### Clone the repository
```bash=
git clone https://github.com/DeepqEducation/t-bert.git
cd t-bert
```

#### Download the singularity image
Singularity ： 類似於docker，利用已經架設好的環境，但是不需要root權限，且能夠讓環境內外的檔案系統更容易互通。

```bash=
module load singularity
singularity pull docker://nvcr.io/nvidia/pytorch:19.12-py3
```

## Step 4. 從文本生成Pre-training資料
<!-- ### Create Pre-training data -->
請檢視`bert/data/create_Tbert_datasets_from_start.sh`，該檔案是從`bert/data/create_datasets_from_start.sh`進行延伸。\
可自行更動:
* `WORKSPACE`：為到`t-bert` repository的路徑(如果在家目錄clone t-bert，則不需要修改).
* `SINGULARITY_PATH`：為到`singularity image`的路徑（依照步驟在t-bert目錄下執行singualrity pull docker，則不需更改）

接續Step 1跟2，可直接執行`sbatch bert/data/create_Tbert_datasets_from_start.sh`

**注意**：須自行修改script中`account`，`partition`

`create_Tbert_datasets_from_start.sh`包含2項前處理：

1. 將`wikicorpus_zh_one_article_per_line.txt`內的文章做斷句，並依照句數，將資料儘量平均分散儲存成多個檔案，再分成train跟test data
檔案格式為：\
一句一行，不同文章之間會再多一行空白行進行區隔，儲存在`bert/data/sharded_training_shards_512_test_shards_512_fraction_0.2/wikicorpus_zh/`，該資料夾包含切分為512個檔案的pretrain data，train:test比例為8:2。 \
train的檔名為：`wikicorpus_zh_training_[0-511].txt` \
test的檔名為：`wikicorpus_zh_test_[0-511].txt`

2. 產生訓練T-BERT的pre-training所需的tensor，對分散儲存的資料做tokenize，將句子的Masked Language Model (MLM)跟Next Sentence Prediction(NSP)的label儲存成HDF5，並儲存在`bert/data/hdf5_lower_case_0_seq_len_512_max_pred_80_masked_lm_prob_0.15_random_seed_12345_dupe_factor_5` \
train的檔名為：`wikicorpus_zh_training_[0-511].hdf5` \
test的檔名為：`wikicorpus_zh_test_[0-511].hdf5`

**注意**：此步驟耗時，4G的文本資料約需六小時。

#### 解釋`bert/data/create_Tbert_datasets_from_start.sh`
使BERT For PyTorch的`create_datasets_from_start.sh`相容於TWCC HPC+Singularity的環境

在BERT For PyTorch中，使用docker將`bert`這個資料夾放在`/workspace/`底下， \
在此專案中透過`singularity -B <t-bert路徑>:/workspace`，將`t-bert`資料夾bind成singularity環境裡的`/workspace`，之後singularity內的指令下給`/workspace`等同於下給`t-bert`。

此外BERT For PyTorch有一個環境變數`BERT_PREP_WORKING_DIR=/workspace/bert/data`，要更改singularity內的環境變數必須設定一個外層的環境變數，
`SINGULARITYENV_<內部環境變數名稱>=<變數值>`，所以我們會在每個singularity指令前加上`SINGULARITYENV_BERT_PREP_WORKING_DIR=/workspace/bert/data`。

`create_datasets_from_start.sh`在此專案所進行更動：
* 移除在BERT For PyTorch中會下載squad dataset，google pretrain weight的動作
* 移除在BERT For PyTorch下載bookcorpus，wikipedia，並對資料做預處理的工作：
* 移除BERT For PyTorch中的128長度訓練，只採用訓練512長度的訓練方法
* 產生HDF5的時候可自行更動的參數：
  * vocab檔案路徑 : 本專案將`t-bert`bind成`/workspace`，如`/workspace/bert/vocab`相等於`t-bert/bert/vocab`
  * `do_lower_case 0`本專案為中文模型，取消將文字轉為小寫的動作
## Step 5. 開始Pre-training

請檢視`bert/run_Tbert.sub`，該檔案為`bert/run.sub`延伸修改。\
同步驟4，需要自定義`WORKSPACE`、`SINGULARITY_PATH`變數。\
`output_dir`為儲存model的資料夾名稱，預設為`Tbert_base`，放在t-bert目錄下 \
`datadir`為步驟4產生的資料夾名稱，預設為`/workspace/bert/data/hdf5_lower_case_0_seq_len_512_max_pred_80_masked_lm_prob_0.15_random_seed_12345_dupe_factor_5/wikicorpus_zh` 

自定義`/bert/run_pretraining.py`預訓練的參數 \
`bert/run_pretraining.py`完整參數介紹，可參照`bert/README.md`中的`Advanced/Parameters/Pre-training parameters`。 \
如下:
`max_seq_length`: 訓練句子長度 \
`max_steps`: 訓練步數（一次gradient更新為一步） \
`num_steps_per_checkpoint`:幾步儲存一個checkpoint \
`config_file`: 指定到Model config的路徑，該config包含Model的架構、層數、vocabulary數量等等，本專案在`bert``Tbert_base_config.json`以及`Tbert_large_config.json`，請根據Model架構以及字典大小，修改config。

自定義`train_batch_size`、`learning_rate`、`gradient_accumulation_step`以及node個數，在執行指令的環境變數中指定：

在8個node(每個node有8張32GB V100)總共64顆GPU預訓練T-BERT Large
<!-- We use the following command to train T-BERT large on 8 nodes (with 8 V100 32GB in each node):\ -->
`BATCHSIZE=512 LR=4e-3 GRADIENT_STEPS=64 sbatch -N8 --ntasks-per-node=8 bert/run_Tbert.sub`

以及 T-BERT Base:\
`BATCHSIZE=512 LR=4e-3 GRADIENT_STEPS=32 sbatch -N8 --ntasks-per-node=8 bert/run_Tbert.sub`

訓練完成的Model將會放至`datadir`

其中Node數量設定:`-N<節點數量>`，16個節點為`-N16` \
TWCC的每個節點皆為八顆GPU，因此`--ntasks-per-node=8` \
`LR`也就是learning rate

剩下設置`BATCHSIZE`、、`GRADIENT_STEPS`請參考下列設定教學

使用兩階段長度訓練，請參考`bert/README.md`的`Advanced/Parameters/Multi-node`的訓練指令
script可以參考`bert/run_Tbert.sub`及`bert/run.sub`修改

### `BATCHSIZE` 及 `GRADIENT_STEPS` 設定教學
注意此處 `BATCHSIZE`的定義跟其他地方有些不一樣。 \
定義公式如下： \
`Effective Batch Size` * `Gradient Accumulation Steps` * `Number of GPUs` = `Global Batch Size` \
其中參數`GRADIENT_STEPS`即為上述公式的`Gradient Accumulation Steps`，代表累加幾次gradient做一次backward pass。 \
但是本專案中`BATCHSIZE`定義為`Effective Batch Size` * `Gradient Accumulation Steps`

例如： \
訓練長度512且`Global Batch Size`=32768，train在64顆GPU上，
參數`BATCHSIZE`必須設成32768/64=512 \
可以調整參數`GRADIENT_STEPS`來測試`Effective Batch Size`的極限
`GRADIENT_STEPS`為64，代表`Effective Batch Size`=8，表示GPU一次載入8個instance.

在T-BERT中，設定`global batch size`＝ 65536 訓練長度128 以及 `global batch size`＝ 32768 訓練長度512，
train在64顆GPU上，參數`BATCHSIZE`=32768/64=512。
且經測試後，每個GPU一次只能載入8個instance，因此累加步數`GRADIENT_STEPS`為512/8=**64**

Tbert-Large：
- 句子長度 128, 每個GPU最大可以載入共64個instance:

`BATCHSIZE`=65536/( <#nodes>*<#GPUs per node> ) = 65536/( Total number of GPUs in the whole cluster )

`GRADIENT_STEPS`=`BATCHSIZE`/64

- 句子長度 512, 每個GPU最大可以載入共8個instance:

`BATCHSIZE` = 32768/( <#nodes>*<#GPUs per node> ) = 32768/( Total number of GPUs in the whole cluster )

`GRADIENT_STEPS`=`BATCHSIZE`/8

T-BERT-Base:

- 句子長度 512, 每個GPU最大可以載入共16個instance:

`BATCHSIZE` = 32768/( <#nodes>*<#GPUs per node> ) = 32768/( Total number of GPUs in the whole cluster )

`GRADIENT_STEPS` = `BATCHSIZE` / 16

## Step 6. 將本專案Model轉換成HuggingFace BERT Model

```bash=
python convert_nvidia_bert_to_hugginface_bert.py -i <NVIDIA_BERT_checkpoint> -o <output_foldername> -c <BERT_config> -v <vocab.txt>
```
`NVIDIA_BERT_checkpoint`本專案所儲存的checkpoint，檔名通常為`ckpt_<訓練步數>.pt` \
`output_foldername`為要儲存的資料夾名稱 \
`BERT_config`步驟5之config，包含Model架構，vocabulary數量等 \
`vocab.txt`

訓練Tbert_base的步驟，可用下列指令轉換
```
python convert_nvidia_bert_to_hugginface_bert.py -i tbert_base/ckpt_10000.pt -o huggingface_tbert_base -c bert/Tbert_base_config.json -v bert/vocab/tbert_vocab.txt
```
最後產出 [T-BERT-Base, Cased](https://t-bert.deepq.ai/download/huggingface_tbert_base/)


# Reference
[BERT For PyTorch](https://github.com/NVIDIA/DeepLearningExamples/tree/e159774d3eeb778b253408d5c910519cf9709a20/PyTorch/LanguageModeling/BERT)


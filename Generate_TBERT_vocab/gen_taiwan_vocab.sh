#!/bin/bash
set -e

lgs=("zhtw" "hakka" "taigi")

for lg in ${lgs[@]}
do 
    python combine_all_articles.py -i ${lg} -o ${lg}_one_article_per_line.txt
done

for lg in ${lgs[@]}
do 
    python tokenize_sents.py -i ${lg}_one_article_per_line.txt -o ${lg}.train
done

for lg in ${lgs[@]}
do
    count=($(wc -l ${lg}_one_article_per_line.txt))
    echo -e "$lg\t${count[0]}" >> lg2count.txt
done


lgs="zhtw-taigi-hakka"
python get_bpe_train_ranking.py --S 0.3 --scale 1e2 --lgs $lgs

python bert-vocab-builder/subword_builder.py \
--corpus_filepattern=bpe.train.factor0.3 \
--output_filename=tbert_uncleaned_vocab.txt \
--min_count=5 \
--num_iterations=4 

python clean_chinese_in_vocab.py -i tbert_uncleaned_vocab.txt -o tbert_vocab.txt
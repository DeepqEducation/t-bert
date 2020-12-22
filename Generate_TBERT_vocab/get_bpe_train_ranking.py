"""
get_bpe_train_ranking.py
Get bpe training set from "$lg.train" files of several languages
"""
import os
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Creation of bpe.train')
parser.add_argument("--S", type=float, default=0.5, help="exponent subsampling factor")
parser.add_argument("--lgs", type=str, default="", help="list of languages hyphen-separated")
parser.add_argument("--scale", type=float, default=1e4, help="controls the minimum number of sentences of each language")
parser.add_argument('--debug', dest='debug', action='store_true')
parser.set_defaults(debug=False)

params = parser.parse_args()

# get the number of words in the corpus of each language 
# lg2count.txt -> tsv file: first column is language (e.g. "en", or "fr") and second column is number of lines
lg2count = {}
with open('lg2count.txt') as f:
    for line in f:
        line = line.rstrip().split('\t')
        lg, count = line[0], int(line[1])
        lg2count[lg] = count
        assert lg2count[lg] > 0, lg

# downsample (S < 1) or upsample (S>1) the importance of high-resource languages
S = params.S
tot = sum([lg2count[lg] for lg in lg2count])
tot_S = sum([lg2count[lg]**S for lg in lg2count])
if params.debug:
    for lg in lg2count:
        print('%s - before resampling: %.2f - after resampling: %.2f' % (lg, 100.0 * lg2count[lg] / tot, 100.0 * lg2count[lg]**S / tot_S))

# minimum count and minimum probability
min_c = min([lg2count[lg] for lg in lg2count])
min_p = min([lg2count[lg]**S for lg in lg2count]) / tot_S

# scale:
for lg in params.lgs.split('-'):
    p = lg2count[lg]**S / tot_S
    print('%s : %.0f' % (lg, params.scale * min_c * (p / min_p)))
    COMMAND = "shuf -r -n %.0f %s.train >> bpe.train.factor=%s" % (params.scale * min_c * (p / min_p), lg, params.S)
    if params.debug:
        print(COMMAND)
    else:
        os.system(COMMAND)
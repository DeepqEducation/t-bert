import argparse
from tokenization import _is_chinese_char, _is_punctuation

parser = argparse.ArgumentParser()
parser.add_argument("--input_vocab", "-i", type=str)
parser.add_argument("--output", "-o", type=str, default="tbert.vocab")
params = parser.parse_args()

reader = open(params.input_vocab)

BERT_TOKEN = ["[UNK]", "[CLS]", "[SEP]", "[MASK]"]

def _is_chinese_or_punctuation(ch):
    return _is_chinese_char(ch) or _is_punctuation(ch)

with open(params.output, "w") as writer:
    writer.write("[PAD]\n")
    for i in range(1, 100):
        writer.write(f"[unused{i}]\n")
    for token in BERT_TOKEN:
        writer.write(token +'\n')
    for idx, word in enumerate(reader):
        if idx <= 5:
            continue
        if len(word) >= 3 and word[:2] == "##" and _is_chinese_or_punctuation(word[2]):
            continue
        writer.write(word)
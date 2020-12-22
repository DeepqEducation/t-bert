import glob
import os 
import argparse
from pathlib import Path
from tokenization import NLTKSegmenter

parser = argparse.ArgumentParser(description="tokenize one article per line into one sentence per line")
parser.add_argument("--input", "-i", type=str, default="language_train")
parser.add_argument("--output", "-o", type=str, default="lg.train")

args = parser.parse_args()

filename = args.input
output = args.output

segmenter = NLTKSegmenter()

# Path(output).mkdir(parents=True, exist_ok=True)


basename = os.path.basename(filename)
with open(filename, "r") as reader, open(output, "w") as writer:
    for line in reader:
        if line.strip() != "":
            segments = segmenter.segment_string(line)
        for segment in segments:
            writer.write(segment +'\n')
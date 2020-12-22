import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input_folder", "-i", type=str)
parser.add_argument("--output_filename", "-o", type=str)

args = parser.parse_args()

folder = args.input_folder
output = args.output_filename
filenames = glob.glob(folder+"/"+"*")

writer =  open(output , "w")
for filename in filenames:
    with open(filename, "r") as reader:
        for line in reader:
            if line.strip() == "":
                continue
            writer.write(line.strip() + '\n\n')

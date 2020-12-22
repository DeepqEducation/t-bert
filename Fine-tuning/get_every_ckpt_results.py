import argparse 
import glob
import re


model_dir = "ltn_256_Tbert_base_10000_results"
output_filename = "ltn_256_Tbert_base_10000_val_results.txt"
task = "taigi"
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--model_dir", default=model_dir, type=str, 
        help="Specify the output folder where the checkpoint live in."
    )
    parser.add_argument("-o", "--output_filename", default=output_filename, type=str, 
        help="Specify the output result filename "
    )
    parser.add_argument("-t", "--task", default=task, type=str, 
        help="Specify the taskname "
    )

    args = parser.parse_args()
    base = args.model_dir

    filenames = glob.glob(base+'/'+f"checkpoint-*/eval_results_{args.task}.txt")
    filenames.sort(key = lambda x: int(re.sub('\D', '', x)))
    result_f = open(args.output_filename, "w")
    filenames.append(base+'/'+f"eval_results_{args.task}.txt")
    for filename in filenames:
        with open(filename, "r") as f:
            score = f.read()
            result_f.write(filename.split('/')[-2]+'\n')
            result_f.write(score)

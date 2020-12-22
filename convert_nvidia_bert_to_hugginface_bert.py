import os
import glob
import torch
import argparse
from pathlib import Path
from shutil import copy
from transformers import BertModel, BertConfig, BertTokenizer



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--nv_checkpoint_path', type=str, required=True,
                        help="Path to nvidia bert checkpoint")

    parser.add_argument("-o", "--huggingface_dump_foldername", type=str, required=True, 
                        help="Path to the output huggingface model.")

    parser.add_argument('-c', '--config', type=str, required=True,
                        help="The config json file specifies the model architecture.")

    parser.add_argument('-v', '--vocab', type=str, required=True,
                        help="the vocabulary file")
    
    args = parser.parse_args()

    config = BertConfig.from_json_file(args.config)
    print(config)

    nvidia_model_path = args.nv_checkpoint_path
    huggingface_dump_path = args.huggingface_dump_foldername
    # nvidia_model_paths = glob.glob(os.path.join(args.input_folder, "*.pt"))
    # for nvidia_model_path in nvidia_model_paths:
    nvidia_model = torch.load(nvidia_model_path)
    state_dict = { k.replace('bert.','').replace('.dense_act','.dense'): v \
        for k,v in nvidia_model['model'].items() if k[:3] != "cls"}

    model = BertModel.from_pretrained(None, config=config, state_dict=state_dict)
    tokenizer = BertTokenizer.from_pretrained(args.vocab, do_lower_case=False)
    basename = os.path.basename(nvidia_model_path)
    # p = Path(f"huggingface_{args.input_folder}_{basename}")
    p = Path(huggingface_dump_path)
    p.mkdir()
    model.save_pretrained(p)
    tokenizer.save_pretrained(p)
    # copy(args.vocab, p/"vocab.txt")
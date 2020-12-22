#!/bin/bash

#SBATCH -J finetune
#SBATCH -o taigi_POJ_512_Tbert_base_5000_2e5_training_log_%j
#SBATCH -N 1
#SBATCH --account=GOV109042
#SBATCH --partition=gp4d
#SBATCH --mem=0
#SBATCH --cpus-per-gpu=4
#SBATCH --ntasks-per-node=8
#SBATCH --gres=gpu:8


module purge 
module load miniconda3
module load nvidia/cuda/10.0
conda activate mypytorch


WORK_DIR=/work/mingyen066/news_classification
DATA_DIR=${WORK_DIR}/taigi_POJ_data/train_dev
TEST_DATA_DIR=${WORK_DIR}/taigi_POJ_data/test
MODEL_DIR=${WORK_DIR}/huggingface_Tbert_base_ckpt_5000
TASK_MODEL_PREFIX=taigi_POJ_512_Tbert_base_5000
OUTPUT_DIR=${WORK_DIR}/${TASK_MODEL_PREFIX}_results
TASK_NAME=taigi
CHECK_STEPS=200
LOGGING_STEPS=1


python -m torch.distributed.launch \
  --nproc_per_node 8 run_ltn.py \
  --model_name_or_path ${MODEL_DIR} \
  --task_name ${TASK_NAME} \
  --data_dir ${DATA_DIR} \
  --output_dir ${OUTPUT_DIR} \
  --do_train \
  --do_eval \
  --num_train_epochs 50 \
  --learning_rate 2e-5 \
  --per_device_train_batch_size 8 \
  --max_seq_length 512 \
  --logging_steps ${LOGGING_STEPS} \
  --save_steps ${CHECK_STEPS} \
  --fp16 \
  # --max_steps 1 \
  # --per_device_eval_batch_size 128 \

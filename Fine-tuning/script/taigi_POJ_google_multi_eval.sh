#!/bin/bash

#SBATCH -J finetune
#SBATCH -o taigi_POJ_512_google_multi_2e5_eval_log_%j
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
MODEL_DIR=bert-base-multilingual-cased
TASK_MODEL_PREFIX=taigi_POJ_512_google_multi
OUTPUT_DIR=${WORK_DIR}/${TASK_MODEL_PREFIX}_results
TASK_NAME=taigi
# CHECK_STEPS=2000
LOGGING_STEPS=1


foldernames=()
for checkpoint in $OUTPUT_DIR/*/ ; do
    foldernames+=(${checkpoint::-1})
done
foldernames+=(${OUTPUT_DIR})


for foldername in "${foldernames[@]}" ; do
echo "Evaluating ${foldername}" 
python -m torch.distributed.launch \
--nproc_per_node 8 run_ltn.py \
--model_name_or_path ${foldername} \
--task_name ${TASK_NAME} \
--data_dir ${DATA_DIR} \
--output_dir ${foldername} \
--do_eval \
--per_device_eval_batch_size 256 \
--max_seq_length 512 \
--logging_steps ${LOGGING_STEPS} \
--fp16 \

wait
done

python get_every_ckpt_results.py -i ${OUTPUT_DIR} -o ${TASK_MODEL_PREFIX}_val_results.txt

for foldername in "${foldernames[@]}" ; do
echo "Evaluating ${foldername}" 
python -m torch.distributed.launch \
--nproc_per_node 8 run_ltn.py \
--model_name_or_path ${foldername} \
--task_name ${TASK_NAME} \
--data_dir ${TEST_DATA_DIR} \
--output_dir ${foldername} \
--do_eval \
--per_device_eval_batch_size 256 \
--max_seq_length 512 \
--logging_steps ${LOGGING_STEPS} \
--fp16 \

wait
done

python get_every_ckpt_results.py -i ${OUTPUT_DIR} -o ${TASK_MODEL_PREFIX}_test_results.txt


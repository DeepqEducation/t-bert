#!/bin/bash

# Copyright (c) 2019 NVIDIA CORPORATION. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


#SBATCH -J create_datasets
#SBATCH -o %j_create_datasets.log
#SBATCH --account=GOV109042
#SBATCH --partition=gp4d
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1

module purge
module load singularity

# **The following variable need to be set**
# The folder containing the BERT repository
WORKSPACE=~/t-bert
# Path to singularity image
SINGULARITY_PATH=${WORKSPACE}/pytorch_19.12-py3.sif


BERT_PREP_WORKING_DIR=${WORKSPACE}/bert/data
export PYTHONUNBUFFERED=TRUE


# Download
# SINGULARITYENV_BERT_PREP_WORKING_DIR=/workspace/bert/data \
# singularity exec --nv -B ${WORKSPACE}:/workspace ${SINGULARITY_PATH} \
# python3 /workspace/bert/data/bertPrep.py --action download --dataset google_pretrained_weights  # Includes vocab


# Shard the text files
SINGULARITYENV_BERT_PREP_WORKING_DIR=/workspace/bert/data \
singularity exec --nv -B ${WORKSPACE}:/workspace ${SINGULARITY_PATH} \
python3 /workspace/bert/data/bertPrep.py --action sharding --dataset wikicorpus_zh --n_training_shards 512 --n_test_shards 512


# Create HDF5 files Phase 1
# SINGULARITYENV_BERT_PREP_WORKING_DIR=/workspace/bert/data \
# singularity exec --nv -B ${WORKSPACE}:/workspace ${SINGULARITY_PATH} \
# python3 /workspace/bert/data/bertPrep.py --action create_hdf5_files --dataset wikicorpus_zh --max_seq_length 128 \
#  --max_predictions_per_seq 20 --vocab_file /workspace/bert/vocab/tbert_vocab.txt --do_lower_case 0


# Create HDF5 files Phase 2
SINGULARITYENV_BERT_PREP_WORKING_DIR=/workspace/bert/data \
singularity exec --nv -B ${WORKSPACE}:/workspace ${SINGULARITY_PATH} \
python3 /workspace/bert/data/bertPrep.py --action create_hdf5_files --dataset wikicorpus_zh --max_seq_length 512 \
--n_training_shards 512 --n_test_shards 512 \
--max_predictions_per_seq 80 --vocab_file /workspace/bert/vocab/tbert_vocab.txt --do_lower_case 0

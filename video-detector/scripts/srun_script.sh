#!/bin/bash
#SBATCH -A ACD110018        # Account name/project number
#SBATCH --ntasks-per-node=1 # Number of MPI tasks (i.e. processes)
#SBATCH -c 1                # Number of cores per MPI task
#SBATCH -N 1                # Maximum number of nodes to be allocated
#SBATCH --gpus-per-node=8

module load miniconda3
module load cuda/11.3
conda activate deep-sort-pytorch

cd /work/lawrence0426/Sharingan/video-detector
# pip3 list
# python deepsort-counter.py videos/zhongsi-rd.mp4 --detector_line "0,0,1000,1000" --output_name "result" --stable_period "1000"
python deepsort-counter.py videos/${VIDEO_ID} --detector_line ${DETECTOR_LINE} --output_name ${OUTPUT_NAME} --stable_period ${STABLE_PERIOD}


#!/bin/bash
#SBATCH --job-name=singlecore_job
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=4G
source /stornext/System/data/apps/anaconda3/anaconda3-4.3.1/etc/profile.d/conda.sh
conda activate CNV_downloading
export TMPDIR=/vast/scratch/users/$USER/tmp
mkdir -p $TMPDIR
python App.py

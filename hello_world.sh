#!/bin/bash
#SBATCH --job-name=singlecore_job
#SBATCH --time=00:10:00
#SBATCH --ntasks=1
#SBATCH --mem=1G
source /stornext/System/data/apps/anaconda3/anaconda3-4.3.1/etc/profile.d/conda.sh
conda activate CNV_downloading
export TMPDIR=/vast/scratch/users/$USER/tmp
mkdir -p $TMPDIR
python helloWorld.py Chris

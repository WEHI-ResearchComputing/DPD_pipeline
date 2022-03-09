#!/bin/bash
#SBATCH --job-name=singlecore_job
#SBATCH --time=48:00:00
#SBATCH --ntasks=4
#SBATCH --mem=1G
#SBATCH --output=app.out

source /stornext/System/data/apps/anaconda3/anaconda3-4.3.1/etc/profile.d/conda.sh
conda activate my_pipeline
export TMPDIR=/vast/scratch/users/$USER/tmp
mkdir -p $TMPDIR
python App.py
#!/bin/bash
#SBATCH --job-name=singlecore_job
#SBATCH --time=48:00:00
#SBATCH --ntasks=1
#SBATCH --mem=1G
#SBATCH --output=cleanup.out

source /stornext/System/data/apps/anaconda3/anaconda3-4.3.1/etc/profile.d/conda.sh
conda activate CNV_downloading

$var1 = $1
$var2 = $2
$var3 = $3

echo $var1
echo $var2
echo $var3

python Cleanup_process.py $1 $2 $3
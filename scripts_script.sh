#!/bin/bash
#SBATCH --job-name=singlecore_job
#SBATCH --time=48:00:00
#SBATCH --ntasks=4
#SBATCH --mem=1G
#SBATCH --output=scripts_script.out

echo $1

source ../../DPD_pipeline/jocelyn_scripts/fastq2bamVivax.sh $1
source ../../DPD_pipeline/jocelyn_scripts/gatk_haplocallVivax.sh $1
source ../../DPD_pipeline/jocelyn_scripts/copynumVivax.sh $1
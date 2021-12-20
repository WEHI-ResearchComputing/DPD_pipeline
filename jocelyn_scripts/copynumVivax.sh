#!/bin/bash
#SBATCH --cpus-per-task=5
#SBATCH --mail-type=END
#SBATCH --mail-user=penington.j@wehi.edu.au
#SBATCH --mem=8G

## Run Rscript to call copy number alterations from a bam file of 2 chromosomes

PAPDIR=/wehisan/bioinf/bioinf-data/Papenfuss_lab/projects
BASEDIR=$PAPDIR/malaria/cowman_lab/plasmepsinIX_X
ALIGNDIR=$BASEDIR/Pvivax/alignment
RDIR=$BASEDIR/malVarR
OUTDIR=$BASEDIR/Pvivax/cnvfiles

module load R/4.1.2
bamf=$ALIGNDIR/${1}_chrom1_13.bam
echo Input bam is $bamf
cd $RDIR
Rscript copynumPlasmepsin.R -s $1  \
  -b $bamf --species vivax --outdir $OUTDIR

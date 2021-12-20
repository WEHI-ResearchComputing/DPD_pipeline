#!/bin/bash
#SBATCH --mail-type=END
#SBATCH --mail-user=penington.j@wehi.edu.au
#SBATCH --mem=1G

## Run Rscript to call copy number alterations from a bam file of 2 chromosomes

PAPDIR=/wehisan/bioinf/bioinf-data/Papenfuss_lab/projects
BASEDIR=$PAPDIR/malaria/cowman_lab/plasmepsinIX_X
ALIGNDIR=$BASEDIR/Pfalciparum/bamfiles
RDIR=$BASEDIR/malVarR
OUTDIR=$BASEDIR/Pfalciparum/cnvfiles

module load R/4.1.2
bamf=$ALIGNDIR/${1}_chrom8_14.bam
echo Input bam is $bamf
Rscript $RDIR/copynumPlasmepsin.R -s $1 -b $bamf --species pfalc \
  --outdir $OUTDIR

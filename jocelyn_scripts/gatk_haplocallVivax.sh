#!/bin/bash
#SBATCH --cpus-per-task=5
#SBATCH --mail-type=END
#SBATCH --mail-user=penington.j@wehi.edu.au
#SBATCH --mem=8G

## Use GATK HaplotypeCaller to call variants from bam files and combine

PAPDIR=/wehisan/bioinf/bioinf-data/Papenfuss_lab/projects
BASEDIR=$PAPDIR/malaria/cowman_lab/plasmepsinIX_X/Pvivax
ALIGNDIR=$BASEDIR/alignment
REFDIR=$PAPDIR/reference_genomes/plasmodium/vivaxP01
VARDIR=$BASEDIR/variants

moday="$(date +"%d%b")"
OUTDIR=$VARDIR/gatk$moday
mkdir -p $OUTDIR
module load gatk/4.1.3.0
module load miniconda3
module load samtools

cd $ALIGNDIR

echo 'Input bam is' $1
fn=$( basename ${1} .bam )

REF=$REFDIR/PlasmoDB-52_PvivaxP01_Genome.fasta
PMX="PvP01_01_v2:555499-559411"
PMIX="PvP01_13_v2:876959-881753"
## call haplotype blocks
gatk --java-options "-Xmx4g" HaplotypeCaller  \
   -R $REF  \
   -I $1 \
   -L $PMIX -L $PMX  \
   -O $OUTDIR/${fn}.g.vcf.gz \
   -ERC GVCF \
   -ploidy 1

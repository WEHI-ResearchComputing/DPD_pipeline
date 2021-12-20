#!/bin/bash
#SBATCH --cpus-per-task=5
#SBATCH --mail-type=END
#SBATCH --mail-user=bollands.c@wehi.edu.au
#SBATCH --mem=8G

## Use bwa mem to align paired-end fastq to the PlasmoDB P falciparum reference genome
## Don't trim adaptors first, or remove duplicates afterwards.
## Positional inputs $1=fastq filename up to _[12]

PAPDIR=/wehisan/bioinf/bioinf-data/Papenfuss_lab/projects
REFDIR=$PAPDIR/reference_genomes/plasmodium/PlasmoDB-52_Pfalciparum3D7
BASEDIR=$PAPDIR/malaria/cowman_lab/plasmepsinIX_X
ALIGNDIR=$BASEDIR/Pfalciparum/bamfiles
DATADIR=$BASEDIR/Pfalciparum/fastqfiles

module add bwa  
module add samtools
f1=${1}'_1.fastq.gz'
f2=${1}'_2.fastq.gz'
fn=$( basename ${1} )
# fdir=$( dirname $1 )
echo 'filebasename is' $fn

## align using bwa tool
# bwa mem -t 4 -o $ALIGNDIR/${fn}.sam -R "@RG\tID:${fn}\tSM:${fn}\tPL:ILLUMINA"  \
#   $REFDIR/PlasmoDB-52_Pfalciparum3D7_Genome $DATADIR/$f1 $DATADIR/$f2  \
# 
# ## Convert to bam, sort and index
# if [ -f $ALIGNDIR/${fn}.sam ] 
# then
#   samtools view -b $ALIGNDIR/${fn}.sam  |  \
#     samtools sort -o $ALIGNDIR/${fn}_s.bam -O bam -@ 4 -
#   samtools index $ALIGNDIR/${fn}_s.bam
# fi
## Remove intermediate file
if [ -f $ALIGNDIR/${fn}_s.bam ] 
  then rm $ALIGNDIR/${fn}.sam 
## Filter to 2 chromosomes of interest
  samtools view -bh -o $ALIGNDIR/${fn}_chrom8_14.bam $ALIGNDIR/${fn}_s.bam   \
    Pf3D7_08_v3 Pf3D7_14_v3
  samtools index $ALIGNDIR/${fn}_chrom8_14.bam
fi
## Remove full bam file
if [ -s $ALIGNDIR/${fn}_chrom8_14.bam ] 
  then rm $ALIGNDIR/${fn}_s.bam* 
fi

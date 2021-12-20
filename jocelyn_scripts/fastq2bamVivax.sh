#!/bin/bash
#SBATCH --cpus-per-task=5
#SBATCH --mail-type=END
#SBATCH --time=48:00:00
#SBATCH --mail-user=bollands.c@wehi.edu.au
#SBATCH --mem=8G

## Use bwa mem to align paired-end fastq to the PlasmoDB P vivax P01 reference genome
## Don't trim adaptors first, or remove duplicates afterwards.
## Positional inputs $1=fastq filename up to _[12]

PAPDIR=/stornext/HPCScratch/home/bollands.c/Malaria_downloads
BASEDIR=$PAPDIR/script_tests
# DATADIR=$BASEDIR/Pvivax/fastqs
ALIGNDIR=$BASEDIR/alignment
REFDIR=/wehisan/bioinf/bioinf-data/Papenfuss_lab/projects/reference_genomes/plasmodium/vivaxP01

module add bwa  
module add samtools
f1=${1}'_1.fastq.gz'
f2=${1}'_2.fastq.gz'
fn=$( basename ${1} )
# fdir=$( dirname $1 )
echo 'filebasename is' $fn

## align using bwa tool
bwa mem -t 4 -o $ALIGNDIR/${fn}.sam -R "@RG\tID:${fn}\tSM:${fn}\tPL:ILLUMINA"  \
  $REFDIR/PlasmoDB-52_PvivaxP01_Genome $f1 $f2  \

## Convert to bam, sort and index
if [ -f $ALIGNDIR/${fn}.sam ] 
then
  samtools view -b $ALIGNDIR/${fn}.sam  |  \
    samtools sort -o $ALIGNDIR/${fn}_s.bam -O bam -@ 4 -
  samtools index $ALIGNDIR/${fn}_s.bam
fi
## Remove intermediate file
if [ -f $ALIGNDIR/${fn}_s.bam ] 
  then rm $ALIGNDIR/${fn}.sam 
fi
## Filter to 2 chromosomes of interest
samtools view -bh -o $ALIGNDIR/${fn}_chrom1_13.bam $ALIGNDIR/${fn}_s.bam   \
  PvP01_01_v2 PvP01_13_v2
samtools index $ALIGNDIR/${fn}_chrom1_13.bam
## Remove full bam file
if [ -s $ALIGNDIR/${fn}_chrom1_13.bam ] 
  then rm $ALIGNDIR/${fn}_s.bam* 
fi

exit 0
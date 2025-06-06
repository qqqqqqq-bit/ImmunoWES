#!/bin/bash

# Function: Use BWA MEM + samtools to compare clean FASTQ and output the sorted BAM file

# Loading Conda environment (need to include bwa and samtools)
source ~/.bashrc
conda activate wes

# Set the path
WORKDIR="/data/yuan/gastric_cancer"
CLEAN_FQ_DIR="${WORKDIR}/2.clean_fq"
ALIGN_DIR="${WORKDIR}/4.align"
CONFIG="${WORKDIR}/0.sra/config"
INDEX="/root/wes_cancer/data/gatk_hg38"

mkdir -p ${ALIGN_DIR}

#Run BWA + SAMtools in parallel
cat ${CONFIG} | parallel -j 8 "
echo 'Start BWA for {}' \$(date)
fq1=${CLEAN_FQ_DIR}/{}_1_val_1.fq.gz
fq2=${CLEAN_FQ_DIR}/{}_2_val_2.fq.gz
bwa mem -M -t 16 -R '@RG\\tID:{}\\tSM:{}\\tLB:WXS\\tPL:Illumina' ${INDEX} \${fq1} \${fq2} |
samtools sort -@ 8 -m 1G -o ${ALIGN_DIR}/{}.bam -
echo 'End BWA for {}' \$(date)
"

echo "Comparison is completed, and the BAM file is saved in ${ALIGN_DIR}/"

#!/bin/bash

# Function: Comparison of BAM files for quality control, generate statistical files and graphic reports

# Loading Conda environment (need to include samtools and plot-bamstats)
source ~/.bashrc
conda activate wes

# Define paths
WORKDIR="/data/yuan/gastric_cancer"
ALIGN_DIR="${WORKDIR}/4.align"
STATS_DIR="${ALIGN_DIR}/stats"
REFERENCE="~/wes_cancer/data/Homo_sapiens_assembly38.fasta"
CONFIG="${WORKDIR}/0.sra/config"

mkdir -p ${STATS_DIR}

# Statistics and plots each BAM file
cat ${CONFIG} | while read id; do
    bam="${ALIGN_DIR}/${id}.bam"
    echo "Running samtools stats for ${id}..."
    samtools stats -@ 16 --reference ${REFERENCE} ${bam} > ${STATS_DIR}/${id}.stat

    echo "Generating plots for ${id}..."
    plot-bamstats -p ${STATS_DIR}/${id} ${STATS_DIR}/${id}.stat
done

echo "BAM QC finished. Output saved in ${STATS_DIR}/"

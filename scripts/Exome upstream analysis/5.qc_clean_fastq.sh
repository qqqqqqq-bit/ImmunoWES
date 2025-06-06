#!/bin/bash

# Function: FastQC quality control of fastq.gz files in clean_fq and summarize using MultiQC

# Conda Environmental Preparation
source ~/.bashrc
conda activate nuggets

# Set the path
WORKDIR="/data/yuan/gastric_cancer"
CLEAN_FASTQ_DIR="${WORKDIR}/2.clean_fq"
QC_DIR="${WORKDIR}/3.qc/clean_qc"
CONFIG="${WORKDIR}/0.sra/config"

mkdir -p ${QC_DIR}

# Execute FastQC
echo "Step 8: FastQC to Clean FASTQ files..."
cd ${WORKDIR}
cat ${CONFIG} | while read id; do
    fastqc --outdir ${QC_DIR} --threads 16 ${CLEAN_FASTQ_DIR}/${id}*.fq.gz \
    >> ${QC_DIR}/${id}_fastqc.log 2>&1
done

#MultiQC Summary
echo "Generate MultiQC Reports..."
multiqc ${QC_DIR}/*zip -o ${QC_DIR}/multiqc

echo "FastQC & MultiQC Completed, the result is saved in：${QC_DIR}"

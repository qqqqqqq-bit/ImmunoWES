#!/bin/bash

# Scripting function: Use FastQC to perform quality evaluation of raw fastq files and summarize results with MultiQC

# Set the working path (based on the config file generated earlier)
WORKDIR="/data/yuan/gastric_cancer"
CONFIG_FILE="${WORKDIR}/0.sra/config"
FASTQ_DIR="${WORKDIR}/1.raw_fq"
QC_DIR="${WORKDIR}/3.qc/raw_qc"
LOG_DIR="${QC_DIR}/logs"

# Create a directory
mkdir -p "${QC_DIR}"
mkdir -p "${LOG_DIR}"

echo "Step 6: FastQC Quality control..."

cd "${WORKDIR}"
cat ${CONFIG_FILE} | while read id; do
    echo "Running FastQC for sample: ${id}"
    fastqc --outdir ${QC_DIR} --threads 16 ${FASTQ_DIR}/${id}_*.fastq.gz >> ${LOG_DIR}/${id}_fastqc.log 2>&1
done

echo "FastQC completed. Start MultiQC summary..."

multiqc ${QC_DIR}/*.zip -o ${QC_DIR}/multiqc

echo "MultiQC summary saved to: ${QC_DIR}/multiqc"


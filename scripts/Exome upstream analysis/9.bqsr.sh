#!/bin/bash

# Function: Base Quality Score Recalibration (BQSR) using GATK

# Conda Environment
source ~/.bashrc
conda activate wes

# Enter configuration
WORKDIR="/data/yuan/gastric_cancer"
CONFIG="${WORKDIR}/0.sra/config"
GATK_DIR="${WORKDIR}/5.gatk"
THREADS=16

#Reference file path
REF="/root/wes_cancer/data/Homo_sapiens_assembly38.fasta"
SNP="/root/wes_cancer/data/dbsnp_146.hg38.vcf.gz"
INDEL="/root/wes_cancer/data/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz"

# Create a function
bqsr_pipeline() {
    id=$1
    MARKED_BAM="${GATK_DIR}/${id}_marked.bam"
    RECAL_TABLE="${GATK_DIR}/${id}_recal.table"
    RECAL_BAM="${GATK_DIR}/${id}_bqsr.bam"
    LOG1="${GATK_DIR}/${id}_log.recal"
    LOG2="${GATK_DIR}/${id}_log.ApplyBQSR"

    if [ ! -f "${RECAL_BAM}" ]; then
        echo "🔧 [$(date)] Start BQSR for ${id}"

        gatk --java-options "-Xmx50G -Djava.io.tmpdir=${WORKDIR}/tmp" BaseRecalibrator \
            -R ${REF} \
            -I ${MARKED_BAM} \
            --known-sites ${SNP} \
            --known-sites ${INDEL} \
            -O ${RECAL_TABLE} \
            1>${LOG1} 2>&1

        gatk --java-options "-Xmx50G -Djava.io.tmpdir=${WORKDIR}/tmp" ApplyBQSR \
            -R ${REF} \
            -I ${MARKED_BAM} \
            -bqsr ${RECAL_TABLE} \
            -O ${RECAL_BAM} \
            1>${LOG2} 2>&1

        echo "✅ [$(date)] Finished BQSR for ${id}"
    else
        echo "⚠️ ${id}_bqsr.bam already exists. Skipping."
    fi
}

# Export functions and variables
export -f bqsr_pipeline
export GATK_DIR REF SNP INDEL WORKDIR

# Parallel execution
cat ${CONFIG} | parallel -j ${THREADS} bqsr_pipeline

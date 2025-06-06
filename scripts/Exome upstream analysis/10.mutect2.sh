#!/bin/bash

# Function: Tumor-normal paired somatic mutation call using GATK Mutect2

# Conda Environment
source ~/.bashrc
conda activate wes

# Configure path
WORKDIR="/data/yuan/gastric_cancer"
CONFIG="${WORKDIR}/0.sra/config1"
GATK_DIR="${WORKDIR}/5.gatk"
OUT_DIR="${WORKDIR}/6.mutect"
TMPDIR="${WORKDIR}/tmp"
mkdir -p $OUT_DIR $TMPDIR

# Reference files
REF="/root/wes_cancer/data/Homo_sapiens_assembly38.fasta"
BED="/root/wes_cancer/data/hg38.exon.bed"

# Main loop
cat ${CONFIG} | while read id; do
    arr=(${id})
    normal_id=${arr[0]}
    tumor_id=${arr[1]}

    TUMOR_BAM="${GATK_DIR}/${tumor_id}_bqsr.bam"
    NORMAL_BAM="${GATK_DIR}/${normal_id}_bqsr.bam"
    RAW_VCF="${OUT_DIR}/${tumor_id}_mutect2.vcf"
    FILTERED_VCF="${OUT_DIR}/${tumor_id}_somatic.vcf"
    PASS_VCF="${OUT_DIR}/${tumor_id}_filter.vcf"

    echo "🔬 [$(date)] Start Mutect2 for ${tumor_id}"

    # 1. Call somatic mutations
    gatk --java-options "-Xmx20G -Djava.io.tmpdir=${TMPDIR}" Mutect2 \
        -R ${REF} \
        -I ${TUMOR_BAM} -tumor ${tumor_id} \
        -I ${NORMAL_BAM} -normal ${normal_id} \
        -L ${BED} \
        -O ${RAW_VCF}

    # 2. filter
    gatk FilterMutectCalls \
        -R ${REF} \
        -V ${RAW_VCF} \
        -O ${FILTERED_VCF}

    # 3. Screening for mutation sites with PASS and normal chromosomes
    cat ${FILTERED_VCF} | perl -alne 'if(/^#/){print}else{next unless $F[6] eq "PASS"; next if $F[0] =~ /_/; print}' > ${PASS_VCF}

    echo "✅ [$(date)] Finish Mutect2 for ${tumor_id}"
done

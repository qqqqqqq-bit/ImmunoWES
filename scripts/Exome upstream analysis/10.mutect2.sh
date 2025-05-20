#!/bin/bash

# 功能：使用 GATK Mutect2 进行肿瘤-正常配对体细胞突变呼叫

# Conda 环境
source ~/.bashrc
conda activate wes

# 配置路径
WORKDIR="/data/yuan/gastric_cancer"
CONFIG="${WORKDIR}/0.sra/config1"
GATK_DIR="${WORKDIR}/5.gatk"
OUT_DIR="${WORKDIR}/6.mutect"
TMPDIR="${WORKDIR}/tmp"
mkdir -p $OUT_DIR $TMPDIR

# 参考文件
REF="/root/wes_cancer/data/Homo_sapiens_assembly38.fasta"
BED="/root/wes_cancer/data/hg38.exon.bed"

# 主循环
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

    # 1. 呼叫体细胞突变
    gatk --java-options "-Xmx20G -Djava.io.tmpdir=${TMPDIR}" Mutect2 \
        -R ${REF} \
        -I ${TUMOR_BAM} -tumor ${tumor_id} \
        -I ${NORMAL_BAM} -normal ${normal_id} \
        -L ${BED} \
        -O ${RAW_VCF}

    # 2. 过滤
    gatk FilterMutectCalls \
        -R ${REF} \
        -V ${RAW_VCF} \
        -O ${FILTERED_VCF}

    # 3. 筛选 PASS 且染色体正常的突变位点
    cat ${FILTERED_VCF} | perl -alne 'if(/^#/){print}else{next unless $F[6] eq "PASS"; next if $F[0] =~ /_/; print}' > ${PASS_VCF}

    echo "✅ [$(date)] Finish Mutect2 for ${tumor_id}"
done

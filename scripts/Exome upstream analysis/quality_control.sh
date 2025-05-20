#!/bin/bash

# 脚本功能：使用 FastQC 对 raw fastq 文件进行质量评估，并用 MultiQC 汇总结果

# 设置工作路径（根据前面生成的 config 文件）
WORKDIR="/data/yuan/gastric_cancer"
CONFIG_FILE="${WORKDIR}/0.sra/config"
FASTQ_DIR="${WORKDIR}/1.raw_fq"
QC_DIR="${WORKDIR}/3.qc/raw_qc"
LOG_DIR="${QC_DIR}/logs"

# 创建目录
mkdir -p "${QC_DIR}"
mkdir -p "${LOG_DIR}"

echo "Step 6: FastQC 质量控制..."

cd "${WORKDIR}"
cat ${CONFIG_FILE} | while read id; do
    echo "Running FastQC for sample: ${id}"
    fastqc --outdir ${QC_DIR} --threads 16 ${FASTQ_DIR}/${id}_*.fastq.gz >> ${LOG_DIR}/${id}_fastqc.log 2>&1
done

echo "FastQC completed. Start MultiQC summary..."

multiqc ${QC_DIR}/*.zip -o ${QC_DIR}/multiqc

echo "MultiQC summary saved to: ${QC_DIR}/multiqc"


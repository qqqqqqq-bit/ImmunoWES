#!/bin/bash

# 功能：对 clean_fq 中的 fastq.gz 文件进行 FastQC 质量控制并使用 MultiQC 汇总

# Conda 环境准备
source ~/.bashrc
conda activate nuggets

# 设定路径
WORKDIR="/data/yuan/gastric_cancer"
CLEAN_FASTQ_DIR="${WORKDIR}/2.clean_fq"
QC_DIR="${WORKDIR}/3.qc/clean_qc"
CONFIG="${WORKDIR}/0.sra/config"

mkdir -p ${QC_DIR}

# 执行 FastQC
echo "Step 8: 对 Clean FASTQ 文件进行 FastQC..."
cd ${WORKDIR}
cat ${CONFIG} | while read id; do
    fastqc --outdir ${QC_DIR} --threads 16 ${CLEAN_FASTQ_DIR}/${id}*.fq.gz \
    >> ${QC_DIR}/${id}_fastqc.log 2>&1
done

# MultiQC 汇总
echo "生成 MultiQC 报告..."
multiqc ${QC_DIR}/*zip -o ${QC_DIR}/multiqc

echo "FastQC & MultiQC 完成，结果保存在：${QC_DIR}"

#!/bin/bash

# 功能：对比对后的 BAM 文件进行质控，生成统计文件和图形报告

# 加载 Conda 环境（需含 samtools 和 plot-bamstats）
source ~/.bashrc
conda activate wes

# 定义路径
WORKDIR="/data/yuan/gastric_cancer"
ALIGN_DIR="${WORKDIR}/4.align"
STATS_DIR="${ALIGN_DIR}/stats"
REFERENCE="~/wes_cancer/data/Homo_sapiens_assembly38.fasta"
CONFIG="${WORKDIR}/0.sra/config"

mkdir -p ${STATS_DIR}

# 对每个 BAM 文件进行统计并绘图
cat ${CONFIG} | while read id; do
    bam="${ALIGN_DIR}/${id}.bam"
    echo "Running samtools stats for ${id}..."
    samtools stats -@ 16 --reference ${REFERENCE} ${bam} > ${STATS_DIR}/${id}.stat

    echo "Generating plots for ${id}..."
    plot-bamstats -p ${STATS_DIR}/${id} ${STATS_DIR}/${id}.stat
done

echo "BAM QC finished. Output saved in ${STATS_DIR}/"

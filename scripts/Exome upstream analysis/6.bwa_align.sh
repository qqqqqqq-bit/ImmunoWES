#!/bin/bash

# 功能：使用 BWA MEM + samtools 对 clean FASTQ 进行比对，输出排序后的 BAM 文件

# 加载 Conda 环境（需含 bwa、samtools）
source ~/.bashrc
conda activate wes

# 设定路径
WORKDIR="/data/yuan/gastric_cancer"
CLEAN_FQ_DIR="${WORKDIR}/2.clean_fq"
ALIGN_DIR="${WORKDIR}/4.align"
CONFIG="${WORKDIR}/0.sra/config"
INDEX="/root/wes_cancer/data/gatk_hg38"

mkdir -p ${ALIGN_DIR}

# 并行运行 BWA + SAMtools
cat ${CONFIG} | parallel -j 8 "
echo 'Start BWA for {}' \$(date)
fq1=${CLEAN_FQ_DIR}/{}_1_val_1.fq.gz
fq2=${CLEAN_FQ_DIR}/{}_2_val_2.fq.gz
bwa mem -M -t 16 -R '@RG\\tID:{}\\tSM:{}\\tLB:WXS\\tPL:Illumina' ${INDEX} \${fq1} \${fq2} |
samtools sort -@ 8 -m 1G -o ${ALIGN_DIR}/{}.bam -
echo 'End BWA for {}' \$(date)
"

echo "比对完成，BAM 文件保存在 ${ALIGN_DIR}/"

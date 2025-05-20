#!/bin/bash

# 功能：使用 GATK MarkDuplicates 对 BAM 文件进行去重并生成索引

# 加载 Conda 或模块环境（需含 GATK 和 samtools）
source ~/.bashrc
conda activate wes

# 路径定义
WORKDIR="/data/yuan/gastric_cancer"
CONFIG="${WORKDIR}/0.sra/config"
ALIGN_DIR="${WORKDIR}/4.align"
GATK_DIR="${WORKDIR}/5.gatk"
TMP_DIR="${WORKDIR}/tmp"
THREADS=16

mkdir -p ${GATK_DIR}
mkdir -p ${TMP_DIR}

# 并行执行 MarkDuplicates 和索引
cat ${CONFIG} | parallel -j ${THREADS} "
    BAM=${ALIGN_DIR}/{1}.bam
    STATUS_FILE=${GATK_DIR}/ok.{1}_marked.status

    if [ ! -f \${STATUS_FILE} ]; then
        echo 'start MarkDuplicates for {1}' \$(date)

        gatk --java-options '-Xmx20G -Djava.io.tmpdir=${TMP_DIR}' MarkDuplicates \
            -I \${BAM} \
            --REMOVE_DUPLICATES \
            -O ${GATK_DIR}/{1}_marked.bam \
            -M ${GATK_DIR}/{1}.metrics \
            1>${GATK_DIR}/{1}_log.mark 2>&1

        if [ \$? -eq 0 ]; then
            touch \${STATUS_FILE}
        fi

        echo 'end MarkDuplicates for {1}' \$(date)

        samtools index -@ 16 -m 4G ${GATK_DIR}/{1}_marked.bam ${GATK_DIR}/{1}_marked.bai
    fi
"

echo "✅ MarkDuplicates 和索引任务完成。"

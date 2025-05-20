
#!/bin/bash

# 脚本功能：将下载好的 .sra 文件批量转换为 fastq，并压缩输出
# 要求：当前目录结构需包含 config 文件（每行一个样本 ID）

# 设置工作路径（可按需修改）
WORKDIR="/data/yuan/gastric_cancer"
SRA_DIR="${WORKDIR}/0.sra"
FASTQ_DIR="${WORKDIR}/1.raw_fq"
CONFIG_FILE="${SRA_DIR}/config"

# 创建 fastq 输出目录
mkdir -p "${FASTQ_DIR}"

echo "Step 5: 转换 SRA 为 FastQ 并压缩..."

# 并行处理每个样本
cd "${SRA_DIR}"
cat "${CONFIG_FILE}" | parallel -j 16 "
    echo Converting {}.sra to fastq...
    fasterq-dump -3 -e 16 {}.sra -O ${FASTQ_DIR} --outfile {}.fastq &&
    pigz -p 10 -f ${FASTQ_DIR}/{}_1.fastq &&
    pigz -p 10 -f ${FASTQ_DIR}/{}_2.fastq
"

echo "All SRA files converted and compressed successfully."

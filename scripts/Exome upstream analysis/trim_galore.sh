
#!/bin/bash

# 功能：使用 Trim Galore 对 raw FASTQ 文件进行去接头处理

# 设置路径
WORKDIR="/data/yuan/gastric_cancer"
RAW_FASTQ_DIR="${WORKDIR}/1.raw_fq"
CLEAN_FASTQ_DIR="${WORKDIR}/2.clean_fq"

mkdir -p ${CLEAN_FASTQ_DIR}

cd ${RAW_FASTQ_DIR}

# 生成配对 fastq 文件列表
ls *_1.fastq.gz > fastq1
ls *_2.fastq.gz > fastq2
paste fastq1 fastq2 > config1

echo "Step 7: Trim Galore 去接头处理..."
cat config1 | parallel -j 16 --colsep '\t' "
trim_galore \
  -q 25 \
  --phred33 \
  --length 36 \
  -e 0.1 \
  --stringency 3 \
  --paired \
  -o ${CLEAN_FASTQ_DIR} {1} {2}
"

echo "Trim Galore 完成。结果保存在: ${CLEAN_FASTQ_DIR}"

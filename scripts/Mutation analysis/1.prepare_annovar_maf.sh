#!/bin/bash
cd /data/yuan/gastric_cancer/7.annote/annovar1

# 加样本名，截取前20列
cat config | while read id; do
    grep -v 'Chr' ${id}.hg38_multianno.txt | cut -f 1-20 | \
    awk -v sample_id="${id}" '{print $0 "\t" sample_id}' > ${id}.maf
done

# 添加表头
head -1 YSU_T9.hg38_multianno.txt | cut -f 1-20 | \
awk '{print $0"\tTumor_Sample_Barcode"}' > header

# 合并所有 MAF 文件
cat header *maf > all_sample.maf

#!/bin/bash

# 设置路径
VCF_DIR="/data/yuan/gastric_cancer/6.mutect"
ANNOVAR_DIR="/data/yuan/annovar"
OUT_DIR="/data/yuan/gastric_cancer/7.annote/annovar1"
DB_DIR="${ANNOVAR_DIR}/humandb"
CONFIG="/data/yuan/gastric_cancer/config"

# Step 1: 转换 VCF 为 avinput 格式
cd ${ANNOVAR_DIR}
cat ${CONFIG} | while read id
do
    echo "[INFO] Converting VCF to avinput for ${id}"
    convert2annovar.pl -format vcf4old ${VCF_DIR}/${id}_filter.vcf > ${VCF_DIR}/${id}_filter.vcf.avinput
done

# Step 2: 使用 table_annovar.pl 进行注释
cd ${ANNOVAR_DIR}
cat ${CONFIG} | while read id
do
    echo "[INFO] Annotating ${id} using Annovar"
    table_annovar.pl \
        ${VCF_DIR}/${id}_filter.vcf.avinput \
        ${DB_DIR} \
        -buildver hg38 \
        -out ${OUT_DIR}/${id} \
        -remove \
        -protocol refGene,avsnp144,gnomad41_genome,dbnsfp42c \
        -operation g,f,f,f \
        -nastring . \
        -vcfinput
done

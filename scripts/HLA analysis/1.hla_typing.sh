
#!/bin/bash

# 功能：使用 HLA-HD 进行 HLA 等位基因分型（多线程并行）

# Conda环境或系统路径可自定义
HLAHD_BIN="/data/yuan/wes_cancer/HLA-HD/hlahd.1.7.0/bin"
FREQ_DATA="${HLAHD_BIN}/freq_data"
GENE_LIST="${HLAHD_BIN}/HLA_gene.split.txt"
DICT="${HLAHD_BIN}/dictionary"
CONFIG="/data/yuan/gastric_cancer/config"
CLEAN_FQ="/data/yuan/gastric_cancer/2.clean_fq"
OUTDIR="/data/yuan/gastric_cancer/hla_estimation"

# 拷贝 config 文件到工作目录中（可选）
cp -r ${CONFIG} ${HLAHD_BIN}/

# 切换到 HLA-HD 的 bin 目录
cd ${HLAHD_BIN}

# 使用 GNU Parallel 多线程执行每个样本的分型任务
cat config | parallel -j 16 --colsep '\t' './hlahd.sh -t 2 -m 100 -c 0.95 -f ${FREQ_DATA} \
    ${CLEAN_FQ}/{}_1_val_1.fq.gz \
    ${CLEAN_FQ}/{}_2_val_2.fq.gz \
    ${GENE_LIST} \
    ${DICT} \
    {} ${OUTDIR}'


#!/bin/bash

# Function: HLA allelic genotyping using HLA-HD (multi-threaded parallel)

# Conda environment or system path can be customized
HLAHD_BIN="/data/yuan/wes_cancer/HLA-HD/hlahd.1.7.0/bin"
FREQ_DATA="${HLAHD_BIN}/freq_data"
GENE_LIST="${HLAHD_BIN}/HLA_gene.split.txt"
DICT="${HLAHD_BIN}/dictionary"
CONFIG="/data/yuan/gastric_cancer/config"
CLEAN_FQ="/data/yuan/gastric_cancer/2.clean_fq"
OUTDIR="/data/yuan/gastric_cancer/hla_estimation"

# Copy the config file to the working directory (optional)
cp -r ${CONFIG} ${HLAHD_BIN}/

# Switch to HLA-HD's bin directory
cd ${HLAHD_BIN}

# Perform typing tasks for each sample using GNU Parallel multithreading
cat config | parallel -j 16 --colsep '\t' './hlahd.sh -t 2 -m 100 -c 0.95 -f ${FREQ_DATA} \
    ${CLEAN_FQ}/{}_1_val_1.fq.gz \
    ${CLEAN_FQ}/{}_2_val_2.fq.gz \
    ${GENE_LIST} \
    ${DICT} \
    {} ${OUTDIR}'

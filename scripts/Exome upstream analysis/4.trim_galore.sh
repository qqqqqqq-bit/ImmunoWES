
#!/bin/bash

# Function: Use Trim Galore to de-join raw FASTQ files

# Set path
WORKDIR="/data/yuan/gastric_cancer"
RAW_FASTQ_DIR="${WORKDIR}/1.raw_fq"
CLEAN_FASTQ_DIR="${WORKDIR}/2.clean_fq"

mkdir -p ${CLEAN_FASTQ_DIR}

cd ${RAW_FASTQ_DIR}

# Generate a paired fastq file list
ls *_1.fastq.gz > fastq1
ls *_2.fastq.gz > fastq2
paste fastq1 fastq2 > config1

echo "Step 7: Trim Galore Remove the connector processing..."
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

echo "Trim Galore Completed. The result is saved in: ${CLEAN_FASTQ_DIR}"

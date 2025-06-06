
#!/bin/bash

# Script function: batch convert the downloaded .sra files to fastq and compress the output
# Requirements: The current directory structure must contain a config file (one sample ID per line)

# Set the working path (can be modified as needed)
WORKDIR="/data/yuan/gastric_cancer"
SRA_DIR="${WORKDIR}/0.sra"
FASTQ_DIR="${WORKDIR}/1.raw_fq"
CONFIG_FILE="${SRA_DIR}/config"

# Create fastq output directory
mkdir -p "${FASTQ_DIR}"

echo "Step 5: Convert SRA to FastQ and compress..."

# Process each sample in parallel
cd "${SRA_DIR}"
cat "${CONFIG_FILE}" | parallel -j 16 "
    echo Converting {}.sra to fastq...
    fasterq-dump -3 -e 16 {}.sra -O ${FASTQ_DIR} --outfile {}.fastq &&
    pigz -p 10 -f ${FASTQ_DIR}/{}_1.fastq &&
    pigz -p 10 -f ${FASTQ_DIR}/{}_2.fastq
"

echo "All SRA files converted and compressed successfully."

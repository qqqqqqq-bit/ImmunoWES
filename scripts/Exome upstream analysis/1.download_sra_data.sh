
#!/bin/bash

# Download and rename the gastric cancer sample data (normal and cancerous tissue) in the SRP043661 project

# Set up the working directory (can be modified as needed)
WORKDIR="/data/yuan/gastric_cancer"
SRR_LIST="${WORKDIR}/SRR_Acc_List.txt"
SRA_TABLE="${WORKDIR}/SraRunTable.csv"
SRA_DIR="${WORKDIR}/0.sra"

# Create a storage directory
mkdir -p "${SRA_DIR}"

echo "Step 1: Multi-threaded download of SRA format raw data..."
# Multithreaded download using prefetch (needs NCBI SRA Toolkit installation)
cat "${SRR_LIST}" | xargs -n 1 -P 16 -I {} prefetch {} -O "${SRA_DIR}"

echo "Step 2: parse SraRunTable.csv to get rename mapping information..."
# Extract the sra ID (first column) and sample ID (column 34), and rename it to remove "_1"
grep "WXS" "${SRA_TABLE}" | cut -f 1 -d , > "${WORKDIR}/sra"
grep "WXS" "${SRA_TABLE}" | cut -f 34 -d , | sed 's/_1//' > "${WORKDIR}/config"

#Merge into two columns to generate a rename comparison table
paste "${WORKDIR}/sra" "${WORKDIR}/config" > "${WORKDIR}/sra2case.txt"

echo "Step 3: Rename the SRA file..."
# Batch renaming
while read -r line; do
    arr=($line)
    sample=${arr[0]}
    case=${arr[1]}
    mv "${SRA_DIR}/${sample}/${sample}.sra" "${SRA_DIR}/${case}.sra"
done < "${WORKDIR}/sra2case.txt"

echo "Step 4: Delete the redundant SRR folder..."
# Delete redundant folders
find "${SRA_DIR}" -type d -name "SRR*" -exec rm -rf {} +

echo "Done. All SRA files have been renamed and cleaned."

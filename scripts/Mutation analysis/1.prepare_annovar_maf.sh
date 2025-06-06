#!/bin/bash
cd /data/yuan/gastric_cancer/7.annote/annovar1

# Add sample name and intercept the first 20 columns
cat config | while read id; do
    grep -v 'Chr' ${id}.hg38_multianno.txt | cut -f 1-20 | \
    awk -v sample_id="${id}" '{print $0 "\t" sample_id}' > ${id}.maf
done

# Add a header
head -1 YSU_T9.hg38_multianno.txt | cut -f 1-20 | \
awk '{print $0"\tTumor_Sample_Barcode"}' > header

# Merge all MAF files
cat header *maf > all_sample.maf

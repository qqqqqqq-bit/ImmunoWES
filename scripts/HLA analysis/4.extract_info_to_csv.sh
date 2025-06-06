#!/bin/bash

# Input and output directories
input_dir="/data/yuan/gastric_cancer/downstream_ukb/gastric_vcf/filter"
output_dir="/data/yuan/gastric_cancer/downstream_ukb/gastric_vcf/filter/filter_extract_csv"

mkdir -p "$output_dir"

for file in "$input_dir"/*_filtered.vcf; do
    filename=$(basename "$file" .vcf)
    output_csv="$output_dir/${filename}.csv"

    echo "[INFO] Processing $filename"

    awk -F'\t' '
    BEGIN {
        print "Chromosome,Start,Ref,Alt,Qual,ExonicFunc.refGene,LRT_pred,SIFT_pred,MutationAssessor_pred,gnomad41_genome_AF,Gene.refGene,AAChange.refGene"
    }
    !/^#/ {
        split($8, info, ";");
        exonic_func = ""; LRT_pred = ""; SIFT_pred = ""; MutationAssessor_pred = "";
        gnomad41_genome_AF = ""; gene_ref = ""; aa_change = "";

        for (i in info) {
            if (info[i] ~ /^ExonicFunc.refGene=/) {
                split(info[i], a, "="); exonic_func = a[2];
            } else if (info[i] ~ /^LRT_pred=/) {
                split(info[i], a, "="); LRT_pred = a[2];
            } else if (info[i] ~ /^SIFT_pred=/) {
                split(info[i], a, "="); SIFT_pred = a[2];
            } else if (info[i] ~ /^MutationAssessor_pred=/) {
                split(info[i], a, "="); MutationAssessor_pred = a[2];
            } else if (info[i] ~ /^gnomad41_genome_AF=/) {
                split(info[i], a, "="); gnomad41_genome_AF = a[2];
            } else if (info[i] ~ /^Gene.refGene=/) {
                split(info[i], a, "="); gene_ref = a[2];
            } else if (info[i] ~ /^AAChange.refGene=/) {
                split(info[i], a, "="); gsub(",", ";", a[2]); aa_change = a[2];
            }
        }

        print $1 "," $2 "," $4 "," $5 "," $6 "," exonic_func "," LRT_pred "," SIFT_pred "," MutationAssessor_pred "," gnomad41_genome_AF "," gene_ref "," aa_change;
    }
    ' "$file" > "$output_csv"

    # Optional: Delete the second row (if you have empty rows or extra data)
    sed -i '2d' "$output_csv"
done

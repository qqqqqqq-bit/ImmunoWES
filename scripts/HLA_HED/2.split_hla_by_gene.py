#!/usr/bin/env python3
import csv
import os

def main():
    input_file = "/data/yuan/gastric_cancer/hla_estimation/all_normal_HLA.txt"
    # Target gene list
    genes = ["DRB1", "DQA1", "DQB1", "DPA1", "DPB1"]
    
    # Read original file (using tab as delimiter)
    data = []
    with open(input_file, "r", newline='') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            data.append(row)
    
    # Generate separate files for each gene
    for gene in genes:
        output_file = f"/data/yuan/gastric_cancer/hla_estimation/{gene}.txt"
        with open(output_file, "w", newline='') as out:
            writer = csv.writer(out, delimiter='\t')
            # Write to the header
            writer.writerow(["Sample", f"{gene}_1", f"{gene}_2"])
            # Extract two columns corresponding to Sample and gene for each row
            for row in data:
                sample = row.get("Sample", "")
                allele1 = row.get(f"{gene}_1", "")
                allele2 = row.get(f"{gene}_2", "")
                writer.writerow([sample, allele1, allele2])
        print(f"Generate files: {output_file}")

if __name__ == "__main__":
    main()

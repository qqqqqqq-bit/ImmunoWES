#!/usr/bin/env python3
import glob
import os

def transform_allele(allele):
    """
    Convert 'HLA-DRB1*04:03:01' to 'DRB10403'
    If allele is "Not typed" or "-", return an empty string
    """
    if allele in ["Not typed", "-"]:
        return ""
    # Remove the prefix "HLA-"
    if allele.startswith("HLA-"):
        allele = allele[len("HLA-"):]
    # Split gene and digital parts, expected format: gene*AA:BB:...
    parts = allele.split("*")
    if len(parts) != 2:
        return allele  # Return the original string directly if the format is inconsistent
    gene = parts[0]
    digits = parts[1]
    # Press ":" to divide the number part and take the first two sets of numbers.
    subparts = digits.split(":")
    if len(subparts) < 2:
        return gene + digits
    return gene + subparts[0] + subparts[1]

def process_file(file_path, target_genes):
    """
    Process a single file, return a dictionary, the key is the target gene name, and the value is (allele1, allele2)
    """
    results = {}
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split("\t")
            gene = fields[0].strip()
            if gene in target_genes:
                # If the data in the file is less than 3 columns, set an empty string
                allele1 = fields[1].strip() if len(fields) > 1 else ""
                allele2 = fields[2].strip() if len(fields) > 2 else ""
                allele1 = transform_allele(allele1)
                allele2 = transform_allele(allele2)
                results[gene] = (allele1, allele2)
    return results

def main():
    # Output file path
    output_file = "/data/yuan/gastric_cancer/hla_estimation/all_normal_HLA.txt"
    # Target gene list
    target_genes = ["DRB1", "DQA1", "DQB1", "DPA1", "DPB1"]
    # Find HLA typing files for all normal tissues (match only YSU_N*, exclude tumors YSU-T*)
    file_pattern = "/data/yuan/gastric_cancer/hla_estimation/YSU_N*/result/*_final.result.txt"
    files = glob.glob(file_pattern)
    files = sorted(files)

    with open(output_file, "w") as out:
        # Write to the header
        header = ["Sample"]
        for gene in target_genes:
            header.append(f"{gene}_1")
            header.append(f"{gene}_2")
        out.write("\t".join(header) + "\n")

        # Process each file
        for file_path in files:
            # Extract sample name from file path
            # for example：/data/yuan/gastric_cancer/hla_estimation/YSU_N1/result/YSU_N1_final.result.txt
            # Take the parent directory of the parent directory, that is, YSU_N1
            sample = os.path.basename(os.path.dirname(os.path.dirname(file_path)))
            results = process_file(file_path, target_genes)
            # Construct the output row, in order of the two alleles of the target gene (empty if not)
            row = [sample]
            for gene in target_genes:
                allele1, allele2 = results.get(gene, ("", ""))
                row.append(allele1)
                row.append(allele2)
            out.write("\t".join(row) + "\n")
    print(f"The result has been saved to {output_file}")

if __name__ == "__main__":
    main()

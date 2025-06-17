import os
import pandas as pd

# Define input and output directories
input_base = "/data/yuan/gastric_cancer/hla_estimation"
output_base = "/data/yuan/MHCflurry/hla"

# Create output directory if it does not exist
os.makedirs(output_base, exist_ok=True)

# Traverse all subdirectories in the input folder
for sample_dir in os.listdir(input_base):
    # Only process normal samples (sample names containing "N")
    if "N" not in sample_dir:
        continue

    # Build the path to the HLA-HD result folder
    full_sample_path = os.path.join(input_base, sample_dir, "result")
    if not os.path.isdir(full_sample_path):
        continue

    # Construct the expected result file path
    result_filename = f"{sample_dir}_final.result.txt"
    result_file = os.path.join(full_sample_path, result_filename)
    if not os.path.exists(result_file):
        print(f"Skipped: {result_file} does not exist")
        continue

    alleles = []

    # Read the result file and extract HLA class I alleles (A, B, C)
    with open(result_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split('\t')
            if parts[0] in ["A", "B", "C"]:
                for allele in parts[1:]:
                    if allele != "-" and allele != "":
                        # Ensure allele names follow the HLA-X* format
                        if not allele.startswith("HLA-"):
                            allele = f"HLA-{allele}"
                        alleles.append(allele)

    # Save the extracted alleles to CSV (MHCflurry input format)
    if alleles:
        df = pd.DataFrame({"allele": alleles})
        out_path = os.path.join(output_base, f"{sample_dir}_hla1.csv")
        df.to_csv(out_path, index=False)
        print(f"Saved: {out_path}")
    else:
        print(f"No HLA-I alleles found in: {result_file}")

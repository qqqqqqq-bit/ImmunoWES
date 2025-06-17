import os
import pandas as pd

# Define input and output directories
hla_dir = "/data/yuan/MHCflurry/hla"               # Directory containing HLA allele files
pep_dir = "/data/yuan/MHCflurry/9mer_mutation"     # Directory containing 9-mer peptide sequences
output_dir = "/data/yuan/MHCflurry/mhcflurry_input" # Output directory for MHCflurry input files

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Function to create sample mapping between normal (HLA) and tumor (peptides) samples
def match_normal_tumor(hla_files, pep_files):
    mapping = {}
    for hla_file in hla_files:
        # Extract the normal sample name (e.g., YSU_N1)
        normal_sample = hla_file.split("_hla1")[0]
        # Generate the corresponding tumor sample name by replacing 'N' with 'T'
        tumor_sample = normal_sample.replace("N", "T")
        # Match with the corresponding peptide file
        matched_pep_file = next((p for p in pep_files if tumor_sample in p), None)
        if matched_pep_file:
            mapping[hla_file] = matched_pep_file
    return mapping

# List all HLA and peptide CSV files
hla_files = [f for f in os.listdir(hla_dir) if f.endswith(".csv")]
pep_files = [f for f in os.listdir(pep_dir) if f.endswith(".csv")]

# Create mapping from HLA files (normal) to peptide files (tumor)
sample_map = match_normal_tumor(hla_files, pep_files)

# Iterate through matched sample pairs
for hla_file, pep_file in sample_map.items():
    hla_path = os.path.join(hla_dir, hla_file)
    pep_path = os.path.join(pep_dir, pep_file)

    # Read HLA alleles
    hla_df = pd.read_csv(hla_path)
    alleles = hla_df["allele"].dropna().tolist()

    # Read 9-mer peptides
    pep_df = pd.read_csv(pep_path)
    peptides = pep_df["peptide"].dropna().tolist()

    # Generate Cartesian product of peptides and alleles
    combined = pd.DataFrame(
        [(pep, hla) for pep in peptides for hla in alleles],
        columns=["peptide", "allele"]
    )

    # Construct output file path and save
    sample_name = os.path.splitext(pep_file)[0].replace("_filtered_filtered", "")
    out_path = os.path.join(output_dir, f"{sample_name}_mhcflurry_input.csv")
    combined.to_csv(out_path, index=False)
    print(f"✅ Saved: {out_path}")

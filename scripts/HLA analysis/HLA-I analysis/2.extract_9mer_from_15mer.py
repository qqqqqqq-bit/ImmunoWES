import os
import pandas as pd

# Define input and output directories
input_dir = "/data/yuan/MHCflurry/15mer_mutation"
output_dir = "/data/yuan/MHCflurry/9mer_mutation"

# Create the output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

# Iterate over all files in the input directory
for filename in os.listdir(input_dir):
    # Skip files that are not .txt or .fasta
    if not filename.endswith(".txt") and not filename.endswith(".fasta"):
        continue

    sample_name = os.path.splitext(filename)[0]
    input_path = os.path.join(input_dir, filename)
    output_path = os.path.join(output_dir, f"{sample_name}.csv")

    peptides_9mer = []

    # Read the input file line by line
    with open(input_path, "r") as f:
        for line in f:
            seq = line.strip()
            # Ensure the sequence is a valid 15-mer
            if len(seq) != 15:
                print(f"Warning: Non-15-mer sequence found in {filename}: {seq}")
                continue
            # Extract the central 9-mer (removing 3 AAs from both ends)
            mid_9mer = seq[3:12]
            peptides_9mer.append(mid_9mer)

    # Save the 9-mer peptides to a CSV file
    if peptides_9mer:
        df = pd.DataFrame({"peptide": peptides_9mer})
        df.to_csv(output_path, index=False)
        print(f"Saved: {output_path}")
    else:
        print(f"No valid 15-mer sequences extracted from {filename}")

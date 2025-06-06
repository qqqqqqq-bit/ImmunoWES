import pandas as pd
import os
import re

# Enter the directory (processed CSV file)
input_path = "/data/yuan/gastric_cancer/downstream_ukb/gastric_vcf/whole_seq/processed"

# Output directory (15mer mutation sequence)
output_path = "/data/LiuRT/mhc2/MixMHCIIpred/gastric_cancer/15mer_mutation"
os.makedirs(output_path, exist_ok=True)  # Make sure the output directory exists

# Iterate through all CSV files
for file_name in os.listdir(input_path):
    if file_name.endswith(".csv"):  # Process only CSV files
        file_path = os.path.join(input_path, file_name)

        # Read CSV files
        df = pd.read_csv(file_path)

        # Make sure the `MappedMutation` column exists
        if "MappedMutation" not in df.columns:
            print(f"Skip {file_name}: Missing MappedMutation column")
            continue

        # Handle the `MappedMutation` column
        def extract_15mer(mapped_seq):
            if pd.isna(mapped_seq):
                return None  # Skip empty values

            # Matching the `(X)` format mutation
            match = re.search(r"\(([A-Z])\)([A-Z])", mapped_seq)
            if not match:
                return None  # No matching mutation format was found

            # Get the location of `(` and `)`
            left_paren = mapped_seq.index('(')
            right_paren = mapped_seq.index(')')

            # Extract 7 characters first and 8 characters after brackets
            start = max(0, left_paren - 7)  # `(` First 7 characters
            end = right_paren + 1 + 8  # `)` The last 8 characters

            # Get the last 8 characters from `(` first 7 characters and `)`
            prefix = mapped_seq[start:left_paren]  # `(` First 7 characters
            suffix = mapped_seq[right_paren + 1:right_paren + 1 + 8]  # `)` The last 8 characters符

            # Splicing the front and back parts, return 15mer
            extracted_seq = prefix + suffix

            return extracted_seq if len(extracted_seq) == 15 else None  # Ensure length is 15

        # Generate 15mer columns
        df["15mer"] = df["MappedMutation"].apply(extract_15mer)

        # Filter out empty lines with `15mer`
        df_filtered = df.dropna(subset=["15mer"])[["15mer"]]

        # Output file path (convert file name format)
        output_file_name = os.path.splitext(file_name)[0] + ".txt"
        output_file_path = os.path.join(output_path, output_file_name)

        # Save as txt file
        df_filtered.to_csv(output_file_path, index=False, header=False)
        print(f"Processing is completed: {file_name}, and the result is saved to {output_file_path}")

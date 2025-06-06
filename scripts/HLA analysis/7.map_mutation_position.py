import pandas as pd
import os
import re

# Input and output paths
input_path = "/data/yuan/gastric_cancer/downstream_ukb/gastric_vcf/whole_seq"
output_path = "/data/yuan/gastric_cancer/downstream_ukb/gastric_vcf/whole_seq/processed"

# Make sure the output directory exists
os.makedirs(output_path, exist_ok=True)

# Iterate through all CSV files
for file_name in os.listdir(input_path):
    if file_name.endswith(".csv"):  # 只处理 CSV 文件
        file_path = os.path.join(input_path, file_name)
        
        # Read CSV files
        df = pd.read_csv(file_path)
        
        # Make sure that the necessary columns exist
        if "AAChange.refGene" not in df.columns or "Sequence" not in df.columns:
            print(f"Skip {file_name}: The required column is missing")
            continue

        # Fill in missing values
        df["AAChange.refGene"] = df["AAChange.refGene"].fillna("").astype(str)
        df["Sequence"] = df["Sequence"].fillna("").astype(str)

        def map_mutation(row):
            sequence = row["Sequence"]
            aa_changes = row["AAChange.refGene"].split(";")  # There may be multiple changes
            
            #If Sequence is empty, return a null value
            if not sequence:
                return ""

            modified_sequence = list(sequence)  # Convert to a list first for easy modification
            matched = False  # Recording whether the match is successful

            for aa_change in aa_changes:
                match = re.search(r"p\.([A-Z])(\d+)([A-Z])", aa_change)
                if match:
                    original_aa, pos, mutated_aa = match.groups()
                    pos = int(pos)  # Convert position to integer

                    # Make sure the position is within the range of the sequence
                    if pos <= len(sequence) and sequence[pos - 1] == original_aa:
                        # Mutation modification(N)T
                        modified_sequence[pos - 1] = f"({original_aa}){mutated_aa}"
                        matched = True
                        break  # Stop after matching

            if not matched:
                return ""  # Make unmatched values ​​empty
            
            return "".join(modified_sequence)  # Convert back to string

        # Apply mapping functions
        df["MappedMutation"] = df.apply(map_mutation, axis=1)

        # Calculate matching situation
        total_rows = len(df)  # Total row count
        empty_sequence_count = df["Sequence"].eq("").sum()  # Sequence Number of empty rows
        unmatched_mutation_count = df["MappedMutation"].eq("").sum() - empty_sequence_count  # Number of rows whose mutation information does not match
        matched_count = total_rows - (empty_sequence_count + unmatched_mutation_count)  # Number on match

        match_rate = (matched_count / total_rows) * 100 if total_rows > 0 else 0
        empty_sequence_rate = (empty_sequence_count / total_rows) * 100 if total_rows > 0 else 0
        unmatched_mutation_rate = (unmatched_mutation_count / total_rows) * 100 if total_rows > 0 else 0

        # Output matching situation
        print(f"{file_name}: Match successfully {matched_count}/{total_rows} ({match_rate:.2f}%)")
        print(f" - Sequence Empty: {empty_sequence_count}/{total_rows} ({empty_sequence_rate:.2f}%)")
        print(f" - AAChange.refGene Not matched: {unmatched_mutation_count}/{total_rows} ({unmatched_mutation_rate:.2f}%)")

        # Save processed CSV
        output_file = os.path.join(output_path, file_name)
        df.to_csv(output_file, index=False)
        print(f"Processing is completed, the result is saved to {output_file}\n")



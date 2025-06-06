import pandas as pd
import os

# Enter the directory path
input_dir = "/data/yuan/gastric_cancer/downstream_ukb/gastric_vcf/filter/filter_extract_csv"

# Iterate through all CSV files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        input_file = os.path.join(input_dir, filename)

        try:
            df = pd.read_csv(input_file, engine='python')

            if len(df.columns) < 12:
                print(f"Skip file {filename}: less than 12 columns")
                continue

            mutation_col = df.columns[11]

            def extract_last_mutation(value):
                if isinstance(value, str):
                    return ';'.join([part.split(':')[-1] for part in value.split(';')])
                return value

            df[mutation_col] = df[mutation_col].apply(extract_last_mutation)

            df.to_csv(input_file, index=False)
            print(f"Process and update files：{filename}")

        except Exception as e:
            print(f"An error occurred while processing file {filename}: {e}")

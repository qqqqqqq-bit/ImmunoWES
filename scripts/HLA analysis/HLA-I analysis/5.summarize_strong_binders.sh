#!/bin/bash

# Define input directory containing MHCflurry prediction results
INPUT_DIR="/data/yuan/MHCflurry/mhcflurry_output"

# Define output summary file path
OUTPUT_FILE="/data/yuan/MHCflurry/strong_binder_summary.csv"

# Initialize the output CSV file with header
echo "Sample,StrongBinderCount" > "$OUTPUT_FILE"

# Loop through all prediction result CSVs
for file in "$INPUT_DIR"/*.csv; do
    # Extract the sample name from the filename
    filename=$(basename "$file")
    sample_name="${filename%_prediction.csv}"

    # Count the number of strong-binding peptides (affinity < 500 nM), skip header
    count=$(awk -F',' 'NR>1 && $3 < 500 { count++ } END { print count+0 }' "$file")

    # Write result to output CSV
    echo "$sample_name,$count" >> "$OUTPUT_FILE"
done

# Completion message
echo "✅ Strong binder summary completed: $OUTPUT_FILE"

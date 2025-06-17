#!/bin/bash

# Set input and output directories
INPUT_DIR="/data/yuan/MHCflurry/mhcflurry_input"
OUTPUT_DIR="/data/yuan/MHCflurry/mhcflurry_output"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Loop through all MHCflurry input CSV files
for infile in "$INPUT_DIR"/*.csv; do
    # Extract the sample name from the filename
    filename=$(basename "$infile")
    sample_name="${filename%_mhcflurry_input.csv}"
    
    # Define output file path
    outfile="$OUTPUT_DIR/${sample_name}_prediction.csv"

    # Log progress
    echo "🔄 Processing $sample_name..."

    # Run MHCflurry prediction with affinity-only mode
    mhcflurry-predict "$infile" --out "$outfile" --affinity-only

    # Log completion
    echo "✅ Done: $outfile"
done

# Final message
echo "🎉 All samples processed!"

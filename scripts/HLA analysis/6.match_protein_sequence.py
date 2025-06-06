import csv
from Bio import SeqIO
import re
import os

def extract_gene_name(header):
    """Extract the gene name after GN= from the fasta sequence name"""
    match = re.search(r'GN=(\w+)', header)
    if match:
        return match.group(1)
    return None

def match_sequences(fasta_file, input_dir, output_dir, gene_col_index=10, seq_col_index=12):

    # Extract gene name and corresponding sequence from fasta file
    gene_to_seq = {}
    for record in SeqIO.parse(fasta_file, "fasta"):
        gene_name = extract_gene_name(record.description)
        if gene_name:
            gene_to_seq[gene_name] = str(record.seq)
    
    # Get all CSV files under input_dir
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            input_csv = os.path.join(input_dir, filename)
            output_csv = os.path.join(output_dir, filename.replace(".csv", "_filtered.csv"))
            
            # Open CSV file for processing
            with open(input_csv, 'r', newline='') as infile, \
                 open(output_csv, 'w', newline='') as outfile:
                
                reader = csv.reader(infile)
                writer = csv.writer(outfile)
                
                header = next(reader)
                
                # Make sure the number of csv columns is correct and add empty columns until the target column is reached
                while len(header) <= seq_col_index:
                    header.append('')
                header[seq_col_index] = 'Sequence'
                writer.writerow(header)
                
                # Iterate through each row and match the corresponding sequence according to the gene name
                for row in reader:
                    while len(row) <= seq_col_index:
                        row.append('')
                    
                    if len(row) > gene_col_index:
                        gene_name = row[gene_col_index]
                        if gene_name in gene_to_seq:
                            row[seq_col_index] = gene_to_seq[gene_name]
                    
                    writer.writerow(row)

if __name__ == "__main__":
    fasta_file = "/data/yuan/IMM/Ref-seq/UP000005640_9606.fasta"
    input_dir = "/data/yuan/gastric_cancer/downstream_ukb/gastric_vcf/filter/filter_extract_csv/"
    output_dir = "/data/yuan/gastric_cancer/downstream_ukb/gastric_vcf/whole_seq/"
    
    # Make sure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Calling functions to process all files
    match_sequences(fasta_file, input_dir, output_dir)



import csv
from Bio import SeqIO
import re
import os

def extract_gene_name(header):
    """从fasta序列名中提取GN=后的基因名"""
    match = re.search(r'GN=(\w+)', header)
    if match:
        return match.group(1)
    return None

def match_sequences(fasta_file, input_dir, output_dir, gene_col_index=10, seq_col_index=12):

    # 从fasta文件中提取基因名和对应的序列
    gene_to_seq = {}
    for record in SeqIO.parse(fasta_file, "fasta"):
        gene_name = extract_gene_name(record.description)
        if gene_name:
            gene_to_seq[gene_name] = str(record.seq)
    
    # 获取input_dir下所有CSV文件
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            input_csv = os.path.join(input_dir, filename)
            output_csv = os.path.join(output_dir, filename.replace(".csv", "_filtered.csv"))
            
            # 打开CSV文件进行处理
            with open(input_csv, 'r', newline='') as infile, \
                 open(output_csv, 'w', newline='') as outfile:
                
                reader = csv.reader(infile)
                writer = csv.writer(outfile)
                
                header = next(reader)
                
                # 确保csv列数正确，添加空列直到达到目标列
                while len(header) <= seq_col_index:
                    header.append('')
                header[seq_col_index] = 'Sequence'
                writer.writerow(header)
                
                # 遍历每一行并根据基因名匹配对应的序列
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
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 调用函数处理所有文件
    match_sequences(fasta_file, input_dir, output_dir)



#!/usr/bin/env python3
import csv
import os

def main():
    input_file = "/data/yuan/gastric_cancer/hla_estimation/all_normal_HLA.txt"
    # 目标基因列表
    genes = ["DRB1", "DQA1", "DQB1", "DPA1", "DPB1"]
    
    # 读取原始文件（使用 tab 作为分隔符）
    data = []
    with open(input_file, "r", newline='') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            data.append(row)
    
    # 针对每个基因生成单独的文件
    for gene in genes:
        output_file = f"/data/yuan/gastric_cancer/hla_estimation/{gene}.txt"
        with open(output_file, "w", newline='') as out:
            writer = csv.writer(out, delimiter='\t')
            # 写入表头
            writer.writerow(["Sample", f"{gene}_1", f"{gene}_2"])
            # 针对每一行数据提取 Sample 及 gene 对应的两列
            for row in data:
                sample = row.get("Sample", "")
                allele1 = row.get(f"{gene}_1", "")
                allele2 = row.get(f"{gene}_2", "")
                writer.writerow([sample, allele1, allele2])
        print(f"生成文件: {output_file}")

if __name__ == "__main__":
    main()

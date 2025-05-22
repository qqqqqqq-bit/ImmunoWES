#!/usr/bin/env python3
import glob
import os

def transform_allele(allele):
    """
    将形如 'HLA-DRB1*04:03:01' 转换为 'DRB10403'
    如果 allele 为 "Not typed" 或 "-"，返回空串
    """
    if allele in ["Not typed", "-"]:
        return ""
    # 去掉前缀 "HLA-"
    if allele.startswith("HLA-"):
        allele = allele[len("HLA-"):]
    # 分割 gene 和数字部分，预期格式： gene*AA:BB:...
    parts = allele.split("*")
    if len(parts) != 2:
        return allele  # 格式不符时直接返回原始字符串
    gene = parts[0]
    digits = parts[1]
    # 按 ":" 分割数字部分，取前两组数字
    subparts = digits.split(":")
    if len(subparts) < 2:
        return gene + digits
    return gene + subparts[0] + subparts[1]

def process_file(file_path, target_genes):
    """
    处理单个文件，返回一个字典，键为目标基因名称，值为 (allele1, allele2)
    """
    results = {}
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split("\t")
            gene = fields[0].strip()
            if gene in target_genes:
                # 如果文件中该行数据不足3列，设置空串
                allele1 = fields[1].strip() if len(fields) > 1 else ""
                allele2 = fields[2].strip() if len(fields) > 2 else ""
                allele1 = transform_allele(allele1)
                allele2 = transform_allele(allele2)
                results[gene] = (allele1, allele2)
    return results

def main():
    # 输出文件路径
    output_file = "/data/yuan/gastric_cancer/hla_estimation/all_normal_HLA.txt"
    # 目标基因列表
    target_genes = ["DRB1", "DQA1", "DQB1", "DPA1", "DPB1"]
    # 查找所有正常组织的 HLA 分型文件（只匹配 YSU_N*，排除肿瘤 YSU-T*）
    file_pattern = "/data/yuan/gastric_cancer/hla_estimation/YSU_N*/result/*_final.result.txt"
    files = glob.glob(file_pattern)
    files = sorted(files)

    with open(output_file, "w") as out:
        # 写入表头
        header = ["Sample"]
        for gene in target_genes:
            header.append(f"{gene}_1")
            header.append(f"{gene}_2")
        out.write("\t".join(header) + "\n")

        # 处理每个文件
        for file_path in files:
            # 从文件路径中提取样本名称
            # 例如：/data/yuan/gastric_cancer/hla_estimation/YSU_N1/result/YSU_N1_final.result.txt
            # 取父目录的父目录，即 YSU_N1
            sample = os.path.basename(os.path.dirname(os.path.dirname(file_path)))
            results = process_file(file_path, target_genes)
            # 构造输出行，顺序依次为目标基因的两个等位基因（若不存在则为空）
            row = [sample]
            for gene in target_genes:
                allele1, allele2 = results.get(gene, ("", ""))
                row.append(allele1)
                row.append(allele2)
            out.write("\t".join(row) + "\n")
    print(f"结果已保存到 {output_file}")

if __name__ == "__main__":
    main()

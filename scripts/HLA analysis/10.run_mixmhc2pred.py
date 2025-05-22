import os
import re
import subprocess

hla_dir = "/data/LiuRT/mhc2/MixMHCIIpred/gastric_cancer/hla"
peptide_dir = "/data/LiuRT/mhc2/MixMHCIIpred/gastric_cancer/15mer_mutation"
output_dir = "/data/LiuRT/mhc2/MixMHCIIpred/gastric_cancer/prediction"
pwm_dir = "/data/LiuRT/mhc2/MixMHCIIpred/PWMdef"
os.makedirs(output_dir, exist_ok=True)

hla_files = {}
peptide_files = {}

for f in os.listdir(hla_dir):
    match = re.search(r"(.+)_N(\d+)\.hla", f)
    if match:
        sample_name, num = match.groups()
        hla_files[num] = os.path.join(hla_dir, f)

for f in os.listdir(peptide_dir):
    match = re.search(r"(.+)_T(\d+)_filtered_filtered\.txt", f)
    if match:
        sample_name, num = match.groups()
        peptide_files[num] = os.path.join(peptide_dir, f)

defined_alleles = {f.replace(".txt", "") for f in os.listdir(pwm_dir) if f.endswith(".txt")}
undefined_alleles = set()

for sample_num in hla_files.keys() & peptide_files.keys():
    hla_file = hla_files[sample_num]
    peptide_file = peptide_files[sample_num]
    output_file = os.path.join(output_dir, f"YSU_T{sample_num}_prediction.txt")

    with open(hla_file, "r") as f:
        alleles = f.read().strip().split()

    valid_alleles = [a for a in alleles if a in defined_alleles]
    skipped_alleles = set(alleles) - set(valid_alleles)

    if skipped_alleles:
        undefined_alleles.update(skipped_alleles)
        print(f"⚠️ 样本 {sample_num} 存在未定义的等位基因：{', '.join(skipped_alleles)}，已跳过")

    if not valid_alleles:
        print(f"❌ 警告：{hla_file} 所有等位基因均未定义，跳过 {sample_num}")
        continue

    with open(peptide_file, "r") as f:
        peptides = f.read().strip().split("\n")

    if not peptides:
        print(f"❌ 警告：{peptide_file} 为空，跳过 {sample_num}")
        continue

    allele_string = " ".join(valid_alleles)
    peptide_sequences = "\n".join(peptides)
    command = f'./MixMHC2pred_unix -i <(echo "{peptide_sequences}") -o {output_file} -a {allele_string} --no_context'

    try:
        subprocess.run(command, shell=True, check=True, executable="/bin/bash")
        print(f"✅ 预测完成：样本 {sample_num}，结果保存在 {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 错误：样本 {sample_num} 预测失败，错误信息：{e}")

if undefined_alleles:
    print("\n⚠️ 以下等位基因未在 PWMdef 目录中定义，无法用于 MixMHC2pred：")
    print(", ".join(undefined_alleles))

print("\n✅ 所有样本处理完成！")


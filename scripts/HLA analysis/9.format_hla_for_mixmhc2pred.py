import os
import re

# 输入路径（HLA 分型数据存放目录）
input_dir = "/data/yuan/gastric_cancer/hla_estimation"
# 输出路径（MixMHC2pred 需要的 HLA 格式）
output_dir = "/data/LiuRT/mhc2/MixMHCIIpred/gastric_cancer/hla"

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 处理 HLA 格式的函数
def format_hla(allele):
    """转换 HLA 等位基因格式，符合 MixMHC2pred 需求，且只保留前两组 _ 分隔的部分"""
    if allele == "Not typed" or allele == "-":
        return None
    formatted = re.sub(r"HLA-|[*:]", lambda x: "_" if x.group() in ["*", ":"] else "", allele)
    return "_".join(formatted.split("_")[:3])  # 只保留基因名 + 两位数字（如 DRB1_04_03）

# 遍历 input_dir 下的所有正常组织文件夹
for sample_folder in os.listdir(input_dir):
    sample_path = os.path.join(input_dir, sample_folder)
    
    # 只处理文件夹且文件夹名包含 "N"（代表正常组织）
    if not os.path.isdir(sample_path) or "N" not in sample_folder:
        continue

    # HLA 结果文件路径
    result_file = os.path.join(sample_path, "result", f"{sample_folder}_final.result.txt")
    if not os.path.exists(result_file):
        print(f"❌ 跳过 {sample_folder}，文件不存在：{result_file}")
        continue

    # 读取 HLA 文件并解析
    hla_dict = {}
    with open(result_file, "r") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 2:
                continue
            gene = parts[0]
            alleles = [format_hla(a) for a in parts[1:] if format_hla(a) is not None]
            if alleles:
                hla_dict[gene] = alleles

    # 处理 HLA-II 基因并格式化
    hla_list = []
    
    # DRB 系列（单独列出）
    for drb in ["DRB1", "DRB3", "DRB4", "DRB5"]:
        if drb in hla_dict:
            hla_list.extend(hla_dict[drb])

    # DQA1 + DQB1（必须成对）
    if "DQA1" in hla_dict and "DQB1" in hla_dict:
        dqa_alleles = hla_dict["DQA1"]
        dqb_alleles = hla_dict["DQB1"]
        dq_pairs = [f"{dqa}__{dqb}" for dqa, dqb in zip(dqa_alleles, dqb_alleles)]
        hla_list.extend(dq_pairs)

    # DPA1 + DPB1（必须成对）
    if "DPA1" in hla_dict and "DPB1" in hla_dict:
        dpa_alleles = hla_dict["DPA1"]
        dpb_alleles = hla_dict["DPB1"]
        dp_pairs = [f"{dpa}__{dpb}" for dpa, dpb in zip(dpa_alleles, dpb_alleles)]
        hla_list.extend(dp_pairs)

    # 如果没有可用的 HLA-II 数据，则跳过
    if not hla_list:
        print(f"⚠️ {sample_folder} 没有可用于 MixMHC2pred 的 HLA-II 数据，跳过")
        continue

    # 生成输出文件路径
    output_file = os.path.join(output_dir, f"{sample_folder}.hla")

    # 写入输出文件
    with open(output_file, "w") as out_f:
        out_f.write(" ".join(hla_list) + "\n")

    print(f"✅ 处理完成：{output_file}")

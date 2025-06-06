import os
import re

# Input path (HLA typing data storage directory)
input_dir = "/data/yuan/gastric_cancer/hla_estimation"
# Output path (HLA format required by MixMHC2pred)
output_dir = "/data/LiuRT/mhc2/MixMHCIIpred/gastric_cancer/hla"

# Make sure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Functions that handle HLA format
def format_hla(allele):
    """Convert the HLA allele format, meets the requirements of MixMHC2pred, and only the first two groups _separated parts are retained"""
    if allele == "Not typed" or allele == "-":
        return None
    formatted = re.sub(r"HLA-|[*:]", lambda x: "_" if x.group() in ["*", ":"] else "", allele)
    return "_".join(formatted.split("_")[:3])  # Only retain gene name + two digits (such as DRB1_04_03)

# Iterate through all normal organization folders under input_dir
for sample_folder in os.listdir(input_dir):
    sample_path = os.path.join(input_dir, sample_folder)
    
    # Process only folders and folder names contain "N" (represents normal organization)
    if not os.path.isdir(sample_path) or "N" not in sample_folder:
        continue

    # HLA result file path
    result_file = os.path.join(sample_path, "result", f"{sample_folder}_final.result.txt")
    if not os.path.exists(result_file):
        print(f"❌ Skip {sample_folder}, the file does not exist：{result_file}")
        continue

    # Read and parse the HLA file
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

    # Processing and formatting HLA-II genes
    hla_list = []
    
    # DRB Series (listed separately)
    for drb in ["DRB1", "DRB3", "DRB4", "DRB5"]:
        if drb in hla_dict:
            hla_list.extend(hla_dict[drb])

    # DQA1 + DQB1(must be paired)
    if "DQA1" in hla_dict and "DQB1" in hla_dict:
        dqa_alleles = hla_dict["DQA1"]
        dqb_alleles = hla_dict["DQB1"]
        dq_pairs = [f"{dqa}__{dqb}" for dqa, dqb in zip(dqa_alleles, dqb_alleles)]
        hla_list.extend(dq_pairs)

    # DPA1 + DPB1(must be paired)
    if "DPA1" in hla_dict and "DPB1" in hla_dict:
        dpa_alleles = hla_dict["DPA1"]
        dpb_alleles = hla_dict["DPB1"]
        dp_pairs = [f"{dpa}__{dpb}" for dpa, dpb in zip(dpa_alleles, dpb_alleles)]
        hla_list.extend(dp_pairs)

    # If no HLA-II data is available, skip
    if not hla_list:
        print(f"⚠️ {sample_folder} There is no HLA-II data available for MixMHC2pred, skip")
        continue

    # Generate output file path
    output_file = os.path.join(output_dir, f"{sample_folder}.hla")

    # Write to the output file
    with open(output_file, "w") as out_f:
        out_f.write(" ".join(hla_list) + "\n")

    print(f"✅ Processing is completed：{output_file}")

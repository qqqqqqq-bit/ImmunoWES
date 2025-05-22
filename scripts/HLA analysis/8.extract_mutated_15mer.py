import pandas as pd
import os
import re

# 输入目录（已处理的 CSV 文件）
input_path = "/data/yuan/gastric_cancer/downstream_ukb/gastric_vcf/whole_seq/processed"

# 输出目录（15mer 突变序列）
output_path = "/data/LiuRT/mhc2/MixMHCIIpred/gastric_cancer/15mer_mutation"
os.makedirs(output_path, exist_ok=True)  # 确保输出目录存在

# 遍历所有 CSV 文件
for file_name in os.listdir(input_path):
    if file_name.endswith(".csv"):  # 只处理 CSV 文件
        file_path = os.path.join(input_path, file_name)

        # 读取 CSV 文件
        df = pd.read_csv(file_path)

        # 确保 `MappedMutation` 列存在
        if "MappedMutation" not in df.columns:
            print(f"跳过 {file_name}：缺少 MappedMutation 列")
            continue

        # 处理 `MappedMutation` 列
        def extract_15mer(mapped_seq):
            if pd.isna(mapped_seq):
                return None  # 跳过空值

            # 匹配 `(X)` 格式的突变
            match = re.search(r"\(([A-Z])\)([A-Z])", mapped_seq)
            if not match:
                return None  # 没有找到符合的突变格式

            # 获取 `(` 和 `)` 的位置
            left_paren = mapped_seq.index('(')
            right_paren = mapped_seq.index(')')

            # 提取括号前 7 个字符，括号后 8 个字符
            start = max(0, left_paren - 7)  # `(` 前 7 个字符
            end = right_paren + 1 + 8  # `)` 后 8 个字符

            # 获取从 `(` 前 7 个字符和 `)` 后 8 个字符
            prefix = mapped_seq[start:left_paren]  # `(` 前 7 个字符
            suffix = mapped_seq[right_paren + 1:right_paren + 1 + 8]  # `)` 后 8 个字符

            # 拼接前后部分，返回 15mer
            extracted_seq = prefix + suffix

            return extracted_seq if len(extracted_seq) == 15 else None  # 确保长度为 15

        # 生成 15mer 列
        df["15mer"] = df["MappedMutation"].apply(extract_15mer)

        # 过滤掉 `15mer` 为空的行
        df_filtered = df.dropna(subset=["15mer"])[["15mer"]]

        # 输出文件路径（转换文件名格式）
        output_file_name = os.path.splitext(file_name)[0] + ".txt"
        output_file_path = os.path.join(output_path, output_file_name)

        # 保存为 txt 文件
        df_filtered.to_csv(output_file_path, index=False, header=False)
        print(f"处理完成：{file_name}，结果保存至 {output_file_path}")

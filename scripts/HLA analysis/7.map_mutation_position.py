import pandas as pd
import os
import re

# 输入和输出路径
input_path = "/data/yuan/gastric_cancer/downstream_ukb/gastric_vcf/whole_seq"
output_path = "/data/yuan/gastric_cancer/downstream_ukb/gastric_vcf/whole_seq/processed"

# 确保输出目录存在
os.makedirs(output_path, exist_ok=True)

# 遍历所有 CSV 文件
for file_name in os.listdir(input_path):
    if file_name.endswith(".csv"):  # 只处理 CSV 文件
        file_path = os.path.join(input_path, file_name)
        
        # 读取 CSV 文件
        df = pd.read_csv(file_path)
        
        # 确保必要的列存在
        if "AAChange.refGene" not in df.columns or "Sequence" not in df.columns:
            print(f"跳过 {file_name}：缺少必要的列")
            continue

        # 填充缺失值
        df["AAChange.refGene"] = df["AAChange.refGene"].fillna("").astype(str)
        df["Sequence"] = df["Sequence"].fillna("").astype(str)

        def map_mutation(row):
            sequence = row["Sequence"]
            aa_changes = row["AAChange.refGene"].split(";")  # 可能有多个变化
            
            # 如果 Sequence 为空，返回空值
            if not sequence:
                return ""

            modified_sequence = list(sequence)  # 先转换为列表，方便修改
            matched = False  # 记录是否成功匹配

            for aa_change in aa_changes:
                match = re.search(r"p\.([A-Z])(\d+)([A-Z])", aa_change)
                if match:
                    original_aa, pos, mutated_aa = match.groups()
                    pos = int(pos)  # 位置转换为整数

                    # 确保位置在序列范围内
                    if pos <= len(sequence) and sequence[pos - 1] == original_aa:
                        # 进行突变修饰 (N)T
                        modified_sequence[pos - 1] = f"({original_aa}){mutated_aa}"
                        matched = True
                        break  # 匹配上后就停止

            if not matched:
                return ""  # 让未匹配的值为空
            
            return "".join(modified_sequence)  # 重新转换回字符串

        # 应用映射函数
        df["MappedMutation"] = df.apply(map_mutation, axis=1)

        # 计算匹配情况
        total_rows = len(df)  # 总行数
        empty_sequence_count = df["Sequence"].eq("").sum()  # Sequence 为空的行数
        unmatched_mutation_count = df["MappedMutation"].eq("").sum() - empty_sequence_count  # 突变信息未匹配的行数
        matched_count = total_rows - (empty_sequence_count + unmatched_mutation_count)  # 匹配上的数量

        match_rate = (matched_count / total_rows) * 100 if total_rows > 0 else 0
        empty_sequence_rate = (empty_sequence_count / total_rows) * 100 if total_rows > 0 else 0
        unmatched_mutation_rate = (unmatched_mutation_count / total_rows) * 100 if total_rows > 0 else 0

        # 输出匹配情况
        print(f"{file_name}: 匹配成功 {matched_count}/{total_rows} ({match_rate:.2f}%)")
        print(f" - Sequence 为空: {empty_sequence_count}/{total_rows} ({empty_sequence_rate:.2f}%)")
        print(f" - AAChange.refGene 未匹配: {unmatched_mutation_count}/{total_rows} ({unmatched_mutation_rate:.2f}%)")

        # 保存处理后的 CSV
        output_file = os.path.join(output_path, file_name)
        df.to_csv(output_file, index=False)
        print(f"处理完成，结果保存至 {output_file}\n")



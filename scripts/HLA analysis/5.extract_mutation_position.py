import pandas as pd
import os

# 输入目录路径
input_dir = "/data/yuan/gastric_cancer/downstream_ukb/gastric_vcf/filter/filter_extract_csv"

# 遍历输入目录中的所有 CSV 文件
for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        input_file = os.path.join(input_dir, filename)

        try:
            df = pd.read_csv(input_file, engine='python')

            if len(df.columns) < 12:
                print(f"跳过文件 {filename}：列数不足12列")
                continue

            mutation_col = df.columns[11]

            def extract_last_mutation(value):
                if isinstance(value, str):
                    return ';'.join([part.split(':')[-1] for part in value.split(';')])
                return value

            df[mutation_col] = df[mutation_col].apply(extract_last_mutation)

            df.to_csv(input_file, index=False)
            print(f"处理并更新文件：{filename}")

        except Exception as e:
            print(f"处理文件 {filename} 时发生错误: {e}")

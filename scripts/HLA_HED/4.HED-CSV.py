import os
import pandas as pd

def find_divergence_files(base_path):
    """递归查找所有包含IndividualDivergence的文件"""
    divergence_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if 'IndividualDivergence' in file and file.endswith('.txt'):
                full_path = os.path.join(root, file)
                divergence_files.append(full_path)
    return divergence_files

def process_divergence_files(base_path):
    # 找到所有相关文件
    all_files = find_divergence_files(base_path)
    
    # 存储所有文件的数据
    all_data = {}
    file_names = []
    
    # 处理每个文件
    for file_path in all_files:
        # 获取文件名作为列名
        file_name = os.path.basename(file_path)
        file_names.append(file_name)
        
        try:
            # 读取文件，只读取第1列和第3列
            data = []
            with open(file_path, 'r') as f:
                # 跳过表头行
                next(f)
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 3:  # 确保行至少有3列
                        id_val = parts[0]
                        div_val = parts[2]
                        try:
                            # 将divergence值转换为浮点数
                            div_val = float(div_val)
                            data.append((id_val, div_val))
                        except ValueError:
                            continue
            
            # 创建ID到Divergence_Average的映射
            all_data[file_name] = dict(data)
            
        except Exception as e:
            print(f"处理文件 {file_name} 时出错: {str(e)}")
            continue
    
    # 获取所有唯一的ID
    all_ids = set()
    for data in all_data.values():
        all_ids.update(data.keys())
    
    # 创建结果DataFrame
    result_data = []
    
    # 对每个ID创建一行数据
    for eid in sorted(all_ids):
        row = {'eid': eid}
        # 添加每个文件中对应的Divergence_Average值
        for file in sorted(file_names):
            row[file] = all_data[file].get(eid, '')  # 如果没有值则使用空字符串
        result_data.append(row)
    
    # 创建DataFrame
    result_df = pd.DataFrame(result_data)
    
    # 确保eid列在最前面
    columns = ['eid'] + sorted([col for col in result_df.columns if col != 'eid'])
    result_df = result_df[columns]
    
    # 保存为CSV，确保数字格式保持原样
    output_path = os.path.join(base_path, 'combined_divergence.csv')
    result_df.to_csv(output_path, index=False, float_format='%.11f')
    
    print(f"处理完成。共处理了{len(file_names)}个文件，包含{len(all_ids)}个唯一ID。")
    print(f"输出文件保存在: {output_path}")
    print("\n前几行数据示例：")
    print(result_df.head().to_string())

# 使用示例
base_path = '/data/yuan/gastric_cancer/hla_estimation'
process_divergence_files(base_path)

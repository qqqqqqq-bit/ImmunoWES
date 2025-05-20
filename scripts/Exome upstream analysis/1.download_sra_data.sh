
#!/bin/bash

# 下载并重命名 SRP043661 项目中的胃癌样本数据（正常和癌组织）

# 设置工作目录（可根据需要修改）
WORKDIR="/data/yuan/gastric_cancer"
SRR_LIST="${WORKDIR}/SRR_Acc_List.txt"
SRA_TABLE="${WORKDIR}/SraRunTable.csv"
SRA_DIR="${WORKDIR}/0.sra"

# 创建存储目录
mkdir -p "${SRA_DIR}"

echo "Step 1: 多线程下载 SRA 格式原始数据..."
# 使用 prefetch 多线程下载（需要 NCBI SRA Toolkit 安装）
cat "${SRR_LIST}" | xargs -n 1 -P 16 -I {} prefetch {} -O "${SRA_DIR}"

echo "Step 2: 解析 SraRunTable.csv 获取重命名映射信息..."
# 提取 sra ID（第一列）和样本 ID（第 34 列），并重命名去掉 "_1"
grep "WXS" "${SRA_TABLE}" | cut -f 1 -d , > "${WORKDIR}/sra"
grep "WXS" "${SRA_TABLE}" | cut -f 34 -d , | sed 's/_1//' > "${WORKDIR}/config"

# 合并成两列，生成重命名对照表
paste "${WORKDIR}/sra" "${WORKDIR}/config" > "${WORKDIR}/sra2case.txt"

echo "Step 3: 重命名 SRA 文件..."
# 批量重命名
while read -r line; do
    arr=($line)
    sample=${arr[0]}
    case=${arr[1]}
    mv "${SRA_DIR}/${sample}/${sample}.sra" "${SRA_DIR}/${case}.sra"
done < "${WORKDIR}/sra2case.txt"

echo "Step 4: 删除多余的 SRR 文件夹..."
# 删除多余文件夹
find "${SRA_DIR}" -type d -name "SRR*" -exec rm -rf {} +

echo "Done. All SRA files have been renamed and cleaned."

#!/bin/bash

# 输入和输出路径
input_dir="/data/yuan/gastric_cancer/downstream_ukb/gastric_vcf"
output_dir="/data/yuan/gastric_cancer/downstream_ukb/gastric_vcf/filter"

# 创建输出目录
mkdir -p "$output_dir"

# 遍历所有 .hg38_multianno.vcf 文件
for vcf_file in "$input_dir"/*.hg38_multianno.vcf; do
    # 提取样本名称
    base_name=$(basename "$vcf_file" .hg38_multianno.vcf)
    output_file="$output_dir/${base_name}_filtered.vcf"

    echo "[INFO] Filtering ${base_name}..."

    # 筛选逻辑
    awk -F"\t" -v OFS="\t" '
    BEGIN {
        print "Chromosome", "Start", "End", "Ref", "Alt", "Genotype", "Qual", "Info";
    }
    {
        info_field = ($9 ~ /ExonicFunc.refGene/) ? 9 : 8;

        if ($1 ~ /^chr(X|Y|M)$/) next;  # 跳过性染色体和线粒体

        if ($info_field !~ /ExonicFunc.refGene=nonsynonymous_SNV/) next;

        split($info_field, info, ";");

        # 功能预测标志
        lrt_met = 0;
        sift_met = 0;
        mutation_assessor_met = 0;

        for (i in info) {
            if (info[i] ~ /^LRT_pred=/) {
                split(info[i], lrt, "=");
                if (lrt[2] == "D") lrt_met = 1;
            }
            if (info[i] ~ /^SIFT_pred=/) {
                split(info[i], sift, "=");
                if (sift[2] == "D") sift_met = 1;
            }
            if (info[i] ~ /^MutationAssessor_pred=/) {
                split(info[i], ma, "=");
                if (ma[2] == "H" || ma[2] == "M") mutation_assessor_met = 1;
            }
        }

        if (lrt_met || sift_met || mutation_assessor_met) {
            print $1, $2, $3, $4, $5, $10, $6, $info_field;
        }
    }
    ' "$vcf_file" > "$output_file"
done

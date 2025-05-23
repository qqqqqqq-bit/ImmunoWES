library(maftools)
options(stringsAsFactors = FALSE)

# 导入 MAF 数据
var.annovar.maf <- annovarToMaf(
  annovar = "data/all_sample.maf",
  refBuild = "hg38",
  tsbCol = "Tumor_Sample_Barcode1",
  table = "refGene",
  MAFobj = TRUE
)

laml <- var.annovar.maf
save(laml, file = "results/input_merge.Rdata")

# 突变总结图
png("results/plotmafSummary_merge.png", res = 150, width = 1080, height = 1080)
plotmafSummary(maf = laml, rmOutlier = TRUE, showBarcodes = TRUE,
               textSize = 0.4, addStat = "median", dashboard = TRUE)
dev.off()

# Top30基因突变图
png("results/oncoplot_top30_merge.png", res = 150, width = 1080, height = 1080)
oncoplot(maf = laml, top = 30, fontSize = 0.5, showTumorSampleBarcodes = TRUE)
dev.off()

# TP53变异图
png("results/TP53.png", res = 150, width = 1080, height = 1080)
lollipopPlot(laml, gene = "TP53", AACol = "AAChange.refGene", labelPos = "all")
dev.off()

# TMB 计算与图表
tmb1 <- tmb(maf = laml)
png("results/output.png")
plot(tmb1)
dev.off()

# TMB散点图
library(ggplot2)
png("results/total_perMB_scatterplot.png", width = 800, height = 600)
ggplot(tmb1, aes(x = Tumor_Sample_Barcode, y = total_perMB)) + 
  geom_point(color = "#69b3a2", size = 4) +
  theme_minimal() +
  ylab("Total Mutations per MB") +
  ggtitle("Total Mutations per MB in Tumor Samples") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        plot.title = element_text(hjust = 0.5))
dev.off()

# 保存数据
write.csv(tmb1, "results/tmb_results.csv", row.names = FALSE)

library(maftools)
options(stringsAsFactors = FALSE)

# Import MAF data
var.annovar.maf <- annovarToMaf(
  annovar = "data/all_sample.maf",
  refBuild = "hg38",
  tsbCol = "Tumor_Sample_Barcode1",
  table = "refGene",
  MAFobj = TRUE
)

laml <- var.annovar.maf
save(laml, file = "results/input_merge.Rdata")

# Mutation summary chart
png("results/plotmafSummary_merge.png", res = 150, width = 1080, height = 1080)
plotmafSummary(maf = laml, rmOutlier = TRUE, showBarcodes = TRUE,
               textSize = 0.4, addStat = "median", dashboard = TRUE)
dev.off()

# Top30 gene mutation map
png("results/oncoplot_top30_merge.png", res = 150, width = 1080, height = 1080)
oncoplot(maf = laml, top = 30, fontSize = 0.5, showTumorSampleBarcodes = TRUE)
dev.off()

# TP53 mutation diagram
png("results/TP53.png", res = 150, width = 1080, height = 1080)
lollipopPlot(laml, gene = "TP53", AACol = "AAChange.refGene", labelPos = "all")
dev.off()

# TMB calculations and charts
tmb1 <- tmb(maf = laml)
png("results/output.png")
plot(tmb1)
dev.off()

# TMB scatter plot
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

# Save data
write.csv(tmb1, "results/tmb_results.csv", row.names = FALSE)

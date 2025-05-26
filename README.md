# Intergration platform for Immunoassay using whole exome sequences 

## Overview
This repository provides a comprehensive analysis workflow that integrates whole-exome sequencing (WES) data with HLA genotyping information. The aim is to explore how somatic mutations interact with the human leukocyte antigen (HLA) system to influence immune-mediated disease progression and clinical outcomes.

Unlike traditional WES analyses that focus solely on mutation detection, our pipeline adds immunogenetic context by incorporating HLA class I and II alleles, mutation–HLA binding affinity prediction, HLA evolutionary divergence (HED) scoring, and survival analysis.

### Note: File paths in scripts are environment-specific. Please modify them according to your local server configuration.

## Workflow Structure
The project includes the following key modules:

### 1. Exome_upstream_analysis/
Performs quality control, alignment, duplicate removal, BQSR, and variant calling.

Outputs somatic variant VCF files.

Key tools: FastQC (v0.12.1), MultiQC (v1.19), BWA-MEM (v0.7.17), SAMtools (v1.9), Picard (v2.18.23), GATK (v4.0.4.0)

### 2. HLA_analysis/
HLA typing using HLA-HD (v1.7.0) from FASTQ files.

Extracts mutation-derived peptides.

Predicts binding affinities using MixMHC2pred for HLA-II alleles.

### 3. HLA_HED/
Calculates HLA evolutionary divergence (HED) scores.

Quantifies the sequence divergence between HLA alleles per individual.

### 4. Mutation_analysis/
Converts VCF to MAF format using Annovar + maftools.

Calculates tumor mutation burden (TMB).

Performs GO and KEGG pathway enrichment based on mutated genes.

### 5. cox/
Integrates mutation immunogenicity scores, binding affinities, and HED.

## Dataset
Project Accession: SRP043661

Publication: PMC4884975

## Abstract
Whole-exome sequencing (WES), owing to its efficiency in identifying mutations within protein-coding regions, has emerged as a powerful tool for elucidating the molecular mechanisms underlying immune-mediated diseases and related conditions. Nevertheless, most current studies primarily focus on the mutation profiling of WES data, often neglecting the potential influence of the human leukocyte antigen (HLA) system—a central component of immune regulation. The interaction between somatic mutations and HLA genotypes remains insufficiently characterized, limiting our understanding of immune-driven disease processes and clinical outcomes.

To refine this understanding, we propose a comprehensive integrative analytical framework that combines WES data with high-resolution HLA typing derived from raw FASTQ sequences. This pipeline includes upstream WES processing, somatic mutation detection, HLA genotyping, prediction of mutation–HLA binding affinity, assessment of HLA evolutionary divergence, and correlation with clinical prognosis. Kaplan–Meier survival analysis demonstrates that incorporating mutation–HLA binding affinity provides additional insights into immune-mediated disease progression and prognostic evaluation.

We anticipate that this framework will support researchers in identifying immune-related mutations that are potentially associated with immune-mediated disease outcomes.

## Dependencies
The pipeline requires the following software versions:

FastQC v0.12.1

MultiQC v1.19

BWA-MEM v0.7.17

SAMtools v1.9

Picard v2.18.23

GATK v4.0.4.0

HLA-HD v1.7.0

Annovar

maftools

clusterProfiler

MixMHC2pred

R 4.1+ with required packages (org.Hs.eg.db, enrichplot, etc.)

## Citation
If you use this workflow in your research, please cite:

Zhang et al., Integrative analysis of exome and HLA data reveals immune features associated with prognosis in gastric cancer. PMC4884975

## Contact
For questions or contributions, please contact:

Name: [Your Name]

Email: [your.email@example.com]

Institution: [Your Institution]

Performs Cox proportional hazards survival analysis to evaluate prognostic significance.

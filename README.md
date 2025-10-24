# PCORI_Meta_LLM
This repository provides the supplementary materials accompanying the study **“Large Language Model–Assisted Approach for Meta-Analysis and Systematic Review.”**
It includes scripts, prompt templates, and example datasets used to demonstrate the end-to-end workflow for automating key components of the evidence synthesis process—ranging from literature screening to manuscript generation and quality evaluation.

## Repository Overview
### 1. Codes and Prompts

`Title and abstract screening.Rmd` – R Markdown workflow for LLM-assisted title and abstract screening.
This directory contains the code and prompt templates used for different stages of the LLM-assisted workflow:

`Extracts_table.figures_langchain.py` – LangChain-based module for automated extraction of tables and figures from included manuscripts.
Extracts_text_langchain.py – LangChain-based module for extracting structured textual content (e.g., study characteristics, results).

`LLM-as-a-judge.Rmd` – R Markdown file implementing the LLM-as-a-Judge framework for quantitative and qualitative evaluation of generated manuscripts following PRISMA 2020 criteria.
Manuscript generating prompt.docx – Prompt template for guiding LLM-based manuscript drafting using retrieved and structured evidence.

### 2. Data

This directory includes sample datasets used to demonstrate and evaluate the workflow:

`All title and abstracts_Coreg and variceal bleeding.xlsx` – Dataset of retrieved records for the carvedilol and variceal bleeding meta-analysis.

`All titles and abstracts_PVT and anticoagulation.xlsx` – Dataset of retrieved records for the anticoagulation and portal vein thrombosis meta-analysis.

All datasets are provided solely for methodological illustration.

## Workflow Summary

The materials in this repository illustrate a modular framework integrating **large language models (LLMs)** and **retrieval-augmented generation (RAG)** for meta-analytic workflows:

### Automated Literature Screening:
LLM-based screening of titles and abstracts with validation against human review.

### Data and Text Extraction:
Structured extraction of study characteristics, tables, and figures using LangChain pipelines.

### Manuscript Generation:
LLM-driven drafting of meta-analysis manuscripts using curated prompts and structured inputs.

### Automated Evaluation:
Quality and completeness assessment through the LLM-as-a-Judge scoring framework.

# scRNA-seq Containerized Pipeline

## About
A single-cell RNA-seq pipeline using Docker and Docker Compose to run quality control, generate alignment metrics, and produce a final HTML report from FASTQ input data. 

This project simulates a reproducible bioinformatics workflow with isolated processing stages. The pipeline is divided into three stages, each depending on the previous one.

## Why This Project

Currently, the team's analysis workflows are often run manually on individual machines. This makes them difficult to reproduce, scale, and maintain consistently across different environments.

This project addresses those challenges by:

- Containerizing each pipeline stage using Docker
- Standardizing inputs and outputs through a shared data volume
- Producing both HTML reports (human-readable) and JSON outputs (machine-ingestable)

## Technologies Used

- Docker
- Docker Compose
- FastQC
- Python
    - Python 3.10
    - pandas
    - numpy
    - matplotlib (for report generation plots if extended)

All dependencies are fully containerized to ensure reproducibility.

## Data

This pipeline processes FASTQ files containing raw sequencing reads and produces structured outputs across multiple stages.

---

### Input Data

Input files are placed in:
  ```text
  data/input/
  ```

Public datasets can be downloaded from the NCBI SRA database for testing. For this project, a subset of data was used to reduce computational and memory requirements.


### Output Data 

The pipeline generates intermediate and final outputs:

#### QC Output
- Location: `data/qc_output/`
- Format: FastQC HTML report

#### Alignment Output
- Location: `data/alignment_output/`
- Format: metrics.json, run.log, BAM/BAI files

#### Final Report Output
- Location: `data/reports/`
- Format: HTML report, metrics.json

## Pipeline Architecture 
FASTQ Input
    ↓
QC Container (FastQC)
    ↓
QC HTML Output
    ↓
Alignment Container
    ↓
Metrics Generation
    ↓
Report Container
    ↓
Summary = HTML Report + JSON

Each stage runs in an isolated Docker container and communicates via a shared `/data` volume.

## Project Structure

scrna-pipeline/
│
├── qc/                                      # Quality Control container
│   └── Dockerfile                           # Builds QC Docker image
│
├── alignment/                               # Alignment container
│   ├── Dockerfile                           # Builds alignment Docker image
│   └── alignment.py                         # Mock alignment script with outputs + metrics
│
├── report/                                  # Report generation container
│   ├── Dockerfile                           # Builds report Docker image
│   └── report.py                            # Mock HTML + JSON summary reports
│
├── data/                                    # Shared volume mounted across containers
│   ├── input/                               # RAW sequencing input files
│   │   └── subset.fastq
│   │
│   ├── qc_output/                           # FastQC results
│   │   ├── subset_fastqc.html  
│   │   └── subset_fastqc.zip
│   │
│   ├── alignment_output/                    # Alignment outputs
│   │   └── SRR8387812/
│   │       ├── metrics.json
│   │       ├── run.log
│   │       ├── Aligned.out.sorted.bam
│   │       └── Aligned.out.sorted.bam.bai
│   │
│   └── reports/                             # Final generated reports
│       ├── SRR8387812_report.html
│       └── SRR8387812_metrics.json
│
├── docker-compose.yml                       # Runs multi-container applications
├── .env.example                             # Example environment configuration 
└── README.md                                # You are here


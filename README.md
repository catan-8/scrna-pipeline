# scRNA-seq Analysis Pipeline Project

## About
A single-cell RNA-seq pipeline using Docker and Docker Compose to run quality control, generate alignment metrics, and produce a final HTML report from FASTQ input data. 

The pipeline simulates a reproducible bioinformatics workflow with container-isolated stages that are executed in a defined dependency order.

## Why This Project

Currently, the team runs single-cell RNA-seq analyses manually on individual machines. This makes them difficult to reproduce, scale, and maintain consistently across different environments.

This project addresses those challenges by:

- Containerizing each pipeline stage using Docker
- Standardizing inputs and outputs through a shared data volume
- Ensuring reproducible execution across environments using Docker Compose

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

## Data Source

This pipeline processes publicly available FASTQ files containing raw single-cell RNA-seq reads downloaded from the NCBI Sequence Read Archive (SRA). For this project, a subset of data was used to reduce computational and memory requirements.

### Input Data

Input files are placed in:
  ```text
  data/input/
  ```

## Pipeline Architecture 
```text
FASTQ Input
    ↓
QC Container (FastQC)
    ↓
Alignment Container
    ↓
Report Container
    ↓
Final Summary = HTML Report + JSON
```

Each stage of the pipeline reads from and writes to a shared data volume. 

1. **QC Stage**
   - Input: FASTQ file
   - Purpose: Assess raw sequencing data quality

2. **Alignment Stage**
   - Input: FASTQ file
   - Purpose: Generate alignment statistics from sequencing reads

3. **Reporting Stage**
   - Input: QC and alignment outputs
   - Purpose: Aggregate results into a unified HTML report and JSON summary

## Project Structure

```text
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
```

## Getting Started

Prerequisites: 
```text
    - Docker Desktop installed
    - Docker Compose installed
```

### 1. Clone the Repository

```bash
git clone https://github.com/catan-8/scrna-pipeline.git
cd scrna-pipeline
```

### 2. Configure Environment Variables

Create a .env file in the project root using the template below:

```bash
cp .env.example .env
```

Example configuration:

```env
SAMPLE_NAME=dataset_id
FASTQ_FILE=/data/input/example.fastq

INPUT_DIR=/data/input
QC_DIR=/data/qc_output
OUTPUT_DIR=/data/alignment_output
ALIGN_DIR=/data/alignment_output
REPORT_DIR=/data/reports
```

### 3. Run the Pipeline

Build and execute the full workflow: 

```bash
docker compose up --build
```

This command will:
- build all Docker images
- run stages sequentially
- generate all outputs in the shared '/data' directory

## Expected Outputs

The pipeline generates outputs across three stages:

### QC Stage

**Output files:**
- `data/qc_output/subset_fastqc.html`

**Description:**
- FastQC HTML report summarizing raw sequencing read quality
- Provides basic QC validation of FASTQ input data

### Alignment Stage

**Output files:**
- `data/alignment_output/SRR8387812/metrics.json`
- `data/alignment_output/SRR8387812/run.log`

**Description:**
- Simulated alignment statistics (mapped reads, alignment rate, etc.)
- Execution logs for debugging and traceability

### Final Reporting Stage

**Output files:**
- `data/reports/SRR8387812_report.html`
- `data/reports/SRR8387812_metrics.json`

**Description:**
- Consolidated QC + alignment summary
- Final HTML report with key metrics and visualizations
- Structured JSON output designed for database ingestion

## Limitations

- This pipeline simulates alignment and QC steps rather than performing full-scale genome alignment (ex.Celranger).
- It is designed for workflow demonstration and orchestration purposes rather than production-scale genomic analysis.

## Security Considerations

- No hardcoded credentials are used; configuration is handled via environment variables.
- Sensitive data managed through `.env` files.
- Containers run with minimal required dependencies to reduce image surface area.

## Acknowledgements

- National Center for Biotechnology Information (NCBI) Sequence Read Archive (SRA) for dataset used in testing
- Docker documentation: https://docs.docker.com/
- OpenAI ChatGPT for assistance in structuring Docker Compose workflows and debugging configuration


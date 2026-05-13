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

FROM eclipse-temurin:17-jre

ARG FASTQC_VER=0.12.1

LABEL base.image="eclipse-temurin:17-jre"
LABEL software="FastQC"
LABEL dockerfile.stage="qc"
LABEL description="A quality control analysis stage for sequencing data"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    unzip \
    wget \
    perl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install FastQC
RUN wget https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v${FASTQC_VER}.zip && \
    unzip fastqc_v${FASTQC_VER}.zip && \
    rm fastqc_v${FASTQC_VER}.zip && \
    chmod +x FastQC/fastqc && \
    ln -s /FastQC/fastqc /usr/local/bin/fastqc

# Set working directory 
WORKDIR /data

# (sanity check)
CMD ["fastqc", "--help"]


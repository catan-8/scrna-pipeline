import os
import json


def get_config():
    sample = os.getenv("SAMPLE_NAME")
    fastq_file = os.getenv("FASTQ_FILE")
    output_dir = os.getenv("OUTPUT_DIR")

    # Validation check
    if not sample:
        raise ValueError("SAMPLE_NAME is not set")
    if not fastq_file:
        raise ValueError("FASTQ_FILE is not set")
    if not output_dir:
        raise ValueError("OUTPUT_DIR is not set")

    return sample, fastq_file, output_dir

def prepare_output(output_dir, sample):
    """
    Output directory for the sample is created.
    """
    path = os.path.join(output_dir, sample)
    os.makedirs(path, exist_ok=True)
    return path

def run_alignment(sample, fastq_file):
    """
    Simulates an alignment step for a sequencing sample with metrics produced. In a real pipeline, this function would run an alignment tool
    (e.g., Cell Ranger) on FASTQ files. 
    """
    print(f"[ALIGN] Running sample: {sample}")
    print(f"[ALIGN] Input: {fastq_file}")

    metrics = {
        "sample_id": sample,
        "total_reads": 1000,
        "mapped_reads": 850,
        "mapping_rate": 0.85,
        "estimated_cells": 500
    }

    return metrics


def save_results(out_path, metrics):
    """
    Saves alignment results to an output directory.
    Creates two files: 'metrics.json' and 'run.log'
    """
    metrics_path = os.path.join(out_path, "metrics.json")
    log_path = os.path.join(out_path, "run.log")

    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)

    with open(log_path, "w") as f:
        f.write("Alignment run complete\n")
        f.write(f"Sample: {metrics['sample_id']}\n")
        f.write(f"Reads: {metrics['total_reads']}\n")
        f.write(f"Mapped: {metrics['mapped_reads']}\n")
        f.write(f"Rate: {metrics['mapping_rate']}\n")

    print(f"[ALIGN] Done → {out_path}")


def main():
    sample, fastq_file, output_dir = get_config()
    out_path = prepare_output(output_dir, sample)
    metrics = run_alignment(sample, fastq_file)
    save_results(out_path, metrics)


if __name__ == "__main__":
    main()

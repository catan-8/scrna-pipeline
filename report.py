import os
import json
from datetime import datetime

def get_config():
    sample = os.getenv("SAMPLE_NAME")
    qc_dir = os.getenv("QC_DIR")
    align_dir = os.getenv("ALIGN_DIR")
    report_dir = os.getenv("REPORT_DIR")

    # Validation check
    if not sample:
        raise ValueError("SAMPLE_NAME is not set")
    if not qc_dir:
        raise ValueError("QC_DIR is not set")
    if not align_dir:
        raise ValueError("ALIGN_DIR is not set")
    if not report_dir:
        raise ValueError("REPORT_DIR is not set")
    return sample, qc_dir, align_dir, report_dir


def load_metrics(align_dir, sample):
    path = os.path.join(align_dir, sample, "metrics.json")
    
    if not os.path.exists(path):
        print(f"[WARN] metrics.json not found: {path}")
        return {}

    with open(path, "r") as f:
        return json.load(f)


def check_qc(qc_dir, sample):
    qc_file = "subset_fastqc.html"
    path = os.path.join(qc_dir, qc_file)

    if not os.path.exists(path):
        print(f"[WARN] QC file missing: {path}")
        return False

    return True

def check_bam_files(align_dir, sample):
    base = os.path.join(align_dir, sample)

    bam_file = os.path.join(base, "Aligned.out.sorted.bam")
    bai_file = os.path.join(base, "Aligned.out.sorted.bam.bai")

    return os.path.exists(bam_file), os.path.exists(bai_file)


def build_metrics_table(metrics):
    return f"""
    <table border="1" cellpadding="6">
        <tr><th>Metric</th><th>Value</th></tr>
        <tr><td>Total Reads</td><td>{metrics.get('total_reads')}</td></tr>
        <tr><td>Mapped Reads</td><td>{metrics.get('mapped_reads')}</td></tr>
        <tr><td>Alignment Rate</td><td>{metrics.get('alignment_rate')}</td></tr>
        <tr><td>Estimated Cells</td><td>{metrics.get('estimated_cells')}</td></tr>
    </table>
    """


def build_html(sample, metrics, qc_ok, bam_ok, bai_ok):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    table_html = build_metrics_table(metrics)

    html = f"""
    <html>
    <head>
        <title>{sample} scRNA-seq Pipeline Report</title>
    </head>

    <body>
        <h1>scRNA-seq Pipeline Report: {sample}</h1>

        <p><b>Generated:</b> {timestamp}</p>

        <h2>QC Summary</h2>
        <p>Status: {"PASS" if qc_ok else "MISSING"}</p>
        <p>FastQC report generated from subset FASTQ input.</p>

        <h2>Alignment Summary</h2>
        {table_html}

        <h2>BAM / BAI Files</h2>
        <ul>
            <li>BAM File: {"FOUND" if bam_ok else "MISSING"}</li>
            <li>BAI Index: {"FOUND" if bai_ok else "MISSING"}</li>
        </ul>

        <h2>IGV Visualization Notes</h2>
        <p>
            The BAM file contains reads aligned to a reference genome.
            The BAI index allows fast access to genomic regions in IGV.
        </p>

        <h2>Inputs Used</h2>
        <ul>
            <li>Subset FASTQ only (not full dataset)</li>
        </ul>

        <p><i>This report was generated automatically as part of a demonstration of a scRNA-seq pipeline structure.</i></p>
    </body>
    </html>
    """

    return html

def save_report(report_dir, sample, html):
    os.makedirs(report_dir, exist_ok=True)

    output_path = os.path.join(report_dir, f"{sample}_report.html")

    with open(output_path, "w") as f:
        f.write(html)

    print(f"[REPORT] saved → {output_path}")

def save_metrics_json(report_dir, sample, metrics):
    output_path = os.path.join(
        report_dir,
        f"{sample}_metrics.json"
    )

    with open(output_path, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"[REPORT] metrics saved → {output_path}")

def main():
    sample, qc_dir, align_dir, report_dir = get_config()

    qc_ok = check_qc(qc_dir, sample)

    bam_ok, bai_ok = check_bam_files(align_dir, sample)

    metrics = load_metrics(align_dir, sample)

    html = build_html(sample, metrics, qc_ok, bam_ok, bai_ok)

    save_report(report_dir, sample, html)

    save_metrics_json(report_dir, sample, metrics)


if __name__ == "__main__":
    main()

FROM python:3.10-slim

WORKDIR /app

COPY report.py .

# For generating plots and data handling
RUN pip install matplotlib pandas

# Report: final HTML from alignment and qc outputs
CMD ["python", "report.py"]


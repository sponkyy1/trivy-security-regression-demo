import json
import csv
import datetime
from collections import deque

# Config
HISTORY_CSV = "trivy-results/history.csv"
TRIVY_JSON = "result.json"
MAX_ROWS = 7

# Load Trivy result
with open(TRIVY_JSON, "r") as f:
    results = json.load(f)

# Count vulnerabilities by severity
counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
for result in results.get("Results", []):
    for vuln in result.get("Vulnerabilities", []):
        severity = vuln.get("Severity")
        if severity in counts:
            counts[severity] += 1

# Create new row with current timestamp
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
new_row = [timestamp, counts["CRITICAL"], counts["HIGH"], counts["MEDIUM"], counts["LOW"]]

# Load existing rows (if any)
rows = deque(maxlen=MAX_ROWS)
try:
    with open(HISTORY_CSV, newline="") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # skip header
        for row in reader:
            rows.append(row)
except FileNotFoundError:
    header = ["timestamp", "CRITICAL", "HIGH", "MEDIUM", "LOW"]

# Append new row
rows.append(new_row)

# Write back only latest 7 rows
with open(HISTORY_CSV, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(rows)

print(f"Saved scan summary to {HISTORY_CSV}")

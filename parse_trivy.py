import json
import csv
import datetime
from collections import deque
from pathlib import Path

TRIVY_JSON = Path("trivy-results/result.json")
HISTORY_CSV = Path("trivy-results/history.csv")
MAX_ROWS = 7

# Завантаження Trivy-результату
with TRIVY_JSON.open() as f:
    results = json.load(f)

# Підрахунок кількості уразливостей за рівнями
counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
for result in results.get("Results", []):
    for vuln in result.get("Vulnerabilities", []):
        severity = vuln.get("Severity")
        if severity in counts:
            counts[severity] += 1

# Створення нового рядка
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
new_row = [timestamp, counts["CRITICAL"], counts["HIGH"], counts["MEDIUM"], counts["LOW"]]

# Читання наявної історії (якщо є)
rows = deque(maxlen=MAX_ROWS)
if HISTORY_CSV.exists():
    with HISTORY_CSV.open() as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append(row)
else:
    header = ["timestamp", "CRITICAL", "HIGH", "MEDIUM", "LOW"]

# Додавання нового скану
rows.append(new_row)

# Запис оновленого CSV
with HISTORY_CSV.open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f"✅ Updated {HISTORY_CSV} with latest scan, keeping {MAX_ROWS} entries.")

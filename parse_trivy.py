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

# Читання CSV з обробкою порожнього файлу
rows = deque(maxlen=MAX_ROWS)
header = ["timestamp", "CRITICAL", "HIGH", "MEDIUM", "LOW"]

if HISTORY_CSV.exists() and HISTORY_CSV.stat().st_size > 0:
    with HISTORY_CSV.open() as f:
        reader = csv.reader(f)
        try:
            next(reader)  # header
        except StopIteration:
            pass  # файл існує, але порожній
        else:
            for row in reader:
                rows.append(row)

# Додати новий скан
rows.append(new_row)

# Запис у файл
with HISTORY_CSV.open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f"✅ Updated {HISTORY_CSV} with latest scan, keeping {MAX_ROWS} entries.")
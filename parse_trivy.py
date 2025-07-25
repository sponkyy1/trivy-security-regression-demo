import json
import csv
import os
from datetime import datetime

# Вхідний Trivy JSON-файл
INPUT_PATH = 'trivy-results/result.json'
OUTPUT_CSV = 'trivy-results/history.csv'

# Ініціалізація лічильника уразливостей
severity_levels = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
severity_count = {level: 0 for level in severity_levels}

# Читання Trivy JSON-звіту
with open(INPUT_PATH, 'r') as f:
    report = json.load(f)

# Збір кількості уразливостей
for result in report.get('Results', []):
    for vuln in result.get('Vulnerabilities', []):
        severity = vuln.get('Severity', '').upper()
        if severity in severity_count:
            severity_count[severity] += 1

# Створення нового рядка
timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
row = [timestamp] + [severity_count[level] for level in severity_levels]

# Перевірка, чи існує CSV — якщо ні, створити з заголовком
file_exists = os.path.isfile(OUTPUT_CSV)
with open(OUTPUT_CSV, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    if not file_exists:
        writer.writerow(['timestamp'] + severity_levels)
    writer.writerow(row)

print(f"✅ Saved scan summary to {OUTPUT_CSV}")

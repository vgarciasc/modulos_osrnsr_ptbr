import csv
from datetime import datetime

import requests
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# === CONFIGURATION ===

# Public CSV link of the Google Spreadsheet (replace with yours)
GOOGLE_SHEET_CSV_URL = 'https://docs.google.com/spreadsheets/d/1ruM9q3xfhkk6-MTBwWixGQdQQS_mQgUmA5oxMYqE4Cc/export?format=csv'

# Output paths
OUTPUT_HTML = Path("index.html")
TEMP_CSV = Path("data.csv")
TEMPLATES_DIR = Path("templates")
TEMPLATE_FILE = "page.html"

# === DOWNLOAD CSV ===

def download_csv(url, output_path):
    print(f"Downloading CSV from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    output_path.write_bytes(response.content)
    print(f"Saved CSV to {output_path}")

# === PARSE CSV ===

def parse_csv(csv_path):
    print(f"Parsing CSV {csv_path}...")
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        entries = list(reader)
    print(f"Parsed {len(entries)} entries.")
    return entries

# === GENERATE HTML WITH JINJA2 ===

def generate_html(entries):
    print(f"Generating HTML with Jinja2...")
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template(TEMPLATE_FILE)

    # Prepare modulesData for JS
    modules_data = []
    for entry in entries:
        modules_data.append({
            "title": entry.get('Título', ''),
            "sistema": entry.get('Sistema', ''),
            "autoria": entry.get('Autoria', ''),
            "tipo": entry.get('Tipo', ''),
        })

    today = datetime.today().strftime('%d/%m/%Y')

    html_content = template.render(
        entries=entries,
        modules_data=modules_data,
        last_update=today
    )
    return html_content


# === MAIN ===

def main():
    download_csv(GOOGLE_SHEET_CSV_URL, TEMP_CSV)
    entries = parse_csv(TEMP_CSV)
    html_content = generate_html(entries)
    OUTPUT_HTML.write_text(html_content, encoding='utf-8')
    print(f"Wrote HTML page to {OUTPUT_HTML}")

if __name__ == "__main__":
    main()

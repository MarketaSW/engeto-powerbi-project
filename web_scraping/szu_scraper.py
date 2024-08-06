"""szu_scraper.py
Run this script with arguments e.g.:
python3 szu_scraper.py "url address" "output" 
"""

import pymupdf
import requests
import csv
import argparse
from bs4 import BeautifulSoup
from pathlib import Path

def get_pdf_links(url) -> list:
    """Return list with all pdf links from the second column of the table.
    Parameters:
    - url: given url address"""

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    pdf_links = []
    rows = soup.find_all('tr')
    for row in rows:
        tds = row.find_all('td')
        if len(tds) > 1:
            second_td = tds[1]
            links = second_td.find_all('a', href=True)
            for link in links:
                href = link['href']
                if href.lower().endswith('.pdf'):
                    if href.startswith('/'):
                        base_url = url.split('//')[1].split('/')[0]
                        absolute_url = f'https://{base_url}{href}'
                    else:
                        absolute_url = href
                    pdf_links.append(absolute_url)
    
    return pdf_links

def download_pdfs(pdf_links):
    """
    Download PDF files from the given list of links and save them to the specified folder.

    Parameters:
    - pdf_links: List of PDF URLs to download.
    - download_folder: Path to the folder where the PDFs should be saved.

    Returns:
    - List of paths to the downloaded PDF files.
    """
    download_folder = Path('./temp_pdfs')
    if not download_folder.exists():
        download_folder.mkdir(parents=True)

    pdf_files = []
    for link in pdf_links:
        pdf_name = download_folder / link.split('/')[-1]
        response = requests.get(link)
        with pdf_name.open('wb') as pdf_file:
            pdf_file.write(response.content)
        pdf_files.append(pdf_name)
    
    return pdf_files

def extract_data_from_pdf(pdf_files) -> list:
    """Extract tables from PDF files.
    Parameters: 
    - pdf_files: a list of pdf_files for extraction """

    tables = []
    for pdf_file in pdf_files:
        doc = pymupdf.open(pdf_file)
        first_page = doc[0]
        tables_found = first_page.find_tables()
        for tab in tables_found:
            table_data = tab.extract()
            if table_data:
                tables.extend(table_data)
    return tables    

def format_table(tables) -> list:
    """Add blank cells to ensure all rows have the same number of columns."""
    
    all_rows = [row for table in tables for row in table]
    max_columns = max(len(row) for row in all_rows if row is not None)
    
    aligned_rows = []
    for row in all_rows:
        if row is None:
            aligned_rows.append([None] * max_columns)
        else:
            aligned_rows.append(row + [None] * (max_columns - len(row)))
    
    return aligned_rows

def write_to_csv(aligned_rows, output_file):
    
    path = Path(output_file)
    with path.open('w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for row in tables:
            if row is not None:
                cleaned_row = [cell if cell is not None else '' for cell in row]
                writer.writerow(cleaned_row)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str, help="url address")
    parser.add_argument("output_file", type=str, help="output CSV file name")
    args = parser.parse_args()

    print(f"Downloading data from URL: {args.url}")
    pdf_links = get_pdf_links(args.url)
    pdf_files = download_pdfs(pdf_links)

    print("Extracting data from pdfs...")
    tables = extract_data_from_pdf(pdf_files)

    print(f"Saving to file: {args.output_file}")
    write_to_csv(tables, args.output_file)

    print("Done!")

if __name__ == "__main__":
    main()    

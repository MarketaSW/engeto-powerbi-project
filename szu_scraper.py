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
            table_data = [tab.extract()]
            if table_data:
                tables.extend(table_data)
    return tables    

def extend_rows(tables) -> list:
    """Add blank cells to specific rows to format table."""
    initial_rows_to_extend = [1, 2, 4, 5]
    rows_to_extend = initial_rows_to_extend.copy()

    for table in tables:
        while rows_to_extend[-1] < len(table):
            if i in rows_to_extend:
                for i in rows_to_extend:
                    table[i].insert(0, None)
                    rows_to_extend = [i + 6 for i in initial_rows_to_extend]
            else: continue    
    
    return tables 

def write_to_csv(tables, output_file):
    
    path = Path(output_file)
    with path.open('w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for row in tables:
            if row is not None:
                writer.writerow(row)

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

    print("Formatting table...")
    # formatted_tables = extend_rows(tables)

    print(f"Saving to file: {args.output_file}")
    write_to_csv(tables, args.output_file)

    print("Done!")

if __name__ == "__main__":
    main()    

#python3 szu_scraper.py "https://szu.cz/temata-zdravi-a-bezpecnosti/a-z-infekce/ch/chripka/zprava-o-chripkove-aktivite-hlaseni-a-vysledky-laboratornich-vysetreni/vyskyt-akutnich-respiracnich-infekci-a-chripky-v-cr-sezona-2022-2023/" "output_file.csv"
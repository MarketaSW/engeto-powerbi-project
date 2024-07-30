
import requests
import csv
import argparse
from bs4 import BeautifulSoup as bs
from pathlib import Path
import sys

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
                    pdf_links.append(href)
    
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

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

def download_pdfs(pdf_links) -> list:
    """Download pdfs into created folder.
    Parameters:
    - pdf_links: a list of links to pdf files"""




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
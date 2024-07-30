import sys
import requests
import csv
import argparse
from bs4 import BeautifulSoup as bs
from pathlib import Path

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
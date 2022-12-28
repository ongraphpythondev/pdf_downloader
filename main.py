import os
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# SET LOCATION OF THE DIRECTORY TO STORE DOWNLOADED PDF
base_location = ""
directory_name = "downloaded_pdf"
file_location = base_location + directory_name

# CREATE THE DOWNLOAD DIRECTORY IF NOT PRESENT
if not os.path.exists(file_location):
    os.mkdir(file_location)

# LOAD THE CSV FILE WITH SCRAPPING URLS TO READ IT
file = open('list_of_url.csv', 'r')
csvFile = csv.reader(file)


# READ THE CSV FILE AND PROCESS IT
for line in csvFile:
    url = line[0]
    print("Processing URL: " + url)

    response = requests.get(url)
    if response.status_code != 200:
        print("ERROR: Processing URL FAILED with STATUS Code:", response.status_code)
    
    soup = BeautifulSoup(response.text, "html.parser")

    downloaded_pdf_file_names = os.listdir(file_location)
    all_pdfs = soup.select('a[href$=".pdf"]')

    print("All PDF Count:", len(all_pdfs))
    print("New PDF Count:", len(all_pdfs) - len(downloaded_pdf_file_names))

    # ITERATE OVER ALL PDFs
    for link in all_pdfs:
        filename = link['href'].split('/')[-1]

        if filename in downloaded_pdf_file_names:
            continue

        filepath = os.path.join(file_location, filename)
        
        # DOWNLOADING THE PDFs
        with open(filepath,'wb') as f:
            f.write(requests.get(urljoin(url, link.get('href'))).content)
        
        print("File", filepath, "downloaded")

file.close()
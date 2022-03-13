"""
Script for Data Scraping and Reformating from GeneLab API

Neeka Sewnath
nsewnath@ufl.edu

# Note: Must be run with Python 3.x
# Need to install fsspec dependency 
# For Mac OS, needed to navigate to Macintosh HD > Applications > Python3.x folder 
#   > double click on "Install Certificates.command" file
"""

#===========================================================================================================================================

#from webdriver_manager.chrome import ChromeDriverManager
#from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import argparse
import json
import re
import urllib

#===========================================================================================================================================

def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='API data scrape and reformat',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-u',
                        '--url',
                        help = 'url of data',
                        metavar = 'url',
                        type = str,
                        default = "https://visualization.genelab.nasa.gov/GLOpenAPI/samples/?study.characteristics.organism=Arabidopsis%20thaliana&file.datatype=unnormalized%20counts&format=browser")

    return parser.parse_args()

#===========================================================================================================================================

def main():

    # Fetch arguments 
    args = get_args()
    url = args.url

    """
    Research Notes

    I think this isn't looking right because the way I'm trying to scrap the href is wrong. W
    Here's what the actual link to the data looks like 
    <a class="file" href="https://visualization.genelab.nasa.gov/GLOpenAPI/data/?study.characteristics.organism=Arabidopsis thaliana&amp;file.datatype=unnormalized counts&amp;file.filename=GLDS-37_rna_seq_Unnormalized_Counts.csv&amp;format=raw">GLDS-37_rna_seq_Unnormalized_Counts.csv</a>
    
    So in that html line above, this is the url: 
    https://visualization.genelab.nasa.gov/GLOpenAPI/data/?study.characteristics.organism=Arabidopsis thaliana&amp;file.datatype=unnormalized counts&amp;file.filename=GLDS-37_rna_seq_Unnormalized_Counts.csv&amp;format=raw

    Here is the url I'm trying to store 
    https://visualization.genelab.nasa.gov/GLOpenAPI/samples/?study.characteristics.organism=Arabidopsis%20thaliana&file.datatype=unnormalized%20counts&format=csv

    I don't completely understand, but it looks as if these urls are being created dynamically based on the ID so I can't
    just scrape it out. 
    
    Here is line 160 of source code that shows it being dynamically created:

    "<a class='file' href='https://visualization.genelab.nasa.gov/GLOpenAPI/data/?study.characteristics.organism=Arabidopsis thaliana&file.datatype=unnormalized counts&file.filename="+escape(v)+"&format=raw'>"+v+"</a>";};

    Actually, I don't think it could also be dynamic because when you inspect element the url is there
    ready to go. I think that the link might be dynmaically created when opened?

    There is a hacky fix to this with just rebuilding each link with column names but there must be a better way that
    doesn't involve any hardcoding. 

    """

    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    urls = []

    # This one doesn't find anything 
    # for link in soup.find_all("a", {"class": "file"}):
    #     print(link)
    #     urls.append(link.get('href'))

    # urls = []

    # for link in soup.find_all('a'):
    #     print(link)
    #     urls.append(link.get('href'))

    # # Get rid of weird Nonetype
    # urls.pop(0)

    # # add url spaces to base urls
    # urls = [i.replace(" ", "%20") for i in urls]

    # print(urls)

    #TODO: Unfortunately the code below is pulling the wrong links 

    # for link in soup.find_all('a'):
    #     urls.append(link.get('href'))

    # # Get rid of weird Nonetype
    # urls.pop(0)

    # # add url spaces to base urls
    # urls = [i.replace(" ", "%20") for i in urls]

    # print(urls[7])

    # # Isolate and add quotes to the csv links
    # csv_urls = [i for i in urls if "csv" in i] 
    # csv_urls = ['"' + i + '"' for i in csv_urls]

    # add url spaces to base urls
    # csv_urls = [i.replace(" ", "%20") for i in csv_urls]

    # WIP: Create dataset list and populate it with uploaded datasets

#===========================================================================================================================================

if __name__ == '__main__':
    main()
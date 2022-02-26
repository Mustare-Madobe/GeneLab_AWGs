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

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import argparse
import json
import re

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

    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    urls = []

    for link in soup.find_all('a'):
        urls.append(link.get('href'))

    # Get rid of weird Nonetype
    urls.pop(0)

    # Isolate and add quotes to the csv links
    csv_urls = [i for i in urls if "csv" in i] 
    csv_urls = ['"' + i + '"' for i in csv_urls]

    # WIP: Create dataset list and populate it with uploaded datasets
    # TODO: figure out weird http issue that arises from making data list
    data_list = []
    for i in csv_urls:
        api_data = pd.read_csv(i)
        data_list.append(api_data)

    # test_data = pd.read_csv("https://visualization.genelab.nasa.gov/GLOpenAPI/samples/?study.characteristics.organism=Arabidopsis thaliana&file.datatype=unnormalized counts&format=csv")
    # print(test_data)

#===========================================================================================================================================

if __name__ == '__main__':
    main()
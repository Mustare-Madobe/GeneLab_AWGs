"""
Script for Data Scraping and Reformating from GeneLab API

Neeka Sewnath
nsewnath@ufl.edu

# Note: Must be run with Python 3.x
# Need to install lxml (pip install lxml)
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

    # Isolate the csv links
    csv_urls = [i for i in urls if "csv" in i] 

    # I think this is correct, just need to confirm that there is a lot of 
    # repetitive urls for the csv files 

    # WIP: Create dataset list
    dataset_dictionary = [] 
    i = 1
    for i in csv_urls:
        df_name = "dataset_" + str(i)
        df = pd.read_csv(csv_url)


#===========================================================================================================================================

if __name__ == '__main__':
    main()
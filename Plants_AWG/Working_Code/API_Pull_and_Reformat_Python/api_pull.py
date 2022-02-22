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

    # Fetch raw html content
    html_content = requests.get(url).text

    # Parse html content
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract csv list from soup
    script = soup.find_all("script")
    script = str(script)
    pattern = re.compile('var data = (.*?);')
    matrix_string = pattern.search(script).group(1)
    matrix_list = matrix_string.split(",")
    matrix_list = [i[:-1] for i in matrix_list if "csv" in i]
    csv_list = [i[:-1] if "]" in i else i for i in matrix_list]

    new_csv_list = [i.strip("") for i in csv_list]

    # TODO: remove quotes
    for i in new_csv_list:
        print(i)

    # TODO use driver to click each link
    # hopefully we can store those new links in a new array 
    # and then essentially open each link with pandas 

    # The goal here is to just get the url associated with each click and add to a list

    # Set up driver for link clicks
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver.get(url)

    # for i in csv_list: 
    #     element = driver.find_element_by_link_text(i)
    #     element.click()



#===========================================================================================================================================

if __name__ == '__main__':
    main()
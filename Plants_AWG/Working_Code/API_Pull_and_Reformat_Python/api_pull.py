"""
Script for Data Scraping and Reformating from GeneLab API

Neeka Sewnath
nsewnath@ufl.edu

# Note: Must be run with Python 3.x
# Need to install fsspec dependency 
# For Mac OS, needed to navigate to Macintosh HD > Applications > Python3.x folder 
#   > double click on "Install Certificates.command" file

# Note: install chromedriver and set executable path 
"""

#===========================================================================================================================================

import requests
import argparse
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.remote.webelement import webelement
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium_move_cursor.MouseActions import move_to_element_chrome
# from selenium.webdriver.common.keys import keys
from selenium.webdriver.chrome.options import Options
# import js
# import json 
# import numpy as np
# import time
# import pandas as pd
# from bs4 import BeautifulSoup
# import ctypes 

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

    I think this isn't looking right because the way I'm trying to scrape the href is wrong. W
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

    opts = Options()
    opts.add_argument('- headless')
    driver = webdriver.Chrome('./chromedriver', options = opts)

    driver.maximize_window()
    driver.get(url)
    driver.implicitly_wait(220)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    
    file_ws_results = driver.find_elements_by_xpath("//a[contains(@class,'file')]")
    total_ws_results=len(file_ws_results)

    csv_urls = set()
    for i in  range(0,len(file_ws_results)):
        csv = file_ws_results[i]
        try:
            csv.click()
            time.sleep(2)
            actual_csv = driver.find_elements_by_css_selector('file')
            for actual_csv in actual_csv:
                if actual_csv.get_attribute('src') and 'https' in actual_csv.get_attribute('src'):
                    csv_urls.add(actual_csv.get_attribute('src'))
        except ElementClickInterceptedException or ElementNotInteractableException as err:
            print(err)



    # reqs = requests.get(url)
    # soup = BeautifulSoup(reqs.text, 'html.parser')

    # urls = []


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
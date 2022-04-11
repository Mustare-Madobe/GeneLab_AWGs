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

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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
    #install driver NOTE: sometimes takes a while
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    #load url using driver: 
    driver.get(url)

    # get element 
    element = driver.find_elements_by_xpath("//a[contains(@class,'file')]")
    driver.quit()

    # get html inside attribute
    all_htmls = []
    [all_htmls.append(i.get_attribute("innerHTML")) for i in element]
    #NOTE: ^ this code raises MaxRetryError ^


#===========================================================================================================================================

if __name__ == '__main__':
    main()
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
import requests
import argparse


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

    # Set up driver for link clicks
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver.get(url)

    # Parse html content
    soup = BeautifulSoup(html_content, "html.parser")
    print(soup)
    
    # TODO take that dataframe in soup, get a list of all the 
    # csv file names, and then use driver to click each link
    # hopefully we can store those new links in a new array 
    # and then essentially open each link with pandas 

    # TODO: Extract data frame from soup
    table = soup.find_all('var_data', attrs={})
    print(table)


    #for i in csv_array
    #    csv_link = driver.find_element_by_link_text(csv_names)
    #    csv_address = csv_link.click()
        # store the csv address

    

  


#===========================================================================================================================================

if __name__ == '__main__':
    main()
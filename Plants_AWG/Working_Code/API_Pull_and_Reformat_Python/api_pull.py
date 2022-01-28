"""
Script for Data Scraping and Reformating from GeneLab API

Neeka Sewnath
nsewnath@ufl.edu

# Note: Must be run with Python 3.x
"""

#===========================================================================================================================================

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

    # Parse html content
    soup = BeautifulSoup(html_content, "lxml")


#===========================================================================================================================================

if __name__ == '__main__':
    main()
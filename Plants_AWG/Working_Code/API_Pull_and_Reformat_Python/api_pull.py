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

import requests
import argparse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from functools import reduce
import time

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

    # this isolates the table, but it's not really useful for what we want
    # data = driver.execute_script('return data')


    # scroll down
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    """

    Research Notes: 

    Sadly I don't think the scroll down method above will work for us since we are scrolling within a table 
    within the webpage. The code above tries to scroll through the entire webpage, which doesn't change anything.

    So it should be sort of straight forward, I'm guessing the class is literally just "table", looking at 
    the page html we see this: 

    "var data = [["GLDS-120","gse94983_transcription_profiling_RNA_Sequencing_(RNA-Seq)"...."

    I'm pretty sure we can just try to scroll through that element using the info above. 

    How do we scroll through a javascript element with selenium?

    """


    element = driver.find_element_by_id("data")

    element.send_keys(Keys.PAGE_DOWN)

    # from selenium.webdriver.common.action_chains import ActionChains

    # element = driver.find_element_by_id("grid")

    # driver.execute_script("arguments[0].scrollIntoView();", element)


    #n_element = driver.findElement(By.id("id_of_element"))
    
    # driver.find_element('data')
    
    # ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView(true);", element)
    # Thread.sleep(500); 

    # element = driver.find_element_by_xpath("//a[contains('data')]")
    # for i in range(60):
    # driver.execute_script("arguments[0].scrollBy(0, 500)", element)
    # time.sleep(2)

    #data = driver.find_element_by_id("body")

    #data = driver.execute_script('return data')

    #driver.execute_script("document.getElementById('data').scrollIntoView();")

    # locate table window 
    #ele_table = driver.find_elements_by_xpath("//div[@class='ui-widget-content']")

    #driver.execute_script("document.getElementById('ele_table').scrollIntoView();")

    # scroll down table window
    
    #driver.execute_script("scrollBy(0, 1080)", ele_table)


    #TODO: figure out how to locate table var with driver, scroll down with driver, then get elements with driver

   # grid = driver.execute_script('return grid')

   # driver.execute_script("document.getElementById('grid').scrollIntoView();")

    # grid = driver.execute_script('return ui-widget-content')

    # driver.execute_script("document.getElementById('grid').scrollIntoView();")

    # get element 
    element = driver.find_elements_by_xpath("//a[contains(@class,'file')]")

    # get html inside attribute
    all_htmls = []

    for i in element: 
        x = i.get_attribute("href")
        all_htmls.append(x)

    # get unique urls 
    unq_urls = reduce(lambda l, x: l.append(x) or l if x not in l else l, all_htmls, [])

#===========================================================================================================================================

if __name__ == '__main__':
    main()
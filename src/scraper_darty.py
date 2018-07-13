# coding: utf-8

from selenium import webdriver
import pandas as pd
import os
import unicodedata


def create_dir(name):
    #create a folder if it doesn't exist
    if not os.path.isdir(name):
        os.makedirs(name)

def clean_str(string):
    
    #get rid of bad characters
    return unicodedata.normalize("NFKD", string).encode("latin-1", "ignore").decode("latin-1")

def clean_str_series(series):
    
    #apply clean_str on a series
    series = series.apply(clean_str)
   
    return series


def get_addresses(url, browser):
    """Get names, address and postal codes"""
    
    browser.get(url)
   
    name_selector = "div.components-outlet-item-search-result-default__address h2"
    address_selector = "div.components-outlet-item-address-basic__line"
    
    names = browser.find_elements_by_css_selector(name_selector)
    addresses = browser.find_elements_by_css_selector(address_selector)

    name_list = [name.text for name in names]
    address_list = [address.text for address in addresses]
    
    street_list = address_list[::2]
    cp_list = address_list[1::2]
    
    del address_list
    
    return name_list, street_list, cp_list


def scraper_darty():
    
    #configure the browser
    browser =  webdriver.Firefox()
    
    url = 'https://magasin.darty.com/fr?page={}'
    
    #get names, address and postal codes for all pages
    lists = [lst for page in range(1, 19) for lst in get_addresses(url.format(page), browser)]
    
    names = [name for lst in lists[::3] for name in lst]
    streets = [street for lst in lists[1::3] for street in lst]
    cp = [cp for lst in lists[2::3] for cp in lst]
    
    browser.quit()
    
    #create a csv file
    df = pd.DataFrame({'nom' : names, 'adresse' : streets, 'code postal' : cp})
    add = [ad.split('\n', 1)[0] for ad in df['adresse']]
    df['adresse'] = add
    create_dir("../data")
    df = df.apply(clean_str_series)
    df.to_csv("../data/scraping_darty.csv", index = False, sep = ';')


scraper_darty()

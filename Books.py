from utils import getNYTUrl, getUserAgent
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs
from datetime import datetime
from pprint import pprint
import pandas as pd
import requests
import json
import yaml
import ast


apiUrl = getNYTUrl(context_='BOOKS_CONTEXT')

data = requests.get(apiUrl).text
data = json.loads(data)

best_sellers_history = []

for index in range(0,len(data['results']['lists'])):
    for book in range(0,len(data['results']['lists'][index]['books'])):
        title = data['results']['lists'][index]['books'][book]['author']
        author = data['results']['lists'][index]['books'][book]['author']
        created_date = data['results']['lists'][index]['books'][book]['created_date']
        description = data['results']['lists'][index]['books'][book]['description']
        primary_isbn10 = data['results']['lists'][index]['books'][book]['primary_isbn10']
        updated_date = data['results']['lists'][index]['books'][book]['updated_date']
        contributor = data['results']['lists'][index]['books'][book]['contributor']
        publisher = data['results']['lists'][index]['books'][book]['publisher']
        rank = data['results']['lists'][index]['books'][book]['rank']
        amazon_product_url = data['results']['lists'][index]['books'][book]['amazon_product_url']


        dictionnaire = {'title': title,
                        'author': author,
                        'created_date':created_date,
                        'description' :description,
                        'primary_isbn10' : primary_isbn10,
                        'updated_date' : updated_date,
                        'contributor' : contributor,
                        'publisher' : publisher,
                        'rank' : rank,
                        'amazon_product_url' : amazon_product_url
                    }
        best_sellers_history.append(dictionnaire)

#pprint(best_sellers_history[0:2])      

#Obtaining amazon_urls from best_sellers_history to do web scraping in order to get the prices of the books that are associated with each URL

for url in range(0,len(best_sellers_history)):
    amazon_product_url = best_sellers_history[url]['amazon_product_url']
    #pprint(amazon_product_url)
    req = Request(amazon_product_url, headers=ast.literal_eval("{'User-Agent': 'Mozilla/5.0'}"))
    page = urlopen(req)
    soup = bs(page, 'html.parser')
    #print(soup) 
    print(soup.find('span',{'class':'a-size-base a-color-price a-color-price'}).get_text(strip=True))

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H%M%S")

filename = "./output/" + dt_string + "_books.json" 
with open(filename, "w") as jsonFile:
    json.dump(data, jsonFile)
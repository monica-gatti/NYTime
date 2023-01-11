import json
from urllib.request import urlopen, Request
from utils import logActivity, getNYTUrl,  getStringCurrentDate, ingestForES
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import ast
import sqlite3 
import logging
import yaml
from time import sleep

logActivity(getStringCurrentDate() + "_logBookPrice.log")

BOOKS_CONTEXT = getNYTUrl(context_="BOOKS_CONTEXT")
data = requests.get(BOOKS_CONTEXT).text
data = json.loads(data)

for index in range(0,len(data['results']['lists'])):
    con = sqlite3.connect('books.db')
    cur = con.cursor()
    for book in range(0,len(data['results']['lists'][index]['books'])):
        
        url = data['results']['lists'][index]['books'][book]['amazon_product_url']
        try:
            req = Request(url, headers=ast.literal_eval("{'User-Agent':'Mozilla/5.0'}"))
            page = urlopen(req)
            soup = bs(page, 'html.parser')  
            price = soup.find('span',{'class':'a-size-base a-color-price a-color-price'})
            if price:
                price = price.get_text(strip=True).replace('$', '')
            else:
                price = "None"
            cur.execute("INSERT INTO book_prices(url,price) VALUES(?, ?)", (url, price))
            con.commit()
            sleep(10)
        except  sqlite3.IntegrityError as err:
            print(f"Integritya error {err=}, {type(err)=}")
          
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
    con.close()
        
    filename = "./output/" + getStringCurrentDate() + "_book_prices.json" 
    with open(filename, "w") as jsonFile:
        json.dump(data, jsonFile)    
      
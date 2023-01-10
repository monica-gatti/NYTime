
import json
from urllib.request import urlopen, Request
from utils import getNYTUrl,  getStringCurrentDate, ingestBooksEs
import requests
from pprint import pprint
import ast
import sqlite3 
import logging

logging.basicConfig(filename="./output/logBooks.log", level=logging.INFO)

BOOKS_CONTEXT = getNYTUrl(context_="BOOKS_CONTEXT")
data = requests.get(BOOKS_CONTEXT).text
data = json.loads(data)

for lists in data['results']['lists']:
    for book in lists['books']:
        con = sqlite3.connect('books.db')
        cur = con.cursor()
        try:  
            cur.execute("INSERT INTO books_full_overview VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
            (book['title'], book['author'], book['contributor'], book['publisher'], book['rank'], book['primary_isbn10'], book['primary_isbn13'],book['updated_date'], book['created_date'],book['amazon_product_url']))
            con.commit()     
        except  sqlite3.IntegrityError as err:
            print(f"Integritya error {err=}, {type(err)=}")
        try:
            ingestBooksEs(book['title'], book['author'], book['rank'],book['description'], )
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
    con.close()
        
    filename = "./output/" + getStringCurrentDate() + "_books_full_overview.json" 
    with open(filename, "w") as jsonFile:
        json.dump(data, jsonFile)    
        
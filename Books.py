import json
import requests
from pprint import pprint
import yaml
from utils import getNYTUrl, getUserAgent
from datetime import datetime

apiUrl = getNYTUrl(context_="BOOKS_CONTEXT")

data = requests.get(apiUrl).text
data = json.loads(data)

list_books = []

for index in range(0,len(data['results']['books'])):
    title = (data['results']['books'][index]['title'])
    author=(data['results']['books'][index]['author'])
    rank=(data['results']['books'][index]['rank'])
    isbn_pri = (data['results']['books'][index]['primary_isbn10'])
    
    dictionnaire = {'title': title,
                    'author': author,
                    'rank':rank,
                    'isbn_pri' : isbn_pri
                    }
    list_books.append(dictionnaire)
pprint(list_books[0:5])

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H%M%S")

filename = "./output/" + dt_string + "_books.json" 
with open(filename, "w") as jsonFile:
    json.dump(data, jsonFile)
import json
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import requests
from pprint import pprint

apiUrl = 'https://api.nytimes.com/svc/news/v3/content/nyt/well.json?api-key=AuG5HVISw4jzEit5G0RkacWynWZ8jtTF'

data = requests.get(apiUrl).text

data = json.loads(data)

url,page,title,updated_Date, = "","", "", ""
for result in data["results"]:
    url = result["url"]
    req = Request(url)
    #req.add_header('Accept-Language', 'fr-FR')
    page = urlopen(req)
    soup = bs(page, 'html.parser')

    print(url)

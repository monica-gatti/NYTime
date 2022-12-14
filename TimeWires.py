import json
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import requests
from pprint import pprint

apiUrl = 'https://api.nytimes.com/svc/news/v3/content/nyt/well.json?api-key=AuG5HVISw4jzEit5G0RkacWynWZ8jtTF'

data = requests.get(apiUrl).text

data = json.loads(data)

for result in data["results"][10:11]:
    url = result["url"]
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req)
    soup = bs(page, 'html.parser')
    body =""
    for t in soup.findAll("p", attrs={"class":"css-at9mc1 evys1bk0"}):
        body = body + t.text
    result["body"] = body

with open("allnyt.json", "w") as jsonFile:
    json.dump(data, jsonFile)



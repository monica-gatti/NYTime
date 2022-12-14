import json
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import requests
from pprint import pprint
import yaml
from utils import getNYTUrl, getHeaders
import ast

apiUrl = getNYTUrl()

data = requests.get(apiUrl).text
data = json.loads(data)

for result in data["results"][10:11]:
    url = result["url"]
    req = Request(url, headers=ast.literal_eval(getHeaders()))
    page = urlopen(req)
    soup = bs(page, 'html.parser')
    body =""
    for t in soup.findAll("p", attrs={"class":"css-at9mc1 evys1bk0"}):
        body = body + t.text
    result["body"] = body

with open("allnyt.json", "w") as jsonFile:
    json.dump(data, jsonFile)



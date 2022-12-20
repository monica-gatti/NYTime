import json
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import requests
from pprint import pprint
import yaml
from utils import getNYTUrl, getUserAgent
import ast
from datetime import datetime


apiUrl = getNYTUrl(context_="ARTICLES_CONTEXT")
data = requests.get(apiUrl).text
data = json.loads(data)

for result in data["response"]["docs"]:
    url = result["web_url"]
    print(url)
    req = Request(url, headers=ast.literal_eval(getUserAgent(user_agent_="MOZILLA_USER_AGENT")))
    page = urlopen(req)
    soup = bs(page, 'html.parser')
    body =""
    for t in soup.findAll("p", attrs={"class":"css-at9mc1 evys1bk0"}):
        body = body + t.text
    result["body"] = body

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H%M%S")

filename = "./output/" + dt_string + "_articles.json" 
print(filename)
with open(filename, "w") as jsonFile:
    json.dump(data, jsonFile)

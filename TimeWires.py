import json
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import requests
from pprint import pprint
from utils import getNYTUrl, getUserAgent
import ast

apiUrl = getNYTUrl(context_="TIME_WIRES_CONTEXT")
data = requests.get(apiUrl).text
data = json.loads(data)

for result in data["results"][10:11]:
    url = result["url"]
    req = Request(url, headers=ast.literal_eval(getUserAgent(user_agent_="CROME_USER_AGENT")))
    page = urlopen(req)
    soup = bs(page, 'html.parser')
    body =""
    for t in soup.findAll("p", attrs={"class":"css-at9mc1 evys1bk0"}):
        body = body + t.text
    result["body"] = body

with open("xxxxxxxx.json", "w") as jsonFile:
    json.dump(data, jsonFile)



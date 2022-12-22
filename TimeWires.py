import json
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import requests
from pprint import pprint
from utils import getNYTUrl, getUserAgent
import ast
from datetime import datetime
from string import Template
from time import sleep

sectionListUrl = getNYTUrl(context_="TIME_WIRES_SECTIONS_LIST")
sectionListData = requests.get(sectionListUrl).text
sectionListData = json.loads(sectionListData)

for element in sectionListData["results"][3:6]:
    section = element["section"]
    timeWireApiUrl = getNYTUrl(context_="TIME_WIRES_CONTEXT")
    sectionUrl = timeWireApiUrl % section
    sectionData = requests.get(sectionUrl).text
    sectionData = json.loads(sectionData)

    for result in sectionData["results"][1:2]:
        url = result["url"]
        req = Request(url, headers=ast.literal_eval(getUserAgent(user_agent_="MOZILLA_USER_AGENT")))
        page = urlopen(req)
        soup = bs(page, 'html.parser')
        body =""
        for t in soup.findAll("p", attrs={"class":"css-at9mc1 evys1bk0"}):
            body = body + t.text
        result["body"] = body

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H%M%S")

    filename = "./output/" + section + dt_string + "_timewires.json" 
    with open(filename, "w") as jsonFile:
        json.dump(sectionData, jsonFile)    
    sleep(6)


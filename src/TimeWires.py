import json
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import requests
from pprint import pprint
from utils import getNYTUrl, getUserAgent, getStringCurrentDate, ingestArticlesEs
import ast
from datetime import datetime
from time import sleep
import sqlite3
import logging

logging.basicConfig(filename="./output/logTimeWires.log", level=logging.INFO)

sectionListUrl = getNYTUrl(context_="TIME_WIRES_SECTIONS_LIST")
sectionListData = requests.get(sectionListUrl).text
sectionListData = json.loads(sectionListData)

for element in sectionListData["results"][1:]:
    con = sqlite3.connect("nytimes1.db")
    cur = con.cursor()
    section = element["section"]
    timeWireApiUrl = getNYTUrl(context_="TIME_WIRES_CONTEXT")
    
    sectionUrl = timeWireApiUrl % section
    sectionData = requests.get(sectionUrl).text
    sectionData = json.loads(sectionData)
    for result in sectionData["results"]:
        available = "Y"
        url = result["url"]
        try:
            req = Request(url, headers=ast.literal_eval(getUserAgent(user_agent_="MOZILLA_USER_AGENT")))
            page = urlopen(req)
            soup = bs(page, 'html.parser')
            body =""
            for t in soup.findAll("p", attrs={"class":"css-at9mc1 evys1bk0"}):
                body = body + t.text
            result["body"] = body
            ingestArticlesEs(result["slug_name"], result["created_date"], body)
        except:
            available = 'N'
        try:
            cur.execute("INSERT INTO ArticlesSection VALUES(?, ?, ?, ?, ?, ?, ?, ?)", 
            ([result["slug_name"], result["created_date"], result["title"], result["section"], result["subsection"], url, available, getStringCurrentDate()]))
            con.commit()
        except sqlite3.IntegrityError as err:
            print(f"Integritya error {err=}, {type(err)=}")
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
    con.close()

    filename = "./output/" + section + getStringCurrentDate() + "_timewires.json" 
    with open(filename, "w") as jsonFile:
        json.dump(sectionData, jsonFile)    
    sleep(2)


import json
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import requests
from pprint import pprint
from utils import getNYTUrl, getUserAgent, getStringCurrentDate, ingestForES
import ast
from datetime import datetime
from time import sleep
import sqlite3
import logging


logging.basicConfig(filename="./output/logTimeWires.log", level=logging.INFO)

timeWireApiUrl = getNYTUrl(context_="TIME_WIRES_CONTEXT_ALL")
sectionData = requests.get(timeWireApiUrl).text
sectionData = json.loads(sectionData)
for result in sectionData["results"]:
    available = "Y"
    url = result["url"]
    try:
        req = Request(url, headers=ast.literal_eval(getUserAgent(user_agent_="MOZILLA_USER_AGENT")))
        page = urlopen(req)
        soup = bs(page, 'html.parser')
        body = ""
        for t in soup.findAll("p", attrs={"class":"css-at9mc1 evys1bk0"}):
            body = body + t.text
        result["body"] = body
        ingestForES(result["slug_name"], result["created_date"], body)
    except:
        available = "N"
    authors = result["byline"].replace("BY", "").replace("AND", ",").split(",")
    con = sqlite3.connect("nytimes.db")
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO Articles VALUES(?, ?, ?, ?, ?, ?, ?, ?)", 
        ([result["slug_name"], result["created_date"], result["title"], result["section"], result["subsection"], url, available, getStringCurrentDate()]))
        con.commit()
        for author in authors:
            cur.execute("INSERT INTO authors VALUES(?,?)",
            ([result["slug_name"], author]))
            con.commit()
    except sqlite3.IntegrityError as err:
        print(f"Integrity error {err=}, {type(err)=}")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
    con.close()
    sleep(1)

filename = "./output/all_" + getStringCurrentDate() + "_timewires.json" 
with open(filename, "w") as jsonFile:
    json.dump(sectionData, jsonFile)    
sleep(6)


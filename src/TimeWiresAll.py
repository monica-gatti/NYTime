import json
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import requests
from model import Article, Author
from utils import dbPostgresGetEngine, logActivity, getNYTUrl, getUserAgent, getStringCurrentDate, ingestArticlesEs
import ast
from datetime import datetime
from time import sleep
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from psycopg2 import IntegrityError, errors

UniqueViolation = errors.lookup('23505') 
logActivity(getStringCurrentDate() + "_timewiresall.log")

timeWireApiUrl = getNYTUrl(context_="TIME_WIRES_CONTEXT_ALL")
sectionData = requests.get(timeWireApiUrl).text
sectionData = json.loads(sectionData)
engine = dbPostgresGetEngine()
Session = sessionmaker(bind=engine)
s = Session()
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
        ingestArticlesEs(result["slug_name"], result["created_date"], body)
    except:
        available = "N"
    authors = result["byline"].replace("BY", "").replace("AND", ",").split(",")
    try:
        article = Article( slug_id= result["slug_name"],article_date =result["created_date"],title = result["title"],section = result["section"],
            subsection = result["subsection"],url = url,webPageAvailability = 'Y',apiInvokeDate = datetime.now())
        s.add(article)
        s.flush()
        s.commit()
        for item in authors:
            author = Author( slug_id = result["slug_name"] , fullname = item)
            s.add(author)
            s.flush()
            s.commit()
    except UniqueViolation as uv:
        continue    
    except IntegrityError as e:
        assert isinstance(e.orig, UniqueViolation) 
        continue
    except SQLAlchemyError as err:
        print(str(err))
        s.rollback()
        continue
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
    s.close()
sleep(6)

#decomment only to save all the json response in file
#filename = "./output/all_" + getStringCurrentDate() + "_timewires.json" 
#with open(filename, "w") as jsonFile:
#    json.dump(sectionData, jsonFile)    


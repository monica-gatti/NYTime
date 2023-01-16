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
from sqlalchemy.exc import SQLAlchemyError
from psycopg2 import IntegrityError, errors

logActivity(getStringCurrentDate() + "_timewires.log")
UniqueViolation = errors.lookup('23505') 

sectionListUrl = getNYTUrl(context_="TIME_WIRES_SECTIONS_LIST")
sectionListData = requests.get(sectionListUrl).text
sectionListData = json.loads(sectionListData)
engine = dbPostgresGetEngine()
for element in sectionListData["results"][1:]:
    section = element["section"]
    timeWireApiUrl = getNYTUrl(context_="TIME_WIRES_CONTEXT")
    sectionUrl = timeWireApiUrl % section
    sectionData = requests.get(sectionUrl).text
    sectionData = json.loads(sectionData)
    Session = sessionmaker(bind=engine)
    s = Session()
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
sleep(2)


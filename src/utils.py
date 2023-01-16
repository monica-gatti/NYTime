import psycopg2
from sqlalchemy import create_engine
import yaml
import os
from typing import Literal
from datetime import datetime
from elasticsearch import Elasticsearch
import logging
from AESCyper import sym_decrypt
from sqlalchemy.engine import Engine

dirname = os.path.dirname(__file__)
appFileName = os.path.join(dirname, '.\\..\\config\\app.yaml')
credFileName = os.path.join(dirname, ".\\..\\config\\nycred.yaml")

contexts = Literal["TIME_WIRES_CONTEXT", "BOOKS_CONTEXT", "ARTICLES_CONTEXT", "TIME_WIRES_SECTIONS_LIST", "TIME_WIRES_CONTEXT_ALL"]
user_agents = Literal["CROME_USER_AGENT","MOZILLA_USER_AGENT"]

def getUserAgent(user_agent_: user_agents) -> str:
    '''
    Return the valid user agent to simulate a browser to get a web page
    @user_agent_: choose a User agent in the list to get the web page
    '''
    stream = open(appFileName, 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)
    header = data.get('SCRAPING').get(user_agent_)
    stream.close()
    return header
    
def getNYTkey() -> str:
    stream = open(credFileName, 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)
    key = sym_decrypt(data.get('API').get('api_key')) 
    stream.close()
    return key

def getNYTUrl(context_:contexts) -> str:
    '''
    Return the valid Url to invoke NYTimes API
    @context_: choose a Url in the list
    '''
    stream = open(appFileName, 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)
    baseUrl = data.get('API').get('BASE_URL')
    context = data.get('API').get(context_)
    stream.close()
    key = str(getNYTkey())
    return str(baseUrl) + str(context) + key

def ingestArticlesEs(slugname:str, created_date, body: str,) -> None:
    stream = open(appFileName, 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)
    es_url = data.get('ELASTIC_SEARCH').get("API_URL")
    es_index = data.get('ELASTIC_SEARCH').get("ARTICLE_INDEX") 
    stream.close()
    stream = open(credFileName, 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)
    es_pwd =  sym_decrypt(data.get('ELASTIC_SEARCH').get('pwd'))
    stream.close()

    try:
        es = Elasticsearch(es_url,basic_auth=("elastic", es_pwd), verify_certs=False)  
        doc = {
            'slug_name': slugname,
            'body':  body,
            'created_date': created_date,
            'word_count': len(body)
        }
        resp = es.index(index=es_index, id=slugname, document=doc)
        print(resp['result'])
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")

def ingestBooksEs(title: str, author: str,rank: int,description) -> None:                 
    stream = open(appFileName, 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)
    es_url = data.get('ELASTIC_SEARCH').get("API_URL")
    es_index = data.get('ELASTIC_SEARCH').get("INDEX") 
    stream.close()
    stream = open(credFileName, 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)
    es_pwd =  sym_decrypt(data.get('ELASTIC_SEARCH').get('pwd'))
    es = Elasticsearch(es_url,basic_auth=("elastic", es_pwd), verify_certs=False)  
    doc = {
        'title': title,
        'author':  author,
        'rank': rank,
        'description': description,
    }
    resp = es.index(index=es_index, document=doc)
    print(resp)

def getStringCurrentDate() -> str:
    now = datetime.now()
    return now.strftime("%d-%m-%Y_%H%M%S")

def logActivity(filename: str) -> None:
    loggingFileName = os.path.join(dirname, ".\\..\\output\\" + filename)
    logging.basicConfig(filename=loggingFileName, level=logging.INFO)


def dbPostgresGetEngine() -> Engine:
    stream = open(credFileName, 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)
    pwd =  sym_decrypt(data.get('DB').get('pwd'))
    connstr = "postgresql://postgres:" + pwd + "@localhost:5432/NyTimes"
    return create_engine(connstr)

def dbPostgresOpenConnection():
    stream = open(credFileName, 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)
    pwd =  sym_decrypt(data.get('DB').get('pwd'))
    
    return psycopg2.connect(
        host="localhost",
        database="NyTimes",
        user="postgres",
        password=sym_decrypt(pwd),
        port=5432)


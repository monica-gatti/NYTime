import yaml
from typing import Literal
from datetime import datetime
from elasticsearch import Elasticsearch

contexts = Literal["TIME_WIRES_CONTEXT", "BOOKS_CONTEXT", "ARTICLES_CONTEXT", "TIME_WIRES_SECTIONS_LIST", "TIME_WIRES_CONTEXT_ALL"]
user_agents = Literal["CROME_USER_AGENT","MOZILLA_USER_AGENT"]

def getUserAgent(user_agent_: user_agents) -> str:
    '''
    Return the valid user agent to simulate a browser to get a web page
    @user_agent_: choose a User agent in the list to get the web page
    '''
    stream = open('./config/app.yaml', 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)
    header = data.get('SCRAPING').get(user_agent_)
    stream.close()
    return header



def getNYTkey() -> str:
    stream = open('./config/nycred.yaml', 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)
    key = data.get('API').get('api_key')
    stream.close()
    return key

def getNYTUrl(context_:contexts) -> str:
    '''
    Return the valid Url to invoke NYTimes API
    @context_: choose a Url in the list
    '''
    stream = open('./config/app.yaml', 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)
    baseUrl = data.get('API').get('BASE_URL')
    context = data.get('API').get(context_)
    stream.close()
    key = str(getNYTkey())
    return str(baseUrl) + str(context) + key

def ingestArticlesEs(slugname:str, created_date, body: str,) -> None:
    stream = open('./config/app.yaml', 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)
    es_url = data.get('ELASTIC_SEARCH').get("API_URL")
    es_index = data.get('ELASTIC_SEARCH').get("INDEX") 
    stream.close()
    es = Elasticsearch(es_url,basic_auth=("elastic", "datascientest"), verify_certs=False)  
    doc = {
        'slug_name': slugname,
        'body':  body,
        'created_date': created_date,
    }
    resp = es.index(index=es_index, id=slugname, document=doc)
    print(resp['result'])


def ingestBooksEs(title: str, author: str,rank: int,description) -> None:                 
    stream = open('./config/app.yaml', 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)
    es_url = data.get('ELASTIC_SEARCH').get("API_URL")
    es_index = data.get('ELASTIC_SEARCH').get("INDEX") 
    stream.close()
    es = Elasticsearch(es_url,basic_auth=("elastic", "datascientest"), verify_certs=False)  
    doc = {
        'title': title,
        'author':  author,
        'rank':rank,
        'description': description,
    }
    resp = es.index(index=es_index, document=doc)
    print(resp)




def getStringCurrentDate() -> str:
    now = datetime.now()
    return now.strftime("%d-%m-%Y_%H%M%S")
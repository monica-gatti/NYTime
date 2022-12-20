import json
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import requests
from pprint import pprint
import yaml
from utils import getNYTUrl, getHeaders
import ast


apiUrl = getNYTUrl(context_="ARTICLES_CONTEXT")
data = requests.get(apiUrl).text
data = json.loads(data)

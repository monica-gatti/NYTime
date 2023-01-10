import json
import requests
from pprint import pprint
import yaml
from utils import getNYTUrl, getUserAgent
from datetime import datetime

apiUrl = getNYTUrl(context_='MOVIES_REVIEWS_CONTEXT')

data = requests.get(apiUrl).text
data = json.loads(data)

list_review = []
for index in range(0,len(data['results'])):
    display_title=(data['results'][index]['display_title'])
    byline=(data['results'][index]['byline'])
    link = (data['results'][index]['link'])
    headline = (data['results'][index]['headline'])
    publication_date = (data['results'][index]['publication_date'])
    mpaa_rating = (data['results'][index]['mpaa_rating'])
    dictionnaire = {'display_title': display_title,
                    'byline': byline,
                    'link':link,
                    'headline' : headline,
                    'publication_date' : publication_date,
                    'mpaa_rating' : mpaa_rating,
                    }
    list_review.append(dictionnaire)
pprint(list_review[0:10])

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H%M%S")

filename = "./output/" + dt_string + "_books.json" 
with open(filename, "w") as jsonFile:
    json.dump(data, jsonFile)




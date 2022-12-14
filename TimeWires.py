import json
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import requests
from pprint import pprint

apiUrl = 'https://api.nytimes.com/svc/news/v3/content/nyt/well.json?api-key=AuG5HVISw4jzEit5G0RkacWynWZ8jtTF'

data = requests.get(apiUrl).text

data = json.loads(data)

url,page,title,updated_Date, = "","", "", ""
for result in data["results"][10:11]:
    url = result["url"]
    print(url)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    #req.add_header('Accept-Language', 'fr-FR')
    page = urlopen(req)
    soup = bs(page, 'html.parser')
    for t in soup.findAll("p", attrs={"class":"css-at9mc1 evys1bk0"}):#[0]#.findAll("td",attrs={"titleColumn"})
        print(t.text)

    #body = soup.find("p", class_="css-at9mc1 evys1bk0").text

    #for e in soup.select('div.css-at9mc1'):
    #    print(e.text)


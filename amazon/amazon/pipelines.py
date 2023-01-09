
from itemadapter import ItemAdapter
import sqlite3
from elasticsearch import Elasticsearch as es
class AmazonPipeline:

    def __init__(self):

        self.con = sqlite3.connect('books.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS book_prices(
            id INTEGER PRIMARY KEY,
            title TEXT,
            price INTEGER,
            ratings INTEGER,
            url TEXT
        )
        """)

    def process_item(self, item, spider):
        ## Define insert statement
        self.cur.execute("""
            INSERT INTO book_prices (title, price, ratings, url) VALUES (?, ?, ?, ?)
        """,
        (
            item['title'],
            item['price'],
            item['ratings'],
            item['url']
        ))

        ## Execute insert of data into database
        self.con.commit()
        return item

    def ingestForES(title: str,rank: int,description):
        es_url = es(hosts=[{'host':'http://34.255.105.149','port': 9200}])
        es = es(es_url,basic_auth=("elastic", "datascientest"), verify_certs=False)
        data = {'title': title,
                'rank':rank,
                'description': description,
                } 
        resp = es.create.index(index='myindex', body=data)
        print(resp)





"""
    def ingestForES(title: str, price: int,ratings: int,url) -> None:                 

        es_url = "http://34.255.105.149:9200"
        es_index = "scrapy"

        es = es(es_url,basic_auth=("elastic", "datascientest"), verify_certs=False)  
        doc = {
            'title': title,
            'price':  price,
            'ratings':ratings,
            'url': url,
        }
        resp = es.index(index= es_index, document=doc)
        print(resp)
      

"""

from itemadapter import ItemAdapter
import sqlite3

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









import sqlite3
import os

con = sqlite3.connect("nytimes.db")
con = sqlite3.connect('books.db')

cur = con.cursor()

cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='articles' ''')
if cur.fetchone()[0]==1 : {
	print('Table articles exists.')
}
else:
    cur.execute("CREATE TABLE articles(slug_name PRIMARY KEY, article_date, title, section, subsection, url, webPageAvailability, APIInvokeDate)")
con.commit()

cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='authors' ''')
if cur.fetchone()[0]==1 : {
	print('Table authors exists.')
}
else:
    cur.execute("CREATE TABLE authors(slug_name, fullname, FOREIGN KEY(slug_name) REFERENCES articles(slug_name))")
con.commit()

cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='books_full_overview' ''')
if cur.fetchone()[0]==1 : {
	print('Table books_full_overview exists.')
}
else:
    cur.execute("CREATE TABLE books_full_overview(title TEXT, author TEXT, publisher TEXT, contributor TEXT, rank INTEGER, primary_isbn13 INTEGER, primary_isbn10 INTEGER, updated_date DATE, created_date DATE, amazon_product_url TEXT)")
con.commit()

cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='book_prices' ''')
if cur.fetchone()[0]==1 : {
	print('Table book_prices exists.')
}
else:
    cur.execute("CREATE TABLE book_prices(id INTEGER PRIMARY KEY, url, price)")
con.commit()

res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchall())
con.close()





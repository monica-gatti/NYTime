import sqlite3

con = sqlite3.connect("nytimes.db")

con = sqlite3.connect('books.db')


cur = con.cursor()

cur.execute("CREATE TABLE articles(slug_name PRIMARY KEY, article_date, title, section, subsection, url, webPageAvailability, APIInvokeDate)")
con.commit()

cur.execute("CREATE TABLE authors(slug_name, fullname, FOREIGN KEY(slug_name) REFERENCES articles(slug_name))")
con.commit()

cur.execute('''CREATE TABLE books_full_overview(id INTEGER PRIMARY KEY, title TEXT, author TEXT, publisher TEXT, contributor TEXT, rank INTEGER, primary_isbn13 INTEGER, primary_isbn10 INTEGER, updated_date DATE, created_date DATE, amazon_product_url TEXT)''')
con.commit()

cur.execute('''CREATE TABLE book_prices(id INTEGER PRIMARY KEY, url, price)''')
con.commit()

res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchall())
con.close()





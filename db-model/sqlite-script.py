import sqlite3
con = sqlite3.connect("nytimes.db")

cur = con.cursor()

cur.execute("CREATE TABLE articles(slug_name PRIMARY KEY, article_date, title, section, subsection, url, webPageAvailability, APIInvokeDate)")
con.commit()

cur.execute("CREATE TABLE authors(slug_name, fullname, FOREIGN KEY(slug_name) REFERENCES articles(slug_name))")
con.commit()

res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchall())
con.close()
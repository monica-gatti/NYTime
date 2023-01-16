# NYTime
Using NY Times API to get Articles, Books and Time Wire.
## Set up
The application stores Article metadata in a Postgres database and article text in Elastic Search index.
### Encrypt sensitive informations
Password for invoking external service in your python application needs to be encrypted. With the following steps, you will encrypt strings with AES cypher with a 128-bit or 256-bit key.
1. Launch for windows
```
pip install pycryptodome
```
or for Ubuntu
```
pip install crypto
```
2. Generate a 16 byte key and save it in en environment variable "NYTIMES_CYPHER_KEY". You can use this tool https://www.allkeysgenerator.com/Random/Security-Encryption-Key-Generator.aspx , set "Encryption Key" and choose 128-bit ( to get a key lenght of 128/8 = 16 byte) or 256-bit to have a
Head the AESCypher.py file, decomment the last rows and set the password you want to encrypt:
```
enc = sym_encrypt("ciaociao")
print(enc)
dec = sym_decrypt(enc)
print(dec)
```
3. Configure the encripted password in config/nycred.py file.
### Database Set up
Provide a Postgres database, assign the database name in app.yaml.
Launch .\db-model\sqlite-script.py in order to create the db tables.
### ElasticSearch
Create an index with the following instruction and save the index name in app.yaml:
```
PUT /articles
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 2
  },
  "mappings": {
    "properties": {
      "slug_name": {
        "type": "keyword"
      },
      "body": {
        "type": "text"
      },
      "created_date": {
        "type": "date"
      },
      "word_count": {
        "type": "integer"
      }
    }
  }
}
```
### Scrapy:
Now we should create our Spider Project of which will create a Tree of our Project as follow:
Here I'll try explain this step using my propre Project Amazon(the idea behind is to gather all the NYTIMES BOOKS available links that are used to reveal book'sprices, ratings, description ans so on..):
```
$scrapy startproject amazon  #I named the project  "amazon" since I am going to scrap through the amazon.com
$cd amazon
$scrapy genspider ny-times https://www.nytimes.com/ ; this will Generate new spider using pre-defined templates
```

```
PS C:\Source_code\NYTime\amazon\amazon> tree /F
```
Structure du dossier

```
Le numéro de série du volume est A679-1F2C
C:.
│   items.py
│   middlewares.py
│   pipelines.py
│   settings.py
│   __init__.py
│   
├───spiders
│   │   books.db
│   │   ny_time.json
│   │   ny_times.py
│   │   __init__.py
│   │   
│   └───__pycache__
│           ny_times.cpython-39.pyc
│           utils.cpython-39.pyc
│           __init__.cpython-39.pyc
│
└───__pycache__
        items.cpython-39.pyc
        pipelines.cpython-39.pyc
        settings.cpython-39.pyc
        __init__.cpython-39.pyc
```
Now and that the project is created as shown by the tree: the files.py that we need to use in order to fulfill the scrapy job are:
1. ny_times.py  # this is the main python file
2.items.py  #this is used to create the data model we want.
3.pipelines.py  # is used to output our data into a connected Database(Sql , Nosql)# in our case Sqlite and ElasticSearch
4.settings: to make sure that the program will run and parsing the data into a created Database you SHOULD add the following command inside the settings.py
```
ITEM_PIPELINES = {
                'amazon.pipelines.AmazonPipeline': 300,   
        }
```
Finally, if you succeed to create the Job. You should "pip install crawl" to use the crawl methode and then type the command below to run the program(I think you should be under the folder where the ny_times resides):

        scrapy crawl ny-times -o ny_time.json    
            #the ny_times is the name of the Project 
NOTE: don't forget to install scrapy: 
            pip install scrapy
        OR
    conda install -c conda-forge scrapy  # if you are using Anaconda

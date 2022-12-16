import yaml

def getNYTkey() -> str:
    stream = open('./config/nycred.yaml', 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)
    key = data.get('API').get('api_key')
    
    #inside the yaml which is located in ''./config/nycred.yaml'' I am loading the following API as follows
           # API:
           #    api_key: CKjGFh7CrNKbbE3ZBeHKdeANKwxkm5c6
    stream.close()
    return key

def getNYTUrl(context) -> str:
    stream = open('./config/app.yaml', 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)
    baseUrl = data.get('API').get('BASE_URL')
    
    # this will load the books_context: remember that we need to create an YAML file which we will create
    #the API Destination that includes the base URL of the site and its descending urls
    #API:
       #   BASE_URL: "https://api.nytimes.com/svc/"
       #   BOOKS_CONTEXT: "books/v3/lists/current/hardcover-fiction.json?api-key="
    context = data.get('API').get(context)
    stream.close()
    key = str(getNYTkey())
    return str(baseUrl) + str(context) + key


def getHeaders():
    stream = open('./config/app.yaml', 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)
    header = data.get('API').get('HEADERS')
    #this is used to fake a browser visit by using python requests or command wget
    #headers = {'User-Agent': 'Chrome/39.0.2171.95 '}  # this should also be created in yaml file all along with the base
    #url and the descending url if it exists.
    stream.close()
    return header
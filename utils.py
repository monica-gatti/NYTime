import yaml


def getNYTkey() -> str:
    stream = open('./config/nycred.yaml', 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)
    key = data.get('API').get('api_key')
    stream.close()
    return key

def getNYTUrl(context) -> str:
    stream = open('./config/app.yaml', 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)
    baseUrl = data.get('API').get('BASE_URL')
    context = data.get('API').get(context)
    stream.close()
    key = str(getNYTkey())
    return str(baseUrl) + str(context) + key

def getHeaders():
    stream = open('./config/app.yaml', 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)
    header = data.get('API').get('HEADERS')
    stream.close()
    return header
FROM python:latest
ADD config .
ADD db-model .
ADD ScrapySpider .
ADD src . 
RUN mkdir output
RUN pip install setuptools requests elasticsearch pysqlite3 scrapy beautifulsoup4 pyyaml
RUN pwd
WORKDIR /db-model
ENTRYPOINT [ "python", "./sqlite-script.py" ]
WORKDIR /src
CMD [ "python", "./TimeWiresAll.py" ]

WORKDIR /
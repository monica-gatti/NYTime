FROM python:latest
ADD config .
ADD db-model .
ADD ScrapySpider .
 
RUN mkdir output
RUN pip install setuptools requests elasticsearch pysqlite3 scrapy beautifulsoup4 pyyaml
CMD [ "python", "./TimeWires.py" ]
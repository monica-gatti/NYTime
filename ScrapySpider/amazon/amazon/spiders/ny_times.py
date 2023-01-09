import scrapy
import json
from amazon.items import AmazonItem
import ast
from elasticsearch import Elasticsearch as es
#from utils import getNYTUrl, getUserAgent
#import sys
#sys.path.append('/.../amazon/amazon/spiders')
from requests import Request
#from time import sleep

class NyTimesSpider(scrapy.Spider):

    name = 'ny-times'
    #start_urls = getNYTUrl(context_="BOOKS_CONTEXT")
    start_urls= ["https://api.nytimes.com/svc/books/v3/lists/full-overview.json?api-key=CKjGFh7CrNKbbE3ZBeHKdeANKwxkm5c6 "]

    def start_requests(self):

        for url in self.start_urls:
            yield scrapy.Request(
                url, callback = self.url_parse, headers=ast.literal_eval("{'User-Agent':'Mozilla/5.0'}"))

    def url_parse(self, response):
        books = []
        data = json.loads(response.text)
        for lists in data['results']['lists']:
            for book in lists['books']:
                yield scrapy.Request(
                book['amazon_product_url'], 
                callback = self.parse)
                #sleep(1)

    def parse(self, response):
        title = response.xpath("//span[@id='productTitle']//text()").get().strip()
        price = response.xpath("//span[@class='a-size-base a-color-price a-color-price']//text()").get().strip().replace('$', '')
        ratings = response.xpath("//span[@id='acrCustomerReviewText']//text()").get().strip().replace('ratings', '')
        loader = AmazonItem()  # Here you create a new item each iteration
        loader['title'] = title
        loader['url'] = response.request.url
        loader['price'] = price
        loader['ratings'] = ratings
        yield loader
        


import scrapy
import json
from amazon.items import AmazonItem
import ast
from amazon.amazon.spiders import utils
from utils import getNYTUrl, getUserAgent

class NyTimesSpider(scrapy.Spider):

    name = 'ny-times'
    start_urls = getNYTUrl(context_="BOOKS_CONTEXT")


    def start_requests(self):

        for url in self.start_urls:
            yield scrapy.Request(
                url, callback = self.url_parse, headers=ast.literal_eval(getUserAgent(user_agent_="MOZILLA_USER_AGENT")))

    def url_parse(self, response):
        books = []
        data = json.loads(response.text)
        for lists in data['results']['lists']:
            for book in lists['books']:
                books.append({
                    'amazon_product_url' : book['amazon_product_url'],
                })
        
        for book in books:
            yield scrapy.Request(
                book['amazon_product_url'], 
                callback = self.parse
            )

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
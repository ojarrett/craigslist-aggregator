import scrapy
from time import sleep
import random

class CraigslistSpider(scrapy.Spider):
    name = "craigslist"

    def start_requests(self):
        urls = [
            'https://minneapolis.craigslist.org/d/sublets-temporary/search/sub',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for result in response.css('li.result-row'):
            title = result.css('a.result-title::text').get()
            price = result.css('span.result-price::text').get()
            rooms = result.css('span.housing::text').get()
            url = result.css('a.result-title::attr(href)').get()
            posting_id = result.attrib['data-pid']

            if title and price and rooms and url and posting_id:
                yield {
                    'title': title, 
                    'price': price, 
                    'rooms': rooms, 
                    'url': url,
                    'posting_id': posting_id,
                }

        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            sleep(random.random()*10.0 + 2.0)
            yield response.follow(next_page, callback=self.parse)

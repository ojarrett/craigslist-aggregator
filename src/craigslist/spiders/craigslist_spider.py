import scrapy
from time import sleep
import random
import re
from posting.craigslist_utils import parse_price, parse_rooms
from db_sync.sync import DbSync

class CraigslistSpider(scrapy.Spider):
    name = "craigslist"

    def start_requests(self):
        self.db_sync = DbSync()
        urls = [
            'https://minneapolis.craigslist.org/d/sublets-temporary/search/sub',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for result in response.css('li.result-row'):
            title = result.css('a.result-title::text').get()
            price = parse_price(result.css('span.result-price::text').get())
            rooms = parse_rooms(result.css('span.housing::text').get())

            url = result.css('a.result-title::attr(href)').get()
            posting_id = result.attrib['data-pid']
            last_updated = result.css('time.result-date::attr(datetime)').get()

            if title and price and rooms and url and posting_id and last_updated:
                new_posting = {
                    'title': title, 
                    'price': price, 
                    'rooms': rooms, 
                    'url': url,
                    'posting_id': posting_id,
                    'last_updated': last_updated
                }

                self.db_sync.add_posting(new_posting)
                yield new_posting

        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            sleep(random.random()*10.0 + 2.0)
            yield response.follow(next_page, callback=self.parse)

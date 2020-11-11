import scrapy
from time import sleep
import random
import re
from posting.craigslist_utils import parse_price, parse_rooms, get_region_from_url
from db_sync.sync import DbSync

class CraigslistSpider(scrapy.Spider):
    name = "craigslist"

    def start_requests(self):
        self.db_sync = DbSync()

        urls = []
        with open('base_sites.cfg', 'r') as f:
            urls = [site + "/d/sublets-temporary/search/sub" for site in f]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            sleep(random.random()*3.0 + 3.0)

    def parse(self, response):
        for result in response.css('li.result-row'):
            title = result.css('a.result-title::text').get()
            price = parse_price(result.css('span.result-price::text').get())
            rooms = parse_rooms(result.css('span.housing::text').get())

            url = result.css('a.result-title::attr(href)').get()
            region = get_region_from_url(url)
            posting_id = result.attrib['data-pid']
            last_updated = result.css('time.result-date::attr(datetime)').get()

            if title and price and rooms and url and posting_id and last_updated:
                new_posting = {
                    'title': title, 
                    'price': price, 
                    'rooms': rooms, 
                    'url': url,
                    'posting_id': posting_id,
                    'last_updated': last_updated,
                    'region': region,
                }

                old_posting = self.db_sync.get_posting(posting_id=posting_id, region=region)

                if old_posting is None:
                    self.db_sync.add_posting(new_posting)
                yield new_posting

        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            sleep(random.random()*10.0 + 2.0)
            yield response.follow(next_page, callback=self.parse)

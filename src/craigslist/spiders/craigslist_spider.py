import scrapy
from bs4 import BeautifulSoup

class CraigslistSpider(scrapy.Spider):
    name = "craigslist"

    def start_requests(self):
        urls = [
            'https://minneapolis.craigslist.org/d/sublets-temporary/search/sub',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'sublets.html'
        with open(filename, 'w') as f:
            soup = BeautifulSoup(response.body, 'html.parser')
            for title in soup.find_all('a', class_='result-title'):
                f.write(title.get_text())
        self.log(f'Saved file {filename}')

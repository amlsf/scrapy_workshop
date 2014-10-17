import scrapy


class BasicSpider(scrapy.Spider):
    name = 'minimal'

    def start_requests(self):
        return (scrapy.Request(url)
                for url in ['http://www.yahoo.com'])

    def parse(self, response):
        self.log('GETTING URL: %s' % response.url)

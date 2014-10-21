from scrapy import Request, Spider, Item, Field


class WineItem(Item):
    link = Field()
    name = Field()
    price = Field()


class DrunkSpider(Spider):
    name = 'bare_bones'
    # start_urls = ['http://www.wine.com/v6/wineshop/']

    # start_requests() is set as default, no need to include. Could just use start_urls list
    def start_requests(self):
        """
        :rtype: scrapy.http.Request
        """
        for url in ['http://www.wine.com/v6/wineshop/']:
            # parse callback is set as default, no need to specify
            yield Request(url, callback=self.parse)

    def parse(self, response):
        """
        :type response: scrapy.http.HtmlResponse
        """
        self.log('Fetched URL: %s' % response.url)

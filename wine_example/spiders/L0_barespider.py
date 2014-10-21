from scrapy import Request, Spider


class BasicSpider(Spider):
    name = 'bare_bones'
    # start_urls = ['http://www.wine.com/v6/wineshop/']

    def start_requests(self):
        """
        :rtype: scrapy.http.Request
        """
        for url in ['http://www.wine.com/v6/wineshop/']:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        """
        :type response: scrapy.http.HtmlResponse
        """
        self.log('Fetched URL: %s' % response.url)

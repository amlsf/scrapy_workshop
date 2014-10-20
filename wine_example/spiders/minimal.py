import scrapy


class BasicSpider(scrapy.Spider):
    name = 'bare_bones'

    def start_requests(self):
        """
        :rtype: scrapy.http.Request
        """
        for url in ['http://www.yahoo.com']:
            return scrapy.Request(url)

    def parse(self, response):
        """
        :type response: scrapy.http.HtmlResponse
        """
        self.log('Fetched URL: %s' % response.url)

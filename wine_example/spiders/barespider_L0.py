import scrapy
# TODO add basic CSS or XPath Selector


class BasicSpider(scrapy.Spider):
    name = 'bare_bones'
    # start_urls = ['http://www.yahoo.com']

    def start_requests(self):
        """
        :rtype: scrapy.http.Request
        """
        for url in ['http://www.yahoo.com']:
            yield scrapy.Request(url,  callback=self.parse)

    def parse(self, response):
        """
        :type response: scrapy.http.HtmlResponse
        """
        self.log('Fetched URL: %s' % response.url)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from scrapy import Spider, Item, Field, Request
import urlparse

# Notes: 1) explain defaults start_requests & parse() method and 2) introduce meta


class Wine(Item):
    link = Field()
    name = Field()


class DrunkSpider(Spider):
    name = 'wine-demo'
    # start_urls = ['http://www.wine.com/v6/wineshop/']

    def start_requests(self):
        for url in ['http://www.wine.com/v6/wineshop/']:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        product_list = response.css('.productList')
        products = product_list.css('.verticalListItem')

        for product in products:
            links_list = product.css('.listProductName::attr(href)').extract()
            if not links_list:
                continue
            link = links_list[0]

            product_url = urlparse.urljoin(response.url, link)

            request = Request(product_url, callback=self.parse_product_page)

            yield request

    @staticmethod
    def parse_product_page(response):
        wine_product = Wine()
        wine_product['link'] = response.url

        product = response.css('[itemtype="http://schema.org/Product"]')
        # TALK about xpath method too
        wine_name = product.css('[itemprop="name"]::text').extract()
        if wine_name:
            wine_product['name'] = wine_name[0]

        yield wine_product

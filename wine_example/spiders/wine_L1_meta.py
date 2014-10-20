# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from scrapy import Item, Field, Request
import urlparse
from .wine_L1 import DrunkSpider
# Notes: 1) explain defaults start_requests & parse() method and 2) introduce meta


class WineItem(Item):
    link = Field()
    name = Field()
    # price = Field()


class MetaDrunkSpider(DrunkSpider):
    name = '%s-meta' % DrunkSpider.name

    def parse(self, response):
        """
        :type response: HtmlResponse
        """
        product_list = response.css('.productList')
        products = product_list.css('.verticalListItem')

        for product in products:
            links_list = product.css('.listProductName::attr(href)').extract()
            if not links_list:
                continue
            link = links_list[0]

            product_url = urlparse.urljoin(response.url, link)

            meta = dict()
            price_list = product.css('[itemprop="price"]::text').extract()
            if price_list:
                current_price = price_list[0]
                meta['price'] = current_price

            request = Request(product_url, meta=meta, callback=self.parse_product_page)
            yield request

    @staticmethod
    def parse_product_page(response):
        wine_product = WineItem()
        wine_product['link'] = response.url

        product = response.css('[itemtype="http://schema.org/Product"]')
        wine_name = product.css('[itemprop="name"]::text').extract()
        if wine_name:
            wine_product['name'] = wine_name[0]

        meta = response.meta
        if 'price' in meta:
            wine_product['price'] = meta['price']

        yield wine_product

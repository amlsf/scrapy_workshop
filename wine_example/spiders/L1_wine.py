# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from scrapy import Spider, Item, Field
import urlparse


class WineItem(Item):
    link = Field()
    name = Field()
    price = Field()


class DrunkSpider(Spider):
    name = 'wine-demo-L1'
    start_urls = ['http://www.wine.com/v6/wineshop/']

    def parse(self, response):
        """
        :type response: scrapy.http.HtmlResponse
        :rtype: WineItem
        """
        product_list = response.css('.productList')
        products = product_list.css('.verticalListItem')

        for product in products:
            wine_product = WineItem()

            # get product link
            links_list = product.css('.listProductName').xpath('@href').extract()
            if not links_list:
                continue

            link = links_list[0]
            wine_product['link'] = urlparse.urljoin(response.url, link)

            # get name
            wine_name = product.css('.listProductName').xpath('text()').extract()
            if wine_name:
                wine_product['name'] = wine_name[0]

            # get price
            price_list = product.css('[itemprop="price"]').xpath('text()').extract()
            if price_list:
                current_price = price_list[0]
                wine_product['price'] = current_price

            yield wine_product




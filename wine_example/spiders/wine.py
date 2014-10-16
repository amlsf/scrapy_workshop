# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from scrapy import Spider, Item, Field, Request
import urlparse

# TODO add pagination & reviews

class Wine(Item):
    link = Field()
    name = Field()
    price = Field()
    wine_type = Field()
    # ratings = scrapy.Field()
    # customer_reviews = scrapy.Field()
    # customers_also_viewed = scrapy.Field()


class MinimalSpider(Spider):
    name = 'wine-demo'
    start_urls = ['http://www.wine.com/v6/wineshop/']

    def parse(self, response):
        product_list = response.css('.productList')
        products = product_list.css('.verticalListItem')

        for product in products:
            links_list = product.css('.listProductName::attr(href)').extract()
            if not links_list:
                # TODO what happens if I return out here? Will the generator continue?
                return

            link = links_list[0]
            product_url = urlparse.urljoin(response.url, link)

            meta = dict()
            price_list = product.css('[itemprop="price"]::text').extract()
            if price_list:
                current_price = price_list[0]
                meta['price'] = current_price

            request = Request(product_url, meta=meta, callback=self.parse_product)
            yield request

    # TODO could also get the javascript script tag dict??
    # TODO issue here with method being "static"
    # TODO can I take out self here since it's not being used?
    def parse_product(self, response):
        wine_product = Wine()
        wine_product['link'] = response.url

        product = response.css('[itemtype="http://schema.org/Product"]')
        # TODO is there a better way to pick the one I want?
        wine_product['name'] = product.css('[itemprop="name"]::text')[0].extract()

        # TODO out of pure curiosity, what happens if there is no meta here that was created?
        meta = response.meta
        if 'price' in meta:
            wine_product['price'] = meta['price']

        # TODO do a better one of this where traverse further down the tree?
        wine_type_list = response.css('.wine-icons li div[title] span[class=offscreen]::text').extract()
        if wine_type_list:
            wine_type = wine_type_list[0]
            wine_product['wine_type'] = wine_type

        yield wine_product




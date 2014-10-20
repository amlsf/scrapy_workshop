# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from scrapy import Spider, Item, Field, Request
import re
import urlparse
import json

# Notes: adds additional attributes, uses XPath; show 2nd way to get price from javascript script tag


class WineItem(Item):
    link = Field()
    name = Field()
    price = Field()

    wine_type = Field()

    tag_data = Field()
    region = Field()


class DrunkSpider(Spider):
    name = 'wine-demo-L2'
    start_urls = ['http://www.wine.com/v6/wineshop/']

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

        meta = response.meta
        if 'price' in meta:
            wine_product['price'] = meta['price']

        product = response.css('[itemtype="http://schema.org/Product"]')
        wine_name = product.css('[itemprop="name"]::text').extract()
        if wine_name:
            wine_product['name'] = wine_name[0]

        wine_type_list = response.css('.wine-icons span[class=offscreen]::text').extract()
        if wine_type_list:
            wine_type = wine_type_list[0]
            wine_product['wine_type'] = wine_type

        tag_data_list = response.xpath(
            '/html/head/link[contains(@href,"//fonts.googleapis.com")]'
            '/following-sibling::script/text()').extract()
        if tag_data_list:
            #: type: unicode
            tag_body = tag_data_list[0]
            tag_body1line = re.sub(r'[\r\n]', '', tag_body)
            tag_json = re.sub(r';\s*$', '',
                              re.sub('^\s*var\s*[^{]+', '', tag_body1line))
            tag_data = json.loads(tag_json)
            wine_product['tag_data'] = tag_data

            omniture_props = tag_data.get('OmnitureProps')
            if omniture_props:
                region = omniture_props.get("Region")
                if region:
                    wine_product['region'] = region

                # another way to get the price:
                # tag_price = omniture_props.get('Price')

        yield wine_product

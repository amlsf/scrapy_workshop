# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from scrapy import Spider, Item, Field, Request
import urlparse
import json

# Add gathering customer reviews & ratings


class Wine(Item):
    link = Field()
    name = Field()
    price = Field()
    wine_type = Field()
    tag_data = Field()
    region = Field()
    customer_review = Field()
    rating = Field()


class DrunkSpider(Spider):
    name = 'wine-demo'
    start_urls = ['http://www.wine.com/v6/wineshop/']

    # TODO add pagination logic here
    def parse(self, response):
        pass

    def get_product_links(self, response):
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

    def parse_product_page(self, response):
        wine_product = Wine()
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
            '/html/head/link[contains(@href,"//fonts.googleapis.com")]/following-sibling::*/text()').extract()
        # TODO change to regex
        if tag_data_list:
            tag_data_str = tag_data_list[0]
            start = tag_data_str.find('{')
            end = tag_data_str.rfind('}')
            if start != -1 and end != -1:
                tag_data_json = tag_data_str[start:end+1]

                # TODO add some try except and show logging here
                tag_data = json.loads(tag_data_json)

                wine_product['tag_data'] = tag_data

                omniture_props = tag_data.get('OmnitureProps')
                if omniture_props:
                    region = omniture_props.get("Region")
                    if region:
                        wine_product['region'] = region

        reviews_link_list = response.css('#ctl00_BodyContent_lnkViewAll::attr(href)').extract()
        if reviews_link_list:
            all_reviews_link = urlparse.urljoin(response.url, reviews_link_list[0])
            meta['wine_item'] = wine_product
            yield Request(all_reviews_link, meta=meta, callback=self.get_prod_reviews)
        else:
            yield wine_product

    # TODO add code to grab ratings & reviews
    def get_prod_reviews(self, response):
        pass
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from scrapy import Spider, Item, Field, Request
import urlparse
import json

# TODO add reviews, regex? How store multiple reivews?
# TODO Production code: talk about logging, errback, testing? Learn how to test the siphon way

# YELP:
# TODO Selector? Why use in Yelp instead of just calling .css directly on response?
# sel = Selector(response=response)
# businesses = sel.css(".column-alpha li")
# TODO why using del?


class Wine(Item):
    link = Field()
    name = Field()
    price = Field()
    wine_type = Field()
    tag_data = Field()
    region = Field()
    # customer_reviews = scrapy.Field()
    # ratings = scrapy.Field()


class DrunkSpider(Spider):
    name = 'wine-demo'
    start_urls = ['http://www.wine.com/v6/wineshop/']

    def parse(self, response):
        """
        handles pagination
        """
        # handles parsing current page (of 10), which is disabled in HTML
        yield Request(response.url, callback=self.get_product_links)

        paging_sel = response.css('.listPaging')
        # handles parsing the remaining 9 pages of 10
        page_list = paging_sel.css('span > a::attr(href)').extract()
        for page in page_list:
            page_link = urlparse.urljoin(response.url, page)
            yield Request(page_link, callback=self.get_product_links)

        # re-queues the link to the first page of the next set of 10 pages
        next_10_list = paging_sel.css('#ctl00_BodyContent_ctrProducts_ctrPagingBottom_lnkNextX::attr(href)').extract()
        if next_10_list:
            next_10_link = urlparse.urljoin(response.url, next_10_list[0])
            yield Request(next_10_link, callback=self.parse)

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

            request = Request(product_url, meta=meta, callback=self.parse_product)
            yield request

    # TODO issue here with method being "static"? But works fine without the @staticmethod decorator - necessary to add?
    # No need for self because not calling any callbacks, but if I remove it, it blows up?
    def parse_product(self, response):
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

                # Could show another way to get the price:
                # tag_price = omniture_props.get('Price')

        yield wine_product

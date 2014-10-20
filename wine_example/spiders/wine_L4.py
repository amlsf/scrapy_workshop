# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from scrapy import Spider, Item, Field, Request
import re
import urlparse
import json

# CHALLENGE: Complete this section on your own at home. Part of it has already been set up for you.
# Crawl one more page deep to collect all reviews and ratings for each wine product


class WineReviewItem(Item):
    review = Field()
    rating = Field()


class WineItem(Item):
    link = Field()
    name = Field()
    price = Field()
    wine_type = Field()
    region = Field()

    customer_reviews = Field()  # list of WineReviewItems


class DrunkSpider(Spider):
    name = 'wine-demo-L4'
    start_urls = ['http://www.wine.com/v6/wineshop/default.aspx?state=CA&pagelength=100']

    def parse(self, response):
        """
        :type response: HtmlResponse
        """
        product_list = response.css('.productList')
        products = product_list.css('.verticalListItem')

        for product in products:
            wine_product = WineItem()

            # get product link
            links_list = product.css('.listProductName::attr(href)').extract()
            if not links_list:
                continue

            link = links_list[0]
            wine_product['link'] = urlparse.urljoin(response.url, link)

            # get name
            wine_name = product.css('.listProductName::text').extract()
            if wine_name:
                wine_product['name'] = wine_name[0]

            # get price
            price_list = product.css('[itemprop="price"]::text').extract()
            if price_list:
                current_price = price_list[0]
                wine_product['price'] = current_price

            # store data already collected in meta to pass to callback function to use
            meta = dict()
            meta['wine_item'] = wine_product

            request = Request(wine_product['link'], meta=meta, callback=self.parse_product_page)
            yield request

        # Pagination, keep going until there is no next page left
        next_page_list = response.css('.listPaging '
                              '#ctl00_BodyContent_ctrProducts_ctrPagingBottom_lnkNext::attr(href)').extract()
        if next_page_list:
            next_page_link = urlparse.urljoin(response.url, next_page_list[0])
            next_page_request = Request(next_page_link, callback=self.parse)
            yield next_page_request

    def parse_product_page(self, response):
        meta = response.meta
        if meta and 'wine_item' in meta:
            wine_product = meta['wine_item']
        else:
            return

        # get wine type field
        wine_type_list = response.css('.wine-icons span[class=offscreen]::text').extract()
        if wine_type_list:
            wine_type = wine_type_list[0]
            wine_product['wine_type'] = wine_type

        # get JSON from html to get region field
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

            # get region field
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

    @staticmethod
    def get_prod_reviews(response):
        # Fill in your code here
        pass

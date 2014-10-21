# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from scrapy import Spider, Item, Field, Request
import re
import urlparse
import json


class WineItem(Item):
    link = Field()
    name = Field()
    price = Field()
    wine_type = Field()
    region = Field()


class DrunkSpider(Spider):
    name = 'wine-demo-L3'
    # change the page to increase to 100 items per page
    start_urls = ['http://www.wine.com/v6/wineshop/default.aspx?state=CA&pagelength=100']

    def parse(self, response):
        """
        :type response: scrapy.http.HtmlResponse
        :rtype: scrapy.http.Request
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

            # store data already collected in meta to pass to callback function to use
            meta = dict()
            meta['wine_item'] = wine_product

            request = Request(wine_product['link'], meta=meta, callback=self.parse_product_page)
            yield request

        """
        <a id="ctl00_BodyContent_ctrProducts_ctrPagingBottom_lnkNext"
        href="/v6/wineshop/default.aspx?Nao=100">Next</a>

        Bottoms out at 5200:
        http://www.wine.com/v6/wineshop/default.aspx?state=CA&pagelength=100&Nao=5200
        """

        # Pagination, keep going until there is no next page left
        next_page_list = response.css('.listPaging a[id$=lnkNext]').xpath('@href').extract()
        if next_page_list:
            next_page_link = urlparse.urljoin(response.url, next_page_list[0])
            next_page_request = Request(next_page_link, callback=self.parse)
            yield next_page_request

    @staticmethod
    def parse_product_page(response):
        """
        :type response: scrapy.http.HtmlResponse
        :rtype: WineItem
        """
        meta = response.meta
        if meta and 'wine_item' in meta:
            wine_product = meta['wine_item']
        else:
            return

        # get wine type field
        wine_type_list = response.css('.wine-icons span[class=offscreen]').xpath('text()').extract()
        if wine_type_list:
            wine_type = wine_type_list[0]
            wine_product['wine_type'] = wine_type

        # get JSON from html using regex in order to retrieve Wine's 'field' region
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

            yield wine_product

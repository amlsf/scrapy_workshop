Scrapy Workshop Demo Spiders
============================

This repo contains Scrapy parsers demonstrated in Radius Intelligence's workshop "Data Collection with Scrapy: Build &amp; Manage Production Web Scraping Pipelines".

[Presentation materials available here](https://docs.google.com/a/radius.com/presentation/d/1QUbdzaI7fRwY1lspgCPnZ5as-NAZzBjYEsuyKrOIBlM/edit#slide=id.g26c11f2d3_02)

There are four scrapers (Level 1 - 4) that collect data about the wine products from www.wine.com. The tasks are broken out into approximately four levels:

* minimal.py spider: set up basic spider to fetch yahoo url
* L1 & L1_meta: Create a spider that creates an item type named 'Wine' containing link and product name fields for each wine product on the first page of 25 wine products at www.wine.com/v6/wineshop.
* L2: Add the following fields to the Wine item: price, wine type, region, tag data (the JSON object following "var utag_data" in the HTML of each product page)
* L3: Teach your spider to crawl through all pages to gather all 5000+ products
* L4: Teach your spider to crawl one more level deep to get all ratings and reviews for each product and store as a list of WineReview items in the Wine item's customer_review and ratings fields
* wine_login.py: create a login authentication aware spider


Development Environment Setup Instructions
------------------------------------------

* For those who do not have pip installed:
    * curl -O https://bootstrap.pypa.io/get-pip.py
    * sudo python get-pip.py (writes to system Python)
* Install & activate virtualenv
    * sudo pip install virtualenv (writes to system Python)
    * virtualenv scrapy_learn (isolated from system Python)
    * source scrapy_learn/bin/activate
* Install Scrapy & Dependencies
    * pip install wheel
    * pip install scrapy
* You will also need Chrome & Bash

Additional Resources
--------------------

* Scrapy Documentation
    * http://scrapy.org
* CSS Selectors
    * http://www.w3.org/TR/CSS2/selector.html
    * http://code.tutsplus.com/tutorials/the-30-css-selectors-you-must-memorize--net-16048
* XPath
    * http://zvon.org/comp/r/tut-XPath_1.html
* Regex
    * https://docs.python.org/2/library/re.html
* Beautiful Soup
    * http://www.crummy.com/software/BeautifulSoup/bs4/doc


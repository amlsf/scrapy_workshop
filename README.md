Scrapy Workshop Samples
=======================

This repo contains Scrapy parsers demonstrated in Radius Intelligence's workshop "Data Collection with Scrapy: Build &amp; Manage Production Web Scraping Pipelines".

[Presentation materials available here](https://docs.google.com/a/radius.com/presentation/d/1QUbdzaI7fRwY1lspgCPnZ5as-NAZzBjYEsuyKrOIBlM/edit#slide=id.g26c11f2d3_02)

There are four scrapers (Level 1 - 4) that collect data about the wine products from www.wine.com. The tasks are broken out into approximately four levels:

* minimal.py spider: set up basic spider crawling yahoo homepage
* L1 & L1_meta: Gets items containing link and product name fields
* L2: Add additional fields: price, wine type, region, tag data (stored as a JSON object in the HTML)
* L3: Add pagination to gather all 5000+ products
* L4: Get ratings and reviews


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


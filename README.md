Scrapy Workshop Demo Spiders
============================

This repo contains Scrapy spiders demo-ed in Radius Intelligence's workshop "Data Collection with Scrapy: Build &amp; Manage Production Web Scraping Pipelines".

####[Presentation materials available here](https://docs.google.com/a/radius.com/presentation/d/1QUbdzaI7fRwY1lspgCPnZ5as-NAZzBjYEsuyKrOIBlM/edit#slide=id.g26c11f2d3_02)

The spiders collect data about the wine products from www.wine.com and are broken out into levels that build new concepts on top of each other.

* __L0 (wine_example/spiders/L0_barespider.py)__
    * set up basic spider to fetch from wine.com url


* __L1 (wine_example/spiders/L1_wine.py)__
    * Create a spider that returns an item type named 'Wine' containing the fields: 1) the specific product page link, 2) product name, and 3) the current sell price. Only do this for the first page of 25 wine products at www.wine.com/v6/wineshop


* __L2 (wine_example/spiders/L2_wine_meta.py)__
    * Add to the Wine item the following fields: 1) wine type and 2) region.


* __L3 (wine_example/spiders/L3_wine_pagination.py)__
    * Teach your spider to crawl through all product pages to gather all 5000+ products


* __Wine_login.py (wine_example/spiders/wine_login.py)__
    * Create a login authentication aware spider



#####Take-Home Challenge:
* __L4 (wine_example/spiders/L4_wine_reviews.py)__
    * Complete this part on your own. Teach your spider to crawl one more page level deep to scrape all ratings and reviews for each product. Good luck and have fun!



Development Environment Setup Instructions
------------------------------------------

* For those who do not have pip installed:
```sh
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py # writes to system Python
```

* Install & activate virtualenv
```sh
sudo pip install virtualenv # writes to system Python
virtualenv scrapy_learn # isolated from system Python
source scrapy_learn/bin/activate
```

* Install Scrapy & Dependencies
```
pip install wheel
pip install scrapy
```

* You will also need Chrome

Additional Resources
--------------------

* Scrapy Documentation
    * http://doc.scrapy.org/en/0.24/
* CSS Selectors
    * http://www.w3.org/TR/CSS2/selector.html
    * http://code.tutsplus.com/tutorials/the-30-css-selectors-you-must-memorize--net-16048
* XPath
    * http://zvon.org/comp/r/tut-XPath_1.html
* Regex
    * https://docs.python.org/2/library/re.html
* Beautiful Soup
    * http://www.crummy.com/software/BeautifulSoup/bs4/doc


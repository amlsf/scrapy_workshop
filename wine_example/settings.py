# this is the name of the package, not a list of spiders
SPIDER_MODULES = ['wine_example.spiders']
# indicates where to put newly generated spiders
NEWSPIDER_MODULE = SPIDER_MODULES[0]
COOKIES_ENABLED = False
COOKIES_DEBUG = True

# BEGIN: slow down request settings for class
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
# CONCURRENT_REQUESTS_PER_IP = 1
DOWNLOAD_DELAY = 1.0  # seconds
# END: slow down request settings for class

DUPEFILTER_DEBUG = True

HTTPCACHE_ENABLED = True

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:33.0) Gecko/20100101 Firefox/33.0'

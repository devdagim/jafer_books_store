# Scrapy settings
SETTINGS = {
    # User Agent
    'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150\
        Safari/537.36',

    # Obey robots.txt rules
    'ROBOTSTXT_OBEY' : True,

    # Configure item pipelines
    'ITEM_PIPELINES' : {
        'telegram_bot.scraper.book.pipelines.BookPipeline': 300,
    },

    # Enable and configure the downloader middlewares
    #'DOWNLOADER_MIDDLEWARES' : {
    #    'myproject.middlewares.MyMiddleware': 543,
    #},

    # Configure the maximum concurrent requests performed by 
    # Scrapy (default: 16)
    'CONCURRENT_REQUESTS' : 16,

    # Configure the delay (in seconds) between consecutive requests to 
    # the same website (default: 0)
    'DOWNLOAD_DELAY' : 0,

    # Configure the maximum number of concurrent items being processed by 
    # each spider (default: 100)
    'CONCURRENT_ITEMS' : 100,

    # Configure the maximum depth limit for crawling requests (default: 0)
    'DEPTH_LIMIT' : 0,

    # Enable or disable cookies middleware (default: enabled)
    'COOKIES_ENABLED' : True,

    # Configure the maximum number of retries for failed requests (default: 2)
    'RETRY_TIMES' : 2,

    # Enable or disable Telnet console (default: disabled)
    'TELNETCONSOLE_ENABLED' : False,

    # Enable or disable DNS caching (default: enabled)
    'DNSCACHE_ENABLED' : True,

    # Configure the log level for Scrapy (default: 'DEBUG')
    'LOG_LEVEL' : 'DEBUG',

    # Configure the log file name (default: None)
    # LOG_FILE : 'scrapy.log'

    # Enable or disable the built-in stats collector (default: enabled)
    'STATS_ENABLED' : True,

    # Enable or disable the Retry middleware (default: enabled)
    'RETRY_ENABLED' : True,

    # Configure the maximum response size (in bytes) allowed by Scrapy 
    # (default: 10485760)
    'DOWNLOAD_MAXSIZE' : 10485760,

    # Enable or disable the AutoThrottle extension (default: disabled)
    'AUTOTHROTTLE_ENABLED' : False,

    # Configure the download timeout (in seconds) for requests made by 
    # Scrapy (default: 180)
    'DOWNLOAD_TIMEOUT' : 180,

    # Enable or disable the Redirect middleware (default: enabled)
    'REDIRECT_ENABLED' : True,

    # Enable or disable the Retry middleware (default: enabled)
    'RETRY_ENABLED' : True,
    
    #output setting
    'FEED_URI': 'book.json',
    'FEED_FORMAT': 'json',
    
    # logging
    'LOG_FILE': 'book_spider_scrapy.log',
    'LOG_LEVEL' : 'ERROR',
    
    # Set settings whose default value is deprecated to a future-proof value
    'REQUEST_FINGERPRINTER_IMPLEMENTATION' : "2.7",
    'TWISTED_REACTOR' : "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    'FEED_EXPORT_ENCODING' : "utf-8"
}

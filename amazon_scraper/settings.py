# Scrapy settings for amazon_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os
import dotenv
import logging

logging.getLogger("scrapy").setLevel(logging.WARNING)

dotenv.load_dotenv()


BOT_NAME = "amazon_scraper"

SPIDER_MODULES = ["amazon_scraper.spiders"]
NEWSPIDER_MODULE = "amazon_scraper.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "amazon_scraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# PLAYWRIGHT
# settings.py

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

PLAYWRIGHT_VIEWPORT = {"width": 1920, "height": 1080}  # Desktop viewport size

# END PLAYWRIGHT

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 2

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2.5
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 2

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "amazon_scraper.middlewares.AmazonScraperSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    "amazon_scraper.middlewares.AmazonScraperDownloaderMiddleware": 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "amazon_scraper.pipelines.DownloadFeaturedImagePipeline": 100,
    "amazon_scraper.pipelines.SaveToDatabasePipeline": 99,
    "amazon_scraper.pipelines.UpdateDescriptionPipeline": 99,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = False
# The initial download delay
AUTOTHROTTLE_START_DELAY = 0
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# amazon-scraper
READ_PRODUCT_CATEGORY_CONFIG_FROM_FILE = False

DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_SERVER = os.getenv("DATABASE_SERVER")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_PORT = os.getenv("DATABASE_PORT", "1433")
CONNECTION_PARAMS = {
    "dbname": DATABASE_NAME,
    "user": DATABASE_USERNAME,
    "password": DATABASE_PASSWORD,
    "host": DATABASE_SERVER,
    "port": DATABASE_PORT,
}


# proxy
DEFAULT_REQUEST_HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    "Sec-Ch-Ua-Platform": '"Windows"',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
}


import random


def generate_desktop_user_agent():
    os_platforms = [
        "Windows NT 10.0; Win64; x64",
        "Windows NT 6.1",
        "Macintosh; Intel Mac OS X 10_15",
        "X11; Linux x86_64",
    ]
    chrome_version = (
        "Chrome/"
        + str(random.randint(70, 93))
        + ".0."
        + str(random.randint(1000, 9999))
        + "."
        + str(random.randint(10, 99))
    )
    safari_version = (
        "Version/" + str(random.randint(10, 14)) + ".0" if random.random() > 0.5 else ""
    )
    user_agent = f"Mozilla/5.0 ({random.choice(os_platforms)}) AppleWebKit/537.36 (KHTML, like Gecko) {chrome_version} Safari/537.36 {safari_version}"
    return user_agent


# Generate new desktop user agents
# USER_AGENT_LIST = [generate_desktop_user_agent() for _ in range(10)]

USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
]


from pathlib import Path

## Insert Your List of Proxies Here
ROTATING_PROXY_LIST = Path("./proxy-ips.txt").read_text().split("\n")


## Enable The Proxy Middleware In Your Downloader Middlewares
DOWNLOADER_MIDDLEWARES = {
    # ...
    "rotating_proxies.middlewares.RotatingProxyMiddleware": 610,
    "rotating_proxies.middlewares.BanDetectionMiddleware": 620,
    # ...
}

DUPEFILTER_DEBUG = False

FOCUS_CATEGORIES_REF_CODES = [
    "FASHION_MEN",
    # "BEAUTY_SKIN_CARE",
    # "FASHION_WOMEN",
    # "BOOKS_BIOGRAPHIES_AND_MEMOIRS",
    # "BOOKS_LITERATURE_AND_FICTION",
    # "BOOKS_MIND_BODY_AND_SPIRIT",
    # "BOOKS_PERSONAL_FINANCE",
    # "BOOKS_BUSINESS_DEVELOPMENT_ENTREPRENUERSHIP",
    # "BOOKS_DIGITAL_LIFESTYLE",
    # "BOOKS_COMPUTING_AND_INTERNET_FOR_PROFESSIONALS",
    # "BOOKS_CHRISTIAN_LIVING",
]

TOTAL_REVIEWS_PAGE_PER_PRODUCT = 10
MAX_PRODUCTS_AT_A_TIME = 2

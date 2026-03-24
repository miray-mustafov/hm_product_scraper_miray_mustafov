import os
from dotenv import load_dotenv

load_dotenv()

PROXY_USER, PROXY_PASS = os.getenv('PROXY_USER'), os.getenv('PROXY_PASS')
PROXY_HOST, PROXY_PORT = os.getenv('PROXY_HOST'), os.getenv('PROXY_PORT')
PROXIES = {
    'http': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}',
    'https': f'https://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}',
}

BOT_NAME = "hm_scraper"

SPIDER_MODULES = ["hm_scraper.spiders"]
NEWSPIDER_MODULE = "hm_scraper.spiders"

ADDONS = {}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# how Scrapy introduces itself to websites
# Scrapy/Version (+https://scrapy.org)  # basically tells hello I am a bot

# OVERRIDE Scrapy's default User Agent
# USER_AGENT = (  # this "ID card" is passed along with the request to a website
#     "Mozilla/5.0 "  # tells to server "I am a modern browser"
#     "(Windows NT 10.0; Win64; x64) "  # specifies the os
#     "AppleWebKit/537.36 "  # specifies the "engine" that renders the site
#     "(KHTML, like Gecko) "
#     "Chrome/122.0.0.0 "  # specifies a recent version of Chrome
#     "Safari/537.36"  # tells, "Also compatible with Safari"
# )

# Obey robots.txt rules
ROBOTSTXT_OBEY = False  # set to false to try avoid bot detection

# Concurrency and throttling settings
# CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:

# DEFAULT_REQUEST_HEADERS = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'Accept-Language': 'en-US,en;q=0.9',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'DNT': '1',
#     'Connection': 'keep-alive',
#     'Upgrade-Insecure-Requests': '1',
#     'Sec-Fetch-Dest': 'document',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-Site': 'none',
#     'Cache-Control': 'max-age=0',
# }

# REMOVE Default request headers entirely (let impersonate handle it)
# The new Asyncio Event Loop is REQUIRED for curl_cffi / impersonate to work properly!

DOWNLOADER_MIDDLEWARES = {
    "hm_scraper.middlewares.HmScraperDownloaderMiddleware": 100,

    # Must be None to prevent conflicts
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    "hm_scraper.pipelines.HmScraperPipeline": 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"
FEED_EXPORT_INDENT = 2  # set the number of spaces per indent level for the JSON output

import os
from dotenv import load_dotenv

load_dotenv()

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": os.getenv('BROWSER_LAUNCH_HEADLESS', False),
}

DB_PARAMS = {
    'dialect': os.getenv('DB_DIALECT'),
    'driver': os.getenv('DB_DRIVER'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'host': os.getenv('DB_HOST'),
    'dbname': os.getenv('DB_NAME'),
    'port': os.getenv('DB_PORT'),
    'db_connection_timeout': os.getenv('DB_CONNECTION_TIMEOUT'),
}

BOT_NAME = "hm_scraper"

SPIDER_MODULES = ["hm_scraper.spiders"]
NEWSPIDER_MODULE = "hm_scraper.spiders"

ADDONS = {}

ROBOTSTXT_OBEY = False  # to avoid bot detection

CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1

DOWNLOADER_MIDDLEWARES = {
    # "hm_scraper.middlewares.HmScraperDownloaderMiddleware": 543,

    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # turn off scrapy's default user agent
    # provides 2k+ common user agents, which are looped through and attached to a request until success is achieved
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

ITEM_PIPELINES = {
    # "hm_scraper.pipelines.HmScraperPipeline": 300,
    "hm_scraper.pipelines.SaveToRDBMSPipeline": 300,
}

FEED_EXPORT_ENCODING = "utf-8"
FEED_EXPORT_INDENT = 2  # set the number of spaces per indent level for the JSON output

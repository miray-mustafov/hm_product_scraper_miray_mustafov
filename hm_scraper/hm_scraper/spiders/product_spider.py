import scrapy


class ProductSpider(scrapy.Spider):
    name = "product_spider"
    allowed_domains = ["hm.com"]
    start_urls = ["https://www2.hm.com/bg_bg/productpage.1274171042.html"]

    def parse(self, response):
        pass

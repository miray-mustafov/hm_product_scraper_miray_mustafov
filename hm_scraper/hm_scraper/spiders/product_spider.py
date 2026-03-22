import scrapy
from .utils import get_proxy_url
from ..settings import PROXY_DOMAIN


class ProductSpider(scrapy.Spider):
    name = "product_spider"
    allowed_domains = ["hm.com", PROXY_DOMAIN]
    start_urls = ["https://www2.hm.com/bg_bg/productpage.1274171042.html"]
    # start_urls = ["https://www.chocolate.co.uk/collections/all"]  # test url

    # # an attempt to apply proxy but it either is too slow or returns Internal Server Error 500
    # def start_requests(self):
    #     """
    #     To define how the initial requests should be started
    #     The reason is to apply a proxy to avoid bot detection
    #     Generator preferred to process urls one by one and not load all at ones, which is not memory efficient
    #     """
    #     yield scrapy.Request(
    #         url=get_proxy_url(self.start_urls[0]),
    #         callback=self.parse  # on successful page download, pass the HTML result to the parse method
    #     )

    def parse(self, response):
        print()
        print()
        print(response.text[:100])
        print()
        print()
        return response

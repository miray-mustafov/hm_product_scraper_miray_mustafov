import scrapy
import json
from decimal import Decimal
from ..items import HmProductItem
from ..utils import yield_urls_for_scraping


class FallbackProductSpider(scrapy.Spider):
    """
    The spider that scrapes from the raw HTML
    """

    name = "fallback_product_spider"
    allowed_domains = ["hm.com"]  # restricts this spider to hm.com so it does not crawl other domains by accident

    def start_requests(self):
        """
        Defining which pages the spider should crawl
        scrapy.Request the raw HTML response from the server behind that specific url
        If you want to get the rendered HTML after js run, then use browser renderer like Playwright
        """
        for url in yield_urls_for_scraping():
            yield scrapy.Request(
                url=url,
                callback=self.parse,  # callback is the function that will handle the response when it is received
            )

    def parse(self, response):  # parse, extract, convert
        """
        This method extracts the product data from the current response/page, building an item product
        """
        item = HmProductItem()
        data: dict = self._get_response_data_as_dict(response)

        item['name'] = data.get('name')
        item['price']: Decimal = self._get_price(response)
        item['current_color'] = self._get_current_color(response)
        item['available_colors'] = self._get_available_colors(data)

        yield self._request_reviews_to_apply_count_and_score(response, item)

    def _request_reviews_to_apply_count_and_score(self, response, item) -> scrapy.Request:
        """
        Requesting ugcsummary endpoint to get current product reviews data
        """
        sku: str = self._get_current_product_sku(response)
        reviews_url = f"https://www2.hm.com/bg_bg/reviews/rrs/ugcsummary?sku={sku}"

        return scrapy.Request(
            url=reviews_url,
            callback=self._parse_item_reviews,
            meta={"item": item},
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

    @staticmethod
    def _parse_item_reviews(response):
        """
        This method takes the reviews response, reads the JSON, and updates the current item
        """
        item = response.meta["item"]
        data = json.loads(response.text)[0]

        item["reviews_count"] = int(data.get("ratings", 0))
        item["reviews_score"] = float(data.get("averageRating", 0.0))

        yield item

    @staticmethod
    def _get_current_product_sku(response) -> str:
        """
        SKU = Stock Keeping Unit (an id that shows the specific variant of a product) = 1274171042001
        [1274171]+[042]+[001] = [product_id]+[color_id(Бял/Fleuri)]+[size_id(XXS)]
        """
        XXS_size_code = '001'  # noticed that H&M always pick the smallest size when requesting ugcsummary
        product_and_color_code = response.url.split('productpage.')[1].split('.html')[0]
        if not product_and_color_code or not XXS_size_code:
            raise ValueError("❌ Error: SKU could not be generated")

        sku = product_and_color_code + XXS_size_code
        return sku

    @staticmethod
    def _get_response_data_as_dict(response) -> dict:
        """convert the raw JSON string to python dicts, lists, etc."""

        json_data_str = response.xpath(  # find tag <script> with id="product-group-schema"
            '//script[@id="product-group-schema"]/text()'  # /text() is to give the raw JSON data
        ).get()
        if not json_data_str:
            raise ValueError("❌ Error: JSON data not found on the page")

        data = json.loads(json_data_str)
        return data

    @staticmethod
    def _get_price(response) -> Decimal:
        price_text = response.css('span[data-testid="white-price"]::text').get()
        if not price_text:
            raise ValueError("❌ Error: Price not found on the page.")

        price_string = price_text.split(' ')[-2]
        price_comma_replaced = price_string.replace(',', '.')
        price = Decimal(price_comma_replaced)
        return price

    @staticmethod
    def _get_current_color(response):
        title = response.xpath('//title/text()').get()
        if not title or ' - ' not in title:
            raise ValueError("❌ Error: Problem with getting current color")

        return title.split(' - ')[1].split(' - ')[0]

    @staticmethod
    def _get_available_colors(data):  # O(n)
        variants = data.get('hasVariant', [])
        colors = set()  # set structure to eliminate duplicates efficiently with O1 lookups
        for v in variants:
            if v.get('color'):
                colors.add(v.get('color'))

        return list(colors)

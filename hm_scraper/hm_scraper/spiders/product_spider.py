import scrapy
import json
from decimal import Decimal
from ..items import HmProductItem


class ProductSpider(scrapy.Spider):
    name = "product_spider"
    allowed_domains = ["hm.com"]
    start_urls = ["https://www2.hm.com/bg_bg/productpage.1274171042.html"]

    @staticmethod
    def _get_response_data_as_dict(response) -> dict:
        """
        convert the raw JSON string to python dicts, lists, etc.
        """
        json_data_str = response.xpath(  # find tag <script> with id="product-group-schema"
            '//script[@id="product-group-schema"]/text()'  # /text() is to give the raw JSON data
        ).get()
        data = json.loads(json_data_str)
        return data

    @staticmethod
    def _get_price(response) -> Decimal:
        price_text = response.css('span[data-testid="white-price"]::text').get()
        price_string = price_text.split(' ')[-2]
        price_comma_replaced = price_string.replace(',', '.')
        price = Decimal(price_comma_replaced)
        return price

    @staticmethod
    def _get_current_color(response):
        title = response.xpath('//title/text()').get()
        if title and ' - ' in title:
            return title.split(' - ')[1].split(' - ')[0]
        return None

    @staticmethod
    def _get_available_colors(data):  # O(n)
        variants = data.get('hasVariant', [])
        colors = set()  # set structure to eliminate the duplicated
        for v in variants:
            if v.get('color'):
                colors.add(v.get('color'))

        return list(colors)

    @staticmethod
    def _get_current_product_sku(response) -> str:
        """
        SKU = Stock Keeping Unit (an id that shows the specific variant of a product) = 1274171042001
        [1274171]+[042]+[001] = [product_id]+[color_id(Бял/Fleuri)]+[size_id(XXS)]
        """
        XXS_size_code = '001'  # noticed that H&M always pick the smallest size when requesting ugcsummary
        product_and_color_code = response.url.split('productpage.')[1].split('.html')[0]
        sku = product_and_color_code + XXS_size_code
        return sku

    @staticmethod
    def _parse_item_reviews(response):
        item = response.meta["item"]
        data = json.loads(response.text)[0]

        item["reviews_count"] = int(data.get("reviews", 0))
        item["reviews_score"] = float(data.get("averageRating", 0.0))

        yield item

    def _request_reviews_to_apply_count_and_score(self, response, item) -> scrapy.Request:
        sku: str = self._get_current_product_sku(response)
        return scrapy.Request(
            url=f"https://www2.hm.com/bg_bg/reviews/rrs/ugcsummary?sku={sku}",
            callback=self._parse_item_reviews,
            meta={"item": item},
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

    def parse(self, response):  # parse = extract, convert
        item = HmProductItem()
        data: dict = self._get_response_data_as_dict(response)

        item['name'] = data.get('name')
        item['price']: Decimal = self._get_price(response)
        item['current_color'] = self._get_current_color(response)
        item['available_colors'] = self._get_available_colors(data)

        yield self._request_reviews_to_apply_count_and_score(response, item)

import scrapy
import re
from decimal import Decimal
from ..items import HmProductItem
from ..utils import yield_urls_for_scraping


class ProductSpider(scrapy.Spider):
    """
    The spider that scrapes from browser rendered HTML
    """

    name = "product_spider"
    allowed_domains = ["hm.com"]

    def start_requests(self):
        for url in yield_urls_for_scraping():
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                }
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]  # get the live browser page object
        # to ensure that we will have the colors available for extraction
        await page.wait_for_selector('div[data-testid="color-selector-wrapper"] div[data-testid="grid"]')
        content = await page.content()
        selector = scrapy.Selector(text=content)

        item = HmProductItem()
        item['name'] = self._get_name(selector)
        item['price'] = self._get_price(selector)
        item['current_color'] = self._get_current_color(selector)
        item['available_colors'] = self._get_available_colors(selector)
        item['reviews_count'] = self._get_reviews_count(selector)
        item['reviews_score'] = self._get_reviews_score(selector)

        await page.close()
        yield item

    @staticmethod
    def _get_name(selector):
        name = selector.css('h1::text').get().strip()
        if not name:
            raise ValueError("❌ Error: Problem getting current name")

        return name

    @staticmethod
    def _get_price(selector) -> Decimal:
        price_text = selector.css('span[data-testid="white-price"]::text').get()
        pattern = r'[\d,]+(?=\s*€)'

        try:
            price_str = re.search(pattern, price_text).group().replace(',', '.')
            price = Decimal(price_str)
        except Exception:
            raise ValueError("❌ Error: Problem getting current price")

        return price

    @staticmethod
    def _get_current_color(selector):
        current_color = selector.css(
            'section[data-testid="color-selector"] p::text'
        ).get()
        if not current_color:
            raise ValueError("❌ Error: Problem getting current color")

        return current_color

    @staticmethod
    def _get_available_colors(selector):
        available_colors = selector.xpath('//div[@data-testid="grid"]//a[@role="radio"]/@title').getall()

        if not available_colors:
            raise ValueError("❌ Error: Problem getting available colors")

        available_colors = [color.strip() for color in available_colors if color]
        return available_colors

    @staticmethod
    def _get_reviews_count(selector) -> int:
        try:
            reviews_count_label = selector.xpath(
                '//div[@data-testid="product-reviews"]//button[contains(@aria-label, "Коментари")]/@aria-label'
            ).get()
            reviews_count_str = re.search(r"(?<=\[)\d+(?=\])", reviews_count_label).group()
            reviews_count = int(reviews_count_str)
        except Exception:
            raise ValueError("❌ Error: Problem getting reviews count")

        return reviews_count

    @staticmethod
    def _get_reviews_score(selector) -> float:
        try:
            reviews_score_text = selector.xpath(
                '//div[@data-testid="product-reviews"]//button[@data-testid="reviews-summary-button"]/@title'
            ).get()
            reviews_score = float(reviews_score_text)
        except ValueError:
            raise ValueError("❌ Error: Problem getting reviews score")

        return reviews_score

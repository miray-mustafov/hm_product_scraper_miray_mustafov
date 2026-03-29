from decimal import Decimal

import scrapy

from hm_scraper.spiders.product_spider import ProductSpider


def test_product_spider_get_name():
    spider = ProductSpider()
    html = "<h1>Test Product</h1>"
    selector = scrapy.Selector(text=html)
    assert spider._get_name(selector) == "Test Product"


def test_product_spider_get_price():
    spider = ProductSpider()
    html = '<span data-testid="white-price">9,99 €</span>'
    selector = scrapy.Selector(text=html)
    assert spider._get_price(selector) == Decimal("9.99")


def test_product_spider_get_current_color():
    spider = ProductSpider()
    html = '<section data-testid="color-selector"><p>Black</p></section>'
    selector = scrapy.Selector(text=html)
    assert spider._get_current_color(selector) == "Black"


def test_product_spider_get_available_colors():
    spider = ProductSpider()
    html = """
    <div data-testid="grid">
        <a role="radio" title="Black"></a>
        <a role="radio" title="White"></a>
    </div>
    """
    selector = scrapy.Selector(text=html)
    colors = spider._get_available_colors(selector)
    assert colors == ["Black", "White"]


def test_product_spider_get_reviews_count():
    spider = ProductSpider()
    html = """
    <div data-testid="product-reviews">
        <button aria-label="Коментари [10]"></button>
    </div>
    """
    selector = scrapy.Selector(text=html)
    assert spider._get_reviews_count(selector) == 10


def test_product_spider_get_reviews_score():
    spider = ProductSpider()
    html = """
    <div data-testid="product-reviews">
        <button data-testid="reviews-summary-button" title="4.5"></button>
    </div>
    """
    selector = scrapy.Selector(text=html)
    assert spider._get_reviews_score(selector) == 4.5

import json
from decimal import Decimal
from unittest.mock import MagicMock, patch

import scrapy
from scrapy.http import HtmlResponse

from hm_scraper.spiders.fallback_product_spider import FallbackProductSpider


def test_fallback_spider_get_price():
    spider = FallbackProductSpider()
    html = '<span data-testid="white-price">9,99 лв.</span>'
    response = HtmlResponse(url="http://hm.com", body=html, encoding="utf-8")

    price = spider._get_price(response)
    assert price == Decimal("9.99")


def test_fallback_spider_get_current_color():
    spider = FallbackProductSpider()
    html = "<title>Product Name - Black - H&M</title>"
    response = HtmlResponse(url="http://hm.com", body=html, encoding="utf-8")

    color = spider._get_current_color(response)
    assert color == "Black"


def test_fallback_spider_get_available_colors():
    spider = FallbackProductSpider()
    data = {
        "hasVariant": [
            {"color": "Black"},
            {"color": "White"},
            {"color": "Black"},  # Duplicate
        ]
    }
    colors = spider._get_available_colors(data)
    assert len(colors) == 2
    assert "Black" in colors
    assert "White" in colors


def test_fallback_spider_get_response_data_as_dict():
    spider = FallbackProductSpider()
    json_data = {"name": "Test Product"}
    html = f'<script id="product-group-schema" type="application/ld+json">{json.dumps(json_data)}</script>'
    response = HtmlResponse(url="http://hm.com", body=html, encoding="utf-8")

    data = spider._get_response_data_as_dict(response)
    assert data == json_data


def test_fallback_spider_get_current_product_sku():
    spider = FallbackProductSpider()
    response = MagicMock()
    response.url = "https://www2.hm.com/bg_bg/productpage.1274171042.html"

    sku = spider._get_current_product_sku(response)
    assert sku == "1274171042001"


def test_fallback_spider_parse():
    spider = FallbackProductSpider()
    response = MagicMock(spec=HtmlResponse)
    response.url = "https://www2.hm.com/bg_bg/productpage.1274171042.html"

    with patch.object(
        spider,
        "_get_response_data_as_dict",
        return_value={"name": "Test Product", "hasVariant": []},
    ):
        with patch.object(spider, "_get_price", return_value=Decimal("9.99")):
            with patch.object(spider, "_get_current_color", return_value="Black"):
                with patch.object(
                    spider, "_get_available_colors", return_value=["Black"]
                ):
                    with patch.object(
                        spider, "_request_reviews_to_apply_count_and_score"
                    ) as mock_request_method:
                        mock_request_method.return_value = scrapy.Request(
                            "http://reviews.com"
                        )

                        results = list(spider.parse(response))

                        assert len(results) == 1
                        assert isinstance(results[0], scrapy.Request)
                        mock_request_method.assert_called_once()


def test_fallback_spider_parse_item_reviews(mock_item):
    spider = FallbackProductSpider()
    response = MagicMock()
    response.meta = {"item": mock_item}
    response.text = json.dumps([{"ratings": 5, "averageRating": 4.5}])

    results = list(spider._parse_item_reviews(response))

    assert len(results) == 1
    item = results[0]
    assert item["reviews_count"] == 5
    assert item["reviews_score"] == 4.5

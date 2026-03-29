from unittest.mock import MagicMock

import pytest

from hm_scraper.items import HmProductItem


@pytest.fixture
def mock_item():
    return HmProductItem(
        name="Test Product",
        price=9.99,
        current_color="Black",
        available_colors=["Black", "White"],
        reviews_count=10,
        reviews_score=4.5,
    )


@pytest.fixture
def mock_spider():
    spider = MagicMock()
    spider.name = "test_spider"
    spider.logger = MagicMock()
    return spider


@pytest.fixture
def mock_db_service(mocker):
    db_service_mock = MagicMock()
    mocker.patch("hm_scraper.pipelines.DatabaseService", return_value=db_service_mock)
    return db_service_mock

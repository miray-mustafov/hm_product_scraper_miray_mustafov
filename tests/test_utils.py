from unittest.mock import mock_open, patch

from hm_scraper.utils import yield_urls_for_scraping


def test_yield_urls_for_scraping():
    mock_content = "http://test1.com\nhttp://test2.com\n"
    # Using patch for Path.exists and Path.open
    with patch("hm_scraper.utils.Path.exists", return_value=True):
        with patch("hm_scraper.utils.Path.open", mock_open(read_data=mock_content)):
            urls = list(yield_urls_for_scraping())
            assert len(urls) == 2
            assert urls[0] == "http://test1.com"
            assert urls[1] == "http://test2.com"


def test_yield_urls_for_scraping_empty():
    mock_content = ""
    with patch("hm_scraper.utils.Path.exists", return_value=True):
        with patch("hm_scraper.utils.Path.open", mock_open(read_data=mock_content)):
            urls = list(yield_urls_for_scraping())
            assert len(urls) == 0


def test_yield_urls_for_scraping_skips_empty_lines():
    mock_content = "http://test1.com\n\n  \nhttp://test2.com"
    with patch("hm_scraper.utils.Path.exists", return_value=True):
        with patch("hm_scraper.utils.Path.open", mock_open(read_data=mock_content)):
            urls = list(yield_urls_for_scraping())
            assert len(urls) == 2
            assert urls[0] == "http://test1.com"
            assert urls[1] == "http://test2.com"

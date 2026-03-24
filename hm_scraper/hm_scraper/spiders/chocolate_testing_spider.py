import scrapy


class ChocolateSpider(scrapy.Spider):
    name = "chocolate_testing_spider"
    allowed_domains = ["www.chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]
    COMMANDS = """
    uv run scrapy crawl chocolate_testing_spider -O results/chocolate_data_result.json
    """

    def parse(self, response):
        print('\n' * 10)
        print(response.text[:10])
        print('\n' * 10)

        for product in response.css('product-item'):
            yield {
                'name': product.css('.product-item-meta__title::text').get(),
                'price': product.css('.price::text').get(),
                'url': product.css('.product-item-meta__title::attr(href)').get(),
                'image': product.css('.product-item__primary-image::attr(src)').get(),
            }

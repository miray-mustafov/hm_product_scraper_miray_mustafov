# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HmProductItem(scrapy.Item):
    """
    This class defines a template for our main Product/Item
    Why: to enforce a frame what our product should look like to avoid mistakes
    An instance provides a dictionary-like behavior with extra metadata info
    """
    name = scrapy.Field()
    price = scrapy.Field()
    current_color = scrapy.Field()
    available_colors = scrapy.Field()
    reviews_count = scrapy.Field()
    reviews_score = scrapy.Field()

from .database import DatabaseService


class SaveToRDBMSPipeline:
    def __init__(self):
        self.db_service = DatabaseService()

    def open_spider(self, spider):
        """Initialize DB connection and prepare the table when the spider starts."""
        is_db_connected = self.db_service.connect()
        is_table_created = self.db_service.create_or_replace_products_table()

        if is_db_connected and is_table_created:
            spider.logger.info("✅ Database connection successful and products table is initialized.")
        else:
            spider.logger.error("❌ Failed to initialize database connection.")

    def close_spider(self):
        self.db_service.close()

    def process_item(self, item, spider):
        if self.db_service.save_product(item):
            spider.logger.info("✅ Saving to DB successful.")
        else:
            spider.logger.error("❌ Error saving to DB.")

        return item

# from itemadapter import ItemAdapter
# class HmScraperPipeline:
#     def process_item(self, item, spider):
#         return item

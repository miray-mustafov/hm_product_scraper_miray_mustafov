import psycopg
from .settings import DB_PARAMS


class SaveToRDBMSPipeline:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def open_spider(self, spider):
        """Initialize connection when the spider starts."""
        # todo: move db logic to separate module
        try:
            self.connection = psycopg.connect(
                user=DB_PARAMS['user'],
                password=DB_PARAMS['password'],
                host=DB_PARAMS['host'],
                dbname=DB_PARAMS['dbname'],
                port=DB_PARAMS['port'],
                connect_timeout=4,
            )
            self.cursor = self.connection.cursor()
            spider.logger.info("✅ Database connection successful.")
        except Exception as e:
            spider.logger.error(f"❌ Failed to initialize database connection: {e}")

    def close_spider(self, spider):
        """Close connection when the spider finishes."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def process_item(self, item, spider):
        if not self.connection or not self.cursor:
            return item

        try:
            self.cursor.execute(
                """
                INSERT INTO products (name, current_color, price, reviews_count, reviews_score)
                VALUES (%s, %s, %s, %s, %s)
                """, (
                    item.get('name'),
                    item.get('current_color'),
                    item.get('price'),
                    item.get('reviews_count', 0),
                    item.get('reviews_score', 0.0)
                )
            )
            self.connection.commit()
            spider.logger.info("✅ Saving to DB successful.")
        except Exception as e:
            spider.logger.error(f"❌ Error saving to DB: {e}")
            self.connection.rollback()

        return item

# from itemadapter import ItemAdapter
# class HmScraperPipeline:
#     def process_item(self, item, spider):
#         return item

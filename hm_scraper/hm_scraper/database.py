import psycopg

from .settings import DB_PARAMS


class DatabaseService:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg.connect(
                user=DB_PARAMS["user"],
                password=DB_PARAMS["password"],
                host=DB_PARAMS["host"],
                dbname=DB_PARAMS["dbname"],
                port=DB_PARAMS["port"],
                connect_timeout=DB_PARAMS["db_connection_timeout"],
            )
            self.cursor = self.connection.cursor()
            return True
        except Exception:
            return False

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def save_product(self, item):
        if not self.connection or not self.cursor:
            return False

        try:
            self.cursor.execute(
                """
                INSERT INTO products (name, current_color, price, reviews_count, reviews_score)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    item.get("name"),
                    item.get("current_color"),
                    item.get("price"),
                    item.get("reviews_count", 0),
                    item.get("reviews_score", 0.0),
                ),
            )
            self.connection.commit()
            return True
        except Exception:
            self.connection.rollback()
            return False

    def create_or_replace_products_table(self):
        if not self.connection or not self.cursor:
            return False

        try:
            self.cursor.execute(
                """
                DROP TABLE IF EXISTS products;
                CREATE TABLE IF NOT EXISTS products
                (
                    product_db_id SERIAL PRIMARY KEY,
                    name          TEXT,
                    current_color TEXT,
                    price         NUMERIC(10, 2),
                    reviews_count INTEGER DEFAULT 0,
                    reviews_score REAL    DEFAULT 0.0
                );
                """
            )
            self.connection.commit()
            return True
        except Exception:
            self.connection.rollback()
            return False

    def drop_products_table(self):
        if not self.connection or not self.cursor:
            return False

        try:
            self.cursor.execute("DROP TABLE IF EXISTS products;")
            self.connection.commit()
            return True
        except Exception:
            self.connection.rollback()
            return False

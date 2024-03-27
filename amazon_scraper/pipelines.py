# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from pathlib import Path
import httpx
import psycopg2

from amazon_scraper.items import ProductItem, ReviewItem, UpdateProductDescriptionItem
from amazon_scraper.settings import CONNECTION_PARAMS

from loguru import logger

from psycopg2.extensions import connection as PsycopgConnection
from psycopg2.extensions import cursor as PsycopgCursor


class SaveToDatabasePipeline:

    def __init__(self) -> None:
        self.tag = f"[{self.__class__.__name__}]: "
        logger.info(f"{self.tag}Connecting to SQL database...")
        self.conn: PsycopgConnection = psycopg2.connect(**CONNECTION_PARAMS)
        self.cursor: PsycopgCursor = self.conn.cursor()

    def open_spider(self, spider):
        logger.info(f"{self.tag}Creating table if not exists.")
        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS products
                (
                    data_asin TEXT PRIMARY KEY,
                    data_uuid TEXT,
                    total_customer_that_rated INTEGER,
                    ratings REAL,
                    config_category_ref_code TEXT,
                    amazon_result_page_number INTEGER,
                    amazon_result_page_position INTEGER,
                    name TEXT,
                    price REAL,
                    currency TEXT,
                    product_page_url TEXT,
                    customer_reviews_url TEXT,
                    img_url TEXT,
                    date_scraped DATE,
                    category TEXT,
                    sub_category TEXT,
                    description TEXT,
                    image_data BYTEA
                )
            """
        )
        self.conn.commit()

        self.cursor.execute(
            """ 
                CREATE TABLE IF NOT EXISTS reviews
                (
                    review_id TEXT PRIMARY KEY,
                    product_asin TEXT ,
                    review_location TEXT,
                    review_date TEXT,
                    review_title TEXT,
                    helpful_vote TEXT,
                    review_rating TEXT,
                    position_on_page INTEGER,
                    date_scraped DATE,
                    review_content TEXT,
                    page_url TEXT,
                    
                    FOREIGN KEY (product_asin) REFERENCES products(data_asin)
                )
        
        """
        )

        self.conn.commit()

    def process_item(self, item, spider):

        item_keys = item.keys()
        parameters = "".join(["%s, " for a in item_keys])[
            :-2
        ]  # removing the last comma
        columns = ", ".join([a for a in item_keys])
        values = tuple([item[key] for key in item_keys])

        if issubclass(ProductItem, type(item)):
            logger.info("Inserting into products table.")
            self.cursor.execute(
                f"INSERT INTO products ({columns}) VALUES ({parameters}) ON CONFLICT (data_asin) DO NOTHING",
                values,
            )
            self.conn.commit()

        elif issubclass(ReviewItem, type(item)):
            logger.info("Inserting into reviews table.")
            self.cursor.execute(
                f"INSERT INTO reviews ({columns}) VALUES ({parameters}) ON CONFLICT (review_id) DO NOTHING",
                values,
            )
            self.conn.commit()

        return item

    def close_spider(self, spider):
        self.conn.close()


class DownloadFeaturedImagePipeline:

    def __init__(self) -> None:
        self.tag = f"[{self.__class__.__name__}]: "
        logger.info(f"{self.tag}Connecting to SQL database...")
        self.conn: PsycopgConnection = psycopg2.connect(**CONNECTION_PARAMS)
        self.cursor: PsycopgCursor = self.conn.cursor()

    def save_image_to_database(
        self, product_uuid: str, image_data: bytes, table_name: str = "products"
    ):
        self.cursor.execute(
            f"UPDATE {table_name} SET image_data = %s WHERE data_uuid = %s",
            (psycopg2.Binary(image_data), product_uuid),
        )
        self.conn.commit()

    def process_item(self, item, spider):

        if issubclass(ProductItem, type(item)):
            # download the featured image
            _item: ProductItem = item

            category = _item["category"]
            img_url = _item["img_url"]
            sub_category = _item["sub_category"]
            data_uuid = _item["data_uuid"]

            response = httpx.get(str(img_url))
            if not response.is_success:
                logger.error(
                    f"{self.tag}Unable to download image {img_url}. {response.status_code} {response.content}"
                )

            directory = f"./products/{category}/{sub_category}"
            os.makedirs(directory, exist_ok=True)

            # Save the image blob into the database
            self.save_image_to_database(
                data_uuid, response.content, table_name="products"
            )
            Path(f"{directory}/{data_uuid}.jpeg").write_bytes(response.content)
            logger.success(f"{self.tag}Downloaded {data_uuid}.jpeg")

        return item


class UpdateDescriptionPipeline:

    def __init__(self) -> None:
        self.tag = f"[{self.__class__.__name__}]: "
        logger.info(f"{self.tag}Connecting to SQL database...")
        self.conn: PsycopgConnection = psycopg2.connect(**CONNECTION_PARAMS)
        self.cursor: PsycopgCursor = self.conn.cursor()

    def save_image_to_database(
        self, product_uuid: str, image_data: bytes, table_name: str = "products"
    ):
        self.cursor.execute(
            f"UPDATE {table_name} SET image_data = %s WHERE data_uuid = %s",
            (psycopg2.Binary(image_data), product_uuid),
        )
        self.conn.commit()

    def process_item(self, item, spider):

        if isinstance(item, UpdateProductDescriptionItem):
            _item: UpdateProductDescriptionItem = item

            if "description" not in item:
                return item

            logger.warning(
                f"Updating {_item['data_asin']} with description {len(item['description'])}"
            )

            sql_stmt = f"""
                UPDATE products 
                SET description = %s
                WHERE data_asin = %s;
            """

            self.cursor.execute(
                sql_stmt,
                (
                    item["description"],
                    item["data_asin"],
                ),
            )
            self.conn.commit()

            logger.success(f"{self.tag}Updated {item['data_asin']}")

        return item

from typing import Iterable
import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy_playwright.page import PageMethod
from playwright.async_api._generated import Page
from amazon_scraper.config import get_config
import psycopg2

from amazon_scraper.items import ProductItem, UpdateProductDescriptionItem
from amazon_scraper.settings import (
    CONNECTION_PARAMS,
    READ_PRODUCT_CATEGORY_CONFIG_FROM_FILE,
    USER_AGENT_LIST,
)

from loguru import logger

import random


from psycopg2.extensions import connection as PsycopgConnection
from psycopg2.extensions import cursor as PsycopgCursor


def get_user_agent():
    return {"User-Agent": USER_AGENT_LIST[random.randint(0, len(USER_AGENT_LIST) - 1)]}


class DescriptionsSpider(scrapy.Spider):
    name = "descriptions"
    allowed_domains = ["amazon.co.uk"]
    start_urls = ["https://amazon.co.uk"]

    pages = get_config(from_file=READ_PRODUCT_CATEGORY_CONFIG_FROM_FILE)

    def __init__(self, name: str | None = None, **kwargs):
        super().__init__(name, **kwargs)

        self.tag = f"[{self.__class__.__name__}]: "
        logger.info(f"{self.tag}Connecting to SQL database...")
        self.conn: PsycopgConnection = psycopg2.connect(**CONNECTION_PARAMS)
        self.cursor: PsycopgCursor = self.conn.cursor()

    def start_requests(self) -> Iterable[scrapy.Request]:
        for page_config in self.pages:
            products_bag = []
            ref_code = page_config["unique_ref_code"]
            self._current_page_config = page_config
            column_names = ", ".join([item for item in ProductItem.fields.keys()])

            self.cursor.execute(
                f"SELECT {column_names} FROM products WHERE config_category_ref_code = %s AND (description IS NULL OR description = '');",
                (ref_code,),
            )

            results = self.cursor.fetchall()
            for result in results:
                # for r in result:
                product_dict = dict()
                for index, value in enumerate(result):
                    _key = [item_key for item_key in ProductItem.fields.keys()][index]
                    product_dict[_key] = value

                products_bag.append(product_dict)

            logger.success(f"NO_OF_PRODUCTS {ref_code} -  {len(products_bag)}")

            # load this page and fetch more css selector from the new image to add to the item item
            expand_elements = self._current_page_config["product_page"][
                "expand_elements"
            ]

            js_script = ""
            for _expand_element in expand_elements:
                style = _expand_element["style"]
                js_action = _expand_element["js_action"]
                js_script += f"document.querySelectorAll('{style}').forEach((e) => e.{js_action}());"

            logger.error(js_script)

            for product_item in products_bag:
                yield scrapy.Request(
                    product_item["product_page_url"],
                    meta=dict(
                        product_item=product_item,
                        playwright=True,
                        playwright_include_page=True,
                        playwright_page_methods=[
                            PageMethod("wait_for_load_state", "load"),
                            PageMethod(
                                "evaluate",
                                "window.scroll(0, window.document.body.scrollHeight)",
                            ),
                            PageMethod("evaluate", js_script),
                        ],
                        errback=self.errback,
                    ),
                    headers={**get_user_agent()},
                )

    async def errback(self, failure):
        logger.error("Failure")
        logger.error(failure)
        page: Page = failure.request.meta["playwright_page"]
        await page.close()

    async def parse(  # type: ignore
        self,
        response: HtmlResponse,
    ):

        page: Page = response.meta["playwright_page"]
        await page.close()

        product_item = response.meta["product_item"]
        product_descriptors = self._current_page_config["product_page"][
            "product_descriptors"
        ]

        description = ""
        for _product_descriptor in product_descriptors:
            _description = response.css(_product_descriptor).get()
            if _description:
                description += _description

        product_item["description"] = description

        yield UpdateProductDescriptionItem(**product_item)

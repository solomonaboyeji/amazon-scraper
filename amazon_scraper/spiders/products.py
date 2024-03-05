import datetime
from typing import Iterable
import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy_playwright.page import PageMethod
from playwright.async_api._generated import Page
from scrapy.loader import ItemLoader
from amazon_scraper.config import get_config

from amazon_scraper.items import ProductItem
from amazon_scraper.settings import READ_PRODUCT_CATEGORY_CONFIG_FROM_FILE

import random

user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "",
]


class ProductSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["amazon.co.uk"]
    pages_scraped: int = 0
    pages_browsed: int = 0

    base_url: str = "https://amazon.co.uk"

    pages = get_config(from_file=READ_PRODUCT_CATEGORY_CONFIG_FROM_FILE)

    def start_requests(self) -> Iterable[scrapy.Request]:
        # pages = get_config(from_file=READ_PRODUCT_CATEGORY_CONFIG_FROM_FILE)
        for index, page_config in enumerate(self.pages):
            current_url = page_config["url"]
            self._current_page_config = page_config
            yield scrapy.Request(
                current_url,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod("wait_for_load_state", "load"),
                    ],
                    errback=self.errback,
                    headers={
                        "User-Agent": user_agent_list[
                            random.randint(0, len(user_agent_list) - 1)
                        ]
                    },
                ),
            )

            ## myspider.py

    async def errback(self, failure):
        page: Page = failure.request.meta["playwright_page"]
        await page.close()

    async def parse(  # type: ignore
        self,
        response: HtmlResponse,
    ):

        page: Page = response.meta["playwright_page"]
        await page.close()

        base_url = self._current_page_config["base_url"]
        unique_ref_code = self._current_page_config["unique_ref_code"]

        maximum_pages = self._current_page_config["maximum_pages"]
        next_page_style = self._current_page_config["styles"]["next_page_href_style"]
        next_page = response.css(next_page_style).get()

        base_component_css = self._current_page_config["styles"]["base_style"]
        html_elements = response.css(base_component_css)

        category_style = self._current_page_config["styles"]["category"]
        category = response.css(category_style).get()

        sub_category_style = self._current_page_config["styles"]["sub_category"]
        sub_category = response.css(sub_category_style).get()

        element_styles = self._current_page_config["styles"]["elements"]
        self.pages_browsed += 1

        if self.pages_browsed >= self._current_page_config["start_page"]:
            self.pages_scraped += 1
            for index, element in enumerate(html_elements):

                item = ItemLoader(item=ProductItem(), selector=element)

                item.add_value("category", category)
                item.add_value("config_category_ref_code", unique_ref_code)
                item.add_value("amazon_result_page_position", index + 1)
                item.add_value("amazon_result_page_number", self.pages_browsed)
                item.add_value("sub_category", sub_category)
                item.add_value("date_scraped", datetime.datetime.today())

                for key, value in element_styles.items():
                    if value.get("get_text", True):
                        scraped_value = element.css(value["target_style"]).get()
                        if value.get("prefix_to_base_url", False):
                            scraped_value = f"{self.base_url}{scraped_value}"

                        item.add_value(key, scraped_value)
                    else:
                        item.add_css(key, value["target_style"])

                item_loaded = item.load_item()

                yield item_loaded

            print("*" * 100)
            print(
                f"Pages Scraped: {self.pages_scraped} \n Total Products: {len(html_elements)}"
            )
            print("*" * 100)

        if next_page is not None and self.pages_scraped < maximum_pages:
            next_page_url = f"{base_url}{next_page}"
            yield scrapy.Request(
                next_page_url,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod("wait_for_load_state", "load"),
                    ],
                    errback=self.errback,
                ),
            )

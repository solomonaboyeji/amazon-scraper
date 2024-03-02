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


class ProductSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["amazon.co.uk"]
    pages_scraped: int = 0
    pages_browsed: int = 0

    base_url: str = "https://amazon.co.uk"

    def start_requests(self) -> Iterable[scrapy.Request]:
        pages = get_config(from_file=READ_PRODUCT_CATEGORY_CONFIG_FROM_FILE)
        for index, page_config in enumerate(pages):
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
                ),
            )

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

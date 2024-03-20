import datetime
from typing import Iterable
import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy_playwright.page import PageMethod
from playwright.async_api._generated import Page
from scrapy.loader import ItemLoader
from amazon_scraper.config import get_config

from amazon_scraper.items import ProductItem
from amazon_scraper.settings import (
    READ_PRODUCT_CATEGORY_CONFIG_FROM_FILE,
    USER_AGENT_LIST,
)

from loguru import logger

import random


def get_user_agent():
    return {"User-Agent": USER_AGENT_LIST[random.randint(0, len(USER_AGENT_LIST) - 1)]}


class ProductSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["amazon.co.uk"]

    base_url: str = "https://amazon.co.uk"

    pages = get_config(from_file=READ_PRODUCT_CATEGORY_CONFIG_FROM_FILE)

    def start_requests(self) -> Iterable[scrapy.Request]:

        for index, page_config in enumerate(self.pages):
            current_url = page_config["url"]

            yield scrapy.Request(
                current_url,
                meta=dict(
                    pages_scraped=0,
                    pages_browsed=0,
                    current_page_config=page_config,
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod("wait_for_load_state", "load"),
                        # PageMethod("wait_for_selector", ".s-pagination-next"),
                        PageMethod(
                            "evaluate",
                            "window.scroll(0, window.document.body.scrollHeight)",
                        ),
                    ],
                    errback=self.errback,
                ),
                headers={**get_user_agent()},
            )

    async def errback(self, failure):
        page: Page = failure.request.meta["playwright_page"]
        await page.close()

    async def parse(  # type: ignore
        self,
        response: HtmlResponse,
    ):

        pages_scraped = response.meta["pages_scraped"]
        pages_browsed = response.meta["pages_browsed"]

        page: Page = response.meta["playwright_page"]
        # Set viewport size to simulate desktop
        await page.set_viewport_size({"width": 1920, "height": 1080})
        await page.reload()

        current_page_config = response.meta["current_page_config"]

        base_url = current_page_config["base_url"]

        unique_ref_code = current_page_config["unique_ref_code"]
        logger.info(unique_ref_code + " " + base_url)

        maximum_pages = current_page_config["maximum_pages"]
        next_page_style = current_page_config["styles"]["next_page_href_style"]

        next_page = response.css(next_page_style).get()
        try:
            await page.screenshot(
                type="jpeg",
                full_page=True,
                path=f"./screenshots/screenshot{pages_browsed}.jpeg",
            )
        except Exception as e:
            logger.error("!!!!!NO SCREENSHOT")
            logger.error(str(e))
            print(await page.content())

        await page.close()

        base_component_css = current_page_config["styles"]["base_style"]
        html_elements = response.css(base_component_css)

        config_category = current_page_config["category"]
        category_style = current_page_config["styles"]["category"]
        category = response.css(category_style).get(default=config_category)

        sub_category_style = current_page_config["styles"]["sub_category"]
        sub_category = response.css(sub_category_style).get(
            default=f"Sub {config_category}"
        )

        element_styles = current_page_config["styles"]["elements"]
        pages_browsed += 1

        if next_page is None:
            logger.info("Getting next page with method 2")
            logger.info(
                f'.s-pagination-item.s-pagination-button-accessibility[aria-label="Go to page {pages_browsed + 1}"]'
            )
            next_page = response.css(
                f'.s-pagination-item.s-pagination-button-accessibility[aria-label="Go to page {pages_browsed + 1}"]::attr(href)'
            ).get()

            next_page_text = response.css(
                f'.s-pagination-item.s-pagination-button-accessibility[aria-label="Go to page {pages_browsed + 1}"]::text'
            ).get()
            logger.info(f"NEXT PAGE: {next_page_text} {next_page}")

        if pages_browsed >= current_page_config["start_page"]:
            pages_scraped += 1

            for index, element in enumerate(html_elements):

                item = ItemLoader(item=ProductItem(), selector=element)

                item.add_value("category", category)
                item.add_value("config_category_ref_code", unique_ref_code)
                item.add_value("amazon_result_page_position", index + 1)
                item.add_value("amazon_result_page_number", pages_browsed)
                item.add_value("sub_category", sub_category)
                item.add_value("date_scraped", datetime.datetime.today())

                for key, value in element_styles.items():
                    if value.get("get_text", True):
                        scraped_value = element.css(value["target_style"]).get()
                        if scraped_value:
                            if value.get("prefix_to_base_url", False):
                                scraped_value = f"{self.base_url}{scraped_value}"

                        item.add_value(key, scraped_value)
                    else:
                        item.add_css(key, value["target_style"])

                item_loaded = item.load_item()
                yield item_loaded

            print("*" * 100)
            print(
                f"Pages Scraped: {pages_scraped} \n Total Products: {len(html_elements)}"
            )
            print("*" * 100)
        logger.error(next_page)
        logger.error(f"{pages_scraped}/{pages_browsed}")
        logger.error(maximum_pages)
        if next_page is not None and pages_scraped < maximum_pages:
            next_page_url = f"{base_url}{next_page}"
            yield response.follow(
                next_page_url,
                callback=self.parse,
                meta=dict(
                    pages_scraped=pages_scraped,
                    pages_browsed=pages_browsed,
                    current_page_config=current_page_config,
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod("wait_for_load_state", "load"),
                        # PageMethod("wait_for_selector", ".s-pagination-next"),
                        PageMethod(
                            "evaluate",
                            "window.scroll(0, window.document.body.scrollHeight)",
                        ),
                    ],
                    errback=self.errback,
                ),
                headers={**get_user_agent()},
            )

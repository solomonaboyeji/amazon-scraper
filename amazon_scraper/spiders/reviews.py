import datetime
from typing import Iterable
import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy_playwright.page import PageMethod
from playwright.async_api._generated import Page
from scrapy.loader import ItemLoader
from amazon_scraper.config import get_config

from amazon_scraper.items import ProductItem, ReviewItem, UpdateProductDescriptionItem
from amazon_scraper.settings import (
    CONNECTION_PARAMS,
    FOCUS_CATEGORIES_REF_CODES,
    MAX_PRODUCTS_AT_A_TIME,
    READ_PRODUCT_CATEGORY_CONFIG_FROM_FILE,
    TOTAL_REVIEWS_PAGE_PER_PRODUCT,
    USER_AGENT_LIST,
)

from loguru import logger

import random


import psycopg2
from psycopg2.extensions import connection as PsycopgConnection
from psycopg2.extensions import cursor as PsycopgCursor


def get_user_agent():
    return {"User-Agent": USER_AGENT_LIST[random.randint(0, len(USER_AGENT_LIST) - 1)]}


class ReviewsSpider(scrapy.Spider):
    name = "reviews"
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
            if (
                FOCUS_CATEGORIES_REF_CODES
                and not page_config["unique_ref_code"] in FOCUS_CATEGORIES_REF_CODES
            ):
                continue

            products_bag = []
            ref_code = page_config["unique_ref_code"]
            column_names = [
                "data_uuid",
                "customer_reviews_url",
                "total_customer_that_rated",
                "ratings",
                "data_asin",
                "name",
            ]

            # Get products we have not scrap reviews for
            self.cursor.execute(
                f"""SELECT {', '.join(column_names)} FROM products 
                    LEFT JOIN reviews ON reviews.product_asin = products.data_asin
                    WHERE config_category_ref_code = %s AND customer_reviews_url IS NOT NULL AND reviews.review_content IS NULL
                    ORDER BY products.date_scraped;
                    """,
                (ref_code,),
            )

            results = self.cursor.fetchall()
            for result in results:
                product_dict = dict()
                for index, value in enumerate(result):
                    _key = [item_key for item_key in column_names][index]
                    product_dict[_key] = value

                products_bag.append(product_dict)

            if len(products_bag) == 0:
                logger.success(f"Reviews Scrap Completed for {ref_code}")
                exit()

            logger.success(f"NO_OF_PRODUCTS {ref_code} -  {len(products_bag)}")
            for product_item in products_bag[0:MAX_PRODUCTS_AT_A_TIME]:
                yield scrapy.Request(
                    product_item["customer_reviews_url"],
                    meta=dict(
                        pages_scraped=0,
                        pages_browsed=0,
                        current_page_config=page_config,
                        product_item=product_item,
                        playwright=True,
                        playwright_include_page=True,
                        playwright_page_methods=[
                            PageMethod("wait_for_load_state", "load"),
                            PageMethod(
                                "evaluate",
                                "window.scroll(0, window.document.body.scrollHeight)",
                            ),
                            PageMethod(
                                "wait_for_selector",
                                '[data-hook="see-all-reviews-link-foot"]',
                            ),
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
        current_page_config = response.meta["current_page_config"]
        base_url = current_page_config["base_url"]
        unique_ref_code = current_page_config["unique_ref_code"]
        product_item = response.meta["product_item"]

        pages_scraped = response.meta["pages_scraped"]
        pages_browsed = response.meta["pages_browsed"]

        # page: Page = response.meta["playwright_page"]
        # # Set viewport size to simulate desktop
        # await page.set_viewport_size({"width": 1920, "height": 1080})
        # await page.reload()

        # await page.close()

        see_all_button = response.css(
            '[data-hook="see-all-reviews-link-foot"] ::attr(href)'
        ).get()
        logger.error(f"SEE ALL BUTTON {see_all_button} ")

        scrap_reviews = True
        end_scraping = False
        if see_all_button is not None:
            # do not scrap the first time, go to the view all page
            scrap_reviews = False

            next_page_url = f"{base_url}{see_all_button}"
            logger.warning("Going to the view all page ")
            selector_to_wait_for = ".reviews-content"
        else:
            next_url = response.css(".a-last a::attr(href)").get()
            if not next_url:
                end_scraping = True
                scrap_reviews = False

            next_page_url = f"{base_url}{next_url}"
            selector_to_wait_for = ".a-last"
            logger.warning("Going to the next page ")

        logger.warning(
            f"Scraping Reviews next_page_button -{see_all_button} | \n\n end_scraping - {end_scraping} | scrap_reviews - {scrap_reviews} | \n\n pages_browsed - {pages_browsed} | pages_scraped - {pages_scraped} / {TOTAL_REVIEWS_PAGE_PER_PRODUCT} "
        )
        logger.warning("*" * 100)

        if scrap_reviews:
            pages_scraped += 1
            reviews_elements = response.css('[data-hook="review"]')
            logger.success("Scraping Items")
            for index, review_element in enumerate(reviews_elements):
                logger.error(str(index))

                review_item = ItemLoader(item=ReviewItem(), selector=review_element)

                review_item.add_css("review_date", '[data-hook="review-date"] ::text')
                review_item.add_css(
                    "review_location", '[data-hook="review-date"] ::text'
                )
                review_item.add_css(
                    "review_content", '[data-hook="review-body"] ::text'
                )
                review_item.add_css(
                    "helpful_vote", '[data-hook="helpful-vote-statement"]::text'
                )
                review_item.add_css(
                    "review_rating", '[data-hook="review-star-rating"] span ::text'
                )
                review_item.add_css(
                    "review_title", '[data-hook="review-title"] :nth-child(3)::text'
                )
                review_item.add_value("product_asin", product_item["data_asin"])
                review_item.add_value("page_url", response.url)
                review_item.add_css("review_id", "::attr(id)")
                review_item.add_value("position_on_page", index + 1)
                review_item.add_value("date_scraped", datetime.datetime.today())

                yield review_item.load_item()

            # since we are on the same page, why not scrap more reviews in other stars

            # &sortBy=helpful
            # &sortBy=recent

            # &filterByStar=positive
            # &filterByStar=critical
            # &filterByStar=two_star
            # &filterByStar=three_star
            # &filterByStar=four_star
            # &filterByStar=five_star

            filters = [
                "positive",
                "critical",
                "one_star",
                "two_star",
                "three_star",
                "four_star",
                "five_star",
            ]
            sorts = ["helpful", "recent"]

            current_url = response.url

            for filter_by in filters:
                for sort_by in sorts:
                    follow_url = (
                        f"{current_url}?filterByStar={filter_by}&sortBy={sort_by}"
                    )
                    logger.info(f"Filtering Reviews: Following URL -> {follow_url}")
                    yield response.follow(
                        follow_url,
                        callback=self.parse,
                        meta=dict(
                            pages_scraped=pages_scraped,
                            pages_browsed=pages_browsed,
                            product_item=product_item,
                            current_page_config=current_page_config,
                            unique_ref_code=unique_ref_code,
                            playwright=True,
                            playwright_include_page=True,
                            playwright_page_methods=[
                                PageMethod("wait_for_load_state", "load"),
                                PageMethod(
                                    "evaluate",
                                    "window.scroll(0, window.document.body.scrollHeight)",
                                ),
                                # PageMethod("wait_for_selector", selector_to_wait_for),
                            ],
                            errback=self.errback,
                        ),
                        headers={**get_user_agent()},
                    )

        logger.warning(
            not end_scraping or int(pages_browsed) <= TOTAL_REVIEWS_PAGE_PER_PRODUCT
        )
        logger.warning(end_scraping)
        logger.warning(pages_browsed <= TOTAL_REVIEWS_PAGE_PER_PRODUCT)
        if not end_scraping or int(pages_browsed) <= TOTAL_REVIEWS_PAGE_PER_PRODUCT:
            pages_browsed += 1  # a page is browsed only if we scraped from it
            logger.success(
                f"Pages Browsed Increased ->  {pages_browsed} GOING TO {next_page_url}"
            )

            yield scrapy.Request(
                next_page_url,
                callback=self.parse,
                meta=dict(
                    pages_scraped=pages_scraped,
                    pages_browsed=pages_browsed,
                    product_item=product_item,
                    current_page_config=current_page_config,
                    unique_ref_code=unique_ref_code,
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod("wait_for_load_state", "load"),
                        PageMethod(
                            "evaluate",
                            "window.scroll(0, window.document.body.scrollHeight)",
                        ),
                        # PageMethod("wait_for_selector", selector_to_wait_for),
                    ],
                    errback=self.errback,
                ),
                headers={**get_user_agent()},
            )

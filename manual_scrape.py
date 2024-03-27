import datetime
import json
import random
from time import sleep
import time
from typing import List, Union
from bs4 import BeautifulSoup
from loguru import logger
from pathlib import Path
from playwright.async_api import async_playwright, Page, ProxySettings
from selectolax.parser import Node, HTMLParser
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags


import psycopg2
from psycopg2.extensions import connection as PsycopgConnection
from psycopg2.extensions import cursor as PsycopgCursor

from amazon_scraper.config import get_config
from amazon_scraper.items import (
    ReviewItem,
    filter_review_date,
    filter_review_location,
    remove_control_characters,
)
from amazon_scraper.settings import (
    CONNECTION_PARAMS,
    FOCUS_CATEGORIES_REF_CODES,
    MAX_PRODUCTS_AT_A_TIME,
    READ_PRODUCT_CATEGORY_CONFIG_FROM_FILE,
    ROTATING_PROXY_LIST,
)


class ManualScrape:
    def __init__(self) -> None:
        self.tag = f"[{self.__class__.__name__}]: "
        logger.info(f"{self.tag}Connecting to SQL database...")
        self.conn: PsycopgConnection = psycopg2.connect(**CONNECTION_PARAMS)
        self.cursor: PsycopgCursor = self.conn.cursor()

        self.pages = get_config(from_file=READ_PRODUCT_CATEGORY_CONFIG_FROM_FILE)

    def start(self):
        for page_config in self.pages:
            base_url = page_config["base_url"]

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
                    ORDER BY products.date_scraped
                    LIMIT {MAX_PRODUCTS_AT_A_TIME};
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
            for product_item in products_bag:
                self.init_scrap_review_for_product(product_item, base_url)
                logger.info("Resting for 10 seconds ..")
                sleep(10)

    async def init_scrap_review_for_product(self, product_item: dict, base_url):
        product_url = product_item["customer_reviews_url"]
        browser_headless = False

        async with async_playwright() as p:
            browser = p.chromium.launch(headless=browser_headless)
            logger.info(f"Browser Connected: { browser.is_connected()}")
            page: Union[None, Page] = None
            proxy_selected = False
            while not proxy_selected:
                for _ip_address in ROTATING_PROXY_LIST:
                    logger.info(f"Trying: {_ip_address}")
                    browser = p.chromium.launch(
                        headless=browser_headless,
                        proxy=ProxySettings(server=_ip_address),
                    )
                    try:
                        page = browser.new_page()
                        await page.goto(product_url)
                        proxy_selected = True
                        break
                    except Exception as e:
                        logger.error(e)

            if page is None:
                exit()

            page.goto(product_url)
            page.evaluate("() => window.scroll(0, document.body.scrollHeight)")
            page.wait_for_load_state("domcontentloaded")

            html = page.inner_html("body")

            node = HTMLParser(html)
            nodes: List[Node] = node.css('[data-hook="see-all-reviews-link-foot"]')

            for selector_item in nodes:
                see_more_link = f"{base_url}/{selector_item.attrs.get('href')}"
                logger.debug(see_more_link)
                if see_more_link:
                    page.goto(see_more_link, wait_until="domcontentloaded")
                    html = page.inner_html("body")
                    node = HTMLParser(html)
                    break

            reviews_elements = node.css('[data-hook="review"]')

            logger.success("Scraping Items")
            # Get the next button URL
            next_button_node = node.css(".a-last a")
            current_url = page.url

            logger.success("Page 1")
            product_reviews = self.parse_page(
                current_url=current_url,
                page=page,
                product_item=product_item,
                reviews_elements=reviews_elements,
            )
            if next_button_node:
                next_button_node = next_button_node[0]
                for page_count in range(2, 10):
                    follow_url = f"{current_url}&pageNumber={page_count}"
                    logger.info(f"\n\nGoing to the next page: {follow_url}")
                    logger.success(f"Page {page_count}")
                    page.goto(
                        follow_url,
                        wait_until="domcontentloaded",
                    )

                    page.goto(follow_url, wait_until="domcontentloaded")
                    reviews_elements = HTMLParser(page.inner_html("body")).css(
                        '[data-hook="review"]'
                    )

                    if not len(reviews_elements):
                        break

                    product_reviews.extend(
                        self.parse_page(
                            current_url=current_url,
                            page=page,
                            product_item=product_item,
                            reviews_elements=reviews_elements,
                        )
                    )
                    time.sleep(random.randint(0, 5))

    def parse_page(
        self,
        current_url: str,
        page: Page,
        product_item: dict,
        reviews_elements: List[Node],
    ):
        filters = [
            "one_star",
            "two_star",
            "three_star",
            "four_star",
            "five_star",
        ]
        page_reviews = []
        for filter_by in filters:
            prefix = "?" if len(current_url.split("?")) == 0 else "&"
            follow_url = f"{current_url}{prefix}filterByStar={filter_by}"

            page.goto(follow_url, wait_until="domcontentloaded")
            reviews_elements = HTMLParser(page.inner_html("body")).css(
                '[data-hook="review"]'
            )

            if not len(reviews_elements):
                break

            sleep(2)
            page_reviews.extend(
                self.parse_content(
                    reviews_elements=reviews_elements,
                    product_item=product_item,
                    page=page,
                )
            )

        return page_reviews

    def process_item(self, item: dict):
        item_keys = item.keys()
        parameters = "".join(["%s, " for a in item_keys])[
            :-2
        ]  # removing the last comma
        columns = ", ".join([a for a in item_keys])
        values = tuple([item[key] for key in item_keys])

        logger.info("Inserting into reviews table.")
        self.cursor.execute(
            f"INSERT INTO reviews ({columns}) VALUES ({parameters}) ON CONFLICT (review_id) DO NOTHING",
            values,
        )
        self.conn.commit()

        return item

    def parse_content(self, reviews_elements, product_item: dict, page: Page):
        current_url = page.url
        reviews = []

        for index, review_element in enumerate(reviews_elements):
            review_item = dict()

            review_item["review_date"] = filter_review_date(
                review_element.css('[data-hook="review-date"]').pop().text()
            )
            review_item["review_location"] = filter_review_location(
                review_element.css('[data-hook="review-date"]').pop().text()
            )
            review_item["review_content"] = str.strip(
                filter_review_location(
                    review_element.css('[data-hook="review-body"]').pop().text()
                )
            )
            if review_element.css('[data-hook="helpful-vote-statement"]'):
                review_item["helpful_vote"] = filter_review_location(
                    review_element.css('[data-hook="helpful-vote-statement"]')
                    .pop()
                    .text()
                )
            else:
                review_item["helpful_vote"] = None

            if review_element.css('[data-hook="review-star-rating"] span'):
                review_item["review_rating"] = filter_review_location(
                    review_element.css('[data-hook="review-star-rating"] span')
                    .pop()
                    .text()
                )

            if review_element.css('[data-hook="review-title"] :nth-child(3)'):
                review_item["review_title"] = str.strip(
                    remove_tags(
                        remove_control_characters(
                            review_element.css(
                                '[data-hook="review-title"] :nth-child(3)'
                            )
                            .pop()
                            .text()
                        )
                    )
                )

            review_item["product_asin"] = product_item["data_asin"]
            review_item["page_url"] = current_url
            review_item["review_id"] = review_element.attrs.get("id")
            review_item["position_on_page"] = index + 1
            review_item["date_scraped"] = str(datetime.datetime.today().date())

            logger.success(
                review_item["review_id"]
                + " "
                + review_item["review_title"]
                + " "
                + current_url
                + "\n\n"
            )

            from pathlib import Path

            all_reviews = json.loads(Path("./results.json").read_text())
            all_reviews = [review_item].append(all_reviews)
            Path("./results.json").write_text(f"")
            Path("./results.json").write_text(json.dumps(all_reviews))

            self.process_item(item=review_item)
            reviews.append(review_item)

        return reviews


if __name__ == "__main__":
    scrape_obj = ManualScrape()
    scrape_obj.start()

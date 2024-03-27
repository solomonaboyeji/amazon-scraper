# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import datetime
import string
import scrapy

from markdownify import markdownify as md
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

import re


def pick_float_number(input_string: str):
    # Regular expression to extract the float number
    float_number_match = re.search(r"(\d+\.\d+)", input_string)

    if float_number_match:
        return float(float_number_match.group(1))
    else:
        return input_string


def take_high_resolution(item: list):
    try:
        return item[0].split(" ")[-2]
    except IndexError:
        return item[0].split(" ")[-1]


def format_name(item: list):
    return item


def format_date_scraped(date: datetime.datetime):
    return f"{date.strftime('%Y-%m-%d')}"


def parse_to_int(input_str: str):
    matched = re.findall(r"(\d+)", input_str)
    try:
        if not matched:
            return input_str
        return int(str("".join(matched)))
    except ValueError:
        print(f"Unable to parse {input_str} ({matched}) to int")
        return input_str


def filter_review_date(review_date_text):
    # Regex pattern to match the date in "day month year" format
    date_pattern = r"\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b"
    result = re.findall(date_pattern, review_date_text)
    if result:
        return result[0]

    return review_date_text


def filter_review_location(review_date_text):
    # Regex pattern to match everything between "Reviewed in" and "on"
    pattern = r"Reviewed in(.*?)on"

    # Using re.search() to find the match
    match = re.search(pattern, review_date_text)

    if match:
        extracted_text = match.group(1).strip()
        return extracted_text
    else:
        return review_date_text


def remove_control_characters(text: str):
    # control_characters = "".join(
    #     c for c in text if c in string.printable and c not in string.ascii_letters
    # )
    return text.replace("\n", "")


def filter_helpful_vote(helpful_text: str):
    if helpful_text.lower().startswith("one"):
        return 1

    number_pattern = r"\b\d+\b"
    # Using re.search() to find the first occurrence of the number in the text
    match = re.search(number_pattern, helpful_text)
    if match:
        number = match.group()
        return number

    return helpful_text


def filter_review_rating(review_rating_text: str):
    return review_rating_text.split(" out of 5 stars")[0]


class ReviewItem(scrapy.Item):
    review_id = scrapy.Field(output_processor=TakeFirst())
    product_asin = scrapy.Field(output_processor=TakeFirst())
    review_location = scrapy.Field(
        input_processor=MapCompose(filter_review_location),
        output_processor=TakeFirst(),
    )
    review_date = scrapy.Field(
        input_processor=MapCompose(filter_review_date), output_processor=TakeFirst()
    )
    helpful_vote = scrapy.Field(
        input_processor=MapCompose(filter_helpful_vote), output_processor=TakeFirst()
    )
    review_rating = scrapy.Field(
        input_processor=MapCompose(filter_review_rating),
        output_processor=TakeFirst(),
    )
    position_on_page = scrapy.Field(output_processor=TakeFirst())

    review_title = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_control_characters, str.strip),
        output_processor=lambda content: " ".join(content),
    )
    review_content = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_control_characters, str.strip),
        output_processor=lambda content: " ".join(content),
    )
    page_url = scrapy.Field(output_processor=TakeFirst())
    date_scraped = scrapy.Field(
        input_processor=MapCompose(format_date_scraped),
        output_processor=TakeFirst(),
    )


class ProductItem(scrapy.Item):
    config_category_ref_code = scrapy.Field(output_processor=TakeFirst())
    amazon_result_page_number = scrapy.Field(output_processor=TakeFirst())
    amazon_result_page_position = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(
        input_processor=MapCompose(
            remove_tags,
            format_name,
        ),
        output_processor=TakeFirst(),
    )
    data_uuid = scrapy.Field(
        input_processor=MapCompose(
            remove_tags,
            str.strip,
        ),
        output_processor=TakeFirst(),
    )
    data_asin = scrapy.Field(
        input_processor=MapCompose(
            remove_tags,
            str.strip,
        ),
        output_processor=TakeFirst(),
    )
    ratings = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, pick_float_number),
        output_processor=TakeFirst(),
    )
    total_customer_that_rated = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, parse_to_int),
        output_processor=TakeFirst(),
    )
    price = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, pick_float_number),
        output_processor=TakeFirst(),
    )
    currency = scrapy.Field(
        input_processor=MapCompose(
            remove_tags,
            str.strip,
        ),
        output_processor=TakeFirst(),
    )
    product_page_url = scrapy.Field(
        output_processor=TakeFirst(),
    )
    customer_reviews_url = scrapy.Field(
        output_processor=TakeFirst(),
    )
    img_url = scrapy.Field(
        output_processor=take_high_resolution,
    )
    date_scraped = scrapy.Field(
        input_processor=MapCompose(format_date_scraped),
        output_processor=TakeFirst(),
    )
    category = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst(),
    )
    sub_category = scrapy.Field(
        input_processor=MapCompose(
            remove_tags,
            str.strip,
        ),
        output_processor=TakeFirst(),
    )


class UpdateProductDescriptionItem(ProductItem):
    description = scrapy.Field(
        # input_processor=MapCompose(md),
        output_processor=TakeFirst()
    )

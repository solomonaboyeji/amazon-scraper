# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import datetime
import scrapy

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
    return item[0].split(" ")[-2]


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

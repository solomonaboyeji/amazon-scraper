import json
import os
from pathlib import Path


scrap_config: list[dict] = [
    {
        "category": "Beauty",
        "sub_category": "Skin Care",
        "maximum_pages": 1,
        "start_page": 3,
        "base_url": "https://amazon.co.uk",
        "url": "https://www.amazon.co.uk/s?rh=n%3A118464031&fs=true&ref=lp_118464031_sar",
        "styles": {
            "next_page_href_style": ".s-pagination-next::attr(href)",
            "base_style": '#search [data-component-type*="s-search-result"]',
            "category": "#departments .s-navigation-item :nth-child(2)::text",
            "sub_category": "#departments .s-navigation-indent-1 span span::text",
            "elements": {
                "data_asin": {
                    "prefix_to_base_url": False,
                    "get_text": False,
                    "target_style": "::attr(data-asin)",
                },
                "data_uuid": {
                    "prefix_to_base_url": False,
                    "get_text": False,
                    "target_style": "::attr(data-uuid)",
                },
                "img_url": {
                    "prefix_to_base_url": False,
                    "get_text": False,
                    "target_style": "img::attr(srcset)",
                },
                "name": {
                    "prefix_to_base_url": False,
                    "get_text": False,
                    "target_style": '[data-cy="title-recipe"] h2 a span',
                },
                "currency": {
                    "prefix_to_base_url": False,
                    "get_text": False,
                    "target_style": '[data-cy="price-recipe"] .a-price-symbol',
                },
                "price": {
                    "prefix_to_base_url": False,
                    "base_style_child": True,
                    "get_text": False,
                    "target_style": '[data-cy="price-recipe"] .a-price span',
                },
                "product_page_url": {
                    "prefix_to_base_url": True,
                    "base_style_child": True,
                    "get_text": True,
                    "target_style": '[data-cy="title-recipe"] h2 a ::attr(href)',
                },
                "customer_reviews_url": {
                    "prefix_to_base_url": True,
                    "base_style_child": True,
                    "get_text": True,
                    "target_style": 'span[aria-label*="out of 5 stars"] + span a::attr(href)',
                },
                "ratings": {
                    "prefix_to_base_url": False,
                    "base_style_child": True,
                    "get_text": False,
                    "target_style": 'span[aria-label*="out of 5 stars"] span',
                },
                "total_customer_that_rated": {
                    "prefix_to_base_url": False,
                    "base_style_child": True,
                    "get_text": False,
                    "target_style": 'span[aria-label*="out of 5 stars"] + span a span',
                },
            },
        },
    }
]


def get_config(from_file: bool = False):
    if from_file:
        return json.loads(Path("./config.json").read_text())

    return scrap_config


if __name__ == "__main__":
    Path("./config.json").write_text(json.dumps(scrap_config))
    print("Configuration file written")

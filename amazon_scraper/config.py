import json
from pathlib import Path

import pandas as pd

scrap_config: list[dict] = [
    {
        "category": "Books",
        "sub_category": "Christian Living",
        "unique_ref_code": "BOOKS_CHRISTIAN_LIVING",
        "maximum_pages": 75,
        "start_page": 1,
        "base_url": "https://amazon.co.uk",
        "url": "https://www.amazon.co.uk/s?rh=n%3A277291&fs=true&ref=lp_277291_sar",
        "product_page": {
            "expand_elements": [{"style": ".a-expander-prompt", "js_action": "click"}],
            "product_descriptors": [
                "#productFactsDesktop_feature_div",
                "#detailBulletsWrapper_feature_div",
                "#featurebullets_feature_div",
                "#productOverview_feature_div",
                "#aplus_feature_div",
                "#productDescription_feature_div",
                "#importantInformation_feature_div",
                "#productDetailsWithModules_feature_div",
                "#detailBulletsWithExceptions_feature_div",
            ],
        },
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
    },
    {
        "category": "Books",
        "sub_category": "Computing and Internet for profressionals",
        "unique_ref_code": "BOOKS_COMPUTING_AND_INTERNET_FOR_PROFESSIONALS",
        "maximum_pages": 75,
        "start_page": 1,
        "base_url": "https://amazon.co.uk",
        "url": "https://www.amazon.co.uk/s?rh=n%3A14224461&fs=true&ref=lp_14224461_sar",
        "product_page": {
            "expand_elements": [{"style": ".a-expander-prompt", "js_action": "click"}],
            "product_descriptors": [
                "#productFactsDesktop_feature_div",
                "#detailBulletsWrapper_feature_div",
                "#featurebullets_feature_div",
                "#productOverview_feature_div",
                "#aplus_feature_div",
                "#productDescription_feature_div",
                "#importantInformation_feature_div",
                "#productDetailsWithModules_feature_div",
                "#detailBulletsWithExceptions_feature_div",
            ],
        },
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
    },
    {
        "category": "Books",
        "sub_category": "Digital Lifestyle  ",
        "unique_ref_code": "BOOKS_DIGITAL_LIFESTYLE",
        "maximum_pages": 75,
        "start_page": 1,
        "base_url": "https://amazon.co.uk",
        "url": "https://www.amazon.co.uk/s?rh=n%3A14288081&fs=true&ref=lp_14288081_sar",
        "product_page": {
            "expand_elements": [{"style": ".a-expander-prompt", "js_action": "click"}],
            "product_descriptors": [
                "#bookDescription_feature_div",
                "#productFactsDesktop_feature_div",
                "#detailBulletsWrapper_feature_div",
                "#featurebullets_feature_div",
                "#productOverview_feature_div",
                "#aplus_feature_div",
                "#productDescription_feature_div",
                "#importantInformation_feature_div",
                "#productDetailsWithModules_feature_div",
                "#detailBulletsWithExceptions_feature_div",
            ],
        },
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
    },
    {
        "category": "Books",
        "sub_category": "Business Development and Entreprenuership",
        "unique_ref_code": "BOOKS_BUSINESS_DEVELOPMENT_ENTREPRENUERSHIP",
        "maximum_pages": 75,
        "start_page": 16,
        "base_url": "https://amazon.co.uk",
        "url": "https://www.amazon.co.uk/s?rh=n%3A268144&fs=true&ref=lp_268144_sar",
        "product_page": {
            "expand_elements": [{"style": ".a-expander-prompt", "js_action": "click"}],
            "product_descriptors": [
                "#bookDescription_feature_div",
                "#productFactsDesktop_feature_div",
                "#detailBulletsWrapper_feature_div",
                "#featurebullets_feature_div",
                "#productOverview_feature_div",
                "#aplus_feature_div",
                "#productDescription_feature_div",
                "#importantInformation_feature_div",
                "#productDetailsWithModules_feature_div",
                "#detailBulletsWithExceptions_feature_div",
            ],
        },
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
    },
    {
        "category": "Books",
        "sub_category": "Personal Finance",
        "unique_ref_code": "BOOKS_PERSONAL_FINANCE",
        "maximum_pages": 75,
        "start_page": 1,
        "base_url": "https://amazon.co.uk",
        "url": "https://www.amazon.co.uk/s?rh=n%3A268203&fs=true&ref=lp_268203_sar",
        "product_page": {
            "expand_elements": [{"style": ".a-expander-prompt", "js_action": "click"}],
            "product_descriptors": [
                "#bookDescription_feature_div",
                "#productFactsDesktop_feature_div",
                "#detailBulletsWrapper_feature_div",
                "#featurebullets_feature_div",
                "#productOverview_feature_div",
                "#aplus_feature_div",
                "#productDescription_feature_div",
                "#importantInformation_feature_div",
                "#productDetailsWithModules_feature_div",
                "#detailBulletsWithExceptions_feature_div",
            ],
        },
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
    },
    {
        "category": "Books",
        "sub_category": "Mind, Body & Spirit",
        "unique_ref_code": "BOOKS_MIND_BODY_AND_SPIRIT",
        "maximum_pages": 75,
        "start_page": 39,
        "base_url": "https://amazon.co.uk",
        "url": "https://www.amazon.co.uk/s?rh=n%3A61&fs=true&ref=lp_61_sar",
        "product_page": {
            "expand_elements": [{"style": ".a-expander-prompt", "js_action": "click"}],
            "product_descriptors": [
                "#bookDescription_feature_div",
                "#productFactsDesktop_feature_div",
                "#detailBulletsWrapper_feature_div",
                "#featurebullets_feature_div",
                "#productOverview_feature_div",
                "#aplus_feature_div",
                "#productDescription_feature_div",
                "#importantInformation_feature_div",
                "#productDetailsWithModules_feature_div",
                "#detailBulletsWithExceptions_feature_div",
            ],
        },
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
    },
    {
        "category": "Books",
        "sub_category": "Literature and Fiction",
        "unique_ref_code": "BOOKS_LITERATURE_AND_FICTION",
        "maximum_pages": 75,
        "start_page": 1,
        "base_url": "https://amazon.co.uk",
        "url": "https://www.amazon.co.uk/s?rh=n%3A62&fs=true&ref=lp_62_sar",
        "product_page": {
            "expand_elements": [{"style": ".a-expander-prompt", "js_action": "click"}],
            "product_descriptors": [
                "#bookDescription_feature_div",
                "#productFactsDesktop_feature_div",
                "#detailBulletsWrapper_feature_div",
                "#featurebullets_feature_div",
                "#productOverview_feature_div",
                "#aplus_feature_div",
                "#productDescription_feature_div",
                "#importantInformation_feature_div",
                "#productDetailsWithModules_feature_div",
                "#detailBulletsWithExceptions_feature_div",
            ],
        },
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
    },
    {
        "category": "Books",
        "sub_category": "Biographies and Memoirs",
        "unique_ref_code": "BOOKS_BIOGRAPHIES_AND_MEMOIRS",
        "maximum_pages": 75,
        "start_page": 1,
        "base_url": "https://amazon.co.uk",
        "url": "https://www.amazon.co.uk/s?rh=n%3A67&fs=true&ref=lp_67_sar",
        "product_page": {
            "expand_elements": [{"style": ".a-expander-prompt", "js_action": "click"}],
            "product_descriptors": [
                "#bookDescription_feature_div",
                "#productFactsDesktop_feature_div",
                "#detailBulletsWrapper_feature_div",
                "#featurebullets_feature_div",
                "#productOverview_feature_div",
                "#aplus_feature_div",
                "#productDescription_feature_div",
                "#importantInformation_feature_div",
                "#productDetailsWithModules_feature_div",
                "#detailBulletsWithExceptions_feature_div",
            ],
        },
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
    },
    {
        "category": "Fashion",
        "sub_category": "Women",
        "unique_ref_code": "FASHION_WOMEN",
        "maximum_pages": 100,
        "start_page": 99,
        "base_url": "https://amazon.co.uk",
        "url": "https://www.amazon.co.uk/s?rh=n%3A12422025031&fs=true&ref=lp_12422025031_sar",
        "product_page": {
            "expand_elements": [{"style": ".a-expander-prompt", "js_action": "click"}],
            "product_descriptors": [
                "#bookDescription_feature_div",
                "#productFactsDesktop_feature_div",
                "#detailBulletsWrapper_feature_div",
                "#featurebullets_feature_div",
                "#productOverview_feature_div",
                "#aplus_feature_div",
                "#productDescription_feature_div",
                "#importantInformation_feature_div",
                "#productDetailsWithModules_feature_div",
                "#detailBulletsWithExceptions_feature_div",
            ],
        },
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
    },
    {
        "category": "Beauty",
        "sub_category": "Skin Care",
        "unique_ref_code": "BEAUTY_SKIN_CARE",
        "maximum_pages": 100,
        "start_page": 99,
        "base_url": "https://amazon.co.uk",
        "url": "https://www.amazon.co.uk/s?rh=n%3A118464031&fs=true&ref=lp_118464031_sar",
        "product_page": {
            "expand_elements": [{"style": ".a-expander-prompt", "js_action": "click"}],
            "product_descriptors": [
                "#bookDescription_feature_div",
                "#productFactsDesktop_feature_div",
                "#detailBulletsWrapper_feature_div",
                "#featurebullets_feature_div",
                "#productOverview_feature_div",
                "#aplus_feature_div",
                "#productDescription_feature_div",
                "#importantInformation_feature_div",
                "#productDetailsWithModules_feature_div",
                "#detailBulletsWithExceptions_feature_div",
            ],
        },
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
    },
    {
        "category": "Fashion",
        "sub_category": "Men",
        "unique_ref_code": "FASHION_MEN",
        "maximum_pages": 75,
        "start_page": 35,
        "base_url": "https://amazon.co.uk",
        "url": "https://www.amazon.co.uk/s?rh=n%3A12422026031&fs=true&ref=lp_12422026031_sar",
        "product_page": {
            "expand_elements": [{"style": ".a-expander-prompt", "js_action": "click"}],
            "product_descriptors": [
                "#bookDescription_feature_div",
                "#productFactsDesktop_feature_div",
                "#detailBulletsWrapper_feature_div",
                "#featurebullets_feature_div",
                "#productOverview_feature_div",
                "#aplus_feature_div",
                "#productDescription_feature_div",
                "#importantInformation_feature_div",
                "#productDetailsWithModules_feature_div",
                "#detailBulletsWithExceptions_feature_div",
            ],
        },
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
    },
]


def validate_config(config: list[dict]):
    """Checks if the configuration confirms to the expected format"""

    # each category must have a unique_ref_code
    if not all(["unique_ref_code" in category for category in config]):
        raise ValueError("Each category must have the unique_ref_code in them.")

    # each unique_ref_code mus be unique
    config_ref_codes = pd.Series([category["unique_ref_code"] for category in config])

    if not (config_ref_codes.unique().size == len(config_ref_codes)):
        raise ValueError("Each category must have a unique 'unique_ref_code'. ")


def get_config(from_file: bool = False):
    if from_file:
        read_config = json.loads(Path("./config.json").read_text())
    else:
        read_config = scrap_config

    validate_config(read_config)

    return read_config


if __name__ == "__main__":
    get_config(from_file=False)

    Path("./config.json").write_text(json.dumps(scrap_config))
    print("Configuration file written")

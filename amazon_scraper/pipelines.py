# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from pathlib import Path
import httpx

from amazon_scraper.items import ProductItem


class DownloadFeaturedImagePipeline:
    def process_item(self, item, spider):

        if issubclass(ProductItem, type(item)):
            # download the featured image
            _item: ProductItem = item

            category = _item["category"]
            img_url = _item["img_url"]
            sub_category = _item["sub_category"]
            data_uuid = _item["data_uuid"]

            response = httpx.get(str(img_url))
            if not response.is_success:
                print(
                    f"Unable to download image {img_url}. {response.status_code} {response.content}"
                )

            directory = f"./products/{category}/{sub_category}"
            os.makedirs(directory, exist_ok=True)

            Path(f"{directory}/{data_uuid}.jpeg").write_bytes(response.content)
            print(f"Downloaded {data_uuid}.jpeg")
        return item

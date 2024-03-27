# amazon_sraper

The goal of this script is to get latest Amazon products. This repository should be used only for Academic purposes!.

> (In Progress): NOTE: This is a new project hence, I will be updating the repository from time to time.

## Setup

Create an environment variable and install packages in `requirements.txt`

```sh
pip install -r requirements.txt
```

## settings.py

The `settings.py` contains a lot of setting that you might need to tweak as you need. A common example of setting you should tweak is the `ROTATING_PROXY_LIST` and `CONCURRENT_REQUESTS`. The higher the `CONCURRENT_REQUESTS`, the more the memory resource of your machine will be used up, ensure you keep an eye on `htop`.

The user-agents in the `USER_AGENT_LIST` variable must not contain a mobile device user-agent, as this will cause the site not serve elements needed by scrapy.

You should create file `proxy-ips.txt` with each IP in a new line. If you do not intend to use proxy IP, create the file with empty content.

## Proxy IP Addresses

You should add a sizeable amount of proxy addresses into the `settings.py` file (`ROTATING_PROXY_LIST`). This will ensure your own IP address does not get banned. You can get free addresses on the internet, but you will need to be changing these once they get banned.

If you will like to disable the use of proxy addresses, comment out `rotating_proxies.middlewares.RotatingProxyMiddleware` and `rotating_proxies.middlewares.BanDetectionMiddleware` in the `DOWNLOADER_MIDDLEWARES` variable of the `settings.py` file.

### Proxy Scape API

I used `proxyscrape.com` for my proxy address which offers a 1 month free IP addresses that are really good and reliable.

## `config.py`

The `config.py` contains a basic amount of HTML/CSS styles that will enable scrapy scrap information from google as at `20th March, 2024`. You might need to update this if need be to mirror the latest changes if there are any breaking changes.

## Scraping Products

The first step is to scrap the products basic information from Amazon. You can do this by running the command below in your terminal.
This will fetched products from the categories that have been indicated in the `config.py` file.

```sh
cd amazon_scraper && scrapy crawl products
```

Change `CONCURRENT_REQUESTS` to 100-200 or a suitable value that won't cog the memory and won't be too slow for your use case.

## Scraping Descriptions

The fetched products will not have their description, hence you will need to run the command below to fetch the descriptions of products that currently does not have their description fetched.

Change `CONCURRENT_REQUESTS` to 16 or a suitable value that won't cog the memory.

```sh
cd amazon_scraper && scrapy crawl descriptions
```

## Scraping Reviews

TODO

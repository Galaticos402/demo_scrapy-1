import json

import scrapy
import time
from demo_scrapy.items import CoinGeckoCrawlerItem
import time
import random
from urllib.parse import urlencode

class CoingeckoSpider(scrapy.Spider):
    urlSeen = []
    name = 'coingecko'
    allowed_domains = ['www.coingecko.com','coingeckochainblade.azurewebsites.net']
    start_urls = ['https://www.coingecko.com']
    # temporary endpoint for testing
    api_endpoint = "https://coingeckochainblade.azurewebsites.net/api/Coingecko/add"
    current_page = 1

    def parse(self, response):
        last_page = response.css("ul.pagination > li.page-item:nth-last-child(2) > a ::text").extract_first()

        urls = response.css("div.coin-table td.coin-name a ::attr(href)").extract()

        for item_url in urls:

            time.sleep(5)
            # headers = {
            #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            # }
            request = scrapy.Request(response.urljoin(item_url), callback=self.parse_coin)
            yield request

        # has_next_page = 'page-item next' == response.css("ul.pagination > li.page-item:nth-last-child(1)").xpath('@class').extract_first()
        if self.current_page <= 3:
            print('\n\n\n\n\n' + str(self.current_page))
            self.current_page += 1
            time.sleep(5)
            # headers = {
            #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            # }
            request = scrapy.Request(response.urljoin('/?page=' + str(self.current_page)), callback=self.parse)
            yield request

    def parse_coin(self, response):
        item = CoinGeckoCrawlerItem()

        item['Name'] = response.css('h1 > span.tw-font-bold ::text').extract_first().strip()
        item['Code'] = response.css('h1 > span.tw-font-normal ::text').extract_first().strip()
        # item['price'] = response.css('span.tw-text-gray-900.tw-text-3xl ::text').extract_first().strip()
        # item['marketCap'] = response.css('body > div.container > div.tw-grid.tw-grid-cols-1.lg\:tw-grid-cols-3.tw-mb-4 > div.tw-col-span-3.md\:tw-col-span-2 > div > div.tw-col-span-2.lg\:tw-col-span-2 > div:nth-child(2) > div:nth-child(1) > div.tw-flex.tw-justify-between.tw-w-full.tw-h-10.tw-py-2\.5.lg\:tw-border-t-0.tw-border-b.tw-border-gray-200.dark\:tw-border-opacity-10.tw-pl-0 > span.tw-text-gray-900.dark\:tw-text-white.tw-font-medium > span ::text').extract_first(default='N/A').strip()
        # item['dayTradingVolume'] = response.css('body > div.container > div.tw-grid.tw-grid-cols-1.lg\:tw-grid-cols-3.tw-mb-4 > div.tw-col-span-3.md\:tw-col-span-2 > div > div.tw-col-span-2.lg\:tw-col-span-2 > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > span.tw-text-gray-900.dark\:tw-text-white.tw-font-medium > span ::text').extract_first(default='N/A').strip()
        # item['fullyDilutedValuation'] = response.css('body > div.container > div.tw-grid.tw-grid-cols-1.lg\:tw-grid-cols-3.tw-mb-4 > div.tw-col-span-3.md\:tw-col-span-2 > div > div.tw-col-span-2.lg\:tw-col-span-2 > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > span.tw-text-gray-900.dark\:tw-text-white.tw-font-medium > span ::text').extract_first(default='N/A').strip()
        # item['circulatingSupply'] = response.css('body > div.container > div.tw-grid.tw-grid-cols-1.lg\:tw-grid-cols-3.tw-mb-4 > div.tw-col-span-3.md\:tw-col-span-2 > div > div.tw-col-span-2.lg\:tw-col-span-2 > div:nth-child(2) > div.tailwind-reset.lg\:tw-pl-4.tw-col-span-2.lg\:tw-col-span-1 > div:nth-child(1) > span.tw-text-gray-900.dark\:tw-text-white.tw-font-medium.tw-mr-1 ::text').extract_first(default='N/A').strip()
        # item['Total_Supply'] = response.css('body > div.container > div.tw-grid.tw-grid-cols-1.lg\:tw-grid-cols-3.tw-mb-4 > div.tw-col-span-3.md\:tw-col-span-2 > div > div.tw-col-span-2.lg\:tw-col-span-2 > div:nth-child(2) > div.tailwind-reset.lg\:tw-pl-4.tw-col-span-2.lg\:tw-col-span-1 > div:nth-child(2) > span.tw-text-gray-900.dark\:tw-text-white.tw-font-medium.tw-mr-1 ::text').extract_first(default='N/A').strip()
        # item['Max_Supply'] = response.css('body > div.container > div.tw-grid.tw-grid-cols-1.lg\:tw-grid-cols-3.tw-mb-4 > div.tw-col-span-3.md\:tw-col-span-2 > div > div.tw-col-span-2.lg\:tw-col-span-2 > div:nth-child(2) > div.tailwind-reset.lg\:tw-pl-4.tw-col-span-2.lg\:tw-col-span-1 > div:nth-child(3) > span.tw-text-gray-900.dark\:tw-text-white.tw-font-medium ::text').extract_first(default='N/A').strip()
        # Info section
        # Website names
        # websites = []
        # websiteNames = response.css("body > div.container > div.tw-grid.tw-grid-cols-1.lg\:tw-grid-cols-3.tw-mb-4 > div.tw-col-span-3.lg\:tw-col-span-1.coin-links-section.lg\:tw-ml-6 > div.tw-hidden.lg\:tw-block.tw-flex.flex-column.tw-mx-2.lg\:tw-mx-3 > div:nth-child(2) > div > a::text").getall()
        # websiteLinks = response.css("body > div.container > div.tw-grid.tw-grid-cols-1.lg\:tw-grid-cols-3.tw-mb-4 > div.tw-col-span-3.lg\:tw-col-span-1.coin-links-section.lg\:tw-ml-6 > div.tw-hidden.lg\:tw-block.tw-flex.flex-column.tw-mx-2.lg\:tw-mx-3 > div:nth-child(2) > div > a::attr(href)").getall()
        # for i in range(len(websiteNames)):
        #     websites.append({
        #         "Name": websiteNames[i],
        #         "Link": websiteLinks[i]
        #     })
        # item['Websites'] = websites
        params = {
            'Name': response.css('h1 > span.tw-font-bold ::text').extract_first().strip(),
            'Code': response.css('h1 > span.tw-font-normal ::text').extract_first().strip(),
        }
        request = scrapy.Request(url=self.api_endpoint, method='POST', body=json.dumps(params), headers={'Content-Type':'application/json'}, callback=self.process_result)
        yield request
        yield item

    def process_result(self, response):
        print(response)
        print(response)

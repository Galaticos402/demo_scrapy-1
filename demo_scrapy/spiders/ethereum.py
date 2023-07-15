import random
import time

import scrapy

from demo_scrapy.common.mongo_helper import MongoHelper
from demo_scrapy.items import CoingeckoDynamicItem


class EthereumCrawler(scrapy.Spider):
    name = 'ethereum'
    url = "https://www.coingecko.com/en/all-cryptocurrencies/show_more_coins?page=1&per_page=300&filter_asset_platform=ethereum"
    allowed_domains = ['www.coingecko.com']
    start_urls = [
        'https://www.coingecko.com/en/all-cryptocurrencies/show_more_coins?page=1&per_page=300&filter_asset_platform=ethereum']
    current_page = 1
    is_continue = True
    mongo_helper = MongoHelper()
    visited_url = []

    def parse(self, response):
        while self.is_continue:
            yield scrapy.Request(
                f'https://www.coingecko.com/en/all-cryptocurrencies/show_more_coins?page={self.current_page}&per_page=300&filter_asset_platform=ethereum',
                callback=self.parse_redirected_link)


    def parse_redirected_link(self, response):
        self.current_page += 1
        all_links = response.css('a::attr(href)').getall()
        if len(all_links) == 0:
            self.is_continue = False
        else:
            for link in all_links:
                if link in self.visited_url:
                    pass
                else:
                    self.visited_url.append(link)
                    yield scrapy.Request(url=f'https://www.coingecko.com{link}', callback=self.parse_coin)

    def parse_coin(self, response):
        item = CoingeckoDynamicItem()

        coin_code = response.css('h1 > span.tw-font-normal ::text').extract_first(default='N/A').strip()
        coin_name = response.css('h1 > span.tw-font-bold ::text').extract_first(default='N/A').strip()
        item['Name'] = response.css('h1 > span.tw-font-bold ::text').extract_first(default='N/A').strip()
        item['Code'] = coin_code
        item['Price'] = response.css('span.tw-text-gray-900.tw-text-3xl ::text').extract_first(default='N/A').strip()
        item['MarketCap'] = response.css(
            'body > div:nth-child(6) > main > div.tw-grid.tw-grid-cols-1.lg\:tw-grid-cols-3.tw-mb-4 > div.tw-col-span-3.md\:tw-col-span-2 > div > div.tw-col-span-2.lg\:tw-col-span-2 > div:nth-child(2) > div:nth-child(1) > div.tw-flex.tw-justify-between.tw-w-full.tw-h-10.tw-py-2\.5.lg\:tw-border-t-0.tw-border-b.tw-border-gray-200.dark\:tw-border-opacity-10.tw-pl-0 > span.tw-text-gray-900.dark\:tw-text-white.tw-font-medium > span ::text').extract_first(
            default='N/A').strip()
        item['DayTradingVolume'] = response.css(
            'body > div:nth-child(6) > main > div.tw-grid.tw-grid-cols-1.lg\:tw-grid-cols-3.tw-mb-4 > div.tw-col-span-3.md\:tw-col-span-2 > div > div.tw-col-span-2.lg\:tw-col-span-2 > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > span.tw-text-gray-900.dark\:tw-text-white.tw-font-medium > span ::text').extract_first(
            default='N/A').strip()
        item['FullyDilutedValuation'] = response.css(
            'body > div:nth-child(6) > main > div.tw-grid.tw-grid-cols-1.lg\:tw-grid-cols-3.tw-mb-4 > div.tw-col-span-3.md\:tw-col-span-2 > div > div.tw-col-span-2.lg\:tw-col-span-2 > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > span.tw-text-gray-900.dark\:tw-text-white.tw-font-medium > span ::text').extract_first(
            default='N/A').strip()
        item['CirculatingSupply'] = response.css(
            'body > div:nth-child(6) > main > div.tw-grid.tw-grid-cols-1.lg\:tw-grid-cols-3.tw-mb-4 > div.tw-col-span-3.md\:tw-col-span-2 > div > div.tw-col-span-2.lg\:tw-col-span-2 > div:nth-child(2) > div.tailwind-reset.lg\:tw-pl-4.tw-col-span-2.lg\:tw-col-span-1 > div:nth-child(1) > span.tw-text-gray-900.dark\:tw-text-white.tw-font-medium.tw-mr-1 ::text').extract_first(
            default='N/A').strip()
        item['Total_Supply'] = response.css(
            'body > div:nth-child(6) > main > div.tw-grid.tw-grid-cols-1.lg\:tw-grid-cols-3.tw-mb-4 > div.tw-col-span-3.md\:tw-col-span-2 > div > div.tw-col-span-2.lg\:tw-col-span-2 > div:nth-child(2) > div.tailwind-reset.lg\:tw-pl-4.tw-col-span-2.lg\:tw-col-span-1 > div:nth-child(2) > span.tw-text-gray-900.dark\:tw-text-white.tw-font-medium.tw-mr-1 ::text').extract_first(
            default='N/A').strip()
        item['Max_Supply'] = response.css(
            'body > div:nth-child(6) > main > div.tw-grid.tw-grid-cols-1.lg\:tw-grid-cols-3.tw-mb-4 > div.tw-col-span-3.md\:tw-col-span-2 > div > div.tw-col-span-2.lg\:tw-col-span-2 > div:nth-child(2) > div.tailwind-reset.lg\:tw-pl-4.tw-col-span-2.lg\:tw-col-span-1 > div:nth-child(3) > span.tw-text-gray-900.dark\:tw-text-white.tw-font-medium ::text').extract_first(
            default='N/A').strip()
        item['Collection'] = 'coin'

        contract_xpath_list = [
            '/html/body/div[3]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/i/@data-address',
            '/html/body/div[3]/main/div[1]/div[2]/div[2]/div[2]/div/div/div/i/@data-address'
        ]
        first_row_value = 'N/A'
        for path in contract_xpath_list:
            first_row_value = response.xpath(path).extract_first(default='N/A').strip()
            if first_row_value != 'N/A':
                break

        contract_details = {
            'Coin_Name': coin_name,
            'Contract_Hash': first_row_value
        }
        self.mongo_helper.save(item=contract_details, collection_name="contract_hash")
        yield item

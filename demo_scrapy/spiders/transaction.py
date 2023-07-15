import time
from urllib.parse import urljoin

import scrapy
import random
from scrapy.spidermiddlewares.httperror import HttpError

from demo_scrapy.common.mongo_helper import MongoHelper
from demo_scrapy.items import TransactionItem
from demo_scrapy.settings import USER_AGENT_CHOICES


class TransactionCrawler(scrapy.Spider):
    name = "transaction"
    allowed_domains = ["etherscan.io"]
    start_urls = ['https://etherscan.io/']
    current_page = 1
    USER_AGENT = random.choice(USER_AGENT_CHOICES)
    item_count_in_page = 1
    contract_hash = None

    def __init__(self, Contract_Hash=None, *args, **kwargs):
        super(TransactionCrawler, self).__init__(*args, **kwargs)
        self.contract_hash = Contract_Hash


    def parse(self, response):
        mongo_helper = MongoHelper()
        while self.current_page <= 10:
            request = scrapy.Request(
                f'https://etherscan.io/txs?a={self.contract_hash}&p={self.current_page}',
                callback=self.parse_redirected)
            self.current_page += 1
            # time.sleep(1)
            yield request

    def parse_redirected(self, response):
        content_table = response.css('#ContentPlaceHolder1_divTransactions > div.table-responsive > table')
        item = TransactionItem()
        for i in range(1,51):
            rows = content_table.css(f'tbody > tr:nth-child({i}) > td')
            item['Txn_Hash'] = rows[1].css('div > span > a::text').extract_first().strip()
            item['Method'] = rows[2].css('span::text').extract_first().strip()
            item['Block'] = rows[3].css('a::text').extract_first().strip()
            item['Age'] = rows[4].css('span::text').extract_first().strip()
            item['From'] = rows[7].css('div > a:nth-child(1)::attr(data-bs-title)').extract_first('').strip()
            item['To'] = rows[9].css('div > span::attr(data-bs-title)').extract_first().strip()
            item['Value'] = rows[10].css('span::text').extract_first().strip()
            item['Txn_Fee'] = ''.join(rows[11].css('::text').getall())
            item['Collection'] = 'transactions'
            yield item

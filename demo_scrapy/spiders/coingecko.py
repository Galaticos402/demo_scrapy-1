import scrapy
import time
from demo_scrapy.items import CoinGeckoCrawlerItem
import time
import random

class CoingeckoSpider(scrapy.Spider):
    urlSeen = []
    name = 'coingecko'
    allowed_domains = ['www.coingecko.com']
    start_urls = ['https://www.coingecko.com']
    current_page = 1
    user_agent_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
        "Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36"
    ]
    # rules = (
    #     Rule(LinkExtractor(allow='/en/coins/'), callback='parse_item_news'),
    #     Rule(LinkExtractor(allow='/?page'), follow=True, )
    # )

    def parse(self, response):
        last_page = response.css("ul.pagination > li.page-item:nth-last-child(2) > a ::text").extract_first()
        # print(last_page)
        #
        # yield last_page
        # print(last_page)
        # print(response)

        urls = response.css("div.coin-table td.coin-name a ::attr(href)").extract()
        # print(len(urls))

        for item_url in urls:
            # print(item_url)
            # time.sleep(1)
            yield scrapy.Request(response.urljoin(item_url), callback=self.parse_coin, headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]})

        # has_next_page = 'page-item next' == response.css("ul.pagination > li.page-item:nth-last-child(1)").xpath('@class').extract_first()
        if self.current_page <= 3:
            print('\n\n\n\n\n' + str(self.current_page))
            self.current_page += 1
            # time.sleep(1)
            yield scrapy.Request(response.urljoin('/?page=' + str(self.current_page)), callback=self.parse, headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]})

    def parse_coin(self, response):
        item = CoinGeckoCrawlerItem()

        item['name'] = response.css('h1 > span.tw-font-bold ::text').extract_first().strip()
        item['code'] = response.css('h1 > span.tw-font-normal ::text').extract_first().strip()
        item['price'] = response.css('span.tw-text-gray-900.tw-text-3xl ::text').extract_first().strip()
        # item['price'] = response.css('div[data-controller="coins-information"]').extract_first()

        print(item)

        yield item

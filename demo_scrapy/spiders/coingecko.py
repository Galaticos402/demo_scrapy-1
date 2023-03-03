import scrapy
import time
from demo_scrapy.items import CoinGeckoCrawlerItem
import time


class CoingeckoSpider(scrapy.Spider):
    urlSeen = []
    name = 'coingecko'
    allowed_domains = ['www.coingecko.com']
    start_urls = ['https://www.coingecko.com']
    current_page = 1
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
            time.sleep(1)
            yield scrapy.Request(response.urljoin(item_url), callback=self.parse_coin)

        # has_next_page = 'page-item next' == response.css("ul.pagination > li.page-item:nth-last-child(1)").xpath('@class').extract_first()
        if self.current_page <= 3:
            print('\n\n\n\n\n' + str(self.current_page))
            self.current_page += 1
            yield scrapy.Request(response.urljoin('/?page=' + str(self.current_page)), callback=self.parse)

    def parse_coin(self, response):
        item = CoinGeckoCrawlerItem()

        item['name'] = response.css('h1 > span.tw-font-bold ::text').extract_first().strip()
        item['code'] = response.css('h1 > span.tw-font-normal ::text').extract_first().strip()
        item['price'] = response.css('span.tw-text-gray-900.tw-text-3xl ::text').extract_first().strip()
        # item['price'] = response.css('div[data-controller="coins-information"]').extract_first()

        print(item)

        yield item

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class DemoScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CoinGeckoCrawlerItem(scrapy.Item):
    name = scrapy.Field()
    code = scrapy.Field()
    price = scrapy.Field()
    marketCap = scrapy.Field()
    dayTradingVolume = scrapy.Field()
    fullyDilutedValuation = scrapy.Field()
    circulatingSupply = scrapy.Field()
    Total_Supply = scrapy.Field()
    Max_Supply = scrapy.Field()



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
    Name = scrapy.Field()
    Code = scrapy.Field()
    Price = scrapy.Field()
    MarketCap = scrapy.Field()
    DayTradingVolume = scrapy.Field()
    FullyDilutedValuation = scrapy.Field()
    CirculatingSupply = scrapy.Field()
    Total_Supply = scrapy.Field()
    Max_Supply = scrapy.Field()
    # Info section
    Websites = scrapy.Field()



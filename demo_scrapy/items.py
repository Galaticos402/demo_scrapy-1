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
    Contract_Hash = scrapy.Field()
    # Info section
    Websites = scrapy.Field()
    Explorer = scrapy.Field()
    Collection = scrapy.Field()



class TransactionItem(scrapy.Item):
    Txn_Hash = scrapy.Field()
    Method = scrapy.Field()
    Block = scrapy.Field()
    Age = scrapy.Field()
    From = scrapy.Field()
    To = scrapy.Field()
    Value = scrapy.Field()
    Txn_Fee = scrapy.Field()
    Collection = scrapy.Field()


class CoingeckoDynamicItem(scrapy.Item):
    """
    A dynamic item class that can be customized at runtime.
    """
    def __setitem__(self, key, value):
        self._values[key] = value
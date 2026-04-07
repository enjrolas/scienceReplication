import scrapy


class DatasetLinkItem(scrapy.Item):
    paper_id = scrapy.Field()
    url = scrapy.Field()
    domain = scrapy.Field()
    description = scrapy.Field()
    verified = scrapy.Field()
    size_info = scrapy.Field()
    content_type = scrapy.Field()

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TtaospiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    rate_id = scrapy.Field()
    comment_user_nike = scrapy.Field()
    comment_user_vip = scrapy.Field()
    comment_date = scrapy.Field()
    goods_color = scrapy.Field()
    comment_content = scrapy.Field()

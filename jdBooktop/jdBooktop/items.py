# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdbooktopItem(scrapy.Item):
    # 销量榜
    sales_list = scrapy.Field()
    # 销量榜url
    sales_list_url = scrapy.Field()
    # 图书分类
    category = scrapy.Field()
    # 图书分类url
    category_url = scrapy.Field()
    # 榜单
    list_category = scrapy.Field()
    # 榜单url
    list_category_url = scrapy.Field()
    # 月份
    month = scrapy.Field()
    # 月份url
    month_url = scrapy.Field()
    # 年份
    year = scrapy.Field()
    # 年份url
    year_url = scrapy.Field()
    # 年龄
    age = scrapy.Field()
    # 年龄url
    age_url = scrapy.Field()
    # 图书排名
    bookNumber = scrapy.Field()
    # 图书名字
    bookName = scrapy.Field()
    # 图书url
    book_url = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 出版社
    press = scrapy.Field()
    # 图书id
    bookId = scrapy.Field()
    # 正价
    price = scrapy.Field()
    # 折扣价
    preferentialPrice = scrapy.Field()
# -*- coding: utf-8 -*-

import re
import json
import copy
import scrapy
import random
import requests
from jdBooktop.items import JdbooktopItem

class BooktopSpider(scrapy.Spider):
    name = "booktop"
    allowed_domains = ["jd.com", "p.3.cn"]
    start_urls = ['http://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-10001-1#comfort']

    def parse(self, response):
        for resp in response.xpath("//div[@class='m m-nav']/div[@class='w']/ul/li"):
            sales_list_url = resp.xpath(".//a/@href").extract_first().encode("utf-8")
            sales_list = resp.xpath(".//a/text()").extract_first().encode("utf-8")

            item = JdbooktopItem()
            item['sales_list'], item['sales_list_url'] = sales_list, sales_list_url
            response.meta['item'] = item

            yield scrapy.Request(response.urljoin(sales_list_url), callback= self.parseCategories, meta=copy.deepcopy(response.meta), dont_filter= True)

    def parseCategories(self, response):
        item = response.meta['item']
        resp = response.xpath("//div[@class='w clearfix']/div[@class='g-side']/div[@class='m m-category']/div[@class='mc']//a")
        if len(resp) == 0: # 作者排行榜
            category = category_url = None

            item['category'], item["category_url"] = category, category_url
            response.meta['item'] = item

            yield scrapy.Request(response.url, callback= self.parseTransfer, meta= copy.deepcopy(response.meta), dont_filter= True)
        for res in resp:
            category_url = res.xpath(".//@href").extract_first().encode("utf-8")
            category = res.xpath(".//text()").extract_first().encode("utf-8")

            item['category'], item['category_url'] = category, category_url
            response.meta['item'] = item

            yield scrapy.Request(response.urljoin(category_url), callback= self.parseTransfer, meta= copy.deepcopy(response.meta), dont_filter= True)

    def parseTransfer(self, response):
        item = response.meta['item']
        resp = response.xpath("//div[@class='w clearfix']/div[@class='g-main']/div[@class='m m-filter']/div[@class='mc']/dl")
        if len(resp) == 0:
            list_category = month = year = age = list_category_url = month_url = year_url = age_url = None

            item['list_category'], item['month'], item['year'], item['age'], item['list_category_url'], item['month_url'], item['year_url'], item['age_url'] = list_category, month, year, age, list_category_url, month_url, year_url, age_url
            response.meta['item'] = item

            yield scrapy.Request(response.url, callback= self.parseBookPage, meta= copy.deepcopy(response.meta), dont_filter = True)
        elif len(resp) == 1:
            month = year = age = month_url = year_url = age_url = None
            for res in resp[0].xpath(".//dd/a"):
                list_category_url = res.xpath(".//@href").extract_first().encode("utf-8")
                list_category = res.xpath(".//text()").extract_first().encode("utf-8")

                item['list_category'], item['month'], item['year'], item['age'], item['list_category_url'], item['month_url'], item['year_url'], item['age_url'] = list_category, month, year, age, list_category_url, month_url, year_url, age_url
                response.meta['item'] = item

                yield scrapy.Request(response.urljoin(list_category_url), callback= self.parseBookPage, meta= copy.deepcopy(response.meta), dont_filter= True)
        elif len(resp) == 2:
            for num, res in enumerate(resp):
                if num == 0:
                    month = year = age = month_url = year_url = age_url = None
                    for r in res.xpath(".//dd/a"):
                        list_category_url = r.xpath(".//@href").extract_first().encode("utf-8")
                        list_category = r.xpath(".//text()").extract_first().encode("utf-8")

                        item['list_category'], item['month'], item['year'], item['age'], item['list_category_url'], item['month_url'], item['year_url'], item['age_url'] = list_category, month, year, age, list_category_url, month_url, year_url, age_url
                        response.meta['item'] = item

                        yield scrapy.Request(response.urljoin(list_category_url), callback= self.parseBookPage, meta= copy.deepcopy(response.meta), dont_filter= True)
                elif num == 1:
                    list_category = year = age = list_category_url = year_url = age_url = None
                    for r in res.xpath(".//dd/a"):
                        month_url = r.xpath(".//@href").extract_first().encode("utf-8")
                        month = r.xpath(".//text()").extract_first().encode("utf-8")
                        if month_url == "javascript:void(0);":
                            continue

                        item['list_category'], item['month'], item['year'], item['age'], item['list_category_url'], item['month_url'], item['year_url'], item['age_url'] = list_category, month, year, age, list_category_url, month_url, year_url, age_url
                        response.meta['item'] = item

                        yield scrapy.Request(response.urljoin(month_url), callback= self.parseBookPage, meta= copy.deepcopy(response.meta), dont_filter= True)
        elif len(resp) == 3:
            for num, res in enumerate(resp):
                if num == 0:
                    month = year = age = month_url = year_url = age_url = None
                    for r in res.xpath(".//dd/a"):
                        list_category_url = r.xpath(".//@href").extract_first().encode("utf-8")
                        list_category = r.xpath(".//text()").extract_first().encode("utf-8")

                        item['list_category'], item['month'], item['year'], item['age'], item['list_category_url'], item['month_url'], item['year_url'], item['age_url'] = list_category, month, year, age, list_category_url, month_url, year_url, age_url
                        response.meta['item'] = item

                        yield scrapy.Request(response.urljoin(list_category_url), callback= self.parseBookPage, meta= copy.deepcopy(response.meta), dont_filter= True)
                elif num == 1:
                    list_category = year = age = list_category_url = year_url = age_url = None
                    for r in res.xpath(".//dd/a"):
                        month_url = r.xpath(".//@href").extract_first().encode("utf-8")
                        month = r.xpath(".//text()").extract_first().encode("utf-8")
                        if month_url == "javascript:void(0);":
                            continue

                        item['list_category'], item['month'], item['year'], item['age'], item['list_category_url'], item['month_url'], item['year_url'], item['age_url'] = list_category, month, year, age, list_category_url, month_url, year_url, age_url
                        response.meta['item'] = item

                        yield scrapy.Request(response.urljoin(month_url), callback= self.parseBookPage, meta= copy.deepcopy(response.meta), dont_filter= True)
                elif num == 2:
                    list_category = month = age = list_category_url = month_url = age_url = None
                    for r in res.xpath(".//dd/a"):
                        year_url = r.xpath(".//@href").extract_first().encode("utf-8")
                        year = r.xpath(".//text()").extract_first().encode("utf-8")

                        item['list_category'], item['month'], item['year'], item['age'], item['list_category_url'], item['month_url'], item['year_url'], item['age_url'] = list_category, month, year, age, list_category_url, month_url, year_url, age_url
                        response.meta['item'] = item

                        yield scrapy.Request(response.urljoin(year_url), callback= self.parseBookPage, meta= copy.deepcopy(response.meta), dont_filter= True)
        elif len(resp) == 4:
            for num, res in enumerate(resp):
                if num == 0:
                    month = year = age = month_url = year_url = age_url = None
                    for r in res.xpath(".//dd/a"):
                        list_category_url = r.xpath(".//@href").extract_first().encode("utf-8")
                        list_category = r.xpath(".//text()").extract_first().encode("utf-8")

                        item['list_category'], item['month'], item['year'], item['age'], item['list_category_url'], item['month_url'], item['year_url'], item['age_url'] = list_category, month, year, age, list_category_url, month_url, year_url, age_url
                        response.meta['item'] = item

                        yield scrapy.Request(response.urljoin(list_category_url), callback= self.parseBookPage, meta= copy.deepcopy(response.meta), dont_filter= True)
                elif num == 1:
                    list_category = year = age = list_category_url = year_url = age_url = None
                    for r in res.xpath(".//dd/a"):
                        month_url = r.xpath(".//@href").extract_first().encode("utf-8")
                        month = r.xpath(".//text()").extract_first().encode("utf-8")
                        if month_url == "javascript:void(0);":
                            continue

                        item['list_category'], item['month'], item['year'], item['age'], item['list_category_url'], item['month_url'], item['year_url'], item['age_url'] = list_category, month, year, age, list_category_url, month_url, year_url, age_url
                        response.meta['item'] = item

                        yield scrapy.Request(response.urljoin(month_url), callback= self.parseBookPage, meta= copy.deepcopy(response.meta), dont_filter= True)
                elif num == 2:
                    list_category = month = age = list_category_url = month_url = age_url = None
                    for r in res.xpath(".//dd/a"):
                        year_url = r.xpath(".//@href").extract_first().encode("utf-8")
                        year = r.xpath(".//text()").extract_first().encode("utf-8")

                        item['list_category'], item['month'], item['year'], item['age'], item['list_category_url'], item['month_url'], item['year_url'], item['age_url'] = list_category, month, year, age, list_category_url, month_url, year_url, age_url
                        response.meta['item'] = item

                        yield scrapy.Request(response.urljoin(year_url), callback= self.parseBookPage, meta= copy.deepcopy(response.meta), dont_filter= True)
                elif num == 3:
                    list_category = month = year = list_category_url = month_url = year_url = None
                    for r in res.xpath(".//dd/a"):
                        age_url = r.xpath(".//@href").extract_first().encode("utf-8")
                        age = r.xpath(".//text()").extract_first().encode("utf-8")

                        item['list_category'], item['month'], item['year'], item['age'], item['list_category_url'], item['month_url'], item['year_url'], item['age_url'] = list_category, month, year, age, list_category_url, month_url, year_url, age_url
                        response.meta['item'] = item

                        yield scrapy.Request(response.urljoin(age_url), callback= self.parseBookPage, meta= copy.deepcopy(response.meta), dont_filter= True)

    def parseBookPage(self, response):
        resp = response.xpath("//div[@class='m m-page']/div[@class='page clearfix']/div[@class='p-wrap']/span[@class='p-num']/a")
        resp = resp[:len(resp) / 2]
        resp = resp[1 : -1]
        for res in resp:
            next_url = res.xpath(".//@href").extract_first()
            yield scrapy.Request(response.urljoin(next_url), callback= self.parseBook, meta= copy.deepcopy(response.meta), dont_filter= True)

    def parseBook(self, response):
        item = response.meta['item']
        for resp in response.xpath("//div[@class='m m-list']/div[@class='mc']/ul[@class='clearfix']/li"):
            bookNumber = resp.xpath(".//div[@class='p-num']/text()").extract_first().strip().encode("utf-8")
            bookName = resp.xpath(".//div[@class='p-detail']/a/text()").extract_first().strip().encode("utf-8")
            book_url = resp.xpath(".//div[@class='p-detail']/a/@href").extract_first().encode("utf-8")
            bookId = book_url.split("/")[-1].split(".")[0].encode("utf-8")
            author = resp.xpath(".//div[@class='p-detail']/dl[1]//text()").extract()
            author = "".join([au.strip() for au in author if len(au.strip()) != 0]).encode("utf-8")
            press = resp.xpath(".//div[@class='p-detail']/dl[2]//text()").extract()
            press = "".join([p.strip() for p in press if len(p.strip()) != 0]).encode("utf-8")
            
            # Ajax 请求
            session = requests.session()
            req = session.get("http://p.3.cn/prices/mgets?skuIds=J_" + bookId, headers= {"User-Agent" : random.choice(UserAgent())}).text
            price = re.findall('"m":"(.*?)"', req, re.S)[0].encode("utf-8")
            preferentialPrice = re.findall('"op":"(.*?)"', req, re.S)[0].encode("utf-8")
            # print price, preferentialPrice

            item['bookNumber'], item['bookName'], item['book_url'], item['bookId'], item['author'], item['press'], item['price'], item['preferentialPrice'] = bookNumber, bookName, book_url, bookId, author, press, price, preferentialPrice

            yield item

def UserAgent():
    user_agent=[\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",\
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    return user_agent
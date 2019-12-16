# -*- coding: utf-8 -*-
import scrapy
from ..items import AmazonItem
from ..userAgents import Get_Headers
import pymongo
import re
import time

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.in']
    items = AmazonItem()
    headers = {'User-Agent': Get_Headers()}
    start_urls = ['https://www.amazon.in/Books/b?ie=UTF8&node=976389031&ref_=sd_allcat_sbc_books_all']

    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',27017
        )
        db = self.conn['Amazon']
        self.collection = db['books']

    def parse(self, response):
        Categories = response.xpath('.//div[@id="leftNav"]//span/a/@href').extract()
        for category in Categories:
            if category[:3] == '/gp':
                pass
            else:
                link = response.urljoin(category)
                yield scrapy.Request(url=link, callback= self.get_ASIN)


    def get_Details_of_Primary_Page(self,asin,response):
        base_query = './/li[@data-asin=' + f'"{str(asin)}"' + ']'
        title = response.xpath(base_query + '//h2[@class = "a-size-medium s-inline s-access-title a-text-normal"]/text()').extract_first()
        link = response.xpath(base_query +
                              '//a[@class="a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal"]/@href').extract_first()
        if link[:5] != 'https':
            link = response.urljoin(link)
        img = response.xpath(base_query +
                             '//div[@class="a-column a-span12 a-text-center"]//img/@src').extract_first()
        paperback = response.xpath(base_query +
                                   '//div[@class="a-column a-span7"]//div/a[@title = "Paperback"]/../following-sibling::div[1]'
                                   '//span[@class="a-size-base a-color-price s-price a-text-bold" or @class="a-size-base a-color-price a-text-bold"]/text()').extract_first()
        kindle_edition = response.xpath(base_query +
                                        '//div[@class="a-column a-span7"]//div/a[@title = "Kindle Edition"]/../following-sibling::div[1]'
                                        '//span[@class="a-size-base a-color-price s-price a-text-bold" or @class="a-size-base a-color-price a-text-bold"]/text()').extract_first()
        hardcover = response.xpath(base_query +
                                   '//div[@class="a-column a-span7"]//div/a[@title = "Hardcover"]/../following-sibling::div[1]'
                                   '//span[@class="a-size-base a-color-price s-price a-text-bold" or @class="a-size-base a-color-price a-text-bold"]/text()').extract_first()

        url = re.findall(r'https://.*/.*/[0-9]*',link)[0]
        if url == 'https://www.amazon.in/gp/slredirect/picassoRedirect.html/':
            pass
        else:
            if self.collection.find({'url': url}):
                for obj in self.collection.find({'url': url}):
                    if paperback != obj['paperback'][-1]['Price']:
                        self.collection.update({'url': url},
                                               {'$push': {'paperback': {"Price": paperback, "Time": time.asctime()}}})
                    if kindle_edition != obj['kindle_edition'][-1]["Price"]:
                        self.collection.update({'url': url},
                                               {'$push': {
                                                   'kindle_edition': {"Price": kindle_edition, "Time": time.asctime()}}})
                    if hardcover != obj['hardcover'][-1]["Price"]:
                        self.collection.update({'url': url},
                                               {'$push': {'hardcover': {"Price": hardcover, "Time": time.asctime()}}})
            else:
                self.collection.insert_one({'url': url, 'title': title, 'img': img,'paperback': [{"Price": paperback, "Time": time.asctime()}],
                                            'kindle_edition': [{"Price": kindle_edition, "Time": time.asctime()}],
                                            'hardcover': [{"Price": hardcover, "Time": time.asctime()}]})


    def get_Details_of_Secondary_Page(self,asin,response):
        base_query = './/div[@data-asin=' + f'"{str(asin)}"' + ']'
        title = response.xpath(base_query +
                               '//span[@class="a-size-medium a-color-base a-text-normal"]/text()').extract_first()
        link = response.xpath(base_query +
                              '//h2[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-2"]/a/@href').extract_first()
        if link[:5] != 'https':
            link = response.urljoin(link)

        img = response.xpath(base_query +
                             '//div[@class="a-section aok-relative s-image-fixed-height"]/img/@src').extract_first()
        paperback = response.xpath(base_query +
                                   '//div[@class="a-row a-size-base a-color-base"]/a[contains(text(),"Paperback")]'
                                   '/../following-sibling::div[1]//span[@class="a-price-whole" or @class="a-color-price"]/text()').extract_first()
        kindle_edition = response.xpath(base_query +
                                        '//div[@class="a-row a-size-base a-color-base"]/a[contains(text(),"Kindle Edition")]'
                                        '/../following-sibling::div[1]//span[@class="a-price-whole" or @class="a-color-price"]/text()').extract_first()
        hardcover = response.xpath(base_query +
                                   '//div[@class="a-row a-size-base a-color-base"]/a[contains(text(),"Hardcover")]'
                                   '/../following-sibling::div[1]//span[@class="a-price-whole" or @class="a-color-price"]/text()').extract_first()

        url = re.findall(r'https://.*/.*/[0-9]*', link)[0]
        if url =='https://www.amazon.in/gp/slredirect/picassoRedirect.html/':
            pass
        else:
            if self.collection.find({'url': url}):
                for obj in self.collection.find({'url': url}):
                    print(obj)
                    if paperback != obj['paperback'][-1]['Price']:
                        self.collection.update({'url': url},
                                               {'$push': {'paperback': {"Price": paperback, "Time": time.asctime()}}})
                    if kindle_edition != obj['kindle_edition'][-1]["Price"]:
                        self.collection.update({'url': url},
                                               {'$push': {
                                                   'kindle_edition': {"Price": kindle_edition, "Time": time.asctime()}}})
                    if hardcover != obj['hardcover'][-1]["Price"]:
                        self.collection.update({'url': url},
                                               {'$push': {'hardcover': {"Price": hardcover, "Time": time.asctime()}}})
            else:
                self.collection.insert_one(
                    {'url': url, 'title': title, 'img': img, 'paperback': [{"Price": paperback, "Time": time.asctime()}],
                     'kindle_edition': [{"Price": kindle_edition, "Time": time.asctime()}],
                     'hardcover': [{"Price": hardcover, "Time": time.asctime()}]})

    def get_ASIN(self, response):
        try:
            ASIN = response.xpath('.//li[@class = "s-result-item celwidget  "]/@data-asin').extract()
            for asin in ASIN:
                if asin in asins:
                    pass
                else:
                    self.get_Details_of_Primary_Page(asin,response)
                    asins.add(asin)
            next_page = response.xpath('.//div[@class="pagnHy"]/span[@class="pagnRA"]/a/@href').extract()
            yield scrapy.Request(url=response.urljoin(next_page[0]), callback=self.get_ASIN,
                                 headers=self.headers)
        except:
            try:
                ASIN_next = response.xpath(
                    './/div[@class="sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28"]/@data-asin').extract()
                for asin_next in ASIN_next:
                    if asin_next in asins:
                        pass
                    else:
                        self.get_Details_of_Secondary_Page(asin_next,response)
                        asins.add(asin_next)
                next_page_link = response.xpath('.//li[@class="a-last"]/a/@href').extract()
                yield scrapy.Request(url=response.urljoin(next_page_link[0]), callback=self.get_ASIN,
                                     headers=self.headers)
            except:
                pass


asins = set()
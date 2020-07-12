# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from leroymerlen.items import LeroymerlenItem
from scrapy.loader import ItemLoader

class LeroymSpider(scrapy.Spider):
    name = 'leroym'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/bloki-stroitelnye/']

    def parse(self, response):
        ads_links = response.xpath("//a[@class='black-link product-name-inner']")
        for link in ads_links:
            yield response.follow(link, callback = self.parse_ads)


    def parse_ads(self, response: HtmlResponse):

        name = response.xpath("//h1[@class='header-2']/text()").extract_first()
        photos = response.xpath("//uc-pdp-card-ga-enriched[@class='card-data']//uc-pdp-media-carousel//meta/@content").extract()
        ch = response.xpath("//dt[@class='def-list__term']/text()").extract()
        cr = response.xpath("//dd[@class='def-list__definition']/text()").extract()
        charact = []
        for i in range(len(ch)):
            char = ch[i] + cr[i]
            charact.append(char)
        linkes = response.url
        price = response.xpath("//uc-pdp-price-view[@class='primary-price']/span[@slot='price']/text()").extract()
        yield LeroymerlenItem(name = name,photos = photos, charact = charact, linkes = linkes, prices = price)
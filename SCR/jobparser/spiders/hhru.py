import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?clusters=true&search_field=name&enable_snippets=true&salary=&st=searchVacancy&fromSearch=true&text=python']

    def parse(self, response:HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()

        vacansy_links = response.css('a.bloko-link.HH-LinkModifier::attr(href)').extract()

        for link in vacansy_links:
            yield response.follow(link, callback=self.vacansy_parse)



        yield response.follow(next_page, callback=self.parse)

        print(1)

    def vacansy_parse(self, respone:HtmlResponse):

        name_vac = respone.css('h1::text').extract_first()
        salary_vac = respone.xpath("//span[@class='bloko-header-2 bloko-header-2_lite']/text()").extract()
        yield JobparserItem(name = name_vac, salary = salary_vac)
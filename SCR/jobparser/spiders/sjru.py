import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response:HtmlResponse):
        next_page = response.css('a.icMQ_ _1_Cht::attr(href)').extract_first()

        vacansy_links = response.css('a.icMQ_._6AfZ9::attr(href)').extract()

        for link in vacansy_links:
            yield response.follow(link, callback=self.vacansy_parse)

        yield response.follow(next_page, callback=self.parse)

        #print(1)

    def vacansy_parse(self, respone:HtmlResponse):

        name_vac = respone.css('h1::text').extract_first()
        salary_vac = respone.xpath("//span[@class='_3mfro _2Wp8I PlM3e _2JVkc']/text()").extract()
        # salary_vac = respone.xpath("//span[@class='_1OuF_ ZON4b']/text()").extract()
        yield JobparserItem(name = name_vac, salary = salary_vac)


from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroymerlen.spiders.leroym import LeroymSpider
from leroymerlen import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymSpider)

    process.start()
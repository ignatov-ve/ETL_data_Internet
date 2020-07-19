from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instagram.spiders.instaspyder import InstaspyderSpider
from instagram import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings = crawler_settings)
    process.crawl(InstaspyderSpider)
    process.start()
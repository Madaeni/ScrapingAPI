from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from LeroyMerlenParser.spiders.leroymerlinru import LeroymerlinruSpider
from LeroyMerlenParser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    query = input('Введите название: ')
    process.crawl(LeroymerlinruSpider, query=query)
    process.start()


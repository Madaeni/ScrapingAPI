from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from security import LOGIN, PASSWORD
from instaparser.spiders.instagram import InstaparserSpider
from instaparser import settings


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    users_list = ['', '']
    insta_login = LOGIN
    insta_pwd = PASSWORD
    process.crawl(InstaparserSpider, users_list=users_list, insta_login=insta_login, insta_pwd=insta_pwd)

    process.start()
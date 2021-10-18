import scrapy
from scrapy.http import HtmlResponse
from LeroyMerlenParser.items import LeroyMerlenParserItem
from scrapy.loader import ItemLoader


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['saratov.leroymerlin.ru']
    start_urls = ['http://saratov.leroymerlin.ru/']

    def __init__(self, query):
        super().__init__()
        self.start_urls = [f'https://saratov.leroymerlin.ru/search/?q={query}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[contains(@aria-label, "Следующая страница:")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//div[@data-qa-product]/a/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyMerlenParserItem(), response=response)
        loader.add_value('link', response.url)
        loader.add_xpath('name', '//h1[@slot="title"]/text()')
        loader.add_xpath('price', '//uc-pdp-price-view[@slot="primary-price"]/span[@slot="price"]/text()')
        loader.add_xpath('photo', '//source[contains(@data-origin, "w_2000,h_2000")]/@srcset')
        yield loader.load_item()
import requests
from lxml import html
from pymongo import MongoClient
from pprint import pprint

# Подключаем базу
client = MongoClient('127.0.0.1', 27017)
db = client['News']
news_yandex = db.yandex_news

# URL источник
url = 'https://yandex.ru/news/region/saratov'

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.3.614 Yowser/2.5 Safari/537.36'}

response = requests.get(url)
dom = html.fromstring(response.text)

items = dom.xpath('//div[@class="mg-grid__col mg-grid__col_xs_4"] | //div[@class="mg-grid__col mg-grid__col_xs_8"]')

news_list = []

for item in items:
    news = {}
    source = item.xpath('.//a[@class="mg-card__source-link"]/@aria-label')
    name = item.xpath('.//h2[@class="mg-card__title"]/text()')
    link = item.xpath('.//a[@class="mg-card__source-link"]/@href')
    data = item.xpath('.//span[contains(@class, "mg-card-source__time")]/text()')

    name = '. '.join(name).replace(u'\xa0', u' ')
    name = [name]

    news['source'] = source
    news['name'] = name
    news['link'] = link
    news['data'] = data

    news_list.append(news)
    # news_yandex.insert_one(news)

pprint(news_list)

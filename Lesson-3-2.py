from pymongo import MongoClient
from pprint import pprint


# Проверяем есть ли null
def check(s):
    if s:
        return s
    else:
        return int('0')


client = MongoClient('127.0.0.1', 27017)
db = client['Jobs']
hh_vacancy = db.hh_vacancy

salary_info = int(input('Введите желаемую зарплату: '))

for doc in hh_vacancy.find({'$or': [{'salary_currency': 'руб.'},
                                    {'salary_currency': 'USD'},
                                    {'salary_currency': 'EUR'},
                                    ]
                            },
                           ):
    if doc['salary_currency'] == 'руб.':
        if check(doc['salary_min']) > salary_info or check(doc['salary_max']) > salary_info:
            pprint(doc)
    elif doc['salary_currency'] == 'USD':
        if (check(doc['salary_min']) * 70) > salary_info or (check(doc['salary_max']) * 70) > salary_info:
            pprint(doc)
    elif doc['salary_currency'] == 'EUR':
        if (check(doc['salary_min']) * 80) > salary_info or (check(doc['salary_max']) * 80) > salary_info:
            pprint(doc)
    else:
        continue
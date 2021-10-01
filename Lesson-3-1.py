import requests
from bs4 import BeautifulSoup as bs
import re
from pymongo import MongoClient


# Проверяем число или нет
def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


# Проверяем есть ли уже такая запись в базе
def check(s):
    for doc in hh_vacancy.find({'link': s}):
        return True


# Подключаем базу
client = MongoClient('127.0.0.1', 27017)
db = client['Jobs']
hh_vacancy = db.hh_vacancy

# URL источник
url = 'https://saratov.hh.ru'

# Выбор вакансии
search_text = input("Введите интересующую Вас вакансию: ")

params = {'clusters': 'true',
          'ored_clusters': 'true',
          'enable_snippets': 'true',
          'st': 'searchVacancy',
          'text': search_text,
          'area': '113'
          }

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.3.614 Yowser/2.5 Safari/537.36'}

# Вынес отдельно добавку к URL на случай если нужно будет что-то поменять
url_link = '/search/vacancy'
vacancy_number = 1
page = 0

while True:
    response = requests.get(url + url_link, params=params, headers=headers)
    soup = bs(response.text, 'html.parser')

    vacancy_list = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})

    # кнопка "дальше"
    button_next = soup.find('a', text='дальше')

    for vacancy in vacancy_list:
        vacancy_data = {}

        # В данной строчке есть наименование вакансии и ссылка на вакансию
        vacancy_name_info = vacancy.find('a', attrs={'class': 'bloko-link'})

        # Наименование вакансии
        vacancy_name = vacancy_name_info.text

        # Ссылка на вакансию
        vacancy_link = vacancy_name_info['href']

        # Наименование работодателя
        vacancy_employer = vacancy.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'})
        if not vacancy_employer:
            vacancy_employer = None
        else:
            vacancy_employer = vacancy_employer.text

        # Город
        vacancy_city = vacancy.find('span', attrs={'class': 'vacancy-serp-item__meta-info'}).text

        # Зарплата
        salary = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
        if not salary:
            salary_min = None
            salary_max = None
            salary_currency = None
        else:
            salary = salary.getText() \
                .replace(u'\xa0', u'')

            salary = re.split(r'\s|<|>', salary)

            if salary[0] == 'до':
                salary_min = None
                if isint(salary[1]) and isint(salary[2]):
                    salary_max = int("".join([salary[1], salary[2]]))
                    salary_currency = salary[3]
                else:
                    salary_max = int(salary[1])
                    salary_currency = salary[2]
            elif salary[0] == 'от':
                if isint(salary[1]) and isint(salary[2]):
                    salary_min = int("".join([salary[1], salary[2]]))
                    salary_currency = salary[3]
                else:
                    salary_min = int(salary[1])
                    salary_currency = salary[2]
                salary_max = None
            else:
                if isint(salary[0]) and isint(salary[1]):
                    salary_min = int("".join([salary[0], salary[1]]))
                    if isint(salary[3]) and isint(salary[4]):
                        salary_max = int("".join([salary[3], salary[4]]))
                        salary_currency = salary[5]
                    else:
                        salary_max = int(salary[3])
                        salary_currency = salary[4]
                else:
                    salary_min = int(salary[0])
                    if isint(salary[2]) and isint(salary[3]):
                        salary_max = int("".join([salary[2], salary[3]]))
                        salary_currency = salary[4]
                    else:
                        salary_max = int(salary[2])
                        salary_currency = salary[3]

        vacancy_data['vacancy_number'] = vacancy_number
        vacancy_data['name'] = vacancy_name
        vacancy_data['link'] = vacancy_link
        vacancy_data['employer'] = vacancy_employer
        vacancy_data['city'] = vacancy_city
        vacancy_data['salary_min'] = salary_min
        vacancy_data['salary_max'] = salary_max
        vacancy_data['salary_currency'] = salary_currency
        vacancy_data['site'] = url

        vacancy_number += 1

        # Проверяем есть ли такая запись в базе
        if check(vacancy_data['link']) is True:
            continue
        else:
            # Добавляем запись в базу
            hh_vacancy.insert_one(vacancy_data)

    # Проверяем есть ли кнопка "дальше"
    if not button_next or not response.ok:
        break

    # Добавляем в параметры страницу
    page += 1
    params = {'clusters': 'true',
              'ored_clusters': 'true',
              'enable_snippets': 'true',
              'st': 'searchVacancy',
              'text': search_text,
              'area': '113',
              'page': page}
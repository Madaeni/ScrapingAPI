from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import time

# Подключаем базу
client = MongoClient('127.0.0.1', 27017)
db = client['MailRU']
letter_box = db.letters

# Подключаем Webdriver
options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
binary_yandex_driver_file = 'yandexdriver.exe'
driver = webdriver.Chrome(binary_yandex_driver_file, options=options)

driver.get('https://mail.ru/')

wait = WebDriverWait(driver, 30)    # Переменная с задержкой

link_list = []  # Создаем список для ссылок
actions = ActionChains(driver)

# Вводим логин
elem = driver.find_element(By.XPATH, '//input[contains(@class, "email-input")]')
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)

# Вводим пароль
elem = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[contains(@class, "password-input")]')))
elem.send_keys('NextPassword172???')
elem.send_keys(Keys.ENTER)

wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@style, "padding-top")]')))

height = driver.find_element(By.XPATH, '//div[contains(@style, "padding-top")]')    # Получаем высоту прокрутки
last_height = height.get_attribute('style')

while True:
    letters = driver.find_elements(By.XPATH, "//a[@data-uidl-id]")

    # Собираем ссылки на письма в список
    for letter in letters:
        link = letter.get_attribute('href')

        if link not in link_list:   # Проверяем нет ли такой ссылки  нашем списке
            link_list.append(link)  # Добавляем в список

    # Прокручиваем вниз
    letters[-1].send_keys(Keys.PAGE_DOWN)

    time.sleep(1)

    # Рассчитываем новую прокрутку и сравниваем с предыдущей
    height = driver.find_element(By.XPATH, '//div[contains(@style, "padding-top")]')
    new_height = height.get_attribute('style')
    if new_height == last_height:
        break

    last_height = new_height

# Добавляем в письма в базу данных
for item in link_list:
    driver.get(item)
    letters_full = {'subject': wait.until(
        EC.presence_of_element_located((By.XPATH, '//h2[@class="thread__subject"]'))).text, 'contact': wait.until(
        EC.presence_of_element_located((By.XPATH, '//span[@class="letter-contact"]'))).text, 'date': wait.until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="letter__date"]'))).text}

    body = wait.until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="letter__body"]'))).text
    letters_full['body'] = body.split('\n')

    letter_box.insert_one(letters_full)

driver.quit()
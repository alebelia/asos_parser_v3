#Функции и переменные, необходимые для работы программы

import requests
import os.path
import csv
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup as bs


def get_item_name(item_url, headers):
    '''Получение названия товара'''
    session = requests.Session() #Для имитации действий реального пользователя надо создать сессию
    request = session.get(item_url, headers=headers) #Эмулируем открытие страницы в браузере
    if request.status_code == 200: #проверяем, что сервер отдал нам нужные данные, и получаем название товара
        soup = bs(request.content, 'lxml')
        try:
            item_name = soup.find('h1').text
        except:
            print('Не удалось получить название товара.')
            pass
        return item_name
    else:
        print('Не удалось получить название товара. Страница недоступна.')

def get_item_price(request_url):
    '''Получение текущей цены товара по заданной ссылке'''
    response = requests.get(request_url)
    response.raise_for_status()
    if response.status_code == requests.codes.ok:
        try:
            json_data = response.json() #преобразование ответа в JSON
            item_info = json_data[0] #получение 1-го элемента
            current_price = item_info['productPrice']['current']['value']
            return current_price
        except:
            print('Не удалось получить информацию о товаре.')
            pass
    else:
        print("Не удалось получить ответ на REST-запрос. Страница недоступна")

def check_csv(csv_file):
    '''Проверка существования CSV-файла с заданным именем'''
    return os.path.isfile(csv_file)

def create_csv(csv_file):
    '''Создание CSV-файла'''
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(('Название', 'Цена', 'URL'))
        print('CSV-файл создан.')

def check_url(csv_file, url):
    '''Проверка наличия ссылки на товар в CSV-файле'''
    found = False
    with open(csv_file, newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if url in row[2]:
                found = True
                break
    return found

def write_item(name, price, url, csv_file):
    '''Запись информации о товаре в CSV-файл'''
    with open(csv_file, 'a', newline='', encoding='utf-8') as csv_obj:
        csv_writer = csv.writer(csv_obj)
        csv_writer.writerow((name, price, url))
        print('Товар добавлен в csv-файл.')

def email_new_prices(email_sender, email_password, email_receiver, email_text):
    '''Соединение с SMTP-сервером и отправка E-mail с изменившимися ценами'''
    try:
        sub = 'Asos price change'
        msg = email_text
        message = "Subject: {} \n{}".format(sub, msg)
        smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_obj.ehlo()
        smtp_obj.starttls()
        smtp_obj.login(email_sender, email_password)
        smtp_obj.sendmail(email_sender, email_receiver, message.encode('utf-8'))
        smtp_obj.quit()
        print('Email отправлен!')
    except:
        print('Возникла проблема при отправке письма!')

csv_file = 'asos_price_list.csv' #CSV-файл, где будут храниться данные об отслеживаемых товарах

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)',
           }

basic_request_url = 'https://www.asos.com/api/product/catalogue/v3/stockprice?' #Основа request_url. Если этот адрес изменился -> см. панель разработчика на сайте -> Network -> запрос

#Параметры для GET-запроса
key_1 = "productIds=" #обязательный параметр, который передается в запросе. Значение параметра зависит от URL

key_2 = "&store=" #обязательный параметр, который передается в запросе
store = "RU" #постоянное значение параметра key_2 (страна)

key_3 = "&currency=" #обязательный параметр, который передается в запросе
currency = "RUB" #постоянное значение параметра key_3 (валюта)

#Переменные окружения
email_sender = os.environ.get('ALBEL_EMAIL_SENDER')
email_password = os.environ.get('ALBEL_EMAIL_PASS')
email_receiver = os.environ.get('ALBEL_EMAIL_RECEIVER')
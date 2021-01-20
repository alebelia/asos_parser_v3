#Добавление товаров с asos.com/ru в список отслеживания

from asos_functions import *

#Формирование ссылки для GET-запроса
item_url = input('Введите ссылку на товар с asos.com/ru: ')[:-1]#Если программа запускается не через PyCharm, необходимо удалить "[:-1]"
item_url = item_url.rsplit('?')[0] #удаление лишних символов
item_id = item_url.split("/")[-1] #получение id товара из item_url
full_request_url = basic_request_url + key_1 + item_id + key_2 + store + key_3 + currency #адрес для GET-запроса

#Получение названия и цены товара
item_name = get_item_name(item_url, headers)
item_price = get_item_price(full_request_url)

#Проверка существования CSV-файла
csv_exists = check_csv(csv_file)
if csv_exists == True:
    url_found = check_url(csv_file, item_url) #Проверка наличия ссылки в данном файле
    if url_found == True:
        print('Данный товар уже записан в csv-файл.')
else:
    url_found = False
    create_csv(csv_file) #Если файл не существует, то будет создан

#Запись сведений о товаре в CSV-файл
if url_found == False:
    write_item(item_name, item_price, item_url, csv_file)

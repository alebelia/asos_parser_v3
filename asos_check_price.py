#Проверка актуальной цены на товары с asos.com/ru, добавленные в список отслеживания, и оповещение по электронной почте в случае ее изменения

from asos_functions import *

#Проверка существования CSV-файла
csv_exists = check_csv(csv_file)
if csv_exists == True:
    #Получение информации о товарах из CSV-файла
    items = []
    with open(csv_file, newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            items.append(row)
else:
    print('CSV-файл не найден.')

#Проверяем, изменилась ли цена на каждый из товаров. Если изменилась - создаем новую запись и обновленный CSV
changed_items = []
changed_items_positions = []
for item in items[1:]:
    old_price = item[1]
    url = item[2]
    item_id = url.split("/")[-1]  # получение id товара из url
    full_request_url = basic_request_url + key_1 + item_id + key_2 + store + key_3 + currency  # адрес для GET-запроса
    try:
        new_price = str(get_item_price(full_request_url))
    except:
        print('Не удалось получить цену товара по ссылке: ' + url)
        continue
    if old_price != new_price:
        print('Цена изменилась!')
        new_item = [item[0], new_price, url, 'Старая цена: '+ old_price]
        changed_items.append(new_item)
        changed_items_positions.append(items.index(item))
    else:
        print('Цена не изменилась.')

#Если цена на какие-либо товары изменилась, будет создан новый CSV-файл с обновленными ценами (старый будет удален)
if changed_items:
    with open(csv_file, newline='', encoding='utf-8') as file:
        #Создание списка из всего содержимого существующего CSV-файла
        csv_reader = csv.reader(file)
        all_info = list(csv_reader)
    #Удаление из полученного списка товаров, цена которых изменилась
    for changed_item in changed_items:
        for j in all_info:
            if changed_item[2] in j:
                all_info.remove(j)
    #Создание списка товаров, цена которых не изменилась, и товаров с обновленной ценой
    info_to_transfer = [k for k in all_info]
    for l in changed_items:
        info_to_transfer.append(l)

    #Сохранение полученного списка в CSV-файл с заменой содержимого
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        for n in info_to_transfer:
            csv_writer.writerow(n)
    print('CSV-файл обновлен.')

    #Формирование уведомления по электронной почте
    temp = []
    for o in changed_items:
        item_text = ', '.join(o)
        temp.append(item_text)
    email_text = '\n'.join(temp)
    email_text = MIMEText(email_text, 'plain', 'utf-8')

    #Отправка уведомления об изменении цен на электронную почту
    email_new_prices(email_sender, email_password, email_receiver, email_text)

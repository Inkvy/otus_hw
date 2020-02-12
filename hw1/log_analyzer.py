#!/usr/bin/env python
# -*- coding: utf-8 -*-


# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';

import os
import gzip
import re
from decimal import Decimal
from statistics import mean, median

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log"
}

# TOTAL_REQUESTS_COUNT = 0
# TOTAL_REQUESTS_TIME = 0
count_data = {
        'request_count': 0,
        'request_time': 0
    }
url_time = dict()
url_data = dict()


def lines_processing(line):
    # pattern_url = []  # there is will be  urls. Later remade to dict, where will be different information from each string
    # pattern_time = [] # there are will be  times. Later remade to dict, where will be different information from each string

    get_url = re.search(r'GET\s(.*)\sHTTP', line).group(1)
    get_time = re.search(r'([.\d]+)$', line).group(1)
    # print(line)
    # pattern_url.append(get_url)
    # pattern_time.append(get_time)
    url_time.setdefault(get_url, []).append(Decimal(get_time))

    count_data['request_count'] += 1
    count_data['request_time'] += Decimal(get_time)


def main():
    files = []  # there will bee files in folder ./log

    #check existing the folder - больше подходит для юнит-тестов
    os.path.exists('./logg')
    #get list files includes in folder
    list_files = os.listdir('./log')
    
    #get only files with 'nginx'
    for file in list_files:
         # if 'nginx-access-ui' in file:
         if file.startswith('nginx-access-ui'):
             files.append(file)

    # sorting list to get the last row
    files.sort()
    newest_log = files[-1]

    # create path at newest log
    path = './log/'+newest_log

    if '.gz' in newest_log:    
    #output all lines in gz-file
        total_requests_count = 0
        with gzip.open(path, 'rb') as f:
            for line in f:
                print(line.decode().strip())
                lines_processing(line.decode().strip())
                # print(line)
    else:
        with open(path, 'r+') as f:     # TODO нужный открыватель лога (open/gzip.open) перед парсингом можно выбрать через тернарный оператор
            for line in f:
                lines_processing(line)

    for row in url_time.items():
        # print(row)
        count_perc = round(100*len(row[1])/count_data['request_count'], 3)
        time_perc = Decimal(100*sum(row[1])/count_data['request_time']).quantize((Decimal('1.000')))
        time_med = median(row[1]).quantize((Decimal('1.000')))
        url_data[row[0]] = {'count': len(row[1]),
                            'count_perc': count_perc,
                            'time_sum': sum(row[1]),
                            'time_perc': time_perc,
                            'time_avg': sum(row[1])/len(row[1]), # TODO округлить до тысячных
                            'time_max': max(row[1]),
                            'time_med': time_med
                            }
        # print(url_data[row[0]])


    # print(pattern_url)
    # print(len(pattern_url))
    # print(pattern_time)
    # print(len(pattern_time))
    print(url_data)
    print(count_data['request_count'])
    print(count_data['request_time'])




if __name__ == "__main__":
    main()







"""

Логи лежать в папке "log"
1. Парсить логи по двум критериям: а) сервис(nginx), б) дата (получаю после сортировки свежий файл, но всё равно нужна дата)
2. После того как выбрали все даты нужного сервиса. Нужно найти самую свежую дату
3. Нашли дату - нужно открыть этот файл
4. Файл может быть как plain text, так и gz(архив)
5. Парсить строки файла
6. Данные хранить в словаре. Ключ - УРЛ, значение - список времен

TODO:
0. Библиотека logging + смотри блок ""Распространённые проблемы" в ДЗ
0.1. Путь не должен зависить от ОС. Он одинаково должен браться как из Windows, так и Linux
1. Скрипт должен уметь читать конфиги из другого файла(использовать try..)
    - На вход скрипту передаётся параметр - путь до файла или папки(а которой он будет искать самый свежий файл, который подойдёт под требуемый шаблон), который нужно открыть
    - Если по данному пути нет нужного файла, то выводим сообщение "нет такого файла"
    - Если файл не в нужном формате, то ошибку "Не верный формат"
    - Если параметр на вход не передан, то открывать "по умолчанию" из папки /log
2. "Основная фунциональность. Пункт 4." О каком конфиге идёт речь ? ЧТо за переменные ?
3. "Основная фунциональность. Пункт 2." Нужно парсить название файла, который разбираю и сохранять его (например, в папке с отработанными логами, или и так уже сохраняем обработанные логи, тогда проверять, что уже есть обработанные на данную дату)
4. Чтобы определить, что скрипт уже разбирался - нужно смотреть даты файлов/отчётов в папке REPORT_DIR

- разобрать строку через регулярное выражение

- [Done]когда фильтрую по названи файла, то использовать метод "начинается с"
- как передать переменную при вызове скрипта

- когда фильтрую по названи файла, то использовать метод "начинается с"

- когда накапливаю данные, то использовать словари и setdefault
    -[TODO] Если УРЛ повторяется, то в его списко добавлять новое значение времени

Автоматизация рутинных задач
стр. 223, 423
"""

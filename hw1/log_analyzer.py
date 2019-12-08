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


def main():
    files = [] # there will bee files in folder ./log
    # pattern_url = []  # there is will be  urls. Later remade to dict, where will be different information from each string
    # pattern_time = [] # there are will be  times. Later remade to dict, where will be different information from each string
    url_time = dict()
    url_data = dict()
    total_requests_count = 0
    total_requests_time = 0
    #check existing the folder
    os.path.exists('./log')
    #get list files includes in folder
    list_files = os.listdir('./log')
    
    #get only files with 'nginx'
    for file in list_files:
         if 'nginx-access-ui' in file:
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
    else:
        with open(path, 'r+') as f:     # TODO нужный открыватель лога (open/gzip.open) перед парсингом можно выбрать через тернарный оператор
            for line in f:
                get_url = re.search(r'GET\s(.*)\sHTTP', line).group(1)
                get_time = re.search(r'([.\d]+)$', line).group(1)
                # print(line)
                # pattern_url.append(get_url)
                # pattern_time.append(get_time)
                url_time.setdefault(get_url, []).append(Decimal(get_time))

                total_requests_count += 1
                total_requests_time += Decimal(get_time)


    for row in url_time.items():
        print(row)
        count_perc = round(100*len(row[1])/total_requests_count, 3)
        time_perc = Decimal(100*sum(row[1])/total_requests_time).quantize((Decimal('1.000')))
        time_med = median(row[1]).quantize((Decimal('1.000')))
        url_data[row[0]] = {'count': len(row[1]),
                            'count_perc': count_perc,
                            'time_sum': sum(row[1]),
                            'time_perc': time_perc,
                            'time_avg': sum(row[1])/len(row[1]), # TODO округлить до тысячных
                            'time_max': max(row[1]),
                            'time_med': time_med}
        print(url_data[row[0]])


    # print(pattern_url)
    # print(len(pattern_url))
    # print(pattern_time)
    # print(len(pattern_time))
    print(url_data)
    print(total_requests_count)
    print(total_requests_time)




if __name__ == "__main__":
    main()







"""

Логи лежать в папке "log"
1. Парсить логи по двум критериям: а) сервис(nginx), б) дата (получаю после сортировки свежий файл, но всё равно нужна дата)
2. После того как выбрали все даты нужного сервиса. Нужно найти самую свежую дату
3. Нашли дату - нужно открыть этот файл
4. Файл может быть как plain text, так и gz(архив)
5. Парсить строки файла

TODO:
0. Библиотека logging + смотри блок ""Распространённые проблемы" в ДЗ
1. Скрипт должен уметь читать конфиги из другого файла(использовать try..)
2. "Основная фунциональность. Пункт 4." О каком конфиге идёт речь ? ЧТо за переменные ?

- разобрать строку через регулярное выражение

- когда фильтрую по названи файла, то использовать метод "начинается с"

- когда накапливаю данные, то использовать словари и setdefault

Автоматизация рутинных задач
стр. 223, 423
"""
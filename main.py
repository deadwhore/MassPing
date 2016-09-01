# -*- coding: utf-8 -*-

import os
import datetime


def get_ip_list():
    ip_file = open('iplist.txt', 'r')
    ip_list = []
    for row in ip_file.readlines():
        if len(row) != 0:
            ip_list.append(row.strip())
    ip_file.close()
    return ip_list



def do_ping(ip):
    response = os.system('ping ' + ip + ' -w 10 -n 1 > NUL')
    if response == 0:
        return True
    else:
        return False


def get_count(elem):
    return elem[2]


def get_succ(elem):
    return elem[3]


# для выравнивания добавляем пробелы в конец IP-адреса
def add_spaces_15(ip):
    if len(ip) < 15:
        # если длина меньше 15, добавляем недостающие до 15 пробелы
        ip += " " * (15 - len(ip))
    return ip


# для выравнивания добавляем пробелы
def add_spaces_3(elem):
    strelem = str(elem)
    if len(strelem) < 3:
        # если длина меньше 15, добавляем недостающие до 15 пробелы
        strelem += " " * (3 - len(strelem))
    return strelem


# округляем до вменяемого числа и возвращаем текстом
def rounder(unsuc, suc):
    return str(round(round(unsuc/suc, 2) * 100)) + "%"


def show_stat(elem):
    print(
        add_spaces_15(elem[0]) + '  -    ' +
        ('YEAP!' if elem[1] == True else 'no :(') +
        '           ' + add_spaces_3(elem[2]) + '             ' +
        add_spaces_3(elem[3]) + '            ' +
        ('no one' if elem[3] == 0 else rounder(elem[3], elem[2]))
    )


def get_time():
    now_time = datetime.datetime.now()
    hour = now_time.hour
    minutes = now_time.minute
    seconds = now_time.second
    print('Time - ' + str(hour) + '.' + str(minutes) + '.' + str(seconds))


# -------------------------------


ping_ip = list()
ping_resp = list()  # статистика пингов (IP, последний результат, количество пакетов, успешные пакеты)
cur_loops = 0

print('')
print('')
print('')


for x in get_ip_list():
    ping_ip.append(x)
    ping_resp.append((x, False, 0, 0))

print('Ping started, plz wait')

while True:
    try:
        for i in range(0, len(ping_ip)):
            if do_ping(ping_ip[i]):
                ping_resp[i] = (ping_ip[i], True, (get_count(ping_resp[i])+1), (get_succ(ping_resp[i])+1))
            else:
                ping_resp[i] = (ping_ip[i], False, (get_count(ping_resp[i])+1), (get_succ(ping_resp[i])))

        os.system('cls' if os.name == 'nt' else 'clear')

        cur_loops += 1

        get_time()
        print('Times - ' + str(cur_loops))
        print('')
        print('.----- IP -----.   .- RESULT -.   .- COUNTS -.  .- SUCCESS -.  .- SUCC RATE -.')

        for w in ping_resp:
            print('')
            show_stat(w)

    except KeyboardInterrupt:
        print('')
        print('Pinging stopped by keybord, press any key to quit')
        input()
        break


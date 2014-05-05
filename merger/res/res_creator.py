#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'litleleprikon'


from datetime import datetime
import random
import string


def generate_log():
    str_gen = lambda: ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(5, 15)))
    name = str_gen().capitalize()
    surname = str_gen().capitalize()
    year = random.randint(2000, 2014)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    dt = datetime(year, month, day, hour, minute)
    mail = '{0:s}@yandex.ru'.format(str_gen())
    return '\t'.join((name, surname, mail, str(dt.date()), str(dt.time())[:-3]))


def main():
    with open('test3.txt', 'w') as file:
        for i in range(10000000):
            s = generate_log()
            print(s, file=file)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as ex:
        print("Keyboard interrupt")
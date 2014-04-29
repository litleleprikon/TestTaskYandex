#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'litleleprikon'

import re
import multiprocessing
from functools import partial
from time import sleep


def waiting_func(delay, text):
    sleep(delay)
    print(text)


def main():
    while True:
        query_parser = re.compile(r"(\d+(.\d+)?) (.+)")
        query = raw_input("Please input delay and text")
        checked_params = query_parser.search(query)
        if checked_params is None:
            raise Exception("Строка не соответствует формату '\"hh:mm\" out t'")
        params = checked_params.groups()
        delay = params[0]
        text = params[-1]
        worker = partial(waiting_func, delay=delay, text=text)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as ex:
        print("Goodbye!\n")
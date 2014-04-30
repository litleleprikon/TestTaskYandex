#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'litleleprikon'

import re
from multiprocessing import Process, Lock
from time import sleep


def waiting_func(delay, text, lock):
    with lock:
        sleep(delay)
        print(text)


def main():
    while True:
        query_parser = re.compile(r"(\d+(.\d+)?) (.+)")
        lock = Lock()

        query = raw_input("Please input delay and text or 'exit' to exit.\n")
        if query.lower().strip() == 'exit':
            return
        checked_params = query_parser.search(query)
        if checked_params is None:
            raise Exception("Bad string. string must be like '1.2 text'.\n")
        params = checked_params.groups()
        delay = float(params[0])

        text = params[-1]
        Process(target=waiting_func, args=(delay, text, lock)).start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as ex:
        print("Goodbye!\n")
    except Exception as ex:
        print(ex.message)
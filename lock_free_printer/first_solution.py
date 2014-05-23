#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'litleleprikon'


import re
import sys
import select
import time

timeout = 0.1  # seconds
last_work_time = time.time()


def waiting_func(delay, text):
    timeout = time.time() + delay
    while True:
        if time.time() >= timeout:
            print(text)
            break
        else:
            yield


def idle_work():
    global last_work_time
    now = time.time()
    # do some other stuff every 2 seconds of idleness
    if now - last_work_time > 2:
        print('Idle for too long; doing some other stuff.')
        last_work_time = now


def main_loop():
    query_parser = re.compile(r"(\d+(.\d+)?) (.+)")
    read_list = [sys.stdin]
    waitors = []
    print("Please input delay and text or 'exit' to exit.\n")
    while read_list:
        ready = select.select(read_list, [], [], timeout)[0]
        if ready:
            for file in ready:
                line = file.readline()
                if not line:
                    read_list.remove(file)
                elif line.rstrip():
                    if line.lower().strip() == 'exit':
                        print('\nGoodbye!\n')
                        return
                    checked_params = query_parser.search(line)
                    if checked_params is not None:
                        params = checked_params.groups()
                        delay = float(params[0])
                        text = params[-1]
                        waitors.append(waiting_func(delay, text))
                        print("Please input delay and text or 'exit' to exit.\n")
                    else:
                        print("Bad string. string must be like '1.2 text'.\n")
        for waitor in waitors:
            try:
                waitor.next()
            except StopIteration:
                pass


try:
    main_loop()
except KeyboardInterrupt:
    print('\nGoodbye!\n')
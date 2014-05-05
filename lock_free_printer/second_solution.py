#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'litleleprikon'

import re
import subprocess


def main():
    while True:
        query_parser = re.compile(r"(\d+(.\d+)?) (.+)")
        query = raw_input("Please input delay and text or 'exit' to exit.\n")
        if query.lower().strip() == 'exit':
            print('\nGoodbye!\n')
            return
        checked_params = query_parser.search(query)
        if checked_params is not None:
            params = checked_params.groups()
            delay = float(params[0])

            text = params[-1]
            subprocess.Popen('python printer.py -s {0:f} -t "{1:s}"'.format(delay, text), shell=True)
        else:
            print("Bad string. string must be like '1.2 text'.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as ex:
        print("\nGoodbye!\n")
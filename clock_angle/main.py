#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'litleleprikon'

import re


class QueryParser:
    """
        Class, that parse string and define programm parameters

        >>> qp = QueryParser('"03:00" deg m')
        >>> qp.hours
        3
        >>> qp.minutes
        0
        >>> qp.out_type
        'deg'
        >>> qp.clock_type
        'm'
    """
    def __init__(self, parse_string):

        self.hours = self.minutes = None
        self.out_type = None
        self.clock_type = None

        parse_string = parse_string.lower()
        input_reg_exp = re.compile(r'^"(\d{1,2}:\d{2})"\s+(rad|deg|dms)\s+(q|m)$')
        checked_params = input_reg_exp.search(parse_string)
        if checked_params is None:
            raise Exception("Строка не соответствует формату '\"hh:mm\" out t'")
        else:
            params = checked_params.groups()

        self.time_parser(params[0])
        self.output_type_parser(params[1])
        self.clock_type_parser(params[2])

    def time_parser(self, query):
        time = query.split(":")
        self.hours = int(time[0])
        self.minutes = int(time[1])

    def output_type_parser(self, query):
        allowed_alias = ["rad", "deg", "dms"]
        if query not in allowed_alias:
            raise Exception("Формат вывода результата неверен!")
        else:
            self.out_type = query

    def clock_type_parser(self, query):
        allowed_alias = ["m", "q"]
        if query not in allowed_alias:
            raise Exception("Формат вывода результата неверен!")
        else:
            self.clock_type = query


class Mathematician:

    def __init__(self):
        pass


def main():
    pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as ex:
        print("Keyboard interrupt")
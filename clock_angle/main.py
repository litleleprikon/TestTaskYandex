#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'litleleprikon'

import re

HELLO_MESSAGE = """
Введите исходные данные строкой в формате \"hh:mm\" out t
hh:mm - время
out - формат вывода, может быть rad, deg, dms
t - тип часов, может быть m - механические или q - кварцевые
"""


class QueryParser:
    """
        Class, that parse string and define programm parameters.
        @param parse_string: string like "hh:mm" out t' that should be parsed.

        >>> qp = QueryParser('"03:00" deg m')
        >>> qp.hours
        3
        >>> qp.minutes
        0
        >>> qp.out_type
        'deg'
        >>> qp.clock_type
        'm'
        >>> qp = QueryParser('"15:00" rad q')
        >>> qp.hours
        15
        >>> qp.minutes
        0
        >>> qp.out_type
        'rad'
        >>> qp.clock_type
        'q'
        >>> qp = QueryParser('"09:00 pm" dms q')
        >>> qp.hours
        9
        >>> qp.minutes
        0
        >>> qp.out_type
        'dms'
        >>> qp.clock_type
        'q'
    """
    def __init__(self, parse_string):

        self.hours = self.minutes = None
        self.out_type = None
        self.clock_type = None

        parse_string = parse_string.lower()
        input_reg_exp = re.compile(r'^"(\d{1,2}:\d{2})(\s+pm|am)?"\s+(rad|deg|dms)\s+(q|m)$')
        checked_params = input_reg_exp.search(parse_string)
        if checked_params is None:
            raise Exception("Строка не соответствует формату '\"hh:mm\" out t'")
        params = checked_params.groups()

        self.time_parser(params[0])
        self.output_type_parser(params[2])
        self.clock_type_parser(params[3])

    def time_parser(self, query):
        time_reg_exp = re.compile(r'(\d{1,2}):(\d{2})(\s+am|pm)?')
        time = time_reg_exp.search(query).groups()
        self.hours = int(time[0])
        self.minutes = int(time[1])

    def output_type_parser(self, query):
        allowed_alias = ["rad", "deg", "dms"]
        if query not in allowed_alias:
            raise Exception("Формат вывода результата неверен!")
        self.out_type = query

    def clock_type_parser(self, query):
        allowed_alias = ["m", "q"]
        if query not in allowed_alias:
            raise Exception("Формат типа часов неверен!")
        self.clock_type = query


class Mathematician:
    """
    Class that calculate angle between hour and minute arrws in clocks
    @param params QueryParser's object which parsed query string
    >>> Mathematician(QueryParser('"09:00 pm" dms q')).result_angle
    "270.0'0''"
    >>> Mathematician(QueryParser('"03:00" deg m')).result_angle
    90
    >>> Mathematician(QueryParser('"15:00" rad q')).result_angle
    1.5708
    """
    def __init__(self, params):
        if not isinstance(params, QueryParser):
            raise Exception("В функцию подсчета угла передан неправильный параметр")
        self.result_angle = None
        self.hours = params.hours % 12
        self.minutes = params.minutes % 60
        self.calculate(params.clock_type)
        self.format_result(params.out_type)

    def calculate(self, clock_type):
        OHA = 30  # One Hour Arc
        hours_angle = 360 * (self.hours/12) + (OHA * self.minutes/60 if clock_type is 'q' else 0)
        minutes_angle = 360 * (self.minutes/60)
        self.result_angle = abs(hours_angle - minutes_angle)

    def format_result(self, out_type):
        PI = 3.1415926

        if out_type == 'deg':
            self.result_angle = int(self.result_angle)
            return
        elif out_type == 'rad':
            self.result_angle = round(self.result_angle * PI/180, 4)
            return
        elif out_type == 'dms':
            degrees = self.result_angle % 1
            mnt, sec = divmod(self.result_angle*3600, 60)
            deg, mnt = divmod(mnt, 60)
            self.result_angle = "{d:.0f}.{m:.0f}'{s:.0f}''".format(d=deg, m=mnt, s=sec)
        else:
            raise Exception("Формат вывода результата неверен!")


def main():
    try:
        input_string = input(HELLO_MESSAGE)
        params = QueryParser(input_string)
        result = Mathematician(params).result_angle
        print(result)
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as ex:
        print(ex)
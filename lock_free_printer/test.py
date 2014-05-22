#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'litleleprikon'

import re
import time
import curses


MAX_VERTICAL_CHARS = 10
MAX_HORIZONTAL_CHARS = 80


class Main(object):
    def __init__(self):
        self.stdscr = curses.initscr()
        self.stdscr.timeout(100)
        self.std_input = self.std_listener()
        self.to_print = []
        self.waiting_workers = []
        self.query_parser = re.compile(r"(\d+(.\d+)?) (.+)")

    def waiting_func(self, delay, text):
        timeout = time.time() + delay
        while True:
            if time.time() >= timeout:
                self.print_string(text)
                break
            else:
                yield

    def print_string(self, message="Please input delay and text or 'exit' to exit.\n"):
        while True:
            if len(self.to_print) > MAX_VERTICAL_CHARS - 1:
                self.to_print = self.to_print[-(MAX_VERTICAL_CHARS-1):]
            if len(message) > MAX_HORIZONTAL_CHARS:
                message = message[-MAX_HORIZONTAL_CHARS:]
            self.to_print.append(message)
            for line_num, line in enumerate(self.to_print):
                self.stdscr.addstr(line_num, 0, line)
            self.stdscr.refresh()

    def print_chars(self, chars):
        pass

    def run(self):
        while True:
            query = self.std_input.next()
            if query:
                if query.lower().strip() == 'exit':
                    self.print_string('\nGoodbye!\n')
                    return
                checked_params = self.query_parser.search(query)
                if checked_params is not None:
                    params = checked_params.groups()
                    delay = float(params[0])
                    text = params[-1]
                    self.waiting_workers.append(self.waiting_func(delay, text))
                    for worker in self.waiting_workers:
                        try:
                            worker.next()
                        except StopIteration:
                            self.waiting_workers.remove(worker)
                else:
                    self.print_string("Bad string. string must be like '1.2 text'.\n")

    def std_listener(self):
        return_str = ""
        while True:
            char_code = self.stdscr.getch()
            if char_code == -1:
                yield False
            elif char_code == 10:
                yield return_str
            else:
                return_str += chr(char_code)
                yield False


if __name__ == "__main__":
    try:
        main = Main()
        main.run()
    except KeyboardInterrupt as ex:
        pass



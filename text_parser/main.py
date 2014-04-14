#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'litleleprikon'


import multiprocessing
import re
from os import path
import stemming


def timeit(func):

    """
    simple decorator, that measure time

    @rtype : object
    @param func: function, we want to check
    @return: func's result
    """
    import time

    def timed(*args, **kw):
        ts = time.time()
        result = func(*args, **kw)
        te = time.time()

        print('%r (%r, %r) %2.2f sec' % (func.__name__, args, kw, te-ts))
        return result

    return timed


def file_chooser():
    """
    Function search file

    @return: file stream from existing file
    """
    while True:
        # file_path = input("Введите путь к входному файлу\n")
        file_path = r"D:\Documents\Projects\TestTaskYandex\text_parser\res\Lorem ipsum.txt"  # TODO REMOVE!!!!
        if path.exists(file_path):
            if path.isfile(file_path):
                return open(file_path, 'r')
        raise Exception("Данного файла не существует!\n")


class TextParser:
    def __init__(self, input_file):
        self.result = None

        self.text = input_file.read()

        sentence_splitter = re.compile(r"([.!?]\W*)|\n+")
        word_splitter = re.compile(r"\b[,.?!-]*\W+\b")
        sentences_list = sentence_splitter.split(self.text)
        words_appearance = {}
        for sentence_num, sentence in enumerate(sentences_list):
            words_list = word_splitter.split(self.text.lower())
            for word in words_list:
                if word in words_appearance.keys():
                    if not sentence_num in words_appearance[word]:
                        words_appearance[word].append(sentence_num)
                else:
                    words_appearance[word] = [int(sentence_num)]
        print()


class Searcher:
    def __init__(self, parsed_dic):
        self.result = None


def main():
    try:
        input_file = file_chooser()
        parsed = TextParser(input_file).result
        result = Searcher(parsed).result
        print(result)
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as ex:
        print("Keyboard interrupt")
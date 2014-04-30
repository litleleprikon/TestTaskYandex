#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'litleleprikon'


from multiprocessing import Pool, Queue
from functools import partial
import re
from os import path


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
        file_path = r"F:\GitHub\TestTaskYandex\text_parser\res\1984.txt"  # TODO REMOVE!!!!
        if path.exists(file_path):
            if path.isfile(file_path):
                return open(file_path, 'r')
        raise Exception("Данного файла не существует!\n")


class TextParser:
    def __init__(self, input_file):
        self.result_dict = dict()

        self.text = input_file.read()

        # sentence_splitter = re.compile(r"(\S.+?[.!?])(?=\s+|$)")
        sentence_splitter = re.compile(r"([.!?]\W*)|[\n\t]+")
        word_splitter = re.compile(r"\b[,.?!-]*\W+\b")
        self.sentences_list = sentence_splitter.split(self.text)

        for i in enumerate(self.sentences_list):
            self.result_callback(TextParser.sentence_parser(word_splitter, i))

        print("1")

    def result_callback(self, result_pairs):
        for key, value in result_pairs:
            if key in self.result_dict.keys():
                self.result_dict[key].append(value)
            else:
                self.result_dict[key] = [value]

    @staticmethod
    def sentence_parser(re_pattern, sentence):
        sentence_num = sentence[0]
        sentence = sentence[1]
        words_list = re_pattern.split(sentence)
        res = []
        for word in words_list:
            res.append((word, sentence_num))
        return res


class Searcher:
    def __init__(self, parsed_dic):
        words_list = input("Введите поисковые слова через пробел\n").lower().split()
        a = set(parsed_dic[words_list.pop()])
        for word in words_list:
            try:
                b = set(parsed_dic[word])
                a = a & b
            except KeyError:
                print("Слова '{w:s}' нет в тексте, поиск окончен".format(w=word))
                return
        self.result = list(a)


def main():
    try:
        input_file = file_chooser()
        parser = TextParser(input_file)
        parsed = parser.result_dict
        result = Searcher(parsed).result
        for s in list(result):
            print(parser.sentences_list[s])
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as ex:
        print("Keyboard interrupt")
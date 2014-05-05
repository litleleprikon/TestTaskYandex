#!/usr/bin/env python3.3
# -*- coding:utf-8 -*-
__author__ = 'litleleprikon'

import argparse
from os import path, makedirs
from multiprocessing import Pool
from functools import partial
import shutil


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", default=6)
    parser.add_argument("-m", default=1024)
    parser.add_argument('folder', nargs='?',
                        default=r"C:\Users\Emil\Documents\Projects\TestTaskYandex\merger\res\test.txt")
    return parser


def file_opener(file_path, memory):
    """
    Function that check file and open it

    @return: generator
    """
    if not path.exists(file_path):
        raise Exception("Данного файла не существует!\n")
    if not path.isfile(file_path):
        raise Exception("Данного файла не существует!\n")
    with open(file_path, 'r') as file:
        while True:
            lines = file.readlines(memory)
            if not lines:
                break
            yield lines


def sorter(data, temp_dir):
    file_num = data[0]
    lines = data[1]
    temp_file = '{dir:s}/{file:d}.txt'.format(dir=temp_dir, file=file_num)
    # lines.sort(key=lambda x: x[-17:])  # работает быстрее, но будет ошибаться, если год<1000 или год>9999
    lines.sort(key=lambda x: ' '.join(x.split('\t')[-2:]))
    with open(temp_file, 'w') as file:
        for line in lines:
            print(line, file=file, end='')
            # return lines.sort(key=lambda x: ' '.join(x.split()[-2:]))


def merger(data, temp_dir):
    pass


def main():
    parser = create_parser()
    namespace = parser.parse_args()
    temp_dir = 'temp'
    if not path.exists(temp_dir):
        makedirs(temp_dir)

    worker = partial(sorter, temp_dir=temp_dir)

    # for lines in file_opener('11', 1024):
    #     worker(lines=lines)
    pool = Pool(namespace.n)
    pool.map(worker, enumerate(file_opener(namespace.folder, namespace.m)))
    # pool.map(worker, file_opener(namespace.folder, namespace.m))
    # print(namespace.n)
    # print(namespace.m)
    # print(namespace.folder)
    # shutil.rmtree(temp_dir)  # TODO


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as ex:
        print("\nGoodbye!\n")
import os
import sys
import random

from distributions import *

DEFAULT_FILE_IN = 'rnd.dat'
DEFAULT_FILE_OUT = 'rnd_out.dat'

DISTS_DICT = {}


def handle_windows_style():
    args = sys.argv[1:]
    for idx, arg in enumerate(args):
        if '/' in arg:
            arg = arg.replace('/', '--')
            if ':' in arg:
                args.insert(idx + 1, arg[arg.index(':') + 1:])
                arg = arg[:arg.index(':')]
            args[idx] = arg

    return args


def handle_dist(args: list):
    if '--d' in args:
        dist_name = args[args.index('--d') + 1]
        print('Выбрано распределение {}'.format(dist_name) + SEPARATOR)
        return dist_name

    dist_name = random.choice(list(DISTS_DICT.keys()))
    print('Случайным образом выбрано распределение {}'.format(dist_name) + SEPARATOR)
    return dist_name


def handle_file_in(args):
    """
    Разбор параметра f - входной файл и считывание ПСП
    Возвращает список значений ПСП из файла
    Разделитель - символ новой строки
    """
    filename = args.f if args.f else DEFAULT_FILE_IN
    if not os.path.exists(os.path.abspath(filename)):
        raise Exception('Не найден входной файл с ПСП!')
    line_to_default = '' if args.fout else 'по умолчанию '
    print('Чтение будет производиться из файла {}{}'.format(line_to_default, filename))

    with open(os.path.abspath('rnd.dat')) as file_in:
        values = list(map(int, file_in.read().split('\n')))
    print('Считано {} значений ПСП'.format(len(values)))
    return values


def handle_file_out(args, values):
    """
    Разбор параметра fout - выходной файл с преобразованной ПСП
    Производит запись в файл
    Разделитель - символ новой строки
    """
    filename = args.fout if args.fout else DEFAULT_FILE_OUT
    line_to_default = '' if args.fout else ' по умолчанию'
    print('Запись будет производиться в файл {}{}'.format(line_to_default, filename) + SEPARATOR)
    with open(os.path.abspath('rnd.dat'), 'w') as file_out:
        file_out.write('\n'.join(values))
    print('Последовательность успешно записана' + SEPARATOR)


def handle_usage(args):
    if '--h' in args:
        print("Строка о помощи")
        sys.exit(0)

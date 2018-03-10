import os
import sys

from task_2.distributions import *
from task_2.distributions.dist_st import *
from task_2.distributions.dist_tr import *
from task_2.distributions.dist_ex import *
from task_2.distributions.dist_nr import *
from task_2.distributions.dist_gm import *
from task_2.distributions.dist_ln import *
from task_2.distributions.dist_ls import *
from task_2.distributions.dist_bi import *

DEFAULT_FILE_IN = 'rnd.dat'
DEFAULT_FILE_OUT = 'rnd_out.dat'

DISTS_DICT = {
    'st': DistST, 'tr': DistTR, 'ex': DistEX, 'nr': DistNR,
    'gm': DistGM, 'ln': DistLN, 'ls': DistLS, 'bi': DistBI
}


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


def handle_dist(args):
    if args.d:
        print('Выбрано распределение {}'.format(args.d) + SEPARATOR)
        return args.d

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
    print('Чтение будет производиться из файла {}{}'.format('' if args.fout else 'по умолчанию ', filename))

    with open(os.path.abspath(filename)) as file_in:
        values = file_in.read().split('\n')
        values = list(map(int, values))
    print('Считано {} значений ПСП'.format(len(values)) + SEPARATOR)
    return values


def handle_file_out(args, values):
    """
    Разбор параметра fout - выходной файл с преобразованной ПСП
    Производит запись в файл
    Разделитель - символ новой строки
    """
    filename = args.fout if args.fout else DEFAULT_FILE_OUT
    print('Запись будет производиться в файл {}{}'.format('' if args.fout else 'по умолчанию ', filename) + SEPARATOR)
    with open(os.path.abspath(filename), 'w') as file_out:
        file_out.write('\n'.join(map(str, values)))
    print('Последовательность успешно записана' + SEPARATOR)


def handle_usage(args):
    if '--h' in args:
        print("Строка о помощи")
        sys.exit(0)

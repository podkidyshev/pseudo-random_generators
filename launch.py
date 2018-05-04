import os
import sys

from distributions.dist_st import *
from distributions.dist_tr import *
from distributions.dist_ex import *
from distributions.dist_nr import *
from distributions.dist_gm import *
from distributions.dist_ln import *
from distributions.dist_ls import *
from distributions.dist_bi import *

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
    if '--h' not in args:
        return

    if args.index('--h') == len(args) - 1 or args[args.index('--h') + 1][:2] == '--':
        s = """Возможные параметры:

/h - получение справки о работе программы
/h:<dist> получение справки о распределении dist
Возможные значения gen: {}

/d:<dist> выбор распределения из списка (по умолчанию веберется случайно)

/p1: /p2: /p3: - параметры распределения. Для подробной справки для каждого распределения см. /h:<dist>
Параметры для каждого распределения являются вещественными числами и могут генерироваться, если не указаны в аргументах

/f: файл для чтения ПСП. По умолчанию: rnd.dat в каталоге запуска процесса
/fout: файл для записи преобразованной ПСП. По умолчанию: rnd_out.dat в каталоге запуска процесса
Возможно введение как абсолютного, так и относительного пути для файлов
    """.format(', '.join(DISTS_DICT.keys()))
        print(s)
    else:
        dist_name = args[args.index('--h') + 1]
        if dist_name in DISTS_DICT.keys():
            dist_class = DISTS_DICT[dist_name]
            print("Описание генератора {} ({}):".format(dist_name, dist_class.NAME) + SEPARATOR, end='')
            dist_class.usage()
        else:
            raise Exception('Неизвестное значение параметра для h: выберите одно из: {}'
                            .format(', '.join(DISTS_DICT.keys())))
    sys.exit(0)

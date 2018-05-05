import os
import random
import argparse

from utils import *

from generators.p5 import Gen5p
from generators.add import GenAdd
from generators.bbs import GenBBS
from generators.lc import GenLC
from generators.lfsr import GenLFSR
from generators.mt import GenMT
from generators.nfsr import GenNFSR
from generators.rc4 import GenRC4
from generators.rsa import GenRSA

from distributions.st import *
from distributions.tr import *
from distributions.ex import *
from distributions.nr import *
from distributions.gm import *
from distributions.ln import *
from distributions.ls import *
from distributions.bi import *

GENS_DICT = {
    '5p': Gen5p,
    'add': GenAdd,
    'bbs': GenBBS,
    'lc': GenLC,
    'lfsr': GenLFSR,
    'nfsr': GenNFSR,
    'mt': GenMT,
    'rc4': GenRC4,
    'rsa': GenRSA,
}

DISTS_DICT = {
    'st': DistST, 'tr': DistTR, 'ex': DistEX, 'nr': DistNR,
    'gm': DistGM, 'ln': DistLN, 'ls': DistLS, 'bi': DistBI
}


def handle_gen(args: list):
    if '--g' in args:
        gen_name = args[args.index('--g') + 1]
        print('Выбран генератор {}'.format(gen_name) + SEPARATOR)
        return gen_name

    gen_name = random.choice(list(GENS_DICT.keys()))
    print('Случайным образом выбран генератор {}'.format(gen_name) + SEPARATOR)
    return gen_name


def init_gen_parser(parser: argparse.ArgumentParser, gen_name: str):
    params = GENS_DICT[gen_name].PARAMS

    for param_name in params:
        parser.add_argument('--{}'.format(param_name))


def handle_dist(args):
    if args.d:
        print('Выбрано распределение {}'.format(args.d) + SEPARATOR)
        return args.d

    dist_name = random.choice(list(DISTS_DICT.keys()))
    print('Случайным образом выбрано распределение {}'.format(dist_name) + SEPARATOR)
    return dist_name


def handle_file_gen(args, values):
    """
    Разбор параметра f - выходной файл со сгенерированной ПСП
    Производит запись в файл
    Разделитель - символ новой строки
    """
    filename = args.f if args.f else DEFAULT_FILE_IN
    line_to_default = '' if args.f else 'по умолчанию '
    print('Запись будет производиться в файл {}{}'.format(line_to_default, filename))

    with open(os.path.abspath(filename), 'w') as file_out:
        file_out.write('\n'.join(map(str, values)))
    print('Последовательность успешно записана')


def handle_file_dist_in(args):
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


def handle_file_dist_out(args, values):
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


def handle_usage_gen(args):
    if '--h' not in args:
        return
    if args.index('--h') == len(args) - 1 or args[args.index('--h') + 1][:2] == '--':
        s = """Возможные параметры:

/h - получение справки о работе программы
/h:<gen> получение справки о генераторе gen
Возможные значения gen: {}

/n:<count> количество генерируемых чисел, по умолчанию 10000

/g:<gen> выбор генератора из списка (по умолчанию веберется случайно)

/i:<i1 i2...> инициализационный вектор. Может содержать несколько значений 
Каждое значение после первого вводится далее через пробел в сторогом порядке. 
Количество значений для каждого генератора фиксировано
Для подробной справки о векторе для каждого генератора смотрите в /h<gen>
Каждый генератор может сам сгенерировать подходящий вектор

/f:<filename> - файл для записи сгенерированных чисел. По умолчанию запись ведется в rnd.dat в каталоге запуска процесса
Возможно введение как абсолютного, так и относительного пути для файла

/<a>:<a_v> - каждый генератор имеет свои параметры. Для справки по ним введите /h:gen
ВСЕ параметры генераторов - числа. 
Возможен ввод чисел в двоичном виде. Для этого бинарный массив <arr> введите как 0b<arr> (например, /p:0b1000 эквивалентно /p:8)
Если требуется полином над GF(2) - введите его эквивалент в десятичной или двоичной системе счисления

/gui - построение в отдельном окне графика с построенными числами (максимальное число точек - 200, иначе построение
графика производится не будет (без ошибки))
""".format(', '.join(GENS_DICT.keys()))
        print(s)
    else:
        gen_name = args[args.index('--h') + 1]
        if gen_name in GENS_DICT.keys():
            gen_class = GENS_DICT[gen_name]
            print("Описание генератора {} ({}):".format(gen_name, gen_class.NAME) + SEPARATOR)
            print("Возможные параметры: {}".format(', '.join(GENS_DICT[gen_name].PARAMS)))
            print(SEPARATOR[1:], end='')
            GENS_DICT[gen_name].usage()
        else:
            raise Exception('Неизвестное значение параметра для h: выберите одно из: {}'
                            .format(', '.join(GENS_DICT.keys())))
    sys.exit(0)


def handle_usage_dist(args):
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

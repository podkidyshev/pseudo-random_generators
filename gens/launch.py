import os
import sys
import random
import argparse

from generators import SEPARATOR
from generators.gen_5p import Gen5p
from generators.gen_add import GenAdd
from generators.gen_bbs import GenBBS
from generators.gen_lc import GenLC
from generators.gen_lfsr import GenLFSR
from generators.gen_mt import GenMT
from generators.gen_nfsr import GenNFSR
from generators.gen_rc4 import GenRC4
from generators.gen_rsa import GenRSA


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

DEFAULT_FILE = 'rnd.dat'


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


def handle_gen(args: list):
    if '--g' in args:
        gen_name = args[args.index('--g') + 1]
        print('Выбран генератор {}'.format(gen_name) + SEPARATOR)
        return gen_name

    gen_name = random.choice(list(GENS_DICT.keys()))
    print('Случайным образом выбран генератор {}'.format(gen_name) + SEPARATOR)
    return gen_name


def init_parser(parser: argparse.ArgumentParser, gen_name: str):
    params = GENS_DICT[gen_name].PARAMS

    for param_name in params:
        parser.add_argument('--{}'.format(param_name))


def handle_file(args, values):
    """
    Разбор параметра f - выходной файл со сгенерированной ПСП
    Производит запись в файл
    Разделитель - символ новой строки
    """
    filename = args.f if args.f else DEFAULT_FILE
    line_to_default = '' if args.f else 'по умолчанию '
    print('Запись будет производиться в файл {}{}'.format(line_to_default, filename))

    with open(os.path.abspath(filename), 'w') as file_out:
        file_out.write('\n'.join(map(str, values)))
    print('Последовательность успешно записана')


def handle_usage(args):
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


def handle_bins(args):

    def handle_bin(v):
        if isinstance(v, str) and v[:2] == '0b':
            return int(v, 2)
        return v

    for arg, value in args.__dict__.items():
        if not isinstance(value, list):
            setattr(args, arg, handle_bin(value))
        else:
            for idx in range(len(value)):
                value[idx] = handle_bin(value[idx])

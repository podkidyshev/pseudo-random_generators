import sys
import random
import argparse

import generators
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


def handle_gen(args: list):
    if '--g' in args:
        gen_name = args[args.index('--g') + 1]
        print('Выбран генератор {}'.format(gen_name) + generators.SEPARATOR)
        return gen_name

    gen_name = random.choice(list(GENS_DICT.keys()))
    print('Случайным образом выбран генератор {}'.format(gen_name) + generators.SEPARATOR)
    return gen_name


def init_parser(parser: argparse.ArgumentParser, gen_name: str):
    params = GENS_DICT[gen_name].PARAMS

    for param_name in params:
        parser.add_argument('--{}'.format(param_name), type=int)


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

/f: файл для записи сгенерированных чисел. По умолчанию запись ведется в rnd.dat в каталоге запуска процесса
Возможно введение как абсолютного, так и относительного пути для файла

/<a>:<a_v> - каждый генератор имеет свои параметры. Для справки по ним введите /h:gen
ВСЕ параметры генераторов - числа. Если требуется полином над GF(2) - введите его эквивалент в десятичной форме (число)
""".format(', '.join(GENS_DICT.keys()))
        print(s)
    else:
        gen_name = args[args.index('--h') + 1]
        if gen_name in GENS_DICT.keys():
            gen_class = GENS_DICT[gen_name]
            print("Описание генератора {} ({}):".format(gen_name, gen_class.NAME) + generators.SEPARATOR)
            print("Возможные параметры: {}".format(', '.join(GENS_DICT[gen_name].PARAMS)))
            print(generators.SEPARATOR[1:], end='')
            GENS_DICT[gen_name].usage()
        else:
            raise Exception('Неизвестное значение параметра для h: выберите одно из: {}'
                            .format(', '.join(GENS_DICT.keys())))
    sys.exit(0)

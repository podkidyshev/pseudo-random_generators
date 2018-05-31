import os
import sys

import utils

from generators.p5 import Gen5p
from generators.add import GenAdd
from generators.bbs import GenBBS
from generators.lc import GenLC
from generators.lfsr import GenLFSR
from generators.mt import GenMT
from generators.nfsr import GenNFSR
from generators.rc4 import GenRC4
from generators.rsa import GenRSA

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

DEFAULT_GEN_NAME = 'lc'
DEFAULT_PLOT_MAX_VALUES = 200


def init_args(parser, args):
    """Инициализация аргументов для конкретного генератора"""
    gen_name = args[args.index('--g') + 1] if '--g' in args else DEFAULT_GEN_NAME
    print('INFO: выбран генератор {}{}'.format('' if '--g' in args else 'по умолчанию ', GENS_DICT[gen_name].NAME))
    print(utils.SEPARATOR)
    for param_name in GENS_DICT[gen_name].PARAMS:
        parser.add_argument('--{}'.format(param_name), action=utils.CheckIntAction)


def write(args, values):
    """
    Разбор параметра f - выходной файл со сгенерированной ПСП
    Производит запись в файл
    Разделитель - символ новой строки
    """
    filename = args.f if args.f else utils.DEFAULT_FILE_IN
    line_to_default = '' if args.f else 'по умолчанию '
    print('INFO: Запись будет производиться в файл {}{}'.format(line_to_default, filename))

    with open(os.path.abspath(filename), 'w') as file_out:
        file_out.write('\n'.join(map(str, values)))
    print('INFO: Последовательность успешно записана')
    print(utils.SEPARATOR)


def plot(args, values):
    if not args.gui:
        return
    if len(values) > DEFAULT_PLOT_MAX_VALUES:
        print('WARN: Слишком много чисел для отображения. Максимум = {}.'.format(DEFAULT_PLOT_MAX_VALUES))
        print(utils.SEPARATOR)
        return

    import matplotlib.pyplot as plt
    plt.figure()
    for idx, value in enumerate(values):
        plt.scatter(idx, value)
    plt.show()


def usage(args):
    if '--h' not in args:
        return

    if utils.check_h_value(args):
        # Общая справка
        s = """Возможные параметры:

/h - получение справки о работе программы
/h:<gen> получение справки о генераторе gen
Возможные значения gen: {}

/n:<count> количество генерируемых чисел, по умолчанию 10000

/g:<gen> выбор генератора из списка (по умолчанию веберется случайно)

/i:<i1 i2...> инициализационный вектор. Может содержать несколько значений 
Каждое значение после первого вводится далее через пробел в сторогом порядке. 
Количество значений для каждого генератора фиксировано.
Для подробной справки о векторе для каждого генератора смотрите в /h<gen>.
Каждый генератор может сам сгенерировать подходящий инициализационный вектор.

/f:<filename> - файл для записи сгенерированных чисел. По умолчанию запись ведется в rnd.dat в каталоге запуска процесса
Возможно введение как абсолютного, так и относительного пути для файла

/<a>:<a_v> - каждый генератор имеет свои параметры. Для справки по ним введите /h:gen
ВСЕ параметры генераторов - целые числа 
Возможен ввод целых чисел в двоичном виде как 0b<bin>, например /arg:0b1001 эквивалентно /arg:9
Если требуется полином над GF(2) - введите его эквивалент в десятичной или двоичной системе счисления

/gui - построение в отдельном окне графика с построенными числами (максимальное число точек - 200, иначе построение
графика производится не будет (без ошибки))
""".format(', '.join(GENS_DICT.keys()))
        print(s)
        return

    gen_name = args[args.index('--h') + 1]
    # Проверяем корректность аргумента
    if gen_name not in GENS_DICT.keys():
        print('ERR: Неизвестное значение /h выберите одно из: {}'.format(', '.join(GENS_DICT.keys())))
        sys.exit(0xE)

    # Выводим хелп для конкретного генератора
    gen_class = GENS_DICT[gen_name]
    print("Описание генератора {} ({}):".format(gen_name, gen_class.NAME))
    print("Возможные параметры: {}".format(', '.join(gen_class.PARAMS)))
    GENS_DICT[gen_name].usage()
    return

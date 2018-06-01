import os
import sys

import utils

from distributions.st import DistST
from distributions.tr import DistTR
from distributions.ex import DistEX
from distributions.nr import DistNR
from distributions.gm import DistGM
from distributions.ln import DistLN
from distributions.ls import DistLS
from distributions.bi import DistBI

DISTS_DICT = {
    'st': DistST, 'tr': DistTR, 'ex': DistEX, 'nr': DistNR,
    'gm': DistGM, 'ln': DistLN, 'ls': DistLS, 'bi': DistBI
}

DEFAULT_DIST_NAME = 'st'
DEFAULT_HIST_COUNT = 25


def read(args):
    """
    Разбор параметра f - входной файл и считывание ПСП
    Возвращает список значений ПСП из файла
    Разделитель - символ новой строки
    """
    filename = args.f if args.f else utils.DEFAULT_FILE_IN
    if not os.path.exists(os.path.abspath(filename)):
        raise Exception('Не найден входной файл с ПСП!')
    print('INFO: Чтение будет производиться из файла {}{}'.format('' if args.f else 'по умолчанию ', filename))

    with open(os.path.abspath(filename)) as file_in:
        values = file_in.read().split('\n')
        values = list(map(int, values))
    print('INFO: Считано {} значений ПСП'.format(len(values)))

    print(utils.SEPARATOR)
    return values


def write(args, values):
    """
    Разбор параметра fout - выходной файл с преобразованной ПСП
    Производит запись в файл
    Разделитель - символ новой строки
    """
    filename = args.fout if args.fout else utils.DEFAULT_FILE_OUT
    print('INFO: Запись будет производиться в файл {}{}'.format('' if args.fout else 'по умолчанию ', filename))
    with open(os.path.abspath(filename), 'w') as file_out:
        file_out.write('\n'.join(map(str, values)))
    print('INFO: Последовательность успешно записана')
    print(utils.SEPARATOR)


def plot(args, values, values_reference):
    if not args.gui:
        return

    import matplotlib.pyplot as plt
    plt.figure()
    plt.subplot(1, 2, 1)
    plt.title('Преобразованная ПСП')
    plt.hist(values, DEFAULT_HIST_COUNT)

    plt.subplot(1, 2, 2)
    plt.title('Генерация системными функциями')
    plt.hist(values_reference, DEFAULT_HIST_COUNT)
    plt.show()


def usage(args):
    if '--h' not in args:
        return

    if utils.check_h_value(args):
        # Общая справка
        s = """Возможные параметры:

/h - получение справки о работе программы
/h:<dist> получение справки о распределении dist
Возможные значения gen: {}

/d:<dist> выбор распределения из списка (по умолчанию веберется случайно)

/p1: /p2: /p3: - параметры распределения. Для подробной справки для каждого распределения см. /h:<dist>
Параметры для каждого распределения являются вещественными числами и могут генерироваться автоматически

/f: файл для чтения ПСП. По умолчанию: rnd.dat в каталоге запуска процесса
/fout: файл для записи преобразованной ПСП. По умолчанию: rnd_out.dat в каталоге запуска процесса
Возможно введение как абсолютного, так и относительного пути для файлов
    """.format(', '.join(DISTS_DICT.keys()))
        print(s)
        sys.exit(0)

    dist_name = args[args.index('--h') + 1]
    # Проверяем корректность аргумента
    if dist_name not in DISTS_DICT.keys():
        print('ERR: Неизвестное значение /h выберите одно из: {}'.format(', '.join(DISTS_DICT.keys())))
        sys.exit(0xE)

    # Выводим хелп для конкретного распределения
    dist_class = DISTS_DICT[dist_name]
    print("Описание параметров распределения {} ({}):".format(dist_name, dist_class.NAME), end='')
    dist_class.usage()
    sys.exit(0)

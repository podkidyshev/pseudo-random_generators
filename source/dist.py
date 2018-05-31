import sys
import time
import argparse

import utils
import utils.launch_dist as launch


def init_args(parser):
    """Параметры только для преобразования ПСП"""
    parser.add_argument('--d', default=launch.DEFAULT_DIST_NAME)
    parser.add_argument('--p1', type=float)
    parser.add_argument('--p2', type=float)
    parser.add_argument('--p3', type=float)


def parse_args():
    args = utils.get_args()
    # Обработка /h аргумента
    launch.usage(args)
    # Добавление аргументов
    parser = argparse.ArgumentParser()
    init_args(parser)
    parser.add_argument('--f', help='Имя выходного файла с выходной ПСП')
    parser.add_argument('--fout', help='Имя выходного файла')
    parser.add_argument('--gui', action='store_true')
    # Парсинг
    return parser.parse_args(args)


def transform(args, values_in):
    if args.d not in launch.DISTS_DICT:
        print('ERR: некорректное значение /g:{}. Смотрите справку /h'.format(args.d))
        sys.exit(0)

    print('INFO: Инициализация распределения {}'.format(launch.DISTS_DICT[args.d].NAME))
    dist = launch.DISTS_DICT[args.d](args)

    print('INFO: Старт преобразования')
    time_start = time.time()
    values_out, values_reference = dist.transform(values_in)
    time_elapsed = int((time.time() - time_start) * 1000)

    print('INFO: Преобразование заняло {} милисекунд'.format(time_elapsed))
    print(utils.SEPARATOR)
    return values_out, values_reference


def main():
    args = parse_args()
    values_in = launch.read(args)                               # Считывание ПСП из файла
    values_out, values_reference = transform(args, values_in)   # Преобразование к распределению
    print('INFO: Длина последовательности на выходе = {}'.format(len(values_out)))
    launch.write(args, values_out)                              # Запись преобразованной ПСП в файл
    launch.plot(args, values_out, values_reference)             # Построение гистограммы


if __name__ == '__main__':
    main()

import sys
import time
import argparse

import utils
import utils.launch_gen as launch

DEFAULT_LEN = 10000
DEFAULT_VALUES_MODULO = 1048576


def init_args(parser, args):
    """Параметры только для генерации ПСП"""
    launch.init_args(parser, args)
    parser.add_argument('--g', type=str, default=launch.DEFAULT_GEN_NAME)
    parser.add_argument('--i', nargs='*', default=None)
    parser.add_argument('--n', type=int, default=DEFAULT_LEN)


def parse_args():
    args = utils.get_args()
    # Обработка /h аргумента
    launch.usage(args)
    # Добавление аргументов
    parser = argparse.ArgumentParser()
    init_args(parser, args)
    parser.add_argument('--f', help='Имя выходного файла с ПСП')
    parser.add_argument('--gui', action='store_true')
    # Парсинг
    args_parsed = parser.parse_args(args)
    utils.handle_bins(args_parsed)
    return args_parsed


def generate(args):
    if args.g not in launch.GENS_DICT:
        print('ERR: некорректное значение /g:{}. Смотрите справку /h'.format(args.g))
        sys.exit(0)

    print('INFO: Инициализация')
    gen = launch.GENS_DICT[args.g](args)

    print('INFO: Будет сгенерировано {} чисел'.format(args.n))
    time_start = time.time()
    values = [next(gen) % DEFAULT_VALUES_MODULO for _idx in range(args.n)]
    time_elapsed = int((time.time() - time_start) * 1000)  # из секунд в милисекунды

    print('INFO: Генарация заняла {} милисекунд'.format(time_elapsed))
    print(utils.SEPARATOR)
    return values


def main():
    args = parse_args()
    values = generate(args)     # Инициализация генератора и генерация чисел
    launch.write(args, values)  # Запись в файл
    launch.plot(args, values)          # Построение графика сгенерированных значений


if __name__ == '__main__':
    main()

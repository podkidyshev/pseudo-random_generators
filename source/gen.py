import argparse
import time

import launch
from utils import SEPARATOR

DEFAULT_LEN = 10000
DEFAULT_VALUES_MODULO = 1000
DEFAULT_PLOT_MAX_VALUES = 200


def parse_args():
    # Костыль 1
    args = launch.get_args()
    # Костыль 2
    launch.handle_usage_gen(args)
    # Костыль 3
    gen_name = launch.handle_gen(args)
    # Общие параметры
    parser = argparse.ArgumentParser()
    parser.add_argument('--g', type=str)
    parser.add_argument('--i', nargs='*', default=None)
    parser.add_argument('--n', type=int, default=DEFAULT_LEN)
    parser.add_argument('--f', type=str)
    parser.add_argument('--gui', action='store_true')
    # Параметры генераторов
    launch.init_gen_parser(parser, gen_name)
    # Собственно парсинг
    args_parsed = parser.parse_args(args)
    # Костыль 4
    launch.handle_bins(args_parsed)

    return gen_name, args_parsed


def generate(gen_name, args):
    print('Инициализация генератора {}'.format(gen_name) + SEPARATOR)
    gen = launch.GENS_DICT[gen_name](args)

    print('Будет сгенерировано {} чисел'.format(args.n))
    time_start = time.time()
    values = [next(gen) % DEFAULT_VALUES_MODULO for _idx in range(args.n)]
    time_elapsed = int((time.time() - time_start) * 1000)  # из секунд в милисекунды
    print('Генарация заняла {} милисекунд'.format(time_elapsed) + SEPARATOR)

    return values


def plot(args, values):
    if len(values) <= DEFAULT_PLOT_MAX_VALUES and args.gui:
        import matplotlib.pyplot as plt
        plt.figure()
        for idx, value in enumerate(values):
            plt.scatter(idx, value)
        plt.show()


def main():
    # Аргументы
    gen_name, args = parse_args()
    # Инициализация генератора и генерация чисел
    values = generate(gen_name, args)
    # Запись в файл
    launch.handle_file_gen(args, values)
    # Построение графика сгенерированных значений
    plot(args, values)


if __name__ == '__main__':
    main()

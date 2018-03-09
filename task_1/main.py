import argparse
import time

import launch
from generators import SEPARATOR

DEFAULT_LEN = 10000
DEFAULT_PLOT_MAX_VALUES = 200


def parse_args():
    # Костыль 1
    args = launch.handle_windows_style()
    # Костыль 2
    launch.handle_usage(args)
    # Костыль 3
    gen_name = launch.handle_gen(args)

    parser = argparse.ArgumentParser()
    parser.add_argument('--g', type=str)
    parser.add_argument('--i', type=int, nargs='*', default=None)
    parser.add_argument('--n', type=int, default=DEFAULT_LEN)
    parser.add_argument('--f', type=str)
    parser.add_argument('--gui', action='store_true')

    launch.init_parser(parser, gen_name)

    return gen_name, parser.parse_args(args)


def generate(gen_name, args):
    print('Инициализация генератора {}'.format(gen_name) + SEPARATOR)
    gen = launch.GENS_DICT[gen_name](args)

    print('Будет сгенерировано {} чисел'.format(args.n))
    time_start = time.time()
    values = [next(gen) % 1000 for _idx in range(args.n)]
    time_elapsed = int((time.time() - time_start) * 1000)
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
    launch.handle_file(args, values)
    # Построение графика сгенерированных значений
    plot(args, values)


if __name__ == '__main__':
    main()

import time
import argparse

import utils
import utils.launch_gen as launch

DEFAULT_LEN = 10000
DEFAULT_VALUES_MODULO = 1048576
DEFAULT_PLOT_MAX_VALUES = 200


def init_args(parser, args):
    """Параметры только для генерации ПРС"""
    launch.init_args(parser, launch.handle_gen(args))
    parser.add_argument('--g', type=str)
    parser.add_argument('--i', nargs='*', default=None)
    parser.add_argument('--n', type=int, default=DEFAULT_LEN)


def parse_args():
    args = utils.get_args()
    # Обработка /h аргумента
    launch.handle_usage_gen(args)
    # Добавление аргументов
    parser = argparse.ArgumentParser()
    init_args(parser, args)
    parser.add_argument('--f', type=str)
    parser.add_argument('--gui', action='store_true')
    # Парсинг
    args_parsed = parser.parse_args(args)
    utils.handle_bins(args_parsed)
    return args_parsed


def generate(args):
    print('INFO: Инициализация генератора {}'.format(args.g))
    gen = launch.GENS_DICT[args.g](args)
    print('INFO: Будет сгенерировано {} чисел'.format(args.n))
    time_start = time.time()
    values = [next(gen) % DEFAULT_VALUES_MODULO for _idx in range(args.n)]
    time_elapsed = int((time.time() - time_start) * 1000)  # из секунд в милисекунды
    print('INFO: Генарация заняла {} милисекунд'.format(time_elapsed))
    print(utils.SEPARATOR)
    return values


def plot(args, values, show=True):
    if not args.gui:
        return
    if len(values) > DEFAULT_PLOT_MAX_VALUES:
        print('WARN: Слишком много чисел для отображения на графике. Максимум = {}, регулируется параметром /n')
        print(utils.SEPARATOR)
        return

    import matplotlib.pyplot as plt
    plt.figure()
    for idx, value in enumerate(values):
        plt.scatter(idx, value)

    if show:
        plt.show()


def main():
    # Аргументы
    args = parse_args()
    # Инициализация генератора и генерация чисел
    values = generate(args)
    # Запись в файл
    launch.handle_file_gen(args, values)
    # Построение графика сгенерированных значений
    plot(args, values)


if __name__ == '__main__':
    main()

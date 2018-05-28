import time
import argparse

import utils
import utils.launch_dist as launch

HIST_COUNT = 25


def init_args(parser):
    # Параметры только для преобразования ПРС
    parser.add_argument('--d')
    parser.add_argument('--p1', type=float)
    parser.add_argument('--p2', type=float)
    parser.add_argument('--p3', type=float)


def parse_args():
    args = utils.get_args()
    # Обработка /h аргумента
    launch.handle_usage_dist(args)
    # Добавление аргументов
    parser = argparse.ArgumentParser()
    init_args(parser)
    parser.add_argument('--f')
    parser.add_argument('--fout')
    parser.add_argument('--gui', action='store_true')
    # Парсинг
    return parser.parse_args(args)


def transform(args, values_in):
    dist_name = launch.handle_dist(args)
    print('INFO: Инициализация распределения {}'.format(dist_name))

    dist = launch.DISTS_DICT[dist_name](args)

    print('INFO: Старт преобразования')
    time_start = time.time()
    values_out, values_reference = dist.transform(values_in)
    time_elapsed = int((time.time() - time_start) * 1000)
    print('INFO: Преобразование заняло {} милисекунд'.format(time_elapsed))
    print(utils.SEPARATOR)
    return values_out, values_reference


def plot(args, values, values_reference, show=True):
    if not args.gui:
        return

    import matplotlib.pyplot as plt
    plt.figure()
    plt.subplot(1, 2, 1)
    plt.title('Преобразованные числа')
    plt.hist(values, HIST_COUNT)

    plt.subplot(1, 2, 2)
    plt.title('Генерация системными функциями')
    plt.hist(values_reference, HIST_COUNT)

    if show:
        plt.show()


def main():
    # Аргументы
    args = parse_args()
    # Считывание ПСП из файла
    values_in = launch.handle_file_dist_in(args)
    # Старт преобразования к распределению
    values_out, values_reference = transform(args, values_in)
    print('INFO: Длина последовательности на выходе = {}'.format(len(values_out)))
    # Запись в файл
    launch.handle_file_dist_out(args, values_out)
    # Построение графика полученного распределения
    plot(args, values_out, values_reference)


if __name__ == '__main__':
    main()

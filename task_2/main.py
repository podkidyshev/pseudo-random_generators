import argparse
import time
from task_2.launch import *
from task_2.distributions import SEPARATOR


def parse_args():
    # Костыль 1
    args = handle_windows_style()
    # Костыль 2
    handle_usage(args)

    parser = argparse.ArgumentParser()
    parser.add_argument('--d')
    parser.add_argument('--p1', type=int)
    parser.add_argument('--p2', type=int)
    parser.add_argument('--p3', type=float)
    parser.add_argument('--f')
    parser.add_argument('--fout')
    parser.add_argument('--gui', action='store_true')

    return parser.parse_args(args)


def transform(args, values_in):
    dist_name = handle_dist(args)
    print('Инициализация распределения {}'.format(dist_name) + SEPARATOR)

    dist = DISTS_DICT[dist_name](args)

    print('Старт преобразования')
    time_start = time.time()
    values_out = dist.transform(values_in)
    time_elapsed = int((time.time() - time_start) * 1000)
    print('Преобразование заняло {} милисекунд'.format(time_elapsed) + SEPARATOR)

    return values_out


def plot(args, values):
    if len(values) <= 200 and args.gui:
        import matplotlib.pyplot as plt
        plt.figure()
        for idx, value in enumerate(values):
            plt.scatter(idx, value)
        plt.show()


def main():
    # Аргументы
    args = parse_args()
    # Считывание ПСП из файла
    values_in = handle_file_in(args)
    # Старт преобразования к распределению
    values_out = transform(args, values_in)
    # Запись в файл
    handle_file_out(args, values_out)
    # Построение графика полученного распределения
    plot(args, values_out)


if __name__ == '__main__':
    main()

import os
from numpy import mean, std
import matplotlib.pyplot as plt

import utils


def stats(prs, args):
    print('INFO: СТАТИСТИКА\n')

    mean_true = 0.5
    std_true = 1 / 12
    print('Истинное мат. ожидание = {:.4f}'.format(mean_true))
    print('Истинное среднеквадрат. отклонение = {:.4f}\n'.format(std_true))

    mx = mean(prs)
    sx = std(prs) ** 2
    print('Принята выборка длиной {}'.format(len(prs)))
    print('Мат. ожидание выборки = {:.4f}'.format(mx))
    print('Среднеквадрат. отклонение выборки = {:.4f}\n'.format(sx))

    counts = [100, 500, 1000, 5000, 10000]
    means = [mean(prs[:c]) for c in counts]
    stds = [std(prs[:c]) ** 2 for c in counts]
    for c, m, s in zip(counts, means, stds):
        print('Для выборки из {:>5d} чисел: m = {:.4f}, std = {:.4f}'.format(c, m, s))

    figure = plt.figure()
    plt.title('Зависимость мат. ожидания от объёма выборки')
    plt.plot(means, 'ro')
    plt.ylabel('Значения мат. ожидания')
    plt.xlabel('Размеры выборок {}'.format(', '.join(map(str, counts))))
    plt.axhline(mean_true)
    figure.savefig(os.path.dirname(os.path.abspath(args.fout)) + '\\means.png')

    figure = plt.figure()
    plt.title('Зависимость среднеквадрат. отклонения от объёма выборки')
    plt.plot(stds, 'ro')
    plt.ylabel('Значения среднеквадрат. отклонения')
    plt.xlabel('Размеры выборок {}'.format(', '.join(map(str, counts))))
    plt.axhline(std_true)
    figure.savefig(os.path.dirname(os.path.abspath(args.fout)) + '\\stds.png')

    sample = 1000
    sample_idx = counts.index(sample)
    mean_dev = abs(means[sample_idx] - mean_true) / means[sample_idx] * 100
    std_dev = abs(stds[sample_idx] - std_true) / stds[sample_idx]

    print('\nОтносительные погрешности для выборки размером {}:'.format(sample))
    print('Для мат. ожидания = {0:.2f}%'.format(mean_dev))
    print('Для среднеквадрат. отклонения = {0:.4f}%'.format(std_dev))
    print(utils.SEPARATOR)
    print(utils.SEPARATOR)

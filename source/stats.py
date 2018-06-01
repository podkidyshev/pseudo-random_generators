from numpy import mean, std
import matplotlib.pyplot as plt

import utils


def stats(prs, args):
    print('INFO: СТАТИСТИКА\n')

    mx = mymean(prs)
    sx = mystd(prs)

    print('Математическое ожидание = {:.4f}'.format(mx))
    print('Среднеквадратическое отклонение = {:.4f}'.format(sx))

    counts = [100, 1000, 3000, 7000, 10000]
    means = [mymean(prs[:c]) for c in counts]
    stds = [mystd(prs[:c]) for c in counts]
    for c, m, s in zip(counts, means, stds):
        print('Для выборки из {:>5d} чисел: m = {:.4f}, std = {:.4f}'.format(c, m, s))

    figure = plt.figure()
    plt.title('Зависимость мат. ожидания от объёма выборки')
    plt.plot(means, 'ro')
    plt.ylabel('Значения мат. ожидания')
    plt.xlabel('Размеры выборок {}'.format(', '.join(map(str, counts))))
    figure.savefig(get_fname(args) + '_means.png')

    plt.figure()
    plt.title('Зависимость среднеквадрат. отклонения от объёма выборки')
    plt.plot(stds, 'ro')
    plt.ylabel('Значения среднеквадрат. отклонения')
    plt.xlabel('Размеры выборок {}'.format(', '.join(map(str, counts))))
    figure.savefig(get_fname(args) + '_stds.png')

    sample = 100
    sample_idx = counts.index(sample)
    mean_true = 0.5
    std_true = 1 / 12
    mean_dev = abs(means[sample_idx] - mean_true) / means[sample_idx] * 100
    std_dev = abs(stds[sample_idx] - std_true) / stds[sample_idx]

    print('\nОтносительные погрешности для выборки размером {}'.format(sample))
    print('Для мат. ожидания = {0:.2f}%'.format(mean_dev))
    print('Для среднеквадрат. отклонения = {0:.4f}%'.format(std_dev))
    print(utils.SEPARATOR)
    print(utils.SEPARATOR)


def mymean(prs):
    return mean(prs)


def mystd(prs):
    return std(prs) ** 2


def get_fname(args):
    name = args.fout
    return name[:name.rfind('.')] if '.' in name else name

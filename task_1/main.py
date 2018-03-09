import os
import sys
import argparse
import time

import launch
import generators

DEFAULT_LEN = 10000


def handle_windows_style():
    args = sys.argv[1:]
    for idx, arg in enumerate(args):
        if '/' in arg:
            arg = arg.replace('/', '--')
            if ':' in arg:
                args.insert(idx + 1, arg[arg.index(':') + 1:])
                arg = arg[:arg.index(':')]
            args[idx] = arg

    return args


def handle_file(params):
    if params.f:
        filename = params.f
        print('Запись будет производиться в файл {}'.format(filename) + generators.SEPARATOR)
        if not os.path.isabs(filename):
            filename = os.path.abspath(filename)
        return filename

    print('Запись будет производиться в файл по умолчанию rnd.dat' + generators.SEPARATOR)
    return os.path.abspath('rnd.dat')


def parse_args():
    # Костыль 1
    args = handle_windows_style()
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


def main():
    gen_name, params = parse_args()
    print('Инициализация генератора {}'.format(gen_name) + generators.SEPARATOR)
    gen = launch.GENS_DICT[gen_name](params)

    print('Будет сгенерировано {} чисел'.format(params.n) + generators.SEPARATOR)
    time_start = time.time()
    values = [next(gen) % 1000 for _idx in range(params.n)]
    time_elapsed = int((time.time() - time_start) * 1000)
    print('Генерация прошла успешно' + generators.SEPARATOR)
    print('Генарация заняла {} милисекунд'.format(time_elapsed))

    filaname = handle_file(params)
    with open(filaname, 'w') as f:
        f.write('\n'.join(map(str, values)))
    print('Файлы записаны' + generators.SEPARATOR)

    if len(values) <= 200 and params.gui:
        import matplotlib.pyplot as plt
        plt.figure()
        for idx, value in enumerate(values):
            plt.scatter(idx, value)
        plt.show()


if __name__ == '__main__':
    main()

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


def handle_usage(args):
    if '--h' not in args:
        return
    if args.index('--h') == len(args) - 1 or args[args.index('--h') + 1][:2] == '--':
        s = """Возможные параметры:
        
/h - получение справки о работе программы
/h:<gen> получение справки о генераторе gen
Возможные значения gen: {}

/n:<count> количество генерируемых чисел, по умолчанию 10000

/g:<gen> выбор генератора из списка (по умолчанию веберется случайно)

/i:<i1 i2...> инициализационный вектор. Может содержать несколько значений 
Каждое значение после первого вводится далее через пробел в сторогом порядке. 
Количество значений для каждого генератора фиксировано
Для подробной справки о векторе для каждого генератора смотрите в /h<gen>
Каждый генератор может сам сгенерировать подходящий вектор

/f: файл для записи сгенерированных чисел. По умолчанию запись ведется в rnd.dat в каталоге запуска процесса
Возможно введение как абсолютного, так и относительного пути для файла

/<a>:<a_v> - каждый генератор имеет свои параметры. Для справки по ним введите /h:gen
ВСЕ параметры генераторов - числа. Если требуется полином над GF(2) - введите его эквивалент в десятичной форме (число)
""".format(', '.join(launch.GENS_DICT.keys()))
        print(s)
    else:
        gen_name = args[args.index('--h') + 1]
        if gen_name in launch.GENS_DICT.keys():
            gen_class = launch.GENS_DICT[gen_name]
            print("Описание генератора {} ({}):".format(gen_name, gen_class.NAME) + generators.SEPARATOR)
            print("Возможные параметры: {}".format(', '.join(launch.GENS_DICT[gen_name].PARAMS)))
            print(generators.SEPARATOR[1:], end='')
            launch.GENS_DICT[gen_name].usage()
        else:
            raise Exception('Неизвестное значение параметра для h: выберите одно из: {}'
                            .format(', '.join(launch.GENS_DICT.keys())))
    sys.exit(0)


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
    handle_usage(args)
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

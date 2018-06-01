import re
import sys
import argparse

SEPARATOR = '------------------------------------'

DEFAULT_FILE_IN = 'rnd.dat'
DEFAULT_FILE_OUT = 'rnd_out.dat'


class CheckIntAction(argparse.Action):
    """Допускает только целочисленные параметры"""
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(CheckIntAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        values = CheckIntAction.cast(self.dest, values)
        setattr(namespace, self.dest, values)

    @staticmethod
    def cast(name, value):
        if CheckIntAction.is_int(value):
            return int(value)
        elif CheckIntAction.is_bin_int(value):
            return int(value, 2)
        else:
            print('ERR: переданное значение аргумента {} = {} не является целым числом'.format(name, value))
            sys.exit(0xE)

    @staticmethod
    def is_int(s):
        return s[1:].isdigit() if s[0] in ('-', '+') else s.isdigit()

    @staticmethod
    def is_bin_int(s):
        return re.match('0b[0-1]+', s)


def get_args():
    """Windows style в Unix style (парсер только в Unix может)"""
    args = sys.argv[1:]
    for idx, arg in enumerate(args):
        if '/' in arg:
            arg = arg.replace('/', '--', 1)
            if ':' in arg:
                args.insert(idx + 1, arg[arg.index(':') + 1:])
                arg = arg[:arg.index(':')]
            args[idx] = arg

    return args


def handle_bins(args):
    """
    Позволяет задавать целочисленные аргументы в бинарном виде 0b<2-ичное число>
    Функция вызывается до непосредственного запуска парсинга аргументов
    :param args: аргументы командной строки программы
    :return: None
    """
    def handle_bin(v):
        if isinstance(v, str) and v[:2] == '0b':
            return int(v, 2)
        return v

    for arg, value in args.__dict__.items():
        if not isinstance(value, list):
            setattr(args, arg, handle_bin(value))
        else:
            for idx in range(len(value)):
                value[idx] = handle_bin(value[idx])


def check_h_value(args):
    return args.index('--h') == len(args) - 1 or args[args.index('--h') + 1][:2] == '--'

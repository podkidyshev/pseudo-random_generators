import sys

SEPARATOR = '\n---------------------------------'

DEFAULT_FILE_IN = 'rnd.dat'
DEFAULT_FILE_OUT = 'rnd_out.dat'


def get_args():
    args = sys.argv[1:]
    for idx, arg in enumerate(args):
        if '/' in arg:
            arg = arg.replace('/', '--')
            if ':' in arg:
                args.insert(idx + 1, arg[arg.index(':') + 1:])
                arg = arg[:arg.index(':')]
            args[idx] = arg

    return args


def handle_bins(args):

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

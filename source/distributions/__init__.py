import random
import operator as op
import numpy.random as rnd
import scipy.stats as stats
import scipy.special as spec
from functools import reduce

SEPARATOR = '\n---------------------------------'

DEFAULT_INTERVAL_A = 0
DEFAULT_INTERVAL_B = 5

DEFAULT_OFFSET_A = (-5, 5)
DEFAULT_SCALE_B = (0.1, 3)
DEFAULT_FORM_C = (0.5, 10)


def ncr(n, r):
    r = min(r, n - r)
    numer = reduce(op.mul, range(n, n - r, -1), 1)
    denom = reduce(op.mul, range(1, r + 1), 1)
    return numer // denom


class Dist:
    NAME = 'Равномерное распределение'

    def __init__(self):
        print(SEPARATOR[1:])

    @staticmethod
    def extract_param(params, param, gen_func, *gen_func_params):
        value = getattr(params, param)
        return value if value is not None else gen_func(*gen_func_params)

    @staticmethod
    def print_genned_param(name, value):
        print('Сгенерирован параметр {} = {}'.format(name, value))

    @staticmethod
    def gen_param(bounds: tuple, name):
        param = random.uniform(bounds[0], bounds[1])
        Dist.print_genned_param(name, param)
        return param

    @staticmethod
    def default_param(default_value, name):
        print('Параметр {} взят по умолчанию = {}'.format(name, default_value))
        return default_value

    @staticmethod
    def transform_standard(values, kostyl=False):
        if kostyl:
            modulo = max(values) + 2
            return [(value + 1) / modulo for value in values]
        else:
            modulo = max(values) + 1
            return [value / modulo for value in values]

    @staticmethod
    def iter_next_pairs(values):
        for v0, v1 in zip(values[:-1], values[1:]):
            yield v0, v1

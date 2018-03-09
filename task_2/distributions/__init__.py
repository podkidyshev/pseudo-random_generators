import random

SEPARATOR = '\n---------------------------------'

DEFAULT_INTERVAL_A = 0
DEFAULT_INTERVAL_B = 1000

DEFAULT_OFFSET_A = (-5, 5)
DEFAULT_SCALE_B = (0.1, 5)


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
    def transform_standard(values):
        modulo = max(values) + 1
        return [value / modulo for value in values]

    @staticmethod
    def separate_values(values):
        values_0 = [values[idx] for idx in range(len(values)) if not idx % 2]
        values_1 = [values[idx] for idx in range(len(values)) if idx % 2]
        return values_0, values_1

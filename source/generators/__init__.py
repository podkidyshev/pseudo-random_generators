import random

import utils

DEFAULT_M = (10000, 1000000)
DEFAULT_P = (10, 32)
DEFAULT_W = 10


class Gen:
    """
    В данном классе в основном реализованы методы для вывода значений параметров на экран, парсинга аргументов и
    их автоматической генерации
    """
    def __init__(self):
        print(utils.SEPARATOR)
        print('INFO: Начало работы генератора. Параметры:')
        for attr, value in self.__dict__.items():
            if isinstance(value, list) and len(value) > 5:
                print('{} = {}'.format(attr, Gen.print_list(value)))
            elif isinstance(value, list) and len(value) == 3 and hasattr(value[0], '__dict__'):
                for idx in range(len(value)):
                    for obj_attr, obj_value in value[idx].__dict__.items():
                        print('{}{} = {}'.format(obj_attr, idx + 1, obj_value))
            elif not hasattr(value, '__dict__'):
                print('{} = {}'.format(attr, value))
            else:
                for obj_attr, obj_value in value.__dict__.items():
                    print('{}{} = {}'.format(obj_attr, '', obj_value))

        print(utils.SEPARATOR)

    @staticmethod
    def print_list(l):
        res = str(l[:5])
        res = res[:-1] + ', ...' + res[-1]
        return res

    @staticmethod
    def print_genned_param(name, value):
        print('Сгенерирован параметр {} = {}'.format(name, value))

    @staticmethod
    def gen_param(bounds: tuple, name):
        param = random.randint(bounds[0], bounds[1])
        Gen.print_genned_param(name, param)
        return param

    @staticmethod
    def default(value, name):
        print('Параметр {} взят по умолчанию = {}'.format(name, value))
        return value

    def assert_attrs_modulo(self, attr_check, attr_modulo):
        assert getattr(self, attr_check) < getattr(self, attr_modulo), '{} = {} больше модуля {} = {}'\
            .format(attr_check, getattr(self, attr_check), attr_modulo, getattr(self, attr_modulo))

    @staticmethod
    def assert_len(i, l, name):
        assert i is None or len(i) == l, 'Инициализационный вектор для {} должен содержать {} элементов'.format(name, l)

    @staticmethod
    def get(params, param, gen_func, *gen_func_params):
        value = getattr(params, param)
        return value if value is not None else gen_func(*gen_func_params)

    @staticmethod
    def getv(params, idx, gen_func, *gen_func_params):
        return int(params.i[idx]) if params.i else gen_func(*gen_func_params)

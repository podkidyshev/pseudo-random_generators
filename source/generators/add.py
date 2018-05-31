from generators import *


class GenAdd(Gen):
    NAME = 'Аддитивный метод'
    PARAMS = ['m']

    def __init__(self, params):
        Gen.assert_ilen(params.i, 2, GenAdd.NAME)
        # Основные параметры
        self.m = Gen.get_arg(params, 'm', Gen.gen_param, DEFAULT_M, 'm')
        assert self.m >= 2, 'Модуль должен быть >= 2'
        # Инициализационный вектор
        self.x0 = Gen.get_iarg(params, 0, Gen.gen_param, (0, self.m), 'x0') % self.m
        self.x1 = Gen.get_iarg(params, 1, Gen.gen_param, (0, self.m), 'x1') % self.m

        super().__init__()

    def __next__(self):
        self.x0, self.x1 = self.x1, (self.x0 + self.x1) % self.m
        return self.x1

    @staticmethod
    def usage():
        usage = """
m - модуль
2 <= m

Инициализационный вектор:

0 <= i(0) < m
0 <= i(1) < m
Введённые значения i(0) и i(1) будут взяты по модулю m автоматически
"""
        print(usage)

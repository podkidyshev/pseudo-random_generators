from generators import *


class GenLC(Gen):
    NAME = 'Линейный конгруэнтный метод'
    PARAMS = ['m', 'a', 'c']

    def __init__(self, params):
        # ассерты
        Gen.assert_i_len(params.i, 1, GenLC.NAME)
        # основные параметры
        self.m = Gen.extract_param(params, 'm', Gen.gen_param, DEFAULT_M, 'm')
        assert 2 <= self.m, 'ограничение 2 <= m'
        self.a = Gen.extract_param(params, 'a', Gen.gen_param, (0, self.m), 'a') % self.m
        self.c = Gen.extract_param(params, 'c', Gen.gen_param, (0, self.m), 'c') % self.m
        # инициализационный вектор
        self.x0 = Gen.extract_param_vec(params, 0, Gen.gen_param, (0, self.m), 'x0') % self.m

        super().__init__()

    def __next__(self):
        self.x0 = (self.a * self.x0 + self.c) % self.m
        return self.x0

    @staticmethod
    def usage():
        usage = """
m - модуль
a - множитель
с - приращение

2 <= m
0 <= a < m
0 <= c < m
Введённые значения a и c будут взяты по модулю m автоматически

Инициализационный вектор:

0 <= x0 < m
Введённое значение x0 будет взято по модулю m автоматически
"""
        print(usage)

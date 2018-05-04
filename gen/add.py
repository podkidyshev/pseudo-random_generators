from gen import *


class GenAdd(Gen):
    NAME = 'Аддитивный метод'
    PARAMS = ['m']

    def __init__(self, params):
        # ассерты
        Gen.assert_i_len(params.i, 2, GenAdd.NAME)
        # основные параметры
        self.m = Gen.extract_param(params, 'm', Gen.gen_param, DEFAULT_M, 'm')
        assert self.m >= 2, 'm должно быть >= 2'
        # инициализационный вектор
        self.x0 = Gen.extract_param_vec(params, 0, Gen.gen_param, (0, self.m), 'x0') % self.m
        self.x1 = Gen.extract_param_vec(params, 1, Gen.gen_param, (0, self.m), 'x1') % self.m

        super().__init__()

    def __next__(self):
        self.x0, self.x1 = self.x1, (self.x0 + self.x1) % self.m
        return self.x1

    @staticmethod
    def usage():
        usage = ("""
m - модуль
2 <= m

Инициализационный вектор:

0 <= x0 < m
0 <= x1 < m
Введённые значения x0 и x1 будут взяты по модулю m автоматически
""")
        print(usage)

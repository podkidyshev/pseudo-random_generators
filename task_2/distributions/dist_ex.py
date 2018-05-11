from math import log
from distributions import *


class DistEX(Dist):
    NAME = 'Общее экспоненциальное распределение'

    def __init__(self, params):
        self.a = Dist.extract_param(params, 'p1', Dist.gen_param, DEFAULT_OFFSET_A, 'a')
        self.b = Dist.extract_param(params, 'p2', Dist.gen_param, DEFAULT_SCALE_B, 'b')
        assert 0 < self.b, 'Масштаб распределения = {} должен быть положительным числом'.format(self.b)

        super().__init__()

    def transform(self, values):
        values_standard = Dist.transform_standard(values, True)
        values_out = [-self.b * log(value) + self.a for value in values_standard]

        return values_out, rnd.exponential(self.b, len(values))

    @staticmethod
    def usage():
        s = """
p1(a) - смещение
p2(b) - масштаб - > 0
"""
        print(s)

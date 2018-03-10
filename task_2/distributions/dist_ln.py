from math import exp
from distributions import *


class DistLN(Dist):
    NAME = 'Логнормальное распределение'

    def __init__(self, params):
        # параметры
        self.a = Dist.extract_param(params, 'p1', Dist.gen_param, DEFAULT_OFFSET_A, 'a')
        self.b = Dist.extract_param(params, 'p2', Dist.gen_param, DEFAULT_SCALE_B, 'b')
        # ассерты
        assert 0 < self.b, 'Масштаб распределения = {} должен быть положительным числом'.format(self.b)

        super().__init__()

    def transform(self, values):
        values_standard = Dist.transform_standard(values)
        return [self.a + exp(self.b - z) for z in values_standard]

    @staticmethod
    def usage():
        s = """
p1(a) - смещение
p2(b) - масштаб - > 0
"""
        print(s)

from math import exp
from distributions import *
from distributions.dist_nr import DistNR


class DistLN(Dist):
    NAME = 'Логнормальное распределение'

    def __init__(self, params):
        # параметры
        self.a = Dist.extract_param(params, 'p1', Dist.gen_param, DEFAULT_OFFSET_A, 'a')
        self.b = Dist.extract_param(params, 'p2', Dist.gen_param, (0.1, 1), 'b')
        # ассерты
        assert 0 < self.b, 'Масштаб распределения = {} должен быть положительным числом'.format(self.b)

        super().__init__()

    def transform(self, values):
        setattr(self, 'p1', self.a)
        setattr(self, 'p2', self.b)
        values_normal, q = DistNR(self).transform(values)
        delattr(self, 'p1')
        delattr(self, 'p2')
        return [self.a + exp(self.b * z) for z in values_normal], rnd.lognormal(self.a, self.b, len(values))

    @staticmethod
    def usage():
        s = """
p1(a) - смещение
p2(b) - масштаб - > 0
"""
        print(s)

from distributions import *


class DistST(Dist):
    NAME = 'Стандартное нормальное распределение'

    def __init__(self, params):
        self.a = Dist.extract_param(params, 'p1', Dist.default_param, DEFAULT_INTERVAL_A, 'a')
        self.b = Dist.extract_param(params, 'p2', Dist.default_param, DEFAULT_INTERVAL_B, 'b')
        assert self.a < self.b, 'Числа а и b должны составлять непустой интервал (a, b)'

        super().__init__()

    def transform(self, values):
        values_standard = Dist.transform_standard(values)
        return [self.b * value + self.a for value in values_standard], rnd.uniform(self.a, self.b, len(values))

    @staticmethod
    def usage():
        s = """
p1(a) - левая граница интервала
p2(b) - правая граница интервала

Параметры a и b должны составлять непустой интервал (a < b)
"""
        print(s)

    def cdf(self, x):
        return (x - self.a) / (self.b - self.a)

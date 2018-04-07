from distributions import *


class DistTR(Dist):
    NAME = 'Треугольное распределение'

    def __init__(self, params):
        self.a = Dist.extract_param(params, 'p1', Dist.default_param, DEFAULT_INTERVAL_A, 'a')
        self.b = Dist.extract_param(params, 'p2', Dist.default_param, DEFAULT_INTERVAL_B, 'b')
        assert self.a < self.b, 'Числа а и b должны составлять непустой интервал (a, b)'

        super().__init__()

    def transform(self, values):
        values_in = Dist.transform_standard(values)

        values_out = []
        for u1, u2 in Dist.iter_next_pairs(values_in):
            values_out.append(self.a + self.b * (u1 + u2 - 1))
        return values_out, rnd.triangular(self.a, self.a + (self.b - self.a) / 2, self.b, len(values))

    @staticmethod
    def usage():
        s = """
p1(a) - левая граница интервала 
p2(b) - правая граница интервала

Параметры a и b должны составлять непустой интервал (a < b)
"""
        print(s, end='')

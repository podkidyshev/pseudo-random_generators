from distributions import *
from scipy.special import comb

DEFAULT_P = (0.1, 0.9)


class DistBI(Dist):
    NAME = 'Биномиальное распределение'

    def __init__(self, params):
        # параметры
        self.p = Dist.extract_param(params, 'p1', Dist.gen_param, DEFAULT_P, 'p')
        # ассерты
        assert 0 <= self.p <= 1, 'Вероятность события должна быть в отрезке [0, 1]'

        super().__init__()

    def transform(self, values):
        values_standard = Dist.transform_standard(values)

        f = []
        n = len(values_standard)
        for y in range(n):
            y_new = 0
            for k in range(y):
                y_new += comb(n, k) * pow(self.p, k) * pow(1 - self.p, n - k)
            f.append(y_new)

        values_out = []
        for value in values_standard:
            for idx, fy in enumerate(f):
                if value <= fy:
                    values_out.append(idx)
                    break

        return values_out

    @staticmethod
    def usage():
        s = """
p1(p) - вероятность события - в отрезке [0, 1]
"""
        print(s)

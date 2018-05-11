from math import log, sqrt, exp, e
from distributions import *


class DistGM(Dist):
    NAME = 'Гамма-распределение'

    def __init__(self, params):
        # параметры
        self.a = Dist.extract_param(params, 'p1', Dist.gen_param, DEFAULT_OFFSET_A, 'a')
        self.b = Dist.extract_param(params, 'p2', Dist.gen_param, DEFAULT_SCALE_B, 'b')
        self.c = Dist.extract_param(params, 'p3', Dist.gen_param, DEFAULT_FORM_C, 'c')
        # ассерты
        assert 0 < self.b, 'Масштаб распределения = {} должен быть положительным числом'.format(self.b)
        assert 0 < self.c, 'Параметр формы = {} должен быть > 0'.format(self.c)

        super().__init__()

    def transform(self, values):
        values_standard = Dist.transform_standard(values, True)
        values_out = []
        if 0 < self.c < 1:
            for u1, u2 in Dist.iter_next_pairs(values_standard):
                b = (e + self.c) / e
                P = b * u1
                if P > 1:
                    Y = -log((b - P) / self.c)
                    if u2 <= pow(Y, self.c - 1):
                        values_out.append(Y * self.b + self.a)
                else:
                    Y = P / self.c
                    if u2 <= exp(Y):
                        values_out.append(Y * self.b + self.a)
        elif self.c == 1:
            for u in values_standard:
                values_out.append(-log(u) * self.b + self.a)
        elif self.c > 1:
            a = self.c - 1
            b = (self.c - 1 / (6 * self.c)) / a
            c = 2 / a
            d = c + 2
            for u1, u2 in Dist.iter_next_pairs(values_standard):
                W = b * u1 / u2
                if c * u2 - d + W + (1 / W) <= 0:
                    values_out.append(self.b * a * W + self.a)

        return values_out, list(map(lambda v: v * self.b + self.a, rnd.gamma(self.c, 1, len(values_out))))

    @staticmethod
    def usage():
        s = """
p1(a) - смещение
p2(b) - масштаб - > 0
p3(c) - форма - > 0
"""
        print(s)

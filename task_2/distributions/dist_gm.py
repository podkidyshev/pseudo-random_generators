from math import log, sqrt, exp
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
        assert 0.5 < self.c, 'Параметр формы = {} должен быть > 0.5'.format(self.c)

        super().__init__()

    def transform(self, values):
        values_standard = Dist.transform_standard(values)

        q = self.c - log(4)
        r = self.c + sqrt(2 * self.c - 1)

        values_out = []
        for u1, u2 in Dist.iter_next_pairs(values_standard):
            V = self.c * log(u1 / (1 - u1))
            W = self.c * exp(u1)
            Z = u1 * u1 * u2
            R = q + r * V - W

            if R >= 4.5 * Z - (1 + log(4.5)) or R >= log(Z):
                values_out.append(self.a + self.b * W)
            else:
                p = 1 / sqrt(2 * self.c - 1)
                q = self.c - log(4)
                r = self.c + sqrt(2 * self.c - 1)

                left = q + p * r * log(u1 / (1 - u1)) - self.c * pow(u1 / (1 - u1), p)
                right = 4.5 * u1 * u1 * u2 - (1 + log(4.5))
                if left >= right:
                    values_out.append(self.a + self.b * self.c * pow(u1 / (1 - u1), p))

        return values_out

    @staticmethod
    def usage():
        s = """
p1(a) - смещение
p2(b) - масштаб - > 0
p3(c) - форма - > 0.5
"""
        print(s)

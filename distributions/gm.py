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
        """ Методичка
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
        """
        """ Оригинальная статья
        values_out = []
        a = self.c - 1
        b = (self.c - 1 / (6 * self.c)) / a
        c = 2 / a
        d = c + 2
        for u1, u2 in Dist.iter_next_pairs(values_standard):
            W = b * u1 / u2
            if c * u2 - d + W + (1 / W) <= 0:
                values_out.append(self.b * a * W)
        """
        # """ Модификация Law и Kelton для c > 1
        values_out = []
        a = sqrt(2 * self.c - 1)
        b = self.c - log(4)
        q = self.c + 1 / self.c
        Q = 4.5
        d = 1 + log(Q)
        for u1, u2 in Dist.iter_next_pairs(values_standard):
            V = a * log(u1 / (1 - u1))
            Y = self.c * exp(V)
            Z = u1 * u1 * u2
            W = b + q * V - Y
            if W + d - Q * Z >= 0 or W >= log(Z):
                values_out.append(self.a + self.b * Y)
        # """
        return values_out, rnd.gamma(self.c, self.b, len(values_out))

    @staticmethod
    def usage():
        s = """
p1(a) - смещение
p2(b) - масштаб - > 0
p3(c) - форма - > 1
"""
        print(s)

    def cdf(self, x):
        return stats.gamma.cdf(x=x, a=self.c, scale=self.b, loc=self.a)

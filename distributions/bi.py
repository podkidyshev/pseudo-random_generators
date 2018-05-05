from distributions import *

DEFAULT_P = (0.1, 0.9)
DEFAULT_BI_N = (50, 100)


class DistBI(Dist):
    NAME = 'Биномиальное распределение'

    def __init__(self, params):
        # параметры
        self.p = Dist.extract_param(params, 'p1', Dist.gen_param, DEFAULT_P, 'p')
        self.n = Dist.extract_param(params, 'p2', DistBI.gen_number_of_tests, DEFAULT_BI_N, 'n')
        # ассерты
        assert 0 <= self.p <= 1, 'Вероятность события должна быть в отрезке [0, 1]'

        super().__init__()

    def transform(self, values):
        values_standard = Dist.transform_standard(values)

        f = []
        for y in range(self.n):
            y_new = 0
            for k in range(1, y + 1):
                y_new += ncr(self.n, k) * pow(self.p, k) * pow(1 - self.p, self.n - k)
            f.append(y_new)

        values_out = []
        for value in values_standard:
            for idx, fy in enumerate(f):
                if value <= fy:
                    values_out.append(idx)
                    break

        return values_out, rnd.binomial(self.n, self.p, len(values))

    @staticmethod
    def usage():
        s = """
p1(p) - вероятность события - в отрезке [0, 1]
p2(n) - число испытаний
"""
        print(s)

    @staticmethod
    def gen_number_of_tests(span, name):
        n = random.randint(*span)
        Dist.print_genned_param(name, n)
        return n

    def cdf(self, x):
        return stats.binom.cdf(k=int(x), n=self.n, p=self.p)
